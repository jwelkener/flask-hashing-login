# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create instances of SQLAlchemy and Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to the provided Flask app.

    This function should be called in your Flask app to initialize the database.
    """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model for storing user information."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    def __init__(self, username, password, email, first_name, last_name):
        """Initialize a user with provided information."""
        self.username = username
        # Hash the password using Bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user, hashing their password."""
        # Hash the password using Bcrypt
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        # Create a new user with hashed password
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        # Add the new user to the session
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exists and the password is correct.

        Return the user if valid; else return False.
        """
        # Query the user by username
        user = cls.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    """Feedback model for storing user feedback."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )
