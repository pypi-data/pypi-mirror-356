# FailoverCache

**FailoverCache** is a flexible and persistent Python caching library that automatically falls back to disk storage when Redis is unavailable. Ideal for development and production environments where Redis may not always be present.

---

## 🚀 Features

- 🔁 Automatic fallback from Redis to diskcache
- ⏳ Time-To-Live (TTL) support for all values
- 🧠 `remember()` helper to avoid duplicate calculations
- 🧹 Flush the entire cache
- 🔄 Extend or set TTL after creation
- ✅ No Redis required during development

---

## 📦 Installation

```bash
pip install FailoverCache
```

---

## 🧪 Example Usage

```python
from FailoverCache import FailoverCache

cache = FailoverCache()

# Store a value for 60 seconds
cache.put("greeting", "hello world", ttl=60)

# Retrieve it later
print(cache.get("greeting"))  # hello world

# Only compute if not cached
data = cache.remember("expensive", lambda: "result_of_heavy_work", ttl=300)

# Extend TTL by 120 seconds
cache.extend_ttl("greeting", 120)

# Set TTL to exactly 300 seconds
cache.set_ttl("greeting", 300)

# Flush all cache entries
cache.flush()
```

---

## 📂 How it works

1. Tries to connect to Redis (`localhost:6379` by default).
2. If Redis is not available or fails, it falls back to local disk storage using `diskcache`.
3. All operations transparently use the first working backend.

---

## 🔧 Configuration

You can customize Redis host/port and disk cache path:

```python
cache = FailoverCache(redis_host="redis", redis_port=6379, diskcache_directory=".my_cache")
```

---

## 📄 License

FailoverCache is licensed under the [MIT License](LICENSE).
