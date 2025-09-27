from flask import jsonify
from datetime import datetime

def create_health_route(app):
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'message': 'Twitter Tweets API Server is running',
            'version': '1.0.0'
        })