from flask import Flask, request, jsonify
from database import db
from models import User, Recipe
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mycookbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_very_secret_key_for_dev') # Use environment variable in production

db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Helper for token-based authentication (simplified for prototype)
# In a real app, you'd use JWTs or similar
def authenticate_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    # For this prototype, let's assume the token is the user's ID for simplicity
    # In a real app, you'd decode a JWT or look up a token in a database
    try:
        user_id = int(token)
        user = User.query.get(user_id)
        return user
    except (ValueError, TypeError):
        return None

# User Authentication Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # For this prototype, return user ID as a simple token
    return jsonify({'message': 'Logged in successfully', 'token': user.id, 'user_id': user.id}), 200

# Recipe Management Routes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    output = []
    for recipe in recipes:
        output.append({
            'id': recipe.id,
            'title': recipe.title,
            'image': recipe.image,
            'ingredients': recipe.ingredients.split('||') if recipe.ingredients else [],
            'instructions': recipe.instructions.split('||') if recipe.instructions else []
        })
    return jsonify({'recipes': output})

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify({
        'id': recipe.id,
        'title': recipe.title,
        'image': recipe.image,
        'ingredients': recipe.ingredients.split('||') if recipe.ingredients else [],
        'instructions': recipe.instructions.split('||') if recipe.instructions else []
    })

@app.route('/recipes', methods=['POST'])
def add_recipe():
    user = authenticate_user()
    if not user:
        return jsonify({'message': 'Authentication required'}), 401

    data = request.get_json()
    title = data.get('title')
    image = data.get('image')
    ingredients = data.get('ingredients') # Expecting a list
    instructions = data.get('instructions') # Expecting a list

    if not title or not ingredients or not instructions:
        return jsonify({'message': 'Title, ingredients, and instructions are required'}), 400

    new_recipe = Recipe(
        title=title,
        image=image,
        ingredients='||'.join(ingredients), # Store as delimited string
        instructions='||'.join(instructions), # Store as delimited string
        user_id=user.id
    )
    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe added successfully', 'recipe_id': new_recipe.id}), 201

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    user = authenticate_user()
    if not user:
        return jsonify({'message': 'Authentication required'}), 401

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != user.id:
        return jsonify({'message': 'You are not authorized to update this recipe'}), 403

    data = request.get_json()
    recipe.title = data.get('title', recipe.title)
    recipe.image = data.get('image', recipe.image)
    recipe.ingredients = '||'.join(data.get('ingredients', recipe.ingredients.split('||')))
    recipe.instructions = '||'.join(data.get('instructions', recipe.instructions.split('||')))

    db.session.commit()

    return jsonify({'message': 'Recipe updated successfully'}), 200

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    user = authenticate_user()
    if not user:
        return jsonify({'message': 'Authentication required'}), 401

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != user.id:
        return jsonify({'message': 'You are not authorized to delete this recipe'}), 403

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Run on a different port than the frontend
