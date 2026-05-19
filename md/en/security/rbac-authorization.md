---
title: "RBAC Authorization Implementation"
description: "A practical guide to implementing Role-Based Access Control with roles, permissions, policies, and middleware in Node.js and Python."
date: 2025-12-19
board: security
url: https://dingjiu1989-hue.github.io/en/security/rbac-authorization.html
---

# RBAC Authorization Implementation

## RBAC Authorization Implementation

### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

#### RBAC Authorization Implementation

What Is RBAC? 

Role-Based Access Control (RBAC) is an authorization model where permissions are assigned to roles, and users are assigned to those roles. Instead of managing permissions for each user individually, you manage roles and their associated permissions, then assign users to appropriate roles. 

Core RBAC Concepts 

| Concept | Definition | Example | |---------|------------|---------| | User | An individual account | alice@example.com | | Role | A collection of permissions | Editor, Admin, Viewer | | Permission | An action on a resource | article:create, article:delete | | Resource | The object being accessed | Article, User, Comment | | Session | A user's active role mapping | Alice as Editor | 

The RBAC Model 

Level 1: Flat RBAC 

Users are assigned roles, and roles have permissions. This simple structure works for most applications. 

Users ──< Role Assignment >── Roles ──< Permission Assignment >── Permissions

Level 2: Hierarchical RBAC 

Roles can inherit permissions from other roles. For example, an Admin role inherits all Editor permissions plus additional administrative permissions. 

Admin ──inherits──> Editor ──inherits──> Viewer

Database Schema 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Core RBAC tables

CREATE TABLE roles (

id SERIAL PRIMARY KEY,

name VARCHAR(50) UNIQUE NOT NULL,

description TEXT

);

CREATE TABLE permissions (

id SERIAL PRIMARY KEY,

resource VARCHAR(50) NOT NULL,

action VARCHAR(20) NOT NULL,

UNIQUE(resource, action)

);

CREATE TABLE role_permissions (

role_id INTEGER REFERENCES roles(id),

permission_id INTEGER REFERENCES permissions(id),

PRIMARY KEY (role_id, permission_id)

);

CREATE TABLE user_roles (

user_id INTEGER REFERENCES users(id),

role_id INTEGER REFERENCES roles(id),

granted_by INTEGER REFERENCES users(id),

granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

PRIMARY KEY (user_id, role_id)

);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- For hierarchical RBAC

CREATE TABLE role_hierarchy (

parent_role_id INTEGER REFERENCES roles(id),

child_role_id INTEGER REFERENCES roles(id),

PRIMARY KEY (parent_role_id, child_role_id)

);

Implementation Patterns 

Node.js / Express Middleware 

// Permission definition

const PERMISSIONS = {

ARTICLE: {

CREATE: 'article:create',

READ: 'article:read',

UPDATE: 'article:update',

DELETE: 'article:delete',

PUBLISH: 'article:publish'

},

USER: {

LIST: 'user:list',

MANAGE: 'user:manage'

}

};

// Role definitions with permission inheritance

const ROLES = {

viewer: {

permissions: ['article:read'],

inherits: []

},

editor: {

permissions: ['article:create', 'article:update'],

inherits: ['viewer']

},

admin: {

permissions: [

'article:delete', 'article:publish',

'user:list', 'user:manage'

],

inherits: ['editor']

}

};

// Authorization middleware

function authorize(...requiredPermissions) {

return (req, res, next) => {

const userRoles = req.user.roles;

const userPermissions = getUserPermissions(userRoles);

const hasPermission = requiredPermissions.every(

p => userPermissions.includes(p)

);

if (!hasPermission) {

return res.status(403).json({

error: 'Insufficient permissions'

});

}

next();

};

}

// Usage in routes

app.post('/api/articles',

authenticate,

authorize(PERMISSIONS.ARTICLE.CREATE),

createArticle

);

app.delete('/api/articles/:id',

authenticate,

authorize(PERMISSIONS.ARTICLE.DELETE),

deleteArticle

);

Python / FastAPI 

from enum import Enum

from functools import wraps

from fastapi import HTTPException, Depends

class Permission(Enum):

ARTICLE_CREATE = "article:create"

ARTICLE_READ = "article:read"

ARTICLE_UPDATE = "article:update"

ARTICLE_DELETE = "article:delete"

USER_MANAGE = "user:manage"

ROLE_PERMISSIONS = {

"viewer": {Permission.ARTICLE_READ},

"editor": {

Permission.ARTICLE_READ,

Permission.ARTICLE_CREATE,

Permission.ARTICLE_UPDATE,

},

"admin": {

Permission.ARTICLE_READ,

Permission.ARTICLE_CREATE,

Permission.ARTICLE_UPDATE,

Permission.ARTICLE_DELETE,

Permission.USER_MANAGE,

},

}

def require_permission(permission: Permission):

def decorator(func):

@wraps(func)

async def wrapper(_args,_ *kwargs):

user = kwargs.get('current_user')

if not user:

raise HTTPException(status_code=401)

user_perms = ROLE_PERMISSIONS.get(user.role, set())

if permission not in user_perms:

raise HTTPException(

status_code=403,

detail="Insufficient permissions"

)

return await func(_args,_ *kwargs)

return wrapper

return decorator

#### Usage

@app.delete("/articles/{article_id}")

@require_permission(Permission.ARTICLE_DELETE)

async def delete_article(article_id: int, current_user = Depends(get_current_user)):

#### Delete logic

pass

Attribute-Based Access Control (ABAC) 

For more granular control, extend RBAC with ABAC policies that consider resource attributes and context: 

def can_access_resource(user, resource, action):

"""Check RBAC first, then ABAC policies."""

#### RBAC check

if not has_role_permission(user.role, action):

return False

#### ABAC policies

policies = {

#### Users can edit their own articles

('article:update', 'article'): lambda u, r: r.author_id == u.id,

#### Admins can edit any article

('article:update', 'article'): lambda u, r: 'admin' in u.roles,

#### Only article authors can delete

('article:delete', 'article'): lambda u, r: r.author_id == u.id,

}

policy = policies.get((action, resource.type))

if policy:

return policy(user, resource)

return False

Performance Optimization 

Cache resolved permissions to avoid repeated database queries: 

import redis

import json

r = redis.Redis()

def get_cached_permissions(user_id):

cache_key = f"perms:{user_id}"

cached = r.get(cache_key)

if cached:

return json.loads(cached)

permissions = resolve_user_permissions(user_id)

r.setex(cache_key, 300, json.dumps(permissions)) # 5 min TTL

return permissions

Audit Logging 

Every authorization decision should be logged: 

def log_authorization(user_id, action, resource, granted, reason=""):

log_entry = {

"timestamp": datetime.utcnow().isoformat(),

"user_id": user_id,

"action": action,

"resource": resource,

"granted": granted,

"reason": reason,

"source_ip": request.remote_addr

}

audit_logger.info(json.dumps(log_entry))

Common Pitfalls 

  * **Role explosion** : Too many fine-grained roles become unmanageable. Aim for 5-10 roles maximum.

  * **Hardcoded role checks** : `if user.role === 'admin'` spreads business logic everywhere. Always check permissions, not role names.

  * **Missing negative permissions** : RBAC naturally handles allow rules. For deny rules, evaluate deny before allow.

  * **User in multiple roles** : Decide whether permissions are additive (union) or restrictive (intersection).




Summary 

RBAC simplifies authorization by grouping permissions into roles and assigning roles to users. Start with flat RBAC and add hierarchy as needed. Always check permissions rather than role names, cache resolved permissions for performance, and layer on ABAC policies for fine-grained access control. Log all authorization decisions for auditability.

**See also:** [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Encryption at Rest Guide](</en/security/encryption-at-rest.html>).

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>)

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>)

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>)

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>)

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>)
