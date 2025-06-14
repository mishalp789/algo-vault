from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

db = SQLAlchemy()



class User(db.Model, UserMixin):  # 👈 Add UserMixin here
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)
    
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    platform = db.Column(db.String(50))
    difficulty = db.Column(db.String(20))
    status = db.Column(db.String(20))  # Solved, Unsolved
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
