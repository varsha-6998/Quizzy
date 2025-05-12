from flask import Flask, render_template, request, redirect, url_for, session
import os
from db_config import get_db_connection

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
)
app.secret_key = 'your_secret_key'  # Change this to a secure random key

@app.route('/')
def index():
    return render_template('index.html')

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
            return redirect(url_for('dashboardw'))
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
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    return render_template('profile.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)