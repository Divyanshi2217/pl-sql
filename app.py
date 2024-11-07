from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor 
from datetime import datetime

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@Devu'
app.config['MYSQL_DB'] = 'event_registration_system'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event_date = request.form['event_date']
        event_name = request.form['event']
        time = request.form['time']
        location = request.form['location']
        created_date=datetime.now()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events(name,email,event_date,event_name,eventtime,event_location,created_date) VALUES(%s, %s, %s,%s,%s,%s,%s)", (name, email, event_date, event_name, time, location, created_date))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))


@app.route('/registrations')
def registrations():
    # Use DictCursor to access rows with column names
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM events")
    registrations = cur.fetchall()
    cur.close()

    return render_template('listevents.html', registrations=registrations)




if __name__ == '__main__':
    app.run(debug=True)