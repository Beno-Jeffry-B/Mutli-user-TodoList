from flask import render_template, flash, request, redirect, url_for, session
from todo import app, db
from todo.forms import sign_up, login
from todo.models import User, Tasks
from datetime import datetime, timedelta
from todo import bcrypt
from flask_mail import Message
from todo import mail

from itsdangerous import URLSafeTimedSerializer


@app.route("/")
def landing_page():
    return render_template("index.html")


@app.route("/home")
def home_page():
    return render_template("homepage.html")


@app.route("/login", methods=['POST', 'GET'])
def login_page():
    form = login()
    if form.validate_on_submit():
        current_user_name = form.user_name.data
        current_password = form.password.data
        user = User.query.filter_by(user_name=current_user_name).first()
        if user and bcrypt.check_password_hash(user.password, current_password):  
            session['user_id'] = user.user_id
            return redirect(url_for('home_page'))
        else:
            flash("Username or Password is Incorrect. Try again...", 'warning')
            return render_template("login.html", form=form)
    else:
        print(form.errors.items())
        return render_template("login.html", form=form)




@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('login_page'))



from sqlalchemy.exc import IntegrityError

@app.route("/sign_up", methods=['POST', 'GET'])
def signup_page():
    form = sign_up()
    if form.validate_on_submit():
        user_name = form.user_name.data
        raw_password = form.password.data
        hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')
        email = form.email.data
        user = User(user_name=user_name, password=hashed_password, email=email)

        try:
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('login_page'))

        except IntegrityError as e:
            db.session.rollback()
            error_msg = str(e.orig)

            if "UNIQUE constraint failed: user.user_name" in error_msg:
                flash("Username already taken. Please choose a different one.", "danger")
            elif "UNIQUE constraint failed: user.email" in error_msg:
                flash("Email already registered. Please use a different one.", "danger")
            else:
                flash("An error occurred while creating your account. Please try again.", "danger")


    else:
        for field, error_msg in form.errors.items():
            for err in error_msg:
                flash(f'{err}', 'warning')

    return render_template("signup.html", form=form)




from flask import send_file
import matplotlib.pyplot as plt
import io
from matplotlib.figure import Figure


@app.route("/createlist", methods=['POST', 'GET'])
def createlist():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login to access your tasks.", "warning")
        return redirect(url_for('login_page'))

    if request.method == "POST":
        # ADD Task (Mobile + Desktop compatibility)
        if 'submit' in request.form:
            input_task = request.form.get('input_task')
            
            # Handle both 'priority' and 'new_priority'
            priority = request.form.get('priority') or request.form.get('new_priority') or 'Low'

            # Handle both 'due_date' and 'new_due_date'
            due_date_str = request.form.get('due_date') or request.form.get('new_due_date')
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

            task = Tasks(tasks=input_task, priority=priority, due_date=due_date, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            flash("Task Added Successfully!", "success")
            return redirect(url_for('createlist'))

        # Update priority (desktop)
        elif 'priority_update_btn' in request.form:
            task_id = request.form['task_id']
            new_priority = request.form['new_priority']
            task = Tasks.query.get(task_id)
            if task:
                task.priority = new_priority
                db.session.commit()
            return redirect(url_for('createlist'))  

        # Update due date (desktop)
        elif 'due_date_update_btn' in request.form:
            task_id = request.form['task_id']
            new_due_date = request.form['new_due_date']
            task = Tasks.query.get(task_id)
            if task and new_due_date:
                task.due_date = datetime.strptime(new_due_date, '%Y-%m-%d').date()
                db.session.commit()
            return redirect(url_for('createlist'))

        # Delete task
        elif 'delete_task' in request.form:
            task = Tasks.query.filter_by(task_id=request.form['task_id'], user_id=user_id).first()
            if task:
                db.session.delete(task)
                db.session.commit()
                flash("Task Deleted Successfully!", "success")
            return redirect(url_for('createlist'))

        # Edit task (mobile + desktop)
        elif 'edit_task' in request.form:
            task = Tasks.query.filter_by(task_id=request.form['task_id'], user_id=user_id).first()
            if task:
                task.tasks = request.form['updated_task']
                task.priority = request.form.get('updated_priority') or task.priority
                due = request.form.get('updated_due_date')
                task.due_date = datetime.strptime(due, '%Y-%m-%d').date() if due else task.due_date
                db.session.commit()
                flash("Task Updated Successfully!", "success")
            return redirect(url_for('createlist'))

        # Update status (mobile + desktop)
        elif 'status_update_btn' in request.form:
            task = Tasks.query.filter_by(task_id=request.form['task_id'], user_id=user_id).first()
            if task:
                task.status = request.form['new_status']
                db.session.commit()
                flash("Status Updated Successfully!", "success")
            return redirect(url_for('createlist'))

    # Handle GET and filtering
    filter_val = request.args.get('filter')
    query = Tasks.query.filter_by(user_id=user_id)
    today = datetime.today().date()
    end_of_week = today + timedelta(days=(6 - today.weekday()))  # Sunday

    if filter_val == 'due_today':
        query = query.filter(Tasks.due_date == today)
    elif filter_val == 'due_week':
        query = query.filter(Tasks.due_date >= today, Tasks.due_date <= end_of_week)
    elif filter_val == 'completed':
        query = query.filter(Tasks.status == 'completed')
    elif filter_val == 'pending':
        query = query.filter(Tasks.status != 'completed')

    tasks = query.order_by(Tasks.due_date).all()
    return render_template("createlist.html", tasks=tasks, current_filter=filter_val)



@app.route("/stats")
def stats():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login_page'))

    tasks = Tasks.query.filter_by(user_id=user_id).all()
    has_tasks = len(tasks) > 0 
    return render_template("stats.html" , has_tasks =has_tasks)



@app.route('/status_pie_chart')
def status_pie_chart():
    user_id = session.get('user_id')
    tasks = Tasks.query.filter_by(user_id=user_id).all()

    status_counts = {'not_started': 0, 'in_progress': 0, 'completed': 0}
    for task in tasks:
        status_counts[task.status] += 1

    fig = Figure()
    ax = fig.subplots()
    ax.pie(
        [status_counts['not_started'], status_counts['in_progress'], status_counts['completed']],
        labels=['Not Started', 'In Progress', 'Completed'],
        colors=['gray', 'orange', 'green'],
        autopct='%1.1f%%'
    )
    ax.set_title('Task Status')

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/priority_bar_chart')
def priority_bar_chart():
    user_id = session.get('user_id')
    tasks = Tasks.query.filter_by(user_id=user_id).all()

    priority_counts = {'Low': 0, 'Medium': 0, 'High': 0}
    for task in tasks:
        priority_counts[task.priority] += 1

    fig = Figure()
    ax = fig.subplots()
    ax.bar(priority_counts.keys(), priority_counts.values(), color=['green', 'orange', 'red'])
    ax.set_title('Task Priority')
    ax.set_xlabel('Priority')
    ax.set_ylabel('Count')

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


@app.route("/calendar")
def calendar():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login to access your calendar.", "warning")
        return redirect(url_for('login_page'))

    tasks = Tasks.query.filter_by(user_id=user_id).all()

    events = []
    for task in tasks:
        if task.due_date:
            events.append({
                "title": task.tasks,
                "start": task.due_date.strftime("%Y-%m-%d"),
                "color": get_color(task.priority)
            })

    return render_template("calendar.html", events=events)





def get_color(priority):
    if priority == 'High':
        return 'red'
    elif priority == 'Medium':
        return 'orange'
    return 'green'





@app.route("/about")
def about_page():
    return render_template('about1.html')

@app.route("/help")
def help_page():
    return render_template('about2.html')

@app.route("/settings")
def settings():
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')  # User not logged in
    
    user = User.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(user_id = session.get('user_id')).first()
    user_name = user.user_name
    email = user.email    
    return render_template('settings.html',user_name = user_name , email = email)

@app.route("/changeEmail", methods=["GET", "POST"])
def changeEmail():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.filter_by(user_id=session["user_id"]).first()

    if request.method == "POST":
        new_email = request.form.get("new_email")
        if new_email:
            user.email = new_email
            db.session.commit()
            flash("Email updated successfully.",'success')
            return redirect("/settings")
        
    return render_template("changeEmail.html", current_email=user.email)


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.filter_by(user_id=session["user_id"]).first()

    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password == confirm_password:
            if bcrypt.check_password_hash(user.password, current_password):
                user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                db.session.commit()
                flash("Password changed successfully.", "success")
                return redirect("/settings")
            else:
                flash("Current password is incorrect.", "danger")
                return redirect("/change_password")
        else:
            flash('New password and Confirm Password are not matched. Try again..!', "warning")
            return redirect("/change_password")

    return render_template("changePassword.html")



@app.route("/delete_account", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.filter_by(user_id=session["user_id"]).first()

    # Delete user and their tasks (if any)
    Tasks.query.filter_by(user_id=user.user_id).delete()  # optional
    db.session.delete(user)
    db.session.commit()
    session.clear()

    flash("Account deleted successfully." , 'success')
    return redirect("/")







def generate_reset_token(email):
    s = URLSafeTimedSerializer(app.secret_key)
    return s.dumps({'email' : email})




@app.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        current_email = request.form.get('email')
        user = User.query.filter_by(email=current_email).first()
        if user:
            token = generate_reset_token(user.email)
            reset_url = url_for('reset_password', token=token, _external=True)

            msg = Message("Password Reset Request",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[user.email])
            msg.body = f'''Hi {user.user_name},

To reset your password, click the following link:
{reset_url}

If you did not request a password reset, please ignore this email.
'''
            mail.send(msg)

            flash("Password reset link sent! Please check your email.", "info")
            return redirect(url_for('forgot_password'))
        else:
            flash("Email not found. Please try again.", "danger")
            return redirect(url_for('forgot_password'))

    return render_template("forgot_password.html")





def verify_token(token, max_age=60):
    s = URLSafeTimedSerializer(app.secret_key)
    try:
        data = s.loads(token, max_age=max_age)
        print(data)
        return data['email']
    except Exception:
        return None
        
    
@app.route('/reset_password/<token>', methods=["POST", "GET"])
def reset_password(token):
    email = verify_token(token)
    if not email:
        flash("Invalid or expired token.", "danger")
        return redirect(url_for('forgot_password'))

    if request.method == "POST":
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password == confirm_password:
            user = User.query.filter_by(email=email).first()
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()

            flash("Password reset successful. Please log in.", "success")
            return redirect(url_for('login_page'))
        else:
            flash("Passwords do not match. Try again.", "danger")

    return render_template('reset_password.html')



# DB testing

from flask import Blueprint, jsonify, request
debug_bp = Blueprint('debug', __name__)



@debug_bp.route('/debug/users', methods=['GET'])
def debug_users():
    secret_token = request.headers.get('X-API-KEY')
    
    if secret_token != 'taskify-debug-key': # Debug-Key
        return jsonify({'error': 'Unauthorized'}), 403

    users = User.query.all()
    user_data = [{'id': user.user_id, 'username': user.user_name, 'email': user.email} for user in users]

    return jsonify({'user_count': len(users), 'users': user_data})















