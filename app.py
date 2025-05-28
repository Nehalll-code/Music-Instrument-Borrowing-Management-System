from flask import Flask, render_template, request, redirect, session
import mysql.connector
from db_config import get_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # for session management

# Home/Login Page
@app.route('/test')
def test_page():
    return render_template('test.html')

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user['userId']
        session['name'] = user['name']
        session['role'] = user['role']

        if user['role'] == 'student':
            return redirect('/student/dashboard')
        elif user['role'] == 'faculty':
            return redirect('/faculty/dashboard')
        elif user['role'] == 'admin':
            return redirect('/admin/dashboard')
    return "Invalid credentials"

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                       (name, email, password, role))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    return render_template('register.html')

# Student Dashboard
@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect('/')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM instruments")
    instruments = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('student_dashboard.html', name=session.get('name'), instruments=instruments)
# Request Instrument
from datetime import date

@app.route('/student/request/<int:instrument_id>')
def request_instrument(instrument_id):
    if session.get('role') != 'student':
        return redirect('/')

    user_id = session.get('user_id')  # gets student ID from session
    today = date.today()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO borrow_requests (userId, instrumentId, date, status)
        VALUES (%s, %s, %s, %s)
    """, (user_id, instrument_id, today, 'pending'))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/student/dashboard')

# View Borrow Requests

# Faculty Dashboard
@app.route('/faculty/dashboard')
def faculty_dashboard():
    if session.get('role') != 'faculty':
        return redirect('/')
    return render_template('faculty_dashboard.html', name=session.get('name'))


# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('admin_dashboard.html', name=session.get('name'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/ping')
def ping_page():
    return "<h1>Ping successful!</h1>"
