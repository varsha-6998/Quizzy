from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import os
from db_config import get_db_connection

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
)
app.secret_key = 'VarshaIsAStrongIndependentWoman'  # Change this to a secure random key

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
        
        # Connect to database and verify user
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]  # Assuming the first column is user_id
            session['username'] = user[1]  # Assuming the second column is username
            return redirect(url_for('dashboard'))
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
        
        # Check if email already exists
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            connection.close()
            return render_template('registration.html', error="Email already exists")
        
        # Insert the user data into the database
        cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
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
    useremail=session.get('useremail')
    return render_template('dashboard.html', is_logged_in=True,username=username,useremail=useremail) 


@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    return render_template('profile.html')

@app.route('/about')
def about():
    is_logged_in = session.get('logged_in', False)
    username = session.get('username', '')  # if you want to show username
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

    # Convert tuples to list of dicts for easier use in template
    course_list = []
    for c in courses:
        course_list.append({
            'id': c[0],
            'name': c[1],
            'description': c[2],
            'duration': c[3]
        })

    return render_template('course.html', is_logged_in=is_logged_in,username=username, courses=course_list)
  




@app.route('/registration')
def registration():
    course = request.args.get('course')
    course_name=request.args.get('course_name')
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
    cursor.execute("INSERT INTO contact_message (name, email, message) VALUES (%s, %s, %s)", 
                   (name, email, message))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Your message has been sent successfully!'})


if __name__ == '__main__':
    app.run(debug=True)