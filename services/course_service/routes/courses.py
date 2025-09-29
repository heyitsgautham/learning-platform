from flask import Blueprint, request, jsonify
from models.database import db, Course, Enrollment
import requests
import os

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
    
    # Enrich courses with instructor details from User Service
    enriched_courses = []
    for course in courses:
        course_dict = course.to_dict()
        instructor = get_instructor_details(course.instructor_id)
        if instructor:
            course_dict['instructor'] = instructor
        else:
            course_dict['instructor'] = {'id': course.instructor_id, 'name': 'Unknown Instructor'}
        enriched_courses.append(course_dict)
    
    return jsonify({
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
        }
    })

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
    
    # Enrich with instructor details
    course_dict = new_course.to_dict()
    course_dict['instructor'] = instructor
    
    return jsonify({
        'message': 'Course created successfully',
        'course': course_dict
    }), 201

@courses_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get a specific course by ID"""
    course = Course.query.get_or_404(course_id)
    course_dict = course.to_dict()
    
    # Enrich with instructor details
    instructor = get_instructor_details(course.instructor_id)
    if instructor:
        course_dict['instructor'] = instructor
    else:
        course_dict['instructor'] = {'id': course.instructor_id, 'name': 'Unknown Instructor'}
    
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
    
    # Enrich with instructor details
    course_dict = course.to_dict()
    instructor = get_instructor_details(course.instructor_id)
    if instructor:
        course_dict['instructor'] = instructor
    else:
        course_dict['instructor'] = {'id': course.instructor_id, 'name': 'Unknown Instructor'}
    
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
    
    return jsonify({
        'message': 'Student enrolled successfully',
        'enrollment': enrollment.to_dict()
    }), 201

@courses_bp.route('/enrollments/student/<int:student_id>', methods=['GET'])
def get_student_enrollments(student_id):
    """Get all enrollments for a specific student"""
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    
    # Enrich with course details
    enriched_enrollments = []
    for enrollment in enrollments:
        enrollment_dict = enrollment.to_dict()
        enrollment_dict['course'] = enrollment.course.to_dict()
        
        # Add instructor details
        instructor = get_instructor_details(enrollment.course.instructor_id)
        if instructor:
            enrollment_dict['course']['instructor'] = instructor
        else:
            enrollment_dict['course']['instructor'] = {'id': enrollment.course.instructor_id, 'name': 'Unknown Instructor'}
        
        enriched_enrollments.append(enrollment_dict)
    
    return jsonify({
        'enrollments': enriched_enrollments,
        'student_id': student_id,
        'total': len(enriched_enrollments)
    })