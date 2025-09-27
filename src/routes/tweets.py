from flask import request, jsonify
from ..twitter_client import twitter_client
from ..cache import tweet_cache
from config import Config

def create_tweet_routes(app):
    
    @app.route('/tweets/<username>', methods=['GET'])
    def get_tweets(username):
        """Get tweets for a single user with caching"""
        try:
            count = request.args.get('count', default=10, type=int)
            
            # Validate count
            if count > Config.MAX_TWEETS_PER_USER:
                count = Config.MAX_TWEETS_PER_USER
            elif count < 1:
                count = 1
            
            # Use synchronous method instead of asyncio.run()
            result = twitter_client.get_user_tweets(username, count)
            
            # Add cache info to response
            # if Config.CACHE_ENABLED:
            #     cache_stats = tweet_cache.get_stats()
            #     result['cache_info'] = {
            #         'cached': result.get('cached', False),
            #         'cache_hit_rate': cache_stats['hit_rate'],
            #         'cache_size': cache_stats['current_size']
            #     }
            
            return jsonify(result)
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/tweets', methods=['POST'])
    def get_tweets_multiple():
        """Get tweets for multiple users with caching"""
        try:
            data = request.get_json()
            
            if not data or 'usernames' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Missing usernames array in request body'
                }), 400
            
            usernames = data['usernames']
            count = data.get('count', 10)
            
            if not isinstance(usernames, list):
                return jsonify({
                    'success': False,
                    'error': 'usernames must be an array'
                }), 400
            
            # Validate parameters
            if count > Config.MAX_TWEETS_MULTIPLE_USERS:
                count = Config.MAX_TWEETS_MULTIPLE_USERS
            elif count < 1:
                count = 1
            
            if len(usernames) > Config.MAX_USERS_PER_REQUEST:
                usernames = usernames[:Config.MAX_USERS_PER_REQUEST]
            
            # Fetch tweets for all users using synchronous method
            results = []
            for username in usernames:
                result = twitter_client.get_user_tweets(username, count)
                results.append(result)
            
            response_data = {
                'success': True,
                'results': results
            }
            
            # Add cache info to response
            if Config.CACHE_ENABLED:
                cache_stats = tweet_cache.get_stats()
                response_data['cache_info'] = {
                    'cache_hit_rate': cache_stats['hit_rate'],
                    'cache_size': cache_stats['current_size']
                }
            
            return jsonify(response_data)
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/cache/clear', methods=['POST'])
    def clear_cache():
        """Clear the tweet cache"""
        try:
            tweet_cache.clear()
            return jsonify({
                'success': True,
                'message': 'Cache cleared successfully'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/cache/stats', methods=['GET'])
    def get_cache_stats():
        """Get cache statistics"""
        try:
            stats = tweet_cache.get_stats()
            return jsonify({
                'success': True,
                'cache_enabled': Config.CACHE_ENABLED,
                'stats': stats
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500