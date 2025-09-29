from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from datetime import datetime
import time

# Initialize SQLAlchemy instance
db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    """User model for storing user information and roles"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', 'admin', name='user_roles'), 
                     nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email} - {self.role}>'
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
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