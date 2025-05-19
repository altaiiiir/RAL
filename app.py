import os
import sys
import webview
import shutil
import threading
import json
from bottle import Bottle, static_file, run, response, request

from controllers.login_controller import LeagueLoginController


class LeagueAutoLoginAPI:
    def __init__(self):
        self.controller = LeagueLoginController()
        self.window = None
    
    def set_window(self, window):
        self.window = window
    
    def get_accounts(self):
        """Get all accounts for the UI"""
        try:
            accounts = self.controller.get_accounts()
            print(f"API: returning {len(accounts)} accounts")
            return accounts
        except Exception as e:
            print(f"Error getting accounts: {str(e)}")
            return []
    
    def get_regions(self):
        """Get list of available regions"""
        try:
            regions = self.controller.get_regions()
            print(f"API: returning {len(regions)} regions")
            return regions
        except Exception as e:
            print(f"Error getting regions: {str(e)}")
            return []
    
    def save_account(self, username, password, region):
        """Save or update an account"""
        try:
            print(f"API: saving account {username} with region {region}")
            return self.controller.save_account(username, password, region)
        except Exception as e:
            print(f"Error saving account: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def delete_account(self, username):
        """Delete an account"""
        try:
            print(f"API: deleting account {username}")
            return self.controller.delete_account(username)
        except Exception as e:
            print(f"Error deleting account: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def login_to_client(self, username):
        """Login to League client using selected account"""
        try:
            print(f"API: logging in account {username}")
            return self.controller.login_to_client(username)
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def minimize_window(self):
        """Minimize the window"""
        if self.window:
            self.window.minimize()
        return {"success": True}


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def copy_resources():
    """Copy necessary resources to the right location"""
    # Copy background image if it doesn't exist
    src_background = resource_path("background.jpeg")
    dst_background = os.path.join("web", "static", "images", "background.jpg")
    
    if os.path.exists(src_background) and not os.path.exists(dst_background):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(dst_background), exist_ok=True)
        shutil.copy2(src_background, dst_background)


def enable_cors(fn):
    """CORS decorator for bottle routes"""
    def _enable_cors(*args, **kwargs):
        # Set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With'

        if request.method != 'OPTIONS':
            # Actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


def start_server(api):
    """Start a Bottle server to serve our app"""
    server_app = Bottle()
    
    # Set the debug level on the app to see more details
    server_app.config['debug'] = True
    
    # Add CORS middleware
    def add_cors_headers():
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With'

    server_app.add_hook('after_request', add_cors_headers)
    
    # Routes for static files
    @server_app.route('/static/<filepath:path>')
    @enable_cors
    def serve_static(filepath):
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web', 'static')
        print(f"Serving static file: {filepath} from {static_dir}")
        return static_file(filepath, root=static_dir)
    
    # Route for main index
    @server_app.route('/')
    @enable_cors
    def serve_index():
        templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web', 'templates')
        print(f"Serving index.html from {templates_dir}")
        return static_file('index.html', root=templates_dir)
    
    # API endpoints
    @server_app.route('/api/accounts', method=['GET', 'OPTIONS'])
    @enable_cors
    def get_accounts():
        if request.method == 'OPTIONS':
            return {}
        accounts = api.get_accounts()
        return json.dumps(accounts)
    
    @server_app.route('/api/regions', method=['GET', 'OPTIONS'])
    @enable_cors
    def get_regions():
        if request.method == 'OPTIONS':
            return {}
        regions = api.get_regions()
        return json.dumps(regions)
    
    @server_app.route('/api/account', method=['POST', 'OPTIONS'])
    @enable_cors
    def save_account():
        if request.method == 'OPTIONS':
            return {}
        data = request.json
        result = api.save_account(data.get('username'), data.get('password'), data.get('region'))
        return json.dumps(result)
    
    @server_app.route('/api/account/<username>', method=['DELETE', 'OPTIONS'])
    @enable_cors
    def delete_account(username):
        if request.method == 'OPTIONS':
            return {}
        result = api.delete_account(username)
        return json.dumps(result)
    
    @server_app.route('/api/login/<username>', method=['POST', 'OPTIONS'])
    @enable_cors
    def login(username):
        if request.method == 'OPTIONS':
            return {}
        result = api.login_to_client(username)
        return json.dumps(result)
    
    # Run the server
    run(server_app, host='localhost', port=8000, quiet=False)


def main():
    # Copy resources if needed
    copy_resources()
    
    # Create API instance
    api = LeagueAutoLoginAPI()
    
    # Start the server in a separate thread
    server_thread = threading.Thread(target=lambda: start_server(api))
    server_thread.daemon = True
    server_thread.start()
    
    # Enable debugging
    debug = False
    debug_options = {
        'port': 8081
    }
    
    # Create window
    window = webview.create_window(
        title='Riot Auto Login',
        url='http://localhost:8000/',
        js_api=api,
        width=600,
        height=800,
        resizable=False
    )
    
    # Set window reference in API
    api.set_window(window)
    
    # Start the app
    webview.start(debug=debug, http_server=debug_options)


if __name__ == '__main__':
    main() 