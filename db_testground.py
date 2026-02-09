import os
from diskcache import Cache
import os
path = r"C:\Users\whwei\OneDrive\coding\llp_system\data_vault.db"

cache_dir = r"C:\Users\whwei\coding_cache"  # Ordner, nicht Datei
os.makedirs(cache_dir, exist_ok=True)

cache = Cache(cache_dir)
cache.set('key', 'value')
print(cache.get('key'))

print(os.access(os.path.dirname(path), os.W_OK)) 

os.makedirs(os.path.dirname(path), exist_ok=True)