import time
import json
import logging
import redis
import inspect
from functools import wraps

logger = logging.getLogger(__name__)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def context_guard(key_fn, ttl=300, ttl_fn=None, redis_client=None, skip_on_success=False, store_metadata=False):
    redis_conn = redis_client or r

    def decorator(func):
        is_async = inspect.iscoroutinefunction(func)

        def _should_skip(context, dynamic_ttl):
            elapsed = time.time() - context['timestamp']
            if elapsed < dynamic_ttl:
                return context.get("status"), elapsed
            return None, elapsed

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = key_fn(*args, **kwargs)
            dynamic_ttl = ttl_fn(*args, **kwargs) if ttl_fn else ttl
            context_raw = redis_conn.get(key)

            if context_raw:
                context = json.loads(context_raw)
                status, elapsed = _should_skip(context, dynamic_ttl)
                if status in ("failed", "success") and (status == "failed" or skip_on_success):
                    logger.info(f"[contextguard:{key}] Skipped due to recent {status} ({elapsed:.2f}s ago)")
                    return {
                        "status": "skipped",
                        "reason": context.get("reason", f"recent_{status}"),
                        "message": f"This action was recently {status}. Skipped to avoid retry.",
                        "meta": {"cached_at": context.get("timestamp"), "elapsed": elapsed} if store_metadata else None
                    }

            try:
                result = await func(*args, **kwargs)
                redis_conn.set(key, json.dumps({"status": "success", "timestamp": time.time()}), ex=dynamic_ttl)
                return result
            except Exception as e:
                redis_conn.set(key, json.dumps({
                    "status": "failed",
                    "timestamp": time.time(),
                    "reason": str(e)
                }), ex=dynamic_ttl)
                logger.warning(f"[contextguard:{key}] Failed: {str(e)}")
                raise e

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            key = key_fn(*args, **kwargs)
            dynamic_ttl = ttl_fn(*args, **kwargs) if ttl_fn else ttl
            context_raw = redis_conn.get(key)

            if context_raw:
                context = json.loads(context_raw)
                status, elapsed = _should_skip(context, dynamic_ttl)
                if status in ("failed", "success") and (status == "failed" or skip_on_success):
                    logger.info(f"[contextguard:{key}] Skipped due to recent {status} ({elapsed:.2f}s ago)")
                    return {
                        "status": "skipped",
                        "reason": context.get("reason", f"recent_{status}"),
                        "message": f"This action was recently {status}. Skipped to avoid retry.",
                        "meta": {"cached_at": context.get("timestamp"), "elapsed": elapsed} if store_metadata else None
                    }

            try:
                result = func(*args, **kwargs)
                redis_conn.set(key, json.dumps({"status": "success", "timestamp": time.time()}), ex=dynamic_ttl)
                return result
            except Exception as e:
                redis_conn.set(key, json.dumps({
                    "status": "failed",
                    "timestamp": time.time(),
                    "reason": str(e)
                }), ex=dynamic_ttl)
                logger.warning(f"[contextguard:{key}] Failed: {str(e)}")
                raise e

        return async_wrapper if is_async else sync_wrapper

    return decorator
