from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from datetime import datetime
import time

# Initialize SQLAlchemy instance
db = SQLAlchemy()
migrate = Migrate()

class Course(db.Model):
    """Course model for storing course information"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, nullable=False)  # References User.id from User Service
    category = db.Column(db.String(100), default='general')
    rating = db.Column(db.Float, default=0.0)
    max_students = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Course {self.title}>'
    
    def to_dict(self):
        """Convert course object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'instructor_id': self.instructor_id,
            'category': self.category,
            'rating': self.rating,
            'max_students': self.max_students,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Enrollment(db.Model):
    """Enrollment model for student-course relationships"""
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)  # References User.id from User Service
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_status = db.Column(db.Enum('enrolled', 'in_progress', 'completed', 'dropped', name='enrollment_status'), 
                                 default='enrolled')
    
    # Relationship
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))
    
    def __repr__(self):
        return f'<Enrollment student_id={self.student_id} course_id={self.course_id}>'
    
    def to_dict(self):
        """Convert enrollment object to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'completion_status': self.completion_status
        }

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Wait for database to be ready
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            with app.app_context():
                # Test connection first
                with db.engine.connect() as connection:
                    connection.execute(text('SELECT 1'))
                # Create all tables
                db.create_all()
                print("Database tables created successfully!")
                return
        except Exception as e:
            retry_count += 1
            print(f"Database connection attempt {retry_count}/{max_retries} failed: {e}")
            if retry_count < max_retries:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Failed to connect to database after all retries.")
                print("Please ensure PostgreSQL is running and accessible.")