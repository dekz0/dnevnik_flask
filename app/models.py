from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from app import login

class User(UserMixin):
    def __init__(self, username, email, password_hash):
        self.id = username  # Flask-Login использует `id` для идентификации
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def create(username, email, password):
        return User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    @staticmethod
    def from_dict(data):
        return User(
            username=data['username'],
            email=data['email'],
            password_hash=data['password']
        )

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password_hash
        }

    def __repr__(self):
        return f'<User {self.username}>'

# Flask-Login user loader
from app.utils import get_user_by_username

@login.user_loader
def load_user(username):
    user_data = get_user_by_username(username)
    return User.from_dict(user_data) if user_data else None
