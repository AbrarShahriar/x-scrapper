import asyncio
import threading
from twikit.guest import GuestClient
from .cache import tweet_cache
from config import Config

class TwitterClient:
    def __init__(self):
        self.client = GuestClient()
        self._initialized = False
        self._lock = threading.Lock()
        # Create and set event loop for this thread
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
    
    def initialize(self):
        """Initialize the Twitter client synchronously"""
        if not self._initialized:
            with self._lock:
                if not self._initialized:  # Double-check locking
                    try:
                        # Run the async initialization in our dedicated loop
                        self._loop.run_until_complete(self._initialize_async())
                        self._initialized = True
                        print("Twitter client initialized successfully")
                    except Exception as e:
                        print(f"Error initializing Twitter client: {e}")
                        raise
    
    async def _initialize_async(self):
        """Async initialization"""
        await self.client.activate()
    
    def get_user_tweets(self, username: str, count: int = 10):
        """Get tweets for a specific user with caching (synchronous wrapper)"""
        if not self._initialized:
            self.initialize()
        
        # Check cache first if enabled
        if Config.CACHE_ENABLED:
            cached_data = tweet_cache.get(username, count)
            if cached_data:
                print(f"Cache HIT for {username} (count: {count})")
                return cached_data
            print(f"Cache MISS for {username} (count: {count})")
        
        try:
            # Run the async function in our dedicated event loop
            result = self._loop.run_until_complete(self._get_user_tweets_async(username, count))
            
            # Store in cache if enabled and successful
            if Config.CACHE_ENABLED and result.get('success'):
                tweet_cache.set(username, count, result)
                print(f"Data cached for {username} (count: {count})")
            
            return result
        
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'username': username,
                'cached': False
            }
            return error_result
    
    async def _get_user_tweets_async(self, username: str, count: int = 10):
        """Actual async implementation"""
        try:
            user = await self.client.get_user_by_screen_name(username)
            tweets = await user.get_tweets('Tweets', count=count)
            
            tweet_data = []
            for tweet in tweets:
                tweet_info = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'timestamp': tweet.created_at,
                    'tweet_link': f"https://x.com/{username}/status/{tweet.id}",
                    'username': username,
                    'retweet_count': getattr(tweet, 'retweet_count', 0),
                    'favorite_count': getattr(tweet, 'favorite_count', 0),
                }
                tweet_data.append(tweet_info)
            
            return {
                'success': True,
                'username': username,
                'tweet_count': len(tweet_data),
                'tweets': tweet_data,
                'cached': False
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'username': username,
                'cached': False
            }

# Global client instance
twitter_client = TwitterClient()