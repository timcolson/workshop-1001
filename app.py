#!/usr/bin/env python3
"""
Recipe Web Server - Flask + Jinja2
Workshop 1001: HTMX & Datastar with Python
"""

import json
from flask import Flask, render_template, abort, request
import logging

from models import Recipe

app = Flask(__name__)


RECIPES_PER_PAGE = 10

# Load recipe data at startup
with open('data/recipes.json', 'r') as f:
    recipe_data = json.load(f)
    RECIPES = [Recipe(data, idx) for idx, data in enumerate(recipe_data)]


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
        'recipe_list': page_recipes,
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
    """Recipe list endpoint for pagination"""
    page = int(request.args.get('page', 1))
    return render_template('home.html', **get_page_data(page))

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Recipe detail page"""
    if recipe_id < 0 or recipe_id >= len(RECIPES):
        abort(404)

    recipe = RECIPES[recipe_id]

    return render_template('recipe.html', recipe=recipe)

@app.route('/search')
def search_recipes():
    """Search recipes by query text"""
    query = request.args.get('q', '').strip().lower()

    if not query:
        # Return empty state if no query
        return render_template('search.html', recipes=[], query='')

    # Filter recipes that contain the query in name or description
    matching_recipes = []
    for recipe in RECIPES:
        name_match = query in recipe.name.lower()
        desc_match = recipe.description and query in recipe.description.lower()
        if name_match or desc_match:
            matching_recipes.append(recipe)

    return render_template('search.html', recipe_list=matching_recipes, query=query, page=1, total_pages=1, total_recipes=len(matching_recipes))


class Status304Filter(logging.Filter):
    """Filter out 304 (not modified) to simplify log"""
    def filter(self, record):
        # Werkzeug format: "GET /static/style.css HTTP/1.1" 304 -
        return '304' not in record.getMessage()


# Apply the logging filter at module level
logging.getLogger('werkzeug').addFilter(Status304Filter())


if __name__ == '__main__':
    print("🍳 Recipe Server starting...")
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True) 