from app import app, db
from models import User

users_to_create = [
    {"username": "user", "password": "password"},
    {"username": "admin", "password": "adminpass"},
    {"username": "test", "password": "testpass"}
]

with app.app_context():
    print("Creating base users...")
    for user_data in users_to_create:
        username = user_data["username"]
        password = user_data["password"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists. Skipping.")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print(f"User '{username}' created with ID: {new_user.id}")
    print("Base user creation complete.")
