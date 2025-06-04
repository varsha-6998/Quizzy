from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import date
import os
from db_config import get_db_connection

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
)

# Secret key (consider moving to environment variable for production)
app.secret_key = 'VarshaIsAStrongIndependentWoman'


# ----------------------------- Routes ----------------------------- #

@app.route('/')
def index():
    is_logged_in = session.get('logged_in', False)
    username = session.get('username') if is_logged_in else None
    return render_template('index.html', is_logged_in=is_logged_in, username=username)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return render_template('signin.html', error="Invalid email or password")

    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()
            return render_template('signin.html', error="Email already exists")

        cursor.execute(
            "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('signin'))

    return render_template('signin.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))

    username = session.get('username')
    user_id = session.get('user_id')
    useremail = session.get('email')  # you can replace this with actual email if stored in session

    # Fetch registered courses for this user
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT 
            c.course_name, 
            r.registration_date, 
            c.duration , 
            r.status
        FROM 
            registrations r
        JOIN 
            course c ON r.course_id = c.course_id
        WHERE 
            r.user_id = %s
    """
    cursor.execute(query, (user_id,))
    registered_courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        'dashboard.html',
        is_logged_in=True,
        username=username,
        useremail=useremail,
        registered_courses=registered_courses
    )


@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))

    return render_template('profile.html')


@app.route('/about')
def about():
    is_logged_in = session.get('logged_in', False)
    username = session.get('username', '')
    return render_template('about.html', is_logged_in=is_logged_in, username=username)


@app.route('/contact')
def contact():
    is_logged_in = session.get('logged_in', False)
    username = session.get('username', '')
    return render_template('contact.html', is_logged_in=is_logged_in, username=username)


@app.route('/course')
def course():
    is_logged_in = session.get('logged_in', False)
    username = session.get('username') if is_logged_in else None

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT course_id, course_name, course_description, duration FROM course")
    courses = cursor.fetchall()
    cursor.close()
    connection.close()

    course_list = [
        {
            'id': c[0],
            'name': c[1],
            'description': c[2],
            'duration': c[3]
        } for c in courses
    ]

    return render_template('course.html', is_logged_in=is_logged_in, username=username, courses=course_list)


@app.route('/registration')
def registration():
    course = request.args.get('course')
    course_name = request.args.get('course_name')
    is_logged_in = 'user' in session
    return render_template('registration.html', course=course, is_logged_in=is_logged_in)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Your message has been sent successfully!'})


@app.route('/enroll', methods=['POST'])
def enroll():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    data = request.get_json()
    course_id = data.get('course_id')
    user_id = session['user_id']

    if not course_id:
        return jsonify({'success': False, 'message': 'Course ID missing'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM registrations WHERE user_id = %s AND course_id = %s",
            (user_id, course_id)
        )
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Already enrolled'}), 400

        cursor.execute(
            "INSERT INTO registrations (user_id, course_id, registration_date, status) VALUES (%s, %s, %s, %s)",
            (user_id, course_id, date.today(), "In Progress")
        )
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Enrolled successfully'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Failed to enroll: {str(e)}'}), 500
    
@app.route('/admin')
def admin():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, email, password FROM user")
    users_data = cursor.fetchall()
        # Fetch courses
    cursor.execute("SELECT * FROM course")
    courses_data = cursor.fetchall()
    # fetch from registration
    cursor.execute("SELECT * FROM REGISTRATIONS")
    registrations_data=cursor.fetchall()



    cursor.close()
    connection.close()
    return render_template('admin.html', users=users_data,courses=courses_data,registrations=registrations_data)

@app.route('/delete_user/<email>', methods=['POST'])
def delete_user(email):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM user WHERE email = %s", (email,))
    connection.commit()
    cursor.close()
    connection.close()

    flash("User deleted successfully!", "success")
    return redirect(url_for('admin'))

@app.route('/edit_user', methods=['POST'])
def edit_user():
    original_email = request.form['original_email']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE user SET name=%s, email=%s, password=%s WHERE email=%s",
        (name, email, password, original_email)
    )
    connection.commit()
    cursor.close()
    connection.close()

    flash("User details updated!", "success")
    return redirect(url_for('admin'))

@app.route('/delete_course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'message': 'Course deleted successfully'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Error deleting course'})






# -------------------------- Run App -------------------------- #

if __name__ == '__main__':
    app.run(debug=True)
