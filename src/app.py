from flask import Flask, jsonify
from .routes.health import create_health_route
from .routes.tweets import create_tweet_routes
from .twitter_client import twitter_client
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Initialize Twitter client when app starts
    def initialize_twitter_client():
        """Initialize Twitter client synchronously"""
        try:
            twitter_client.initialize()
            print("✅ Twitter client initialized successfully")
            print(f"✅ Cache enabled: {Config.CACHE_ENABLED}")
            if Config.CACHE_ENABLED:
                print(f"✅ Cache TTL: {Config.CACHE_TTL} seconds")
                print(f"✅ Cache max size: {Config.CACHE_MAXSIZE} items")
        except Exception as e:
            print(f"❌ Error initializing Twitter client: {e}")
    
    # Initialize routes
    create_health_route(app)
    create_tweet_routes(app)
    
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            'message': 'Twitter Tweets API Server',
            'cache_enabled': Config.CACHE_ENABLED,
            'endpoints': {
                'GET /health': 'Health check',
                'GET /tweets/<username>': 'Get tweets by username (cached)',
                'POST /tweets': 'Get tweets for multiple users (cached)',
                'POST /cache/clear': 'Clear cache',
                'GET /cache/stats': 'Get cache statistics',
                'GET /': 'This information page'
            }
        })
    
    # Initialize client when app is created
    initialize_twitter_client()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)