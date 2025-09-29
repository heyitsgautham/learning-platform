"""
OpenAPI specification for Course Service
"""

def get_swagger_spec():
    """Returns the OpenAPI specification for Course Service"""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Course Service API",
            "description": "API for managing courses, enrollments, and related operations in the Smart Learning Platform",
            "version": "1.0.0",
            "contact": {
                "name": "Learning Platform Team"
            }
        },
        "servers": [
            {
                "url": "http://localhost:5003",
                "description": "Development server"
            }
        ],
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "query",
                    "name": "apiKey",
                    "description": "API key required for analytics endpoint"
                }
            },
            "schemas": {
                "Course": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "Course ID"},
                        "title": {"type": "string", "description": "Course title"},
                        "description": {"type": "string", "description": "Course description"},
                        "instructor_id": {"type": "integer", "description": "Instructor's user ID"},
                        "category": {"type": "string", "description": "Course category"},
                        "rating": {"type": "number", "format": "float", "description": "Course rating (0-5)"},
                        "max_students": {"type": "integer", "description": "Maximum number of students"},
                        "created_at": {"type": "string", "format": "date-time", "description": "Course creation timestamp"},
                        "instructor": {
                            "type": "object",
                            "description": "Instructor details from User Service"
                        },
                        "_links": {
                            "type": "object",
                            "description": "HATEOAS links for related operations"
                        }
                    }
                },
                "CourseCreate": {
                    "type": "object",
                    "required": ["title", "instructor_id"],
                    "properties": {
                        "title": {"type": "string", "description": "Course title"},
                        "description": {"type": "string", "description": "Course description"},
                        "instructor_id": {"type": "integer", "description": "Instructor's user ID"},
                        "category": {"type": "string", "description": "Course category"},
                        "max_students": {"type": "integer", "description": "Maximum number of students", "default": 50}
                    }
                },
                "CourseUpdate": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Course title"},
                        "description": {"type": "string", "description": "Course description"},
                        "category": {"type": "string", "description": "Course category"},
                        "rating": {"type": "number", "format": "float", "description": "Course rating (0-5)"},
                        "max_students": {"type": "integer", "description": "Maximum number of students"}
                    }
                },
                "Enrollment": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "Enrollment ID"},
                        "student_id": {"type": "integer", "description": "Student's user ID"},
                        "course_id": {"type": "integer", "description": "Course ID"},
                        "enrollment_date": {"type": "string", "format": "date-time", "description": "Enrollment timestamp"},
                        "course": {"$ref": "#/components/schemas/Course"},
                        "_links": {
                            "type": "object",
                            "description": "HATEOAS links for related operations"
                        }
                    }
                },
                "EnrollmentRequest": {
                    "type": "object",
                    "required": ["student_id"],
                    "properties": {
                        "student_id": {"type": "integer", "description": "Student's user ID"}
                    }
                },
                "CoursesResponse": {
                    "type": "object",
                    "properties": {
                        "courses": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Course"}
                        },
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer"},
                                "limit": {"type": "integer"},
                                "total": {"type": "integer"},
                                "pages": {"type": "integer"},
                                "has_next": {"type": "boolean"},
                                "has_prev": {"type": "boolean"}
                            }
                        },
                        "filters": {
                            "type": "object",
                            "properties": {
                                "category": {"type": "string"},
                                "sort": {"type": "string"}
                            }
                        },
                        "_links": {
                            "type": "object",
                            "description": "HATEOAS links for pagination and operations"
                        }
                    }
                },
                "EnrollmentsResponse": {
                    "type": "object",
                    "properties": {
                        "enrollments": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Enrollment"}
                        },
                        "student_id": {"type": "integer"},
                        "total": {"type": "integer"},
                        "_links": {
                            "type": "object",
                            "description": "HATEOAS links for related operations"
                        }
                    }
                },
                "ReportResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Report generation status"},
                        "timestamp": {"type": "string", "format": "date-time", "description": "Report generation timestamp"}
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
                },
                "AnalyticsResponse": {
                    "type": "object",
                    "properties": {
                        "total_courses": {"type": "integer", "description": "Total number of courses"},
                        "total_enrollments": {"type": "integer", "description": "Total number of enrollments"},
                        "course_categories": {
                            "type": "object",
                            "description": "Breakdown of courses by category",
                            "additionalProperties": {"type": "integer"}
                        },
                        "average_rating": {"type": "number", "format": "float", "description": "Average course rating"},
                        "timestamp": {"type": "string", "format": "date-time", "description": "Analytics generation timestamp"},
                        "_links": {
                            "type": "object",
                            "description": "HATEOAS links for related operations"
                        }
                    }
                }
            }
        },
        "paths": {
            "/": {
                "get": {
                    "summary": "Health check",
                    "description": "Check if the Course Service is healthy",
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
                    "description": "Get information about the Course Service",
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
                                            "endpoints": {"type": "object"},
                                            "dependencies": {"type": "object"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/courses": {
                "get": {
                    "summary": "Get all courses",
                    "description": "Retrieve courses with pagination, filtering, and sorting. Includes HATEOAS links.",
                    "tags": ["Courses"],
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "description": "Page number for pagination",
                            "schema": {"type": "integer", "default": 1, "minimum": 1}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "description": "Number of items per page",
                            "schema": {"type": "integer", "default": 10, "minimum": 1, "maximum": 100}
                        },
                        {
                            "name": "category",
                            "in": "query",
                            "description": "Filter by course category",
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "sort",
                            "in": "query",
                            "description": "Sort order",
                            "schema": {
                                "type": "string",
                                "enum": ["id_asc", "id_desc", "title_asc", "title_desc", "rating_asc", "rating_desc"],
                                "default": "id_asc"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "List of courses with pagination and HATEOAS links",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/CoursesResponse"}
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Create a new course",
                    "description": "Create a new course with instructor verification",
                    "tags": ["Courses"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CourseCreate"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Course created successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "course": {"$ref": "#/components/schemas/Course"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid request data",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        },
                        "404": {
                            "description": "Instructor not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/courses/{course_id}": {
                "get": {
                    "summary": "Get specific course",
                    "description": "Get a specific course by ID with instructor details and HATEOAS links",
                    "tags": ["Courses"],
                    "parameters": [
                        {
                            "name": "course_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the course to retrieve",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Course details",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "course": {"$ref": "#/components/schemas/Course"}
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Course not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                },
                "put": {
                    "summary": "Update course",
                    "description": "Update course details",
                    "tags": ["Courses"],
                    "parameters": [
                        {
                            "name": "course_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the course to update",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CourseUpdate"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Course updated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "course": {"$ref": "#/components/schemas/Course"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid request data",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        },
                        "404": {
                            "description": "Course not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                },
                "delete": {
                    "summary": "Delete course",
                    "description": "Delete a course and all associated enrollments",
                    "tags": ["Courses"],
                    "parameters": [
                        {
                            "name": "course_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the course to delete",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Course deleted successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SuccessMessage"}
                                }
                            }
                        },
                        "404": {
                            "description": "Course not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/courses/{course_id}/enroll": {
                "post": {
                    "summary": "Enroll student in course",
                    "description": "Enroll a student in a specific course",
                    "tags": ["Enrollments"],
                    "parameters": [
                        {
                            "name": "course_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the course to enroll in",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/EnrollmentRequest"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Student enrolled successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "enrollment": {"$ref": "#/components/schemas/Enrollment"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid request or student already enrolled or course at capacity",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        },
                        "404": {
                            "description": "Course not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/enrollments/student/{student_id}": {
                "get": {
                    "summary": "Get student enrollments",
                    "description": "Get all enrollments for a specific student with course details and HATEOAS links",
                    "tags": ["Enrollments"],
                    "parameters": [
                        {
                            "name": "student_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the student",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Student enrollments",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/EnrollmentsResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/generateReport": {
                "get": {
                    "summary": "Generate async report",
                    "description": "Generate a report using async patterns to simulate long-running tasks",
                    "tags": ["Reports"],
                    "responses": {
                        "200": {
                            "description": "Report generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ReportResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/analytics": {
                "get": {
                    "summary": "Get analytics data",
                    "description": "Get analytics data about courses and enrollments. Requires valid API key.",
                    "tags": ["Analytics"],
                    "security": [{"ApiKeyAuth": []}],
                    "parameters": [
                        {
                            "name": "apiKey",
                            "in": "query",
                            "required": True,
                            "description": "Valid API key for analytics access",
                            "schema": {"type": "string"},
                            "example": "validKey"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Analytics data retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AnalyticsResponse"}
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid or missing API key",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "tags": [
            {
                "name": "Courses",
                "description": "Course management operations with pagination, filtering, sorting, and HATEOAS"
            },
            {
                "name": "Enrollments",
                "description": "Student enrollment management"
            },
            {
                "name": "Reports",
                "description": "Async report generation"
            },
            {
                "name": "Analytics",
                "description": "Analytics data with API key authentication"
            }
        ]
    }