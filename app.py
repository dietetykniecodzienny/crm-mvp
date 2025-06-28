from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)
DATABASE = 'crm.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db()
    patients = db.execute('SELECT * FROM patients').fetchall()
    return render_template('index.html', patients=patients)

@app.route('/patient/<int:patient_id>')
def patient_detail(patient_id):
    db = get_db()
    patient = db.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
    visits = db.execute('SELECT * FROM visits WHERE patient_id = ? ORDER BY date DESC', (patient_id,)).fetchall()
    return render_template('patient_detail.html', patient=patient, visits=visits)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    db = get_db()
    db.execute('INSERT INTO patients (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    db.commit()
    return redirect(url_for('index'))

@app.route('/add_visit/<int:patient_id>', methods=['POST'])
def add_visit(patient_id):
    date = request.form['date']
    note = request.form['note']
    db = get_db()
    db.execute('INSERT INTO visits (patient_id, date, note) VALUES (?, ?, ?)', (patient_id, date, note))
    db.commit()
    return redirect(url_for('patient_detail', patient_id=patient_id))

if __name__ == '__main__':
    app.run(debug=True)
