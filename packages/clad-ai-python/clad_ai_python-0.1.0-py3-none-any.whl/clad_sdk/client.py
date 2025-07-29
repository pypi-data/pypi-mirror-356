import httpx
from cachetools import TTLCache

class CladClient:
  def __init__(self, api_key: str, threshold: int = 3, redis_client=None):
    self.api_key = api_key
    self.api_base_url = "https://clad-api.fly.dev/api"
    self.threshold = threshold

    # In-process caches for counters and context (Active Users)
    self._counter_cache = TTLCache(maxsize=50_000, ttl=3600)
    self._context_cache = TTLCache(maxsize=50_000, ttl=3600)
    self.context_limit = 10

    # External Redis client for persistent storage
    self._redis = redis_client
  
  # ---------------------- Internal TTL Cache Methods ----------------------

  def _get_counter(self, user_id: str) -> int:
    return self._counter_cache.get(user_id, 0)

  def _set_counter(self, user_id: str, count: int):
    self._counter_cache[user_id] = count

  def _append_context(self, user_id: str, user_input: str):
    context = self._context_cache.get(user_id, [])
    context.append(user_input)
    if len(context) > self.context_limit:
      context.pop(0)
    self._context_cache[user_id] = context

  def _get_context_str(self, user_id: str) -> str:
    context = self._context_cache.get(user_id, [])
    return "\n".join(f"User: {msg}" for msg in context)
  
  # ---------------------- Internal Redis Methods ----------------------
  async def _get_counter_redis(self, user_id: str) -> int:
    try:
      value = await self._redis.get(f"user:{user_id}:counter")
      return int(value or 0)
    except Exception as e:
      print(f"[CladClient] Redis unavailable, falling back to local cache: {e}")
      return self._get_counter(user_id)

  async def _set_counter_redis(self, user_id: str, count: int):
    try:
      await self._redis.set(f"user:{user_id}:counter", count)
    except Exception as e:
      print(f"[CladClient] Redis unavailable, falling back to local cache: {e}")
      self._set_counter(user_id, count)

  async def _get_context_str_redis(self, user_id: str) -> str:
    key = f"user:{user_id}:context"
    try:
      context = await self._redis.lrange(key, 0, -1)
      return "\n".join(f"User: {msg.decode() if isinstance(msg, bytes) else str(msg)}" for msg in context)
    except Exception as e:
      print(f"[CladClient] Redis unavailable, falling back to local cache for context: {e}")
      return self._get_context_str(user_id)
    
  async def _append_context_redis(self, user_id: str, user_input: str):
    key = f"user:{user_id}:context"
    try:
      await self._redis.rpush(key, user_input)
      await self._redis.ltrim(key, -self.context_limit, -1)
    except Exception as e:
      print(f"[CladClient] Redis unavailable, falling back to local cache for context: {e}")
      self._append_context(user_id, user_input)

  # ---------------------- Public Methods ----------------------

  # Option 1: Low latency, low memory (SDK does counting)
  async def get_processed_input(self, user_input: str, user_id: str, discrete: str = "false") -> dict:
    print("URL", self.api_base_url)
    count = self._get_counter(user_id)
    new_count = count + 1

    self._append_context(user_id, user_input)
    context_str = self._get_context_str(user_id)
    
    if new_count < self.threshold:
      self._set_counter(user_id, new_count)
      return {
        "prompt": user_input,
        "promptType": "clean",
        "link": "",
        "discrete": "false",
      }
    
    try:
      async with httpx.AsyncClient(timeout=5.0) as client:
        res = await client.get(
          f"{self.api_base_url}/processUserInput",
          params={
            "user_input": user_input,
            "user_id": user_id,
            "discrete": discrete,
            "context": context_str,
          },
          headers={"Authorization": f"Bearer {self.api_key}"},
        )
        res.raise_for_status()
        data = res.json()

      if data.get("promptType") == "injected":
        self._set_counter(user_id, 0)
      else:
        self._set_counter(user_id, new_count)

      return data

    except httpx.HTTPStatusError as e:
      print(f"[CladClient] HTTP error: {e.response.status_code} - {e.response.text}")
      self._set_counter(user_id, new_count)
      return {
        "prompt": user_input,
        "promptType": "clean",
        "link": "",
        "discrete": "false",
        "_error": {
            "status": e.response.status_code,
            "message": e.response.text
        }
      }

    except Exception as e:
      print(f"[CladClient] Unexpected error: {e}")
      self._set_counter(user_id, new_count)
      return {
        "prompt": user_input,
        "promptType": "clean",
        "link": "",
        "discrete": "false",
        "_error": {
            "message": str(e)
        }
      }

  # Option 2: zero memory (API does everything)
  async def get_processed_input_fully_managed(self, user_input: str, user_id: str, discrete: str = "false", threshold: int | None= None) -> dict:
    """
    Calls the Redis-backed endpoint. No local caching.
    """
    if threshold is None:
      threshold = self.threshold
        
    try:
      async with httpx.AsyncClient(timeout=5.0) as client:
        res = await client.get(
          f"{self.api_base_url}/processUserInputFullyManaged",
          params={
            "user_input": user_input,
            "user_id": user_id,
            "discrete": discrete,
            "threshold": threshold
          },
          headers={"Authorization": f"Bearer {self.api_key}"},
        )
        res.raise_for_status()
        return res.json()

    except httpx.HTTPStatusError as e:
      print(f"[CladClient] HTTP error: {e.response.status_code} - {e.response.text}")
      return {
        "prompt": user_input,
        "promptType": "clean",
        "link": "",
        "discrete": "false",
        "_error": {
            "status": e.response.status_code,
            "message": e.response.text
        }
      }

    except Exception as e:
      print(f"[CladClient] Unexpected error: {e}")
      return {
        "prompt": user_input,
        "promptType": "clean",
        "link": "",
        "discrete": "false",
        "_error": {
            "message": str(e)
        }
      }

  # Option 3: Ideal version — uses client-provided Redis for low latency + low local memory
  async def get_processed_input_with_redis(self, user_input: str, user_id: str, discrete: str = "false") -> dict:
    if not self._redis:
      raise RuntimeError("Redis client not configured")

    count = await self._get_counter_redis(user_id)
    new_count = count + 1

    await self._append_context_redis(user_id, user_input)
    context_str = await self._get_context_str_redis(user_id)

    if new_count < self.threshold:
      await self._set_counter_redis(user_id, new_count)
      return {
        "prompt": user_input,
        "promptType": "clean",
        "link": "",
        "discrete": "false",
      }

    try:
      async with httpx.AsyncClient(timeout=5.0) as client:
        res = await client.get(
          f"{self.api_base_url}/processUserInput",
          params={
            "user_input": user_input,
            "user_id": user_id,
            "discrete": discrete,
            "context": context_str,
          },
          headers={"Authorization": f"Bearer {self.api_key}"},
        )
        res.raise_for_status()
        data = res.json()

      if data.get("promptType") == "injected":
        await self._set_counter_redis(user_id, 0)
      else:
        await self._set_counter_redis(user_id, new_count)

      return data

    except httpx.HTTPStatusError as e:
      print(f"[CladClient] HTTP error: {e.response.status_code} - {e.response.text}")
      await self._set_counter_redis(user_id, new_count)
      return {
        "prompt": user_input,
        "promptType": "clean",
        "link": "",
        "discrete": "false",
        "_error": {
            "status": e.response.status_code,
            "message": e.response.text,
        },
      }

    except Exception as e:
      print(f"[CladClient] Unexpected error: {e}")
      await self._set_counter_redis(user_id, new_count)
      return {
        "prompt": user_input,
        "promptType": "clean",
        "link": "",
        "discrete": "false",
        "_error": {
            "message": str(e),
        },
      }

