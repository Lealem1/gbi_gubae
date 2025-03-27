from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

@app.route('/')
def home():
    return render_template('homePage.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        phone = request.form['phone']
        department = request.form['department']
        batch = request.form['batch']
        registration_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create registrations.csv if it doesn't exist
        if not os.path.exists('registrations.csv'):
            with open('registrations.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Phone', 'Department', 'Batch', 'Registration Time'])

        # Append registration data
        with open('registrations.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, phone, department, batch, registration_time])

        flash('Registration successful!', 'success')
    except Exception as e:
        flash('Error during registration. Please try again.', 'error')
        print(f"Error: {str(e)}")

    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    try:
        registrations = []
        if os.path.exists('registrations.csv'):
            with open('registrations.csv', 'r') as file:
                reader = csv.DictReader(file)
                registrations = list(reader)
        return render_template('admin.html', registrations=registrations)
    except Exception as e:
        flash('Error loading registrations.', 'error')
        return render_template('admin.html', registrations=[])

@app.route('/download-csv')
def download_csv():
    return send_file('registrations.csv',
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name='registrations.csv')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True) 