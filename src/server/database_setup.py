from flask_sqlalchemy import SQLAlchemy
import os

# Add SQLAlchemy-Objekt
db = SQLAlchemy()

def get_db_uri_and_path():
    # Pfad zur SQLite-Datenbank
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'local.db')
    db_uri = f'sqlite:///{db_path}'
    return db_uri, db_path

# Database model for the 'auth' table
class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Auth('{self.username}')"

# Add the SQLite Database if not exist.
def add_database(app):
    db_uri, db_path = get_db_uri_and_path()
    if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        db.init_app(app)

        with app.app_context():
            if not os.path.exists(db_path):
                db.create_all()

# Create the 'auth' table if it doesn't exist and add the default admin user if no user exists.
def create_auth_table(app):
    with app.app_context():
        db.create_all()

        # Überprüfen, ob die Tabelle leer ist
        count = db.session.query(Auth).count()

        # Falls die Tabelle leer ist, Standard-Admin-Benutzer hinzufügen
        if count == 0:
            admin = Auth(username='Admin', password='Password')
            db.session.add(admin)
            db.session.commit()
