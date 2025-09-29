from flask import Blueprint, request, jsonify, session
from middleware.rbac import require_auth, require_role, require_roles, get_current_user

courses_bp = Blueprint('courses', __name__)

# Sample courses data (in real app, this would be from database)
sample_courses = [
    {"id": 1, "title": "Python Basics", "instructor": "John Doe", "category": "tech"},
    {"id": 2, "title": "Web Development", "instructor": "Jane Smith", "category": "tech"},
    {"id": 3, "title": "Data Science", "instructor": "Bob Johnson", "category": "tech"}
]

@courses_bp.route('/courses', methods=['GET'])
@require_roles(['student', 'teacher', 'admin'])
def get_courses():
    """Get all courses (accessible by students, teachers, and admins)"""
    current_user = get_current_user()
    return jsonify({
        'courses': sample_courses,
        'accessed_by': current_user.to_dict() if current_user else None
    })

@courses_bp.route('/courses', methods=['POST'])
@require_roles(['teacher', 'admin'])
def create_course():
    """Create a new course (teachers and admins only)"""
    current_user = get_current_user()
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Course title is required'}), 400
    
    new_course = {
        "id": len(sample_courses) + 1,
        "title": data['title'],
        "instructor": data.get('instructor', current_user.name),
        "category": data.get('category', 'general')
    }
    
    sample_courses.append(new_course)
    
    return jsonify({
        'message': 'Course created successfully',
        'course': new_course,
        'created_by': current_user.to_dict()
    }), 201

@courses_bp.route('/courses/<int:course_id>', methods=['PUT'])
@require_roles(['teacher', 'admin'])
def update_course(course_id):
    """Update a course (teachers and admins only)"""
    current_user = get_current_user()
    data = request.get_json()
    
    # Find course
    course = next((c for c in sample_courses if c['id'] == course_id), None)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # Update course data
    if 'title' in data:
        course['title'] = data['title']
    if 'instructor' in data:
        course['instructor'] = data['instructor']
    if 'category' in data:
        course['category'] = data['category']
    
    return jsonify({
        'message': 'Course updated successfully',
        'course': course,
        'updated_by': current_user.to_dict()
    })

@courses_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@require_role('student')
def enroll_course(course_id):
    """Enroll in a course (students only)"""
    current_user = get_current_user()
    
    # Find course
    course = next((c for c in sample_courses if c['id'] == course_id), None)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    return jsonify({
        'message': f'Successfully enrolled in {course["title"]}',
        'course': course,
        'student': current_user.to_dict()
    })

@courses_bp.route('/admin/analytics', methods=['GET'])
@require_role('admin')
def admin_analytics():
    """Get admin analytics (admins only)"""
    current_user = get_current_user()
    
    analytics_data = {
        'total_courses': len(sample_courses),
        'course_categories': {},
        'accessed_by': current_user.to_dict()
    }
    
    # Count courses by category
    for course in sample_courses:
        category = course['category']
        analytics_data['course_categories'][category] = analytics_data['course_categories'].get(category, 0) + 1
    
    return jsonify(analytics_data)