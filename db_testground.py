from diskcache import Cache
import os

path = r"C:\Temp\diskcache_test"
os.makedirs(path, exist_ok=True)

cache = Cache(path)
cache["x"] = 1
print(cache["x"])