import sqlite3
from sqlite3.dbapi2 import connect
from flask import Flask,g,render_template,request,session,flash,redirect, url_for,abort


#database setup
DATABASE = "projects.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "1234"

#create a new app
app = Flask(__name__)


#load the db
app.config.from_object(__name__)


#connect to database
def connect_db():
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv

#create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("dbschema.sql",mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

#open DB connection
def get_db():
    if not hasattr(g,"sqlite_db"):
        g.sqllite_db = connect_db()
    return g.sqllite_db

#close DB connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,"sqlite_db"):
        g.sqllite_db.close()

# @app.route("/")
# def hello():
#     return "Well done, buddy!"
@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    db = get_db()
    cur = db.execute('select * from projects order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to database."""
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute(
        'insert into projects (projectname, technology) values (TDD, Flask)',
        [request.form['projectname'], request.form['technology']]
    )
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

# id integer primary key autoincrement,
#   projectname text not null,
#   technology text not null

if __name__ == "__main__":
    app.run()

