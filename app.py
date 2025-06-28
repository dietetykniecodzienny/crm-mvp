from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key'
DATABASE = 'crm.db'
USERNAME = 'admin'
PASSWORD = 'haslo123'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    patients = db.execute('SELECT * FROM patients').fetchall()
    return render_template('index.html', patients=patients)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Nieprawidłowy login lub hasło')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/patient/<int:patient_id>')
def patient_detail(patient_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    patient = db.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
    visits = db.execute('SELECT * FROM visits WHERE patient_id = ? ORDER BY date DESC', (patient_id,)).fetchall()
    return render_template('patient_detail.html', patient=patient, visits=visits)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    db = get_db()
    db.execute('INSERT INTO patients (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    db.commit()
    return redirect(url_for('index'))

@app.route('/add_visit/<int:patient_id>', methods=['POST'])
def add_visit(patient_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    date = request.form['date']
    note = request.form['note']
    db = get_db()
    db.execute('INSERT INTO visits (patient_id, date, note) VALUES (?, ?, ?)', (patient_id, date, note))
    db.commit()
    return redirect(url_for('patient_detail', patient_id=patient_id))

if __name__ == '__main__':
    app.run(debug=True)
