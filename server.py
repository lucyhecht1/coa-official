import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variable
google_credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
creds_dict = json.loads(google_credentials_json)  # Convert JSON string to dictionary
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

def create_db():
    conn = sqlite3.connect('rsvp.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rsvps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            guests INTEGER NOT NULL,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_db()

# Home route
@app.route('/')
def homepage():
    return render_template('homepage.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Gallery route
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/gallery/2024')
def gallery_2024():
    return render_template('gallery_2024.html')

@app.route('/gallery/2025')
def gallery_2025():
    return render_template('gallery_2025.html')

@app.route('/gallery/2026')
def gallery_2026():
    return render_template('gallery_2026.html')

# Register route
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/submit-rsvp', methods=['POST'])
def submit_rsvp():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')

    sheet.append_row([firstName, lastName, email])  # Add RSVP to Google Sheet
    
    return jsonify({"message": "RSVP Submitted! You will receive a confirmation email shortly."})

@app.route('/export-rsvp', methods=['GET'])
def export_rsvps():
    conn = sqlite3.connect('rsvp.db')
    df = pd.read_sql_query("SELECT * FROM rsvps", conn)
    df.to_csv('rsvp.csv', index=False)
    conn.close()
    return jsonify({"message": "RSVPs exported to rsvp.csv!"})

# Contact route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Register route
@app.route('/chessed')
def chessed():
    return render_template('chessed.html')


if __name__ == '__main__':
    app.run(debug=True)
