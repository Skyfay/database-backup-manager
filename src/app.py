# Import the modules we need.
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from livereload import Server
from server.database_setup import db, Auth, Databases
from server.databases import test_mysql_connection, test_postgresql_connection
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


@app.route('/databases', methods=['GET', 'POST'])
def databases():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        db_type = request.form['dropdown']
        name = request.form['Add_DB_Name']
        db_host = request.form['Add_DB_Host']
        db_port = int(request.form['Add_DB_Port'])
        db_user = request.form['Add_DB_User']
        db_password = request.form['Add_DB_Password']
        db_name = request.form['Add_DB_DB_Name']

        # Überprüfung der Datenbankverbindung
        try:
            if db_type == 'mysql':
                success, message = test_mysql_connection(db_host, db_user, db_password, db_port)
                if not success:
                    session['error'] = message
                    return redirect(url_for('databases'))
            elif db_type == 'postgresql':
                success, message = test_postgresql_connection(db_host, db_user, db_password, db_port)
                if not success:
                    session['error'] = message
                    return redirect(url_for('databases'))
            elif db_type == 'mongodb':
                success, message = test_mysql_connection(db_host, db_user, db_password, db_port)
                if not success:
                    session['error'] = message
                    return redirect(url_for('databases'))
            else:
                session['error'] = "Ungültiger Datenbanktyp"
                return redirect(url_for('databases'))

        except Exception as e:
            session['error'] = f"Verbindung zur Datenbank konnte nicht hergestellt werden: {str(e)}"
            return redirect(url_for('databases'))

        # Erstellen eines neuen Databases-Objekts
        new_db = Databases(db_type=db_type, name=name, db_host=db_host, db_port=db_port, db_user=db_user, db_password=db_password, db_name=db_name)

        # Hinzufügen zur Datenbank und Commit
        db.session.add(new_db)
        db.session.commit()

        return redirect(url_for('databases'))

    if 'error' in session:
        error = session.pop('error')

    return render_template('databases.html', username=session['username'], active_page='databases', error=error)

# Add the login route.
@app.route('/login', methods=['GET', 'POST'])
def login():
    show_error = False

    if request.method == 'POST':
        # Get the username and password from the form.
        username = request.form['username']
        password = request.form['password']

        # Create the 'auth' table if it doesn't exist.
        database_setup.create_database_table(app)

        # Perform authentication logic by checking the username and password in the 'auth' table.
        user = Auth.query.filter_by(username=username).first()

        # If the user exists, add the username to the session and redirect to the home page.
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('dashboard'))

        # If the user doesn't exist, set the error flag in the session.
        else:
            session['show_error'] = True
            return redirect(url_for('login'))

    # If the request method is GET, check for the error flag in the session.
    if 'show_error' in session:
        show_error = True
        # Remove the flag from the session after retrieving it.
        session.pop('show_error')

    return render_template('login.html', show_error=show_error)



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
