#!/usr/bin/env python3
"""
Twitter Tweets API Server Runner
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import create_app

def main():
    """Main function to run the server"""
    app = create_app()
    
    print("🚀 Starting Twitter Tweets API Server...")
    print("📍 Server URL: http://localhost:5000")
    print("📋 Available Endpoints:")
    print("   GET  /health              - Health check")
    print("   GET  /tweets/<username>   - Get user tweets (cached)")
    print("   POST /tweets              - Get multiple users tweets (cached)")
    print("   POST /cache/clear         - Clear cache")
    print("   GET  /cache/stats         - Get cache statistics")
    print("   GET  /                    - API information")
    print("\n⏹️  Press Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()