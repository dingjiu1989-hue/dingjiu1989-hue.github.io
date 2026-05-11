#!/usr/bin/env python3
"""One-time OAuth 2.0 setup for WordPress.com API access.

Usage:
  1. Run: python3 scripts/wp_oauth2_setup.py
  2. Open the printed URL in your browser
  3. Authorize the app
  4. Token is saved automatically
"""
import json, os, subprocess, sys, urllib.parse, secrets
from http.server import HTTPServer, BaseHTTPRequestHandler

CLIENT_ID = os.environ.get('WP_CLIENT_ID', '139351')
CLIENT_SECRET = os.environ.get('WP_CLIENT_SECRET', 'lJZUDbvDkAa0CKcuza5I40x4t1KtyNV9t48hsgsRjnhgr1x3Tk5vF8g6CFMbNUKx')
REDIRECT_URI = 'http://localhost:8080/callback'
PORT = 8080
SCOPES = 'global'

auth_code = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization successful!</h1>'
                           b'<p>You can close this window now.</p></body></html>')
        else:
            error = params.get('error', ['unknown'])[0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f'<html><body><h1>Authorization failed</h1>'
                           f'<p>Error: {error}</p></body></html>'.encode())
        self.server.shutdown_after_request = True

    def log_message(self, format, *args):
        pass


def exchange_code(code):
    """Exchange authorization code for access token."""
    data = urllib.parse.urlencode({
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
    })
    result = subprocess.run([
        'curl', '-s', '--max-time', '15',
        'https://public-api.wordpress.com/oauth2/token',
        '-H', 'Content-Type: application/x-www-form-urlencoded',
        '-d', data,
    ], capture_output=True, text=True, timeout=20)
    if result.returncode != 0:
        print(f'Token exchange failed (curl): {result.stderr[:200]}')
        return None
    try:
        tokens = json.loads(result.stdout)
        if 'error' in tokens:
            print(f'Token exchange denied: {tokens.get("error")}: {tokens.get("error_description", "")}')
            return None
        return tokens
    except json.JSONDecodeError as e:
        print(f'Token exchange parse error: {e}')
        print(f'Response: {result.stdout[:300]}')
        return None


def main():
    print('=' * 60, flush=True)
    print('WordPress.com OAuth 2.0 Setup', flush=True)
    print('=' * 60, flush=True)
    print(flush=True)

    # Kill any process on our port
    subprocess.run(['lsof', '-ti:8080'], capture_output=True)
    import os, signal
    try:
        pid = int(subprocess.run(['lsof', '-ti', ':8080'],
                                  capture_output=True, text=True).stdout.strip())
        os.kill(pid, signal.SIGKILL)
    except (ValueError, OSError):
        pass

    state = secrets.token_hex(16)

    params = urllib.parse.urlencode({
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': SCOPES,
        'state': state,
    })
    auth_url = f'https://public-api.wordpress.com/oauth2/authorize?{params}'

    server = HTTPServer(('localhost', PORT), CallbackHandler)
    server.shutdown_after_request = False
    server.timeout = 300

    print('Authorization URL (open in browser):', flush=True)
    print(f'{auth_url}', flush=True)
    print(flush=True)
    import webbrowser
    webbrowser.open(auth_url)

    while auth_code is None:
        server.handle_request()

    print('\nAuthorization code received! Exchanging for token...')

    tokens = exchange_code(auth_code)
    if not tokens:
        print('Failed to get token.')
        return 1

    access_token = tokens.get('access_token', '')
    blog_url = tokens.get('blog_url', '')
    blog_id = tokens.get('blog_id', '')

    print('\n' + '=' * 60)
    print('SUCCESS! Token received.')
    print('=' * 60)

    # Test the token
    print('\nTesting access token...')
    try:
        result = subprocess.run([
            'curl', '-s', '--max-time', '10',
            'https://public-api.wordpress.com/rest/v1.1/me/sites',
            '-H', f'Authorization: Bearer {access_token}',
        ], capture_output=True, text=True, timeout=15)
        sites = json.loads(result.stdout)
        site_list = sites.get('sites', [])
        print(f'  Connected to {len(site_list)} WordPress.com site(s):')
        for s in site_list:
            print(f'    - {s.get("name", "?")} ({s.get("URL", "?")})')
            print(f'      Site ID: {s.get("ID", "?")}')
    except Exception as e:
        print(f'  Token test failed: {e}')

    print('\n--- Save these values ---')
    print()
    print('WP_ACCESS_TOKEN (for GitHub Secrets):')
    print(f'  {access_token}')
    print()
    print(f'Blog ID: {blog_id}')
    print(f'Blog URL: {blog_url}')

    # Save locally
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    local_file = os.path.join(data_dir, 'wp-tokens.json')
    with open(local_file, 'w') as f:
        json.dump({
            'access_token': access_token,
            'blog_id': blog_id,
            'blog_url': blog_url,
        }, f, indent=2)
    print(f'\nToken info saved to {local_file}')
    print()
    print('You can now run: python3 scripts/syndicate_wordpress.py')

    return 0


if __name__ == '__main__':
    sys.exit(main())
