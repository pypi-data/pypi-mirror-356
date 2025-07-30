# ContextGuard 🛡️
A plug-and-play decorator to guard your API calls and background tasks using Redis-based context awareness.

## 🚀 Features
- ✅ Prevent retrying recent failures (e.g., rate limits, flaky APIs)
- 🔄 Auto-reset after TTL
- ⚡ Works for both `sync` and `async` functions
- 🎯 Supports dynamic TTL logic
- 🧠 Skips re-execution on recent success (optional)
- 🧰 Namespace-safe Redis keys

## 📦 Installation
```bash
pip install redis
```

## 🧑‍💻 Usage

### For Sync Functions
```python
@context_guard(lambda x: f"zoom:{x}", ttl=60)
def call_api(x):
    raise Exception("Rate limit error")
```

### For Async Functions
```python
@context_guard(lambda x: f"zoom:{x}", ttl=60)
async def async_call_api(x):
    raise Exception("Async rate limit error")
```

## 🔁 Options
- `ttl`: static fallback TTL
- `ttl_fn`: dynamic TTL per invocation
- `skip_on_success=True`: also skip recent successes
- `store_metadata=True`: return `cached_at` and `elapsed` info
- `redis_client`: custom Redis instance

## ✅ Ideal Use Cases
- Avoiding rate-limit loops (Zoom, Gmail, Slack, etc.)
- Skipping repeat ETL calls in Airflow or workers
- Backoff logic without external libraries
