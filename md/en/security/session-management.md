---
title: "Session Management Security"
description: "Guide to secure session management covering JWT vs opaque tokens, rotation strategies, secure cookies, and session fixation prevention."
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/session-management.html
---

# Session Management Security

Introduction   
Session management is the mechanism by which a web application maintains state across multiple requests from the same user. Flawed session management leads to session hijacking, fixation, and replay attacks. A robust session management strategy must address token generation, storage, transmission, rotation, and invalidation.   
JWT vs Opaque Tokens   
JSON Web Tokens   
JWTs are self-contained tokens carrying claims in a signed JSON payload. They enable stateless authentication — the server validates the signature without database lookups.   

    
    
    import jwt
    
    from datetime import datetime, timedelta
    
    
    
    # Generate a JWT access token
    
    def create_access_token(user_id, roles, secret_key):
    
        payload = {
    
            'sub': user_id,
    
            'roles': roles,
    
            'iat': datetime.utcnow(),
    
            'exp': datetime.utcnow() + timedelta(minutes=15),
    
            'jti': secrets.token_hex(16),  # Unique token ID for revocation
    
            'type': 'access'
    
        }
    
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    
    
    # Generate a refresh token
    
    def create_refresh_token(user_id, secret_key):
    
        payload = {
    
            'sub': user_id,
    
            'exp': datetime.utcnow() + timedelta(days=7),
    
            'jti': secrets.token_hex(16),
    
            'type': 'refresh'
    
        }
    
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    
    
    # Verify and decode
    
    def verify_token(token, secret_key):
    
        try:
    
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    
            # Check if token is revoked (check jti against blocklist)
    
            if is_revoked(payload['jti']):
    
                raise jwt.InvalidTokenError('Token revoked')
    
            return payload
    
        except jwt.ExpiredSignatureError:
    
            raise
    
        except jwt.InvalidTokenError:
    
            raise
    
    

  
JWT advantages: stateless, self-validating, carries user claims. Disadvantages: cannot revoke without a blocklist, payload is signed not encrypted (unless JWE), token size can be large.   
Opaque Tokens   
Opaque tokens are random strings stored server-side in a session store. The client presents the token, and the server looks up the associated session data.   

    
    
    import secrets
    
    import redis
    
    
    
    class OpaqueTokenManager:
    
        def __init__(self, redis_client):
    
            self.redis = redis_client
    
            self.token_length = 32
    
        
    
        def create_session(self, user_id, claims, ttl_seconds=3600):
    
            token = secrets.token_hex(self.token_length)
    
            session_key = f"session:{token}"
    
            
    
            session_data = {
    
                'user_id': user_id,
    
                'claims': claims,
    
                'created_at': datetime.utcnow().isoformat(),
    
                'last_activity': datetime.utcnow().isoformat()
    
            }
    
            
    
            self.redis.setex(session_key, ttl_seconds, json.dumps(session_data))
    
            return token
    
        
    
        def validate_session(self, token):
    
            session_key = f"session:{token}"
    
            data = self.redis.get(session_key)
    
            if not data:
    
                return None
    
            
    
            session = json.loads(data)
    
            # Update last activity
    
            session['last_activity'] = datetime.utcnow().isoformat()
    
            self.redis.setex(session_key, 3600, json.dumps(session))
    
            return session
    
        
    
        def revoke_session(self, token):
    
            self.redis.delete(f"session:{token}")
    
        
    
        def revoke_all_user_sessions(self, user_id):
    
            # Pattern-based revocation
    
            for key in self.redis.scan_iter(f"session:*"):
    
                data = json.loads(self.redis.get(key))
    
                if data['user_id'] == user_id:
    
                    self.redis.delete(key)
    
    

  
Token Rotation   
Rotating tokens limits the window of opportunity for stolen tokens.   

    
    
    # Refresh token rotation
    
    def refresh_access_token(refresh_token, secret_key):
    
        payload = verify_token(refresh_token, secret_key)
    
        
    
        if payload['type'] != 'refresh':
    
            raise InvalidTokenError('Not a refresh token')
    
        
    
        # Revoke old refresh token
    
        revoke_token(payload['jti'])
    
        
    
        # Issue new tokens
    
        new_access = create_access_token(payload['sub'], payload['roles'], secret_key)
    
        new_refresh = create_refresh_token(payload['sub'], secret_key)
    
        
    
        return {'access_token': new_access, 'refresh_token': new_refresh}
    
    

  
Secure Cookies   
For web applications, cookies remain the primary session token transport mechanism.   

    
    
    from flask import make_response
    
    
    
    def set_session_cookie(response, token):
    
        response.set_cookie(
    
            'session_token',
    
            value=token,
    
            httponly=True,      # Not accessible via JavaScript
    
            secure=True,        # Only over HTTPS
    
            samesite='Strict',  # Not sent with cross-origin requests
    
            max_age=3600,
    
            path='/'
    
        )
    
    
    
    # Modern recommended cookie configuration
    
    session_cookie_config = {
    
        'http_only': True,
    
        'secure': True,
    
        'same_site': 'Lax',
    
        'max_age': 3600,          # 1 hour
    
        'domain': 'app.example.com',
    
        'path': '/',
    
        # __Host- prefix for cookie name ensures path=/ and no domain attribute
    
        'name': '__Host-session'
    
    }
    
    

  
Session Fixation Prevention   
Session fixation occurs when an attacker forces a victim to use a known session identifier. Mitigation: regenerate the session ID after authentication.   

    
    
    def login(request, username, password):
    
        if authenticate(username, password):
    
            # Regenerate session ID after successful login
    
            old_session = request.session
    
            request.session.regenerate()  # New session ID, same data
    
            
    
            # Copy relevant data and invalidate old session
    
            request.session['user_id'] = get_user_id(username)
    
            request.session['authenticated'] = True
    
            request.session['auth_time'] = datetime.utcnow().isoformat()
    
            
    
            # Invalidate old session in store
    
            session_store.delete(old_session.session_key)
    
            
    
            return redirect('/dashboard')
    
    

  
Session Timeout Strategies   

    
    
    session_timeouts = {
    
        'idle_timeout': timedelta(minutes=30),  # Absolute: no activity for 30 min
    
        'absolute_timeout': timedelta(hours=8), # Absolute: max session lifetime
    
    }
    
    
    
    def check_session_timeout(session):
    
        now = datetime.utcnow()
    
        
    
        # Idle timeout
    
        last_activity = datetime.fromisoformat(session['last_activity'])
    
        if now - last_activity > session_timeouts['idle_timeout']:
    
            return {'expired': True, 'reason': 'idle_timeout'}
    
        
    
        # Absolute timeout
    
        auth_time = datetime.fromisoformat(session['auth_time'])
    
        if now - auth_time > session_timeouts['absolute_timeout']:
    
            return {'expired': True, 'reason': 'absolute_timeout'}
    
        
    
        return {'expired': False}
    
    

  
Conclusion   
Secure session management requires defense in depth. Use JWTs for stateless distributed systems with short expiration times, or opaque tokens for server-side control with instant revocation. Always use `HttpOnly`, `Secure`, and `SameSite` attributes on session cookies, regenerate session IDs after login, enforce idle and absolute timeouts, and implement proper token rotation for refresh flows.
