# Import the modules we need.
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from livereload import Server
from server.database_setup import db, Auth
from server import database_setup

# Create the app.
app = Flask(__name__)
# Set the secret key for the session.
app.secret_key = 'my_secret_key'

# Add the SQLite Database if not exist.
database_setup.add_database(app)

@app.route('/')
def dashboard():
    if 'username' in session:
        return render_template('index.html', username=session['username'], active_page='dashboard')
    return redirect(url_for('login'))


@app.route('/databases')
def databases():
    if 'username' in session:
        return render_template('databases.html', username=session['username'], active_page='databases')
    return redirect(url_for('login'))

# Add the login route.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form.
        username = request.form['username']
        password = request.form['password']

        # Create the 'auth' table if it doesn't exist
        database_setup.create_database_table(app)

        # Perform authentication logic by checking the username and password in the 'auth' table
        user = Auth.query.filter_by(username=username).first()

        # If the user exists, add the username to the session and redirect to the home page.
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('dashboard'))

        # If the user doesn't exist, show an error message.
        else:
            return render_template('login.html', show_error=True)

    # If the request method is GET, show the login page.
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()
    #app.run(host='0.0.0.0', port=5000)
