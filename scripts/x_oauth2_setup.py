#!/usr/bin/env python3
"""One-time OAuth 2.0 setup for X/Twitter posting (Authorization Code flow).

Usage:
  1. Run: python3 scripts/x_oauth2_setup.py
  2. Open the printed URL in your browser
  3. Authorize the app
  4. Copy the refresh token

Requires: curl
"""
import base64, hashlib, json, os, secrets, subprocess, sys, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

CLIENT_ID = os.environ.get('X_CLIENT_ID', 'VmtCYWV1aDgxemVGWnMyTzU4ZVA6MTpjaQ')
CLIENT_SECRET = os.environ.get('X_CLIENT_SECRET', 'Uc4Jk5pqgRjrAZoWwW24X9bgK_fjkkztpS5yG3W7alWcy2kboF')
REDIRECT_URI = 'http://localhost:8080/callback'
PORT = 8080
SCOPES = 'tweet.read tweet.write users.read offline.access'

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
    """Exchange authorization code for tokens (non-PKCE, client_secret in body)."""
    data = urllib.parse.urlencode({
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
    })
    result = subprocess.run([
        'curl', '-s', '--max-time', '15',
        'https://api.twitter.com/2/oauth2/token',
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
    print('=' * 60)
    print('X (Twitter) OAuth 2.0 Setup')
    print('=' * 60)
    print()

    state = secrets.token_hex(16)

    # Build authorization URL (NO PKCE - using client_secret instead)
    params = urllib.parse.urlencode({
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
        'state': state,
    })
    auth_url = f'https://twitter.com/i/oauth2/authorize?{params}'

    server = HTTPServer(('localhost', PORT), CallbackHandler)
    server.shutdown_after_request = False
    server.timeout = 300

    print('Authorization URL (open in browser):')
    print(f'{auth_url}')
    print()
    import webbrowser
    webbrowser.open(auth_url)

    while auth_code is None:
        server.handle_request()

    print(f'\nAuthorization code received! Exchanging for tokens...')

    tokens = exchange_code(auth_code)
    if not tokens:
        print('Failed to get tokens.')
        return 1

    access_token = tokens.get('access_token', '')
    refresh_token = tokens.get('refresh_token', '')

    print('\n' + '=' * 60)
    print('SUCCESS! Tokens received.')
    print('=' * 60)

    # Test the access token
    print('\nTesting access token...')
    try:
        result = subprocess.run([
            'curl', '-s', '--max-time', '10',
            'https://api.twitter.com/2/users/me',
            '-H', f'Authorization: Bearer {access_token}',
        ], capture_output=True, text=True, timeout=15)
        me = json.loads(result.stdout)
        username = me.get('data', {}).get('username', 'unknown')
        print(f'  Authenticated as: @{username}')
    except Exception as e:
        print(f'  Token test failed: {e}')

    print('\n--- Save these values to GitHub Secrets ---')
    print()
    print('1. X_REFRESH_TOKEN:')
    print(f'   {refresh_token}')
    print()
    print('Already set (verify they match):')
    print(f'   X_CLIENT_ID = {CLIENT_ID}')
    print(f'   X_CLIENT_SECRET = [hidden]')
    print()

    # Save locally
    local_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'x-tokens.json')
    with open(local_file, 'w') as f:
        json.dump({
            'refresh_token': refresh_token,
            'client_id': CLIENT_ID,
            'username': username if 'username' in dir() else 'unknown',
        }, f, indent=2)
    print(f'Token info saved to {local_file}')

    # Copy to clipboard hint
    print()
    print('You can now run the GitHub Actions workflow to test posting.')

    return 0


if __name__ == '__main__':
    sys.exit(main())
