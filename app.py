from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Get the PostgreSQL URL from the environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Connect to the PostgreSQL database
def connect_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

# Create the table in the database (run only once)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pre_task_form (
            id SERIAL PRIMARY KEY,
            project TEXT,
            contractor TEXT,
            location TEXT,
            task TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Home route to display the form
@app.route('/')
def index():
    return render_template('form.html')

# Handle form submissions and store them in the database
@app.route('/submit', methods=['POST'])
def submit_form():
    project = request.form['project']
    contractor = request.form['contractor']
    location = request.form['location']
    task = request.form['task']
    notes = request.form['notes']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pre_task_form (project, contractor, location, task, notes) VALUES (%s, %s, %s, %s, %s)",
                   (project, contractor, location, task, notes))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# View all form submissions
@app.route('/view')
def view_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pre_task_form")
    rows = cursor.fetchall()
    conn.close()
    return render_template('view_data.html', rows=rows)

if __name__ == '__main__':
    create_table()  # Create the table when starting the app
    app.run(debug=True)
