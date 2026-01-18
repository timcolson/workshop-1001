#!/usr/bin/env python3
"""
Recipe Web Server - Flask + Jinja2
Workshop 1001: HTMX & Datastar with Python
"""

import json
from flask import Flask, render_template, abort, request
import logging

app = Flask(__name__)

RECIPES_PER_PAGE = 10

class Recipe:
    """Recipe data model"""

    def __init__(self, data, index):
        self.index = index
        self.name = data.get('Name', 'Unknown Recipe')
        self.url = data.get('url', '#')
        self.description = data.get('Description', 'No description available.')
        self.author = data.get('Author', 'Unknown')
        self.ingredients = data.get('Ingredients', [])
        self.method = data.get('Method', [])

    def get_image_url(self):
        """Generate placeholder image URL"""
        return f"https://static.photos/food/200x200/{self.index}"


def get_page_data(page):
    """Get recipe list data for a given page"""
    page = max(1, page)
    total_recipes = len(RECIPES)
    total_pages = (total_recipes + RECIPES_PER_PAGE - 1) // RECIPES_PER_PAGE
    page = min(page, total_pages)

    start_idx = (page - 1) * RECIPES_PER_PAGE
    end_idx = start_idx + RECIPES_PER_PAGE
    page_recipes = RECIPES[start_idx:end_idx]

    return {
        'page_recipes': page_recipes,
        'page': page,
        'total_pages': total_pages,
        'total_recipes': total_recipes
    }


@app.route('/')
def home():
    """Home page with recipe list and pagination"""
    page = int(request.args.get('page', 1))
    return render_template('home.html', **get_page_data(page))


@app.route('/recipes')
def list_recipes():
    """Recipe list fragment for HTMX pagination"""
    page = int(request.args.get('page', 1))
    return render_template('recipe_list_fragment.html', **get_page_data(page))


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Recipe detail page"""
    if recipe_id < 0 or recipe_id >= len(RECIPES):
        abort(404)

    recipe = RECIPES[recipe_id]

    # Check if this is an HTMX request
    if request.headers.get('HX-Request'):
        # Return just the fragment for HTMX
        return render_template('recipe_detail_fragment.html', recipe=recipe)
    else:
        # Return full page for direct navigation
        return render_template('recipe.html', recipe=recipe)


@app.route('/search')
def search_recipes():
    """Search recipes by query text"""
    query = request.args.get('q', '').strip().lower()

    if not query:
        # Return empty state if no query
        return render_template('search_results_fragment.html', recipes=[], query='')

    # Filter recipes that contain the query in name or description
    matching_recipes = []
    for recipe in RECIPES:
        name_match = query in recipe.name.lower()
        desc_match = recipe.description and query in recipe.description.lower()
        if name_match or desc_match:
            matching_recipes.append(recipe)
            if len(matching_recipes) >= 20:
                break

    return render_template('search_results_fragment.html', recipes=matching_recipes, query=query)


@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404


class Status304Filter(logging.Filter):
    """Filter out 304 not modified responses from logs"""
    def filter(self, record):
        # Check if '304' appears in the log message
        # Werkzeug formats as: "GET /static/style.css HTTP/1.1" 304 -
        return '304' not in record.getMessage()

# Apply the filter
logger = logging.getLogger('werkzeug')
logger.addFilter(Status304Filter())


if __name__ == '__main__':
    print("🍳 Recipe Server starting on http://localhost:8000")
    
    # Load recipe data at startup
    with open('data/recipes.json', 'r') as f:
        recipe_data = json.load(f)
        RECIPES = [Recipe(data, idx) for idx, data in enumerate(recipe_data)]
        print(f"📚 Loaded {len(RECIPES)} recipes")

    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, port=8000)
