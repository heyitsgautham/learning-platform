"""
OpenAPI specification for User Service
"""

def get_swagger_spec():
    """Returns the OpenAPI specification for User Service"""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "User Service API",
            "description": "API for managing users, authentication, and roles in the Smart Learning Platform",
            "version": "1.0.0",
            "contact": {
                "name": "Learning Platform Team"
            }
        },
        "servers": [
            {
                "url": "http://localhost:5002",
                "description": "Development server"
            }
        ],
        "components": {
            "securitySchemes": {
                "OAuth2": {
                    "type": "oauth2",
                    "description": "Google OAuth2 authentication",
                    "flows": {
                        "authorizationCode": {
                            "authorizationUrl": "https://accounts.google.com/o/oauth2/auth",
                            "tokenUrl": "https://oauth2.googleapis.com/token",
                            "scopes": {
                                "openid": "OpenID Connect",
                                "email": "Access email address",
                                "profile": "Access profile information"
                            }
                        }
                    }
                },
                "SessionAuth": {
                    "type": "apiKey",
                    "in": "cookie",
                    "name": "session",
                    "description": "Session-based authentication"
                }
            },
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "User ID"},
                        "email": {"type": "string", "format": "email", "description": "User email"},
                        "name": {"type": "string", "description": "User full name"},
                        "role": {"type": "string", "enum": ["student", "teacher", "admin"], "description": "User role"},
                        "google_id": {"type": "string", "description": "Google OAuth ID"},
                        "created_at": {"type": "string", "format": "date-time", "description": "User creation timestamp"}
                    }
                },
                "UserList": {
                    "type": "object",
                    "properties": {
                        "users": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/User"}
                        },
                        "total": {"type": "integer", "description": "Total number of users"}
                    }
                },
                "RoleUpdate": {
                    "type": "object",
                    "required": ["role"],
                    "properties": {
                        "role": {"type": "string", "enum": ["student", "teacher", "admin"], "description": "New role for the user"}
                    }
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string", "description": "Error message"}
                    }
                },
                "SuccessMessage": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "Success message"}
                    }
                }
            }
        },
        "paths": {
            "/": {
                "get": {
                    "summary": "Health check",
                    "description": "Check if the User Service is healthy",
                    "responses": {
                        "200": {
                            "description": "Service is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "service": {"type": "string"},
                                            "status": {"type": "string"},
                                            "message": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/info": {
                "get": {
                    "summary": "Service information",
                    "description": "Get information about the User Service",
                    "responses": {
                        "200": {
                            "description": "Service information",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "service": {"type": "string"},
                                            "version": {"type": "string"},
                                            "description": {"type": "string"},
                                            "endpoints": {"type": "object"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/auth/login": {
                "get": {
                    "summary": "Initiate Google OAuth login",
                    "description": "Redirects to Google OAuth consent screen",
                    "tags": ["Authentication"],
                    "responses": {
                        "302": {
                            "description": "Redirect to Google OAuth"
                        },
                        "500": {
                            "description": "OAuth not configured",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/auth/callback": {
                "get": {
                    "summary": "OAuth callback",
                    "description": "Handle OAuth callback from Google",
                    "tags": ["Authentication"],
                    "parameters": [
                        {
                            "name": "code",
                            "in": "query",
                            "description": "Authorization code from Google",
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "user": {"$ref": "#/components/schemas/User"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Authentication failed",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/auth/logout": {
                "post": {
                    "summary": "Logout user",
                    "description": "Clear user session",
                    "tags": ["Authentication"],
                    "security": [{"SessionAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Logged out successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SuccessMessage"}
                                }
                            }
                        }
                    }
                }
            },
            "/auth/profile": {
                "get": {
                    "summary": "Get current user profile",
                    "description": "Get profile of the currently authenticated user",
                    "tags": ["Authentication"],
                    "security": [{"SessionAuth": []}],
                    "responses": {
                        "200": {
                            "description": "User profile",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "user": {"$ref": "#/components/schemas/User"}
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Not authenticated",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/auth/change-role": {
                "post": {
                    "summary": "Change user role",
                    "description": "Change the role of the currently authenticated user (for testing purposes)",
                    "tags": ["Authentication"],
                    "security": [{"SessionAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RoleUpdate"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Role changed successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "user": {"$ref": "#/components/schemas/User"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid role",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        },
                        "401": {
                            "description": "Not authenticated",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/users": {
                "get": {
                    "summary": "Get all users",
                    "description": "Retrieve a list of all users in the system",
                    "tags": ["Users"],
                    "responses": {
                        "200": {
                            "description": "List of users",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/UserList"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/users/{user_id}": {
                "get": {
                    "summary": "Get specific user",
                    "description": "Get a specific user by their ID",
                    "tags": ["Users"],
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the user to retrieve",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "User details",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "user": {"$ref": "#/components/schemas/User"}
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "User not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/users/by-role/{role}": {
                "get": {
                    "summary": "Get users by role",
                    "description": "Get all users with a specific role",
                    "tags": ["Users"],
                    "parameters": [
                        {
                            "name": "role",
                            "in": "path",
                            "required": True,
                            "description": "Role to filter by",
                            "schema": {"type": "string", "enum": ["student", "teacher", "admin"]}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Users with specified role",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "users": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/User"}
                                            },
                                            "role": {"type": "string"},
                                            "total": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid role",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/users/{user_id}/role": {
                "put": {
                    "summary": "Update user role",
                    "description": "Update the role of a specific user",
                    "tags": ["Users"],
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the user to update",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RoleUpdate"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Role updated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "user": {"$ref": "#/components/schemas/User"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid role",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        },
                        "404": {
                            "description": "User not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/users/instructors": {
                "get": {
                    "summary": "Get all instructors",
                    "description": "Get all users with teacher role (instructors)",
                    "tags": ["Users"],
                    "responses": {
                        "200": {
                            "description": "List of instructors",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "instructors": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/User"}
                                            },
                                            "total": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "tags": [
            {
                "name": "Authentication",
                "description": "OAuth2 authentication and session management"
            },
            {
                "name": "Users",
                "description": "User management and role-based operations"
            }
        ]
    }