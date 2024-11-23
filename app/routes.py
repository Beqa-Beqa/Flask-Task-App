from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from .models import User, Task

def register_routes(app, db):
    # Bcrypt instance for hashing
    bcrypt = Bcrypt(app)
    
    
    # Index page
    @app.route('/')
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
        # Fetch tasks from databse
        own_tasks = Task.query.filter_by(owner_id=current_user.uid).all()
        
        return render_template('auth/index.html', styles='styles/index.css', scripts='scripts/index.js', tasks=own_tasks)
    
    
    # Login page
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # If user is authenticated, we don't want them to access login page
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'GET':
            return render_template('core/login.html', styles='styles/login-register.css')
        
        elif request.method == 'POST':
            # Get user info from request
            username = request.form.get('username')
            password = request.form.get('password')
            
            # If any field is empty, flash respective message
            if not all((username, password)):
                flash('Please fill all the fields!')
                return redirect(url_for('login'))
        
            # Get user
            user = User.query.filter_by(username=username).one_or_none()
            # Check match if user is found, else it's false
            is_password_match = bcrypt.check_password_hash(user.password, password) if user else False
            
            # If user is not found or is found and passwords do not match flash
            # Respective message
            if not user or not is_password_match:
                flash('Invalid credentials!')
                return redirect(url_for('login'))
            
            flash('Logged in successfully!')
            login_user(user)
            
            return redirect(url_for('index'))
        
        
    # Register page
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        # If user is authenticated, we don't want them to access register page
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'GET':
            return render_template('core/register.html', styles='styles/login-register.css')

        elif request.method == 'POST':
            # Get usesrs information
            username = request.form.get('username')
            age = request.form.get('age')
            password = request.form.get('password')
            
            # Check if user exists
            existing_user = User.query.filter_by(username=username).one_or_none()
            
            # Check if all fields are provided
            if not all((username, age, password)):
                flash('Not all fields are filled!')
                return redirect(url_for('register'))
            
            elif existing_user:
                flash('Username already in use!')
                return redirect(url_for('register'))
            
            # Generate password hash
            password = bcrypt.generate_password_hash(password)
            
            # Create new user
            new_user = User(username=username, age=age, password=password)
            
            # Add that user to db
            db.session.add(new_user)
            db.session.commit()
            
            flash('You registered successfully!')
            login_user(new_user)
            
            return redirect(url_for('index'))
        
    
    # Logout route
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    
    # Task upload route
    @app.route('/upload_task', methods=['POST'])
    def upload_task():
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not all((title, description)):
            flash('You should fill both title and description fields!')
            return redirect(url_for('index'))
        
        new_task = Task(title=title, description=description, owner_id=current_user.uid)
        
        db.session.add(new_task)
        db.session.commit()
        
        return redirect(url_for('index'))