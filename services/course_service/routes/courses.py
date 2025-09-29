from flask import Blueprint, request, jsonify
from models.database import db, Course, Enrollment
import requests
import os
from datetime import datetime

courses_bp = Blueprint('courses', __name__)

# User Service URL
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5002')

def get_instructor_details(instructor_id):
    """Fetch instructor details from User Service"""
    try:
        response = requests.get(f"{USER_SERVICE_URL}/api/users/{instructor_id}")
        if response.status_code == 200:
            return response.json().get('user')
        else:
            return None
    except Exception as e:
        print(f"Error fetching instructor details: {e}")
        return None

def add_hateoas_links(course_dict, base_url):
    """Add HATEOAS links to course dictionary"""
    course_id = course_dict['id']
    course_dict['_links'] = {
        'self': {
            'href': f"{base_url}/courses/{course_id}",
            'method': 'GET'
        },
        'update': {
            'href': f"{base_url}/courses/{course_id}",
            'method': 'PUT'
        },
        'delete': {
            'href': f"{base_url}/courses/{course_id}",
            'method': 'DELETE'
        },
        'enroll': {
            'href': f"{base_url}/courses/{course_id}/enroll",
            'method': 'POST'
        },
        'instructor': {
            'href': f"{USER_SERVICE_URL}/api/users/{course_dict['instructor_id']}",
            'method': 'GET'
        }
    }
    return course_dict

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    """Get all courses with pagination, filtering, and sorting"""
    # Pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Filtering
    category = request.args.get('category')
    
    # Sorting
    sort = request.args.get('sort', 'id_asc')
    
    # Build query
    query = Course.query
    
    if category:
        query = query.filter(Course.category == category)
    
    # Apply sorting
    if sort == 'title_asc':
        query = query.order_by(Course.title.asc())
    elif sort == 'title_desc':
        query = query.order_by(Course.title.desc())
    elif sort == 'rating_asc':
        query = query.order_by(Course.rating.asc())
    elif sort == 'rating_desc':
        query = query.order_by(Course.rating.desc())
    elif sort == 'id_desc':
        query = query.order_by(Course.id.desc())
    else:  # default: id_asc
        query = query.order_by(Course.id.asc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    courses = pagination.items
    
    # Get base URL for HATEOAS links
    base_url = request.url_root.rstrip('/')
    
    # Enrich courses with instructor details from User Service and add HATEOAS links
    enriched_courses = []
    for course in courses:
        course_dict = course.to_dict()
        instructor = get_instructor_details(course.instructor_id)
        if instructor:
            course_dict['instructor'] = instructor
        else:
            course_dict['instructor'] = {'id': course.instructor_id, 'name': 'Unknown Instructor'}
        
        # Add HATEOAS links
        course_dict = add_hateoas_links(course_dict, base_url)
        enriched_courses.append(course_dict)
    
    # Prepare response with HATEOAS links for pagination
    response_data = {
        'courses': enriched_courses,
        'pagination': {
            'page': page,
            'limit': limit,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        },
        'filters': {
            'category': category,
            'sort': sort
        },
        '_links': {
            'self': {
                'href': request.url,
                'method': 'GET'
            },
            'create': {
                'href': f"{base_url}/courses",
                'method': 'POST'
            }
        }
    }
    
    # Add pagination links
    if pagination.has_next:
        next_url = request.base_url + f"?page={page + 1}&limit={limit}"
        if category:
            next_url += f"&category={category}"
        if sort != 'id_asc':
            next_url += f"&sort={sort}"
        response_data['_links']['next'] = {
            'href': next_url,
            'method': 'GET'
        }
    
    if pagination.has_prev:
        prev_url = request.base_url + f"?page={page - 1}&limit={limit}"
        if category:
            prev_url += f"&category={category}"
        if sort != 'id_asc':
            prev_url += f"&sort={sort}"
        response_data['_links']['prev'] = {
            'href': prev_url,
            'method': 'GET'
        }
    
    return jsonify(response_data)

@courses_bp.route('/courses', methods=['POST'])
def create_course():
    """Create a new course"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'instructor_id' not in data:
        return jsonify({'error': 'Course title and instructor_id are required'}), 400
    
    # Verify instructor exists in User Service
    instructor = get_instructor_details(data['instructor_id'])
    if not instructor:
        return jsonify({'error': 'Instructor not found'}), 404
    
    new_course = Course(
        title=data['title'],
        description=data.get('description', ''),
        instructor_id=data['instructor_id'],
        category=data.get('category', 'general'),
        max_students=data.get('max_students', 50)
    )
    
    db.session.add(new_course)
    db.session.commit()
    
    # Get base URL for HATEOAS links
    base_url = request.url_root.rstrip('/')
    
    # Enrich with instructor details and HATEOAS links
    course_dict = new_course.to_dict()
    course_dict['instructor'] = instructor
    course_dict = add_hateoas_links(course_dict, base_url)
    
    return jsonify({
        'message': 'Course created successfully',
        'course': course_dict
    }), 201

@courses_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get a specific course by ID"""
    course = Course.query.get_or_404(course_id)
    course_dict = course.to_dict()
    
    # Get base URL for HATEOAS links
    base_url = request.url_root.rstrip('/')
    
    # Enrich with instructor details
    instructor = get_instructor_details(course.instructor_id)
    if instructor:
        course_dict['instructor'] = instructor
    else:
        course_dict['instructor'] = {'id': course.instructor_id, 'name': 'Unknown Instructor'}
    
    # Add HATEOAS links
    course_dict = add_hateoas_links(course_dict, base_url)
    
    return jsonify({'course': course_dict})

@courses_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Update a course"""
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'title' in data:
        course.title = data['title']
    if 'description' in data:
        course.description = data['description']
    if 'category' in data:
        course.category = data['category']
    if 'rating' in data:
        course.rating = data['rating']
    if 'max_students' in data:
        course.max_students = data['max_students']
    
    db.session.commit()
    
    # Get base URL for HATEOAS links
    base_url = request.url_root.rstrip('/')
    
    # Enrich with instructor details
    course_dict = course.to_dict()
    instructor = get_instructor_details(course.instructor_id)
    if instructor:
        course_dict['instructor'] = instructor
    else:
        course_dict['instructor'] = {'id': course.instructor_id, 'name': 'Unknown Instructor'}
    
    # Add HATEOAS links
    course_dict = add_hateoas_links(course_dict, base_url)
    
    return jsonify({
        'message': 'Course updated successfully',
        'course': course_dict
    })

@courses_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Delete a course"""
    course = Course.query.get_or_404(course_id)
    
    # Delete associated enrollments first
    Enrollment.query.filter_by(course_id=course_id).delete()
    
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': 'Course deleted successfully'})

@courses_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
def enroll_student(course_id):
    """Enroll a student in a course"""
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    
    if not data or 'student_id' not in data:
        return jsonify({'error': 'student_id is required'}), 400
    
    student_id = data['student_id']
    
    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        student_id=student_id, 
        course_id=course_id
    ).first()
    
    if existing_enrollment:
        return jsonify({'error': 'Student already enrolled in this course'}), 400
    
    # Check if course is at capacity
    current_enrollments = Enrollment.query.filter_by(course_id=course_id).count()
    if current_enrollments >= course.max_students:
        return jsonify({'error': 'Course is at maximum capacity'}), 400
    
    # Create enrollment
    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id
    )
    
    db.session.add(enrollment)
    db.session.commit()
    
    # Get base URL for HATEOAS links
    base_url = request.url_root.rstrip('/')
    
    # Add HATEOAS links to enrollment response
    enrollment_dict = enrollment.to_dict()
    enrollment_dict['_links'] = {
        'self': {
            'href': f"{base_url}/enrollments/student/{student_id}",
            'method': 'GET'
        },
        'course': {
            'href': f"{base_url}/courses/{course_id}",
            'method': 'GET'
        },
        'student': {
            'href': f"{USER_SERVICE_URL}/api/users/{student_id}",
            'method': 'GET'
        }
    }
    
    return jsonify({
        'message': 'Student enrolled successfully',
        'enrollment': enrollment_dict
    }), 201

@courses_bp.route('/enrollments/student/<int:student_id>', methods=['GET'])
def get_student_enrollments(student_id):
    """Get all enrollments for a specific student"""
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    
    # Get base URL for HATEOAS links
    base_url = request.url_root.rstrip('/')
    
    # Enrich with course details and HATEOAS links
    enriched_enrollments = []
    for enrollment in enrollments:
        enrollment_dict = enrollment.to_dict()
        course_dict = enrollment.course.to_dict()
        
        # Add instructor details
        instructor = get_instructor_details(enrollment.course.instructor_id)
        if instructor:
            course_dict['instructor'] = instructor
        else:
            course_dict['instructor'] = {'id': enrollment.course.instructor_id, 'name': 'Unknown Instructor'}
        
        # Add HATEOAS links to course
        course_dict = add_hateoas_links(course_dict, base_url)
        enrollment_dict['course'] = course_dict
        
        # Add HATEOAS links to enrollment
        enrollment_dict['_links'] = {
            'self': {
                'href': f"{base_url}/enrollments/student/{student_id}",
                'method': 'GET'
            },
            'course': {
                'href': f"{base_url}/courses/{enrollment.course_id}",
                'method': 'GET'
            },
            'student': {
                'href': f"{USER_SERVICE_URL}/api/users/{student_id}",
                'method': 'GET'
            }
        }
        
        enriched_enrollments.append(enrollment_dict)
    
    return jsonify({
        'enrollments': enriched_enrollments,
        'student_id': student_id,
        'total': len(enriched_enrollments),
        '_links': {
            'self': {
                'href': f"{base_url}/enrollments/student/{student_id}",
                'method': 'GET'
            },
            'student': {
                'href': f"{USER_SERVICE_URL}/api/users/{student_id}",
                'method': 'GET'
            }
        }
    })

@courses_bp.route('/analytics', methods=['GET'])
def analytics():
    """
    Analytics endpoint that requires valid API key.
    Get analytics data about courses and enrollments.
    """
    # Check for API key
    api_key = request.args.get('apiKey')
    expected_key = os.getenv('ANALYTICS_API_KEY', 'validKey')
    
    if not api_key or api_key != expected_key:
        return jsonify({'error': 'Valid API key required. Use ?apiKey=validKey'}), 401
    
    # Generate analytics data
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    # Course categories breakdown
    course_categories = {}
    courses = Course.query.all()
    for course in courses:
        category = course.category or 'uncategorized'
        course_categories[category] = course_categories.get(category, 0) + 1
    
    # Average rating
    courses_with_rating = Course.query.filter(Course.rating.isnot(None)).all()
    avg_rating = sum(c.rating for c in courses_with_rating) / len(courses_with_rating) if courses_with_rating else 0
    
    analytics_data = {
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'course_categories': course_categories,
        'average_rating': round(avg_rating, 2),
        'timestamp': datetime.now().isoformat(),
        '_links': {
            'self': {
                'href': request.url,
                'method': 'GET'
            },
            'courses': {
                'href': f"{request.url_root.rstrip('/')}/api/courses",
                'method': 'GET'
            }
        }
    }
    
    return jsonify(analytics_data)