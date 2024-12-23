from flask import Flask, render_template, request, redirect, url_for, session, jsonify ,flash
from models import db, User, Schedule, Goal
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Note 
import os

app = Flask(__name__)

# Configure the app
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("instance/database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

# Ensure the `instance` folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

db.init_app(app)

# ----------- ROUTES -----------

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        try:
            # Debugging: Print email being queried
            print(f"Registering user with email: {email}")
            
            # Check if the email is already registered
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email is already registered. Please login.', 'error')
                return redirect(url_for('login'))

            # Save the new user
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            print(f"Unexpected error during registration: {e}")
            flash('An unexpected error occurred. Please try again.', 'error')

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Check if user exists
            user = User.query.filter_by(email=email).first()
            if not user:
                flash('User not found. Please register first.', 'error')
                return render_template('login.html')

            # Check password
            if not check_password_hash(user.password, password):
                flash('Incorrect password. Please try again.', 'error')
                return render_template('login.html')

            # Log the user in
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        except AttributeError:
            flash('Database error: User object or attribute missing.', 'error')
        except Exception as e:
            print(f"Unexpected error: {e}")
            flash('User not Found, Click On Register to Register', 'error')

        return render_template('login.html')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """Render the user's dashboard."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    # Fetch the schedules for the user
    schedules = Schedule.query.filter_by(user_id=user_id).all()

    # Fetch the most recent goal for the user (limit to 1)
    recent_goal = Goal.query.filter_by(user_id=user_id).order_by(Goal.id.desc()).first()

    # Fetch the most recent note for the user (limit to 1)
    recent_note = Note.query.filter_by(user_id=user_id).order_by(Note.id.desc()).first()

    return render_template('dashboard.html', user=user, schedules=schedules, recent_goal=recent_goal, recent_note=recent_note)



@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    """Add a new schedule."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        task_name = request.form.get('task_name')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')

        if not task_name or not due_date or not priority:
            return jsonify({"error": "All fields are required!"}), 400

        user_id = session['user_id']
        new_schedule = Schedule(user_id=user_id, task_name=task_name, due_date=due_date, priority=priority)
        try:
            db.session.add(new_schedule)
            db.session.commit()
            return redirect(url_for('view_schedules'))
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return render_template('add_schedule.html')


@app.route('/schedules')
def view_schedules():
    """View all schedules for the logged-in user."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    schedules = Schedule.query.filter_by(user_id=user_id).all()
    return render_template('view_schedules.html', schedules=schedules)


@app.route('/edit_schedule/<int:schedule_id>', methods=['GET', 'POST'])
def edit_schedule(schedule_id):
    """Edit an existing schedule."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.user_id != session['user_id']:
        return jsonify({"error": "Forbidden"}), 403

    if request.method == 'POST':
        schedule.task_name = request.form.get('task_name')
        schedule.due_date = request.form.get('due_date')
        schedule.priority = request.form.get('priority')
        try:
            db.session.commit()
            return redirect(url_for('view_schedules'))
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return render_template('edit_schedule.html', schedule=schedule)


@app.route('/delete_schedule/<int:schedule_id>', methods=['POST'])
def delete_schedule(schedule_id):
    if 'user_id' not in session:
        return "Unauthorized", 401  # Ensure the user is logged in

    schedule = Schedule.query.get(schedule_id)
    if not schedule or schedule.user_id != session['user_id']:
        return "Not Found", 404  # Return 404 if not found or not owned by user

    try:
        db.session.delete(schedule)
        db.session.commit()
        return '', 204  # Return HTTP 204 No Content on success
    except Exception as e:
        print(f"Error deleting schedule: {e}")
        return "Server Error", 500  # Handle server errors gracefully


#logout
@app.route('/logout')
def logout():
    """Log the user out and clear the session."""
    session.pop('user_id', None)
    return redirect(url_for('home'))

# For testing pupose

@app.route('/print_users')
def print_users():
    # Query all users from the database
    users = User.query.all()

    # Print each username and password in the terminal
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}")

    return "Usernames and passwords printed in the terminal."

# Goals

@app.route('/goals', methods=['GET', 'POST'])
def manage_goals():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if not title or not description:
            flash("Title and description cannot be empty!", "error")
            return redirect(url_for('manage_goals'))
        
        new_goal = Goal(user_id=user_id, title=title, description=description, progress=0)
        try:
            db.session.add(new_goal)
            db.session.commit()
            flash("Goal added successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
        return redirect(url_for('manage_goals'))

    goals = Goal.query.filter_by(user_id=user_id).all()
    return render_template('goals.html', goals=goals)


# Notes

@app.route('/notes', methods=['GET', 'POST'])
def manage_notes():
    """View and add notes."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            flash("Title and content cannot be empty!", "error")
            return redirect(url_for('manage_notes'))
        new_note = Note(user_id=user_id, title=title, content=content)
        try:
            db.session.add(new_note)
            db.session.commit()
            flash("Note added successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
        return redirect(url_for('manage_notes'))

    notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
    return render_template('notes.html', notes=notes)

# Route for editing a note
@app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    """Edit an existing note."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    note = Note.query.filter_by(id=note_id, user_id=user_id).first_or_404()

    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        try:
            db.session.commit()
            flash("Note updated successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
        return redirect(url_for('manage_notes'))  # Redirect back to notes list

    return render_template('edit_note.html', note=note)


# Route for deleting a note
@app.route('/notes/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    """Delete an existing note."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    note = Note.query.filter_by(id=note_id, user_id=user_id).first_or_404()

    try:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted successfully!", "danger")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")

    return redirect(url_for('manage_notes'))  # Redirect after delete to the notes page


# update status

@app.route('/update_task_status/<int:schedule_id>', methods=['POST'])
def update_task_status(schedule_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.user_id != session['user_id']:
        return redirect(url_for('dashboard'))

    status = request.form.get('status')
    if status in ['done', 'to-do']:
        schedule.status = status
        db.session.commit()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    app.run(debug=True)
