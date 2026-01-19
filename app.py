#!/usr/bin/env python3
"""
Workshop 1001: HTMX & Datastar with Python
Recipe Web Server - Flask + Jinja2
"""

from flask import Flask, redirect, render_template, abort, request
import logging
from models import RecipeRepository

app = Flask(__name__)

RECIPES_PER_PAGE = 10
recipes = RecipeRepository('data/recipes.json')


@app.route('/')
def home():
    """Home page with recipe list and pagination"""
    return redirect('/recipes')

@app.route('/recipes')
def list_recipes():
    """Recipe list endpoint for pagination"""
    page = int(request.args.get('page', 1))
    page_data = recipes.get_page(page, RECIPES_PER_PAGE)
    
    return render_template('home.html', **page_data)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Recipe detail page"""
    recipe = recipes.get_by_id(recipe_id)
    if not recipe:
        abort(404)
    return render_template('recipe.html', recipe=recipe)



@app.route('/search')
def search_recipes():
    """Search recipes by query text"""
    query = request.args.get('q', '')
    results = recipes.search(query)

    return render_template('search.html',
        recipe_list=results, query=query,
        page=1, total_pages=1, total_recipes=len(results))


class Status304Filter(logging.Filter):
    """Filter out 304 (not modified) to simplify log"""
    def filter(self, record):
        # Werkzeug format: "GET /static/style.css HTTP/1.1" 304 -
        return '304' not in record.getMessage()


# Apply the logging filter 
logging.getLogger('werkzeug').addFilter(Status304Filter())


if __name__ == '__main__':
    print("🍳 Recipe Server starting...")
    app.run(debug=True) 
   