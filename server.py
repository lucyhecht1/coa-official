from flask import Flask, render_template

app = Flask(__name__)

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
