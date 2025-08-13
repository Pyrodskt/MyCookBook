from flask import Flask, render_template, request, redirect, url_for, session
import requests

BACKEND_API_URL = "http://127.0.0.1:5001"

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here' # Replace with a strong, random key in production

@app.context_processor
def inject_user_status():
    return dict(logged_in=session.get('logged_in'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            response = requests.post(f"{BACKEND_API_URL}/login", json={'username': username, 'password': password})
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            
            data = response.json()
            session['logged_in'] = True
            session['user_id'] = data.get('user_id') # Store user_id from backend
            session['token'] = data.get('token') # Store token from backend
            return redirect(url_for('index'))
        except requests.exceptions.RequestException as e:
            error_message = "Login failed. Please try again."
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('message', error_message)
                except ValueError: # Not a JSON response
                    error_message = f"Server error: {e.response.status_code}"
            else:
                error_message = f"Network error: {e}"
            return render_template('login.html', error=error_message)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('token', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    recipes = []
    try:
        response = requests.get(f"{BACKEND_API_URL}/recipes")
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        recipes = response.json().get('recipes', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recipes: {e}")
        # Optionally, add a flash message to display error on frontend

    return render_template('index.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
