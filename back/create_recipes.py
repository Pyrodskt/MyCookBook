from app import app, db
from models import User, Recipe

# Ensure you have at least one user created, e.g., by running create_users.py first

recipes_to_create = [
    {
        'title': 'Spaghetti Carbonara',
        'image': 'https://images.unsplash.com/photo-1588013277068-f99924115e87?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'ingredients': [
            '200g spaghetti',
            '100g pancetta or guanciale',
            '2 large eggs',
            '50g Pecorino Romano cheese, grated',
            'Black pepper to taste'
        ],
        'instructions': [
            'Cook spaghetti according to package directions.',
            'While spaghetti cooks, cut pancetta into small pieces and cook in a skillet over medium heat until crispy. Remove pancetta and set aside, leaving rendered fat in the skillet.',
            'In a bowl, whisk eggs, Pecorino Romano, and a generous amount of black pepper.',
            'Drain spaghetti, reserving about 1/2 cup of pasta water. Add hot spaghetti to the skillet with the pancetta fat. Toss to coat.',
            'Quickly pour egg mixture over spaghetti, tossing constantly to coat. Add a splash of reserved pasta water to create a creamy sauce. Add cooked pancetta and toss again.',
            'Serve immediately, garnished with extra Pecorino Romano and black pepper.'
        ]
    },
    {
        'title': 'Chicken Curry',
        'image': 'https://images.unsplash.com/photo-1626804475176-f4b6730929d8?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'ingredients': [
            '500g chicken breast, diced',
            '1 onion, chopped',
            '2 cloves garlic, minced',
            '1 tbsp ginger, grated',
            '2 tbsp curry powder',
            '400ml coconut milk',
            '1 red bell pepper, sliced',
            'Salt and pepper to taste'
        ],
        'instructions': [
            'Heat oil in a large pan over medium heat. Add chicken and cook until browned. Remove chicken and set aside.',
            'Add onion to the pan and cook until softened. Add garlic and ginger and cook for 1 minute until fragrant.',
            'Stir in curry powder and cook for another minute.',
            'Return chicken to the pan. Pour in coconut milk and add red bell pepper. Bring to a simmer.',
            'Reduce heat, cover, and cook for 15-20 minutes, or until chicken is cooked through and sauce has thickened.',
            'Season with salt and pepper. Serve with rice.'
        ]
    },
    {
        'title': 'Vegetable Stir-fry',
        'image': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'ingredients': [
            '1 tbsp sesame oil',
            '1 head broccoli, chopped',
            '2 carrots, sliced',
            '1 bell pepper, sliced',
            '1 cup snap peas',
            '2 tbsp soy sauce',
            '1 tbsp honey',
            '1 tsp ginger, grated'
        ],
        'instructions': [
            'Heat sesame oil in a large wok or skillet over high heat.',
            'Add broccoli and carrots and stir-fry for 3-4 minutes until slightly tender-crisp.',
            'Add bell pepper and snap peas and stir-fry for another 2-3 minutes.',
            'In a small bowl, whisk together soy sauce, honey, and grated ginger.',
            'Pour sauce over vegetables and toss to coat. Cook for 1-2 minutes until sauce has thickened slightly.',
            'Serve immediately with rice or noodles.'
        ]
    }
]

with app.app_context():
    print("Adding recipes to the database...")
    # Get an existing user to associate recipes with
    # Assuming 'user' exists from create_users.py
    default_user = User.query.filter_by(username='user').first()

    if not default_user:
        print("Error: Default user 'user' not found. Please run create_users.py first.")
    else:
        for recipe_data in recipes_to_create:
            title = recipe_data['title']
            existing_recipe = Recipe.query.filter_by(title=title).first()
            if existing_recipe:
                print(f"Recipe '{title}' already exists. Skipping.")
            else:
                new_recipe = Recipe(
                    title=title,
                    image=recipe_data['image'],
                    ingredients='||'.join(recipe_data['ingredients']),
                    instructions='||'.join(recipe_data['instructions']),
                    user_id=default_user.id
                )
                db.session.add(new_recipe)
                db.session.commit()
                print(f"Added recipe: {title}")
    print("Recipe creation complete.")
