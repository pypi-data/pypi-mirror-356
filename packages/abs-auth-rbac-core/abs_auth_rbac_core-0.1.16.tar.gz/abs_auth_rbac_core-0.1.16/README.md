# ABS Auth RBAC Core

A comprehensive authentication and Role-Based Access Control (RBAC) package for FastAPI applications. This package provides robust JWT-based authentication and flexible role-based permission management using Casbin.

## Features

- JWT-based authentication with customizable token expiration
- Password hashing using bcrypt
- Role-Based Access Control (RBAC) with Casbin integration
- Flexible permission management
- User-role and role-permission associations
- Middleware for authentication and authorization

## Installation

```bash
pip install abs-auth-rbac-core
```

## Quick Start

### 1. Authentication Setup

```python
from abs_auth_rbac_core.auth.jwt_functions import JWTFunctions
import os

# Initialize JWT functions with environment variables
jwt_functions = JWTFunctions(
    secret_key=os.getenv("JWT_SECRET_KEY"),
    algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
)

# Create access token
token = jwt_functions.create_access_token(data={"sub": "user_id"})

# Verify password
is_valid = jwt_functions.verify_password(plain_password, hashed_password)

# Get password hash
hashed_password = jwt_functions.get_password_hash(plain_password)
```

### 2. RBAC Setup

```python
from abs_auth_rbac_core.rbac.service import RBACService

# Initialize RBAC service
rbac_service = RBACService(
    session=your_db_session
)

# Create a role with permissions
role = rbac_service.create_role(
    name="admin",
    description="Administrator role",
    permission_ids=["permission_uuid1", "permission_uuid2"]
)

# Assign roles to user
rbac_service.bulk_assign_roles_to_user(
    user_uuid="user_uuid",
    role_uuids=["role_uuid1", "role_uuid2"]
)

# Check permission
has_permission = rbac_service.check_permission(
    user_uuid="user_uuid",
    resource="resource_name",
    action="action_name",
    module="module_name"
)
```

## Core Components

### Authentication (`auth/`)
- `jwt_functions.py`: JWT token management and password hashing
- `middleware.py`: Authentication middleware for FastAPI
- `auth_functions.py`: Core authentication functions

### RBAC (`rbac/`)
- `service.py`: Main RBAC service with role and permission management
- `decorator.py`: Decorators for permission checking

### Models (`models/`)
- `user.py`: User model
- `roles.py`: Role model
- `permissions.py`: Permission model
- `user_role.py`: User-Role association model
- `role_permission.py`: Role-Permission association model
- `rbac_model.py`: Base RBAC model
- `base_model.py`: Base model with common fields

## Usage Examples

### 1. Setting Up Authentication Middleware

```python
from fastapi import FastAPI, Depends
from dependency_injector import containers, providers
from abs_auth_rbac_core.auth.middleware import auth_middleware
from abs_auth_rbac_core.rbac import RBACService

# Create a container for dependency injection
class Container(containers.DeclarativeContainer):
    # Database session provider
    db_session = providers.Factory(your_db_session_factory)
    
    # RBAC service provider
    rbac_service = providers.Factory(
        RBACService,
        session=db_session
    )
    
    # Auth middleware provider
    get_auth_middleware = providers.Factory(
        auth_middleware,
        db_session=db_session,
        jwt_secret_key=os.getenv("JWT_SECRET_KEY"),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256")
    )

# Initialize FastAPI app
app = FastAPI()
container = Container()
app.container = container
```

### 2. Applying Middleware to Routers

```python
from fastapi import FastAPI, Depends
from src.core.container import Container

class CreateApp:
    def __init__(self):
        self.container = Container()
        self.auth_middleware = self.container.get_auth_middleware()
        
        self.app = FastAPI(
            title="Your Service",
            description="Service Description",
            version="0.0.1"
        )
        
        # Apply middleware to specific routers
        self.app.include_router(
            users_router,
            dependencies=[Depends(self.auth_middleware)],
            tags=["Users"]
        )
        
        # Public routes (no middleware)
        self.app.include_router(
            public_router,
            tags=["Public"]
        )
```

### 3. Permission Management

```python
from abs_auth_rbac_core.util.permission_constants import (
    PermissionAction,
    PermissionModule,
    PermissionResource
)

# permissions
permission = PermissionData(
    name="User Management",
    description="Manage user accounts",
    module=PermissionModule.USER_MANAGEMENT,
    resource=PermissionResource.USER_MANAGEMENT,
    action=PermissionAction.MANAGE
)

# Check permissions in route
@app.get("/users")
@rbac_require_permission(
    f"{PermissionModule.USER_MANAGEMENT.value}:{PermissionResource.USER_MANAGEMENT.value}:{PermissionAction.VIEW.value}"
)
async def list_users():
    return {"users": [...]}
```

## Error Handling

The package includes comprehensive error handling for common scenarios:
- `UnauthorizedError`: For invalid or expired tokens
- `ValidationError`: For invalid token formats
- `DuplicatedError`: For duplicate role names
- `NotFoundError`: For non-existent resources
- `PermissionDeniedError`: For insufficient permissions

## Best Practices

1. Always use environment variables for sensitive data (secret keys, etc.)
2. Implement proper error handling for authentication and authorization failures
3. Use the middleware for global authentication
4. Implement proper logging for security-related events
5. Regularly rotate secret keys and tokens
6. Use strong password policies
7. Implement rate limiting for authentication endpoints

## License

This project is licensed under the MIT License - see the LICENSE file for details.
