import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template
from flask_compress import Compress

app = Flask(__name__)
Compress(app)  # Enable compression

# Load environment variables from .env file
load_dotenv()

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
google_credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

if not google_credentials_json:
    raise ValueError("❌ GOOGLE_CREDENTIALS_JSON environment variable not set!")

try:
    creds_dict = json.loads(google_credentials_json)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")  # 🔥 FIX HERE

    print("✅ Google Credentials Loaded Successfully")
    print(f"Private Key Exists: {'private_key' in creds_dict}")
    print(f"First 50 characters of Private Key: {creds_dict.get('private_key', '')[:50]}")

except json.JSONDecodeError:
    raise ValueError("❌ Failed to parse GOOGLE_CREDENTIALS_JSON. Check formatting.")

# Authenticate with Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("Yavneh-Arts-RSVP").sheet1

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

# Gallery routes
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

    if not firstName or not lastName or not email:
        return jsonify({"error": "All fields are required!"}), 400

    sheet.append_row([firstName, lastName, email])  # Add RSVP to Google Sheet
    
    return jsonify({"message": "Thank you! Your response has been submitted!"})

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

# Chessed route
@app.route('/chessed')
def chessed():
    return render_template('chessed.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render requires this
    app.run(debug=True)
