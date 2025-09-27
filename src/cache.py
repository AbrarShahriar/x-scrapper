from cachetools import TTLCache
import hashlib
import functools
from typing import Any

class TweetCache:
    """
    Simple in-memory cache for tweet data using cachetools
    """
    
    def __init__(self, maxsize: int = 1000, ttl: int = 300):
        """
        Initialize cache
        
        Args:
            maxsize: Maximum number of items to cache
            ttl: Time to live in seconds (5 minutes default)
        """
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.stats = {'hits': 0, 'misses': 0, 'size': 0}
    
    def _generate_key(self, username: str, count: int) -> str:
        """Generate cache key from username and count"""
        key_data = f"tweets:{username.lower()}:{count}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, username: str, count: int) -> Any:
        """Get cached data"""
        key = self._generate_key(username, count)
        result = self.cache.get(key)
        
        if result is not None:
            self.stats['hits'] += 1
        else:
            self.stats['misses'] += 1
        
        self.stats['size'] = len(self.cache)
        return result
    
    def set(self, username: str, count: int, data: Any):
        """Store data in cache"""
        key = self._generate_key(username, count)
        self.cache[key] = data
        self.stats['size'] = len(self.cache)
    
    def clear(self):
        """Clear all cache entries"""
        self.cache.clear()
        self.stats = {'hits': 0, 'misses': 0, 'size': 0}
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate': round(hit_rate, 2),
            'current_size': self.stats['size'],
            'max_size': self.cache.maxsize,
            'ttl': self.cache.ttl
        }

# Global cache instance
tweet_cache = TweetCache(maxsize=500, ttl=300)  # 5 minutes TTL, 500 items max