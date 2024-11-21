from .app import db, app
from flask_login import UserMixin

# User class ( UserMixin is used here due to User being used in authentication )
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=True, unique=True)
    password = db.Column(db.String, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    
    def __repr__(self) -> str:
        return f'User({self.username=}, {self.password=}, {self.age=})'
    
    def get_id(self):
        return self.uid
    
    
class Task(db.Model):
    __tablename__ = 'tasks'
    
    tid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    owner = db.relationship('User', backref='tasks')
    
    def __repr__(self) -> str:
        return f'Task({self.title=}, {self.description=}, {self.owner_id=})'
    
    def get_id(self):
        return self.tid

# Push app context to create all db tables
app.app_context().push()
# Create tables
db.create_all()