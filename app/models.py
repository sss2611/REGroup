from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(64), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    points = db.Column(db.Integer, default=0)
    
    # Relación: Un usuario puede tener muchos depósitos
    deposits = db.relationship('Deposit', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class RegPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    
    # Relación: Un punto puede tener muchos depósitos
    deposits = db.relationship('Deposit', backref='reg_point', lazy=True)

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'lat': self.lat,
            'lon': self.lon
        }

class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_declared = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending_verification') # 'pending_verification', 'verified', 'rejected'
    points_awarded = db.Column(db.Integer, default=0)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reg_point_id = db.Column(db.Integer, db.ForeignKey('reg_point.id'))
    
    def __repr__(self):
        return f'<Deposit {self.item_declared}>'