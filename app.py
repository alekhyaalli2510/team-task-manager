import os
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "mysecretkey"

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# ABOUT PAGE
@app.route('/about')
def about():
    return render_template('about.html')

# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['username'] = username
            session['role'] = user[3]

            return redirect('/dashboard')

        else:
            return "Invalid Username or Password"

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('role', None)

    return redirect('/login')

# CREATE PROJECT
@app.route('/create-project', methods=['GET', 'POST'])
def create_project():

    if 'username' not in session:
        return redirect('/login')

    if session['role'] != 'Admin':
        return "Access Denied"

    if request.method == 'POST':

        project_name = request.form['project_name']
        created_by = session['username']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO projects(project_name, created_by) VALUES (?, ?)",
            (project_name, created_by)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('create_project.html')

# CREATE TASK
@app.route('/create-task', methods=['GET', 'POST'])
def create_task():

    if 'username' not in session:
        return redirect('/login')

    if session['role'] != 'Admin':
        return "Access Denied"

    if request.method == 'POST':

        task_name = request.form['task_name']
        assigned_to = request.form['assigned_to']
        project_id = request.form['project_id']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks(task_name, assigned_to, status, project_id) VALUES (?, ?, ?, ?)",
            (task_name, assigned_to, "Pending", project_id)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('create_task.html')

# COMPLETE TASK
@app.route('/complete-task/<int:id>')
def complete_task(id):

    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'username' in session:

        username = session['username']
        role = session['role']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()

        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()

        conn.close()

        return render_template(
            'dashboard.html',
            username=username,
            role=role,
            projects=projects,
            tasks=tasks
        )

    return redirect('/login')

# RUN APP
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)