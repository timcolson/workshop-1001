#!/usr/bin/env python3
"""
Workshop 1001: HTMX & Datastar with Python
Recipe Web Server - Flask + Jinja2
"""

from flask import Flask, redirect, render_template, abort, request, Response
import logging
from models import RecipeRepository
from datastar_py import ServerSentEventGenerator as SSE

app = Flask(__name__, template_folder='templates-datastar')

RECIPES_PER_PAGE = 10
SSE_MIMETYPE = 'text/event-stream'
recipes = RecipeRepository('data/recipes.json')


@app.route('/')
def home():
    """Home page with recipe list and pagination"""
    return redirect('/recipes')

@app.route('/recipes')
def list_recipes():
    """Recipe list - full page, fragment, or SSE"""
    page = int(request.args.get('page', 1))
    page_data = recipes.get_page(page, RECIPES_PER_PAGE)

    # Datastar SSE request (infinite scroll)
    if 'datastar' in request.args:
        html = render_template('_recipe_list_items.html', **page_data)
        def generate():
            yield SSE.patch_elements(html, selector='#load-more-trigger', mode='outer')
        return Response(generate(), mimetype=SSE_MIMETYPE)

    # Regular full page request
    return render_template('home.html', **page_data)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Recipe detail page - returns full page or SSE fragment"""
    recipe = recipes.get_by_id(recipe_id)
    if not recipe:
        abort(404)

    # Check if this is a Datastar request (has datastar query param)
    if 'datastar' in request.args:
        html = render_template('_recipe_detail_fragment.html', recipe=recipe)
        def generate():
            yield SSE.patch_elements(html, selector='#recipe-details', mode='inner')
        return Response(generate(), mimetype=SSE_MIMETYPE)

    # Regular full page response
    return render_template('recipe.html', recipe=recipe)



@app.route('/search')
def search_recipes():
    """Search recipes by query text"""
    query = request.args.get('q', '').strip()

    # If query is empty, return the full recipe list
    if not query:
        page_data = recipes.get_page(1, RECIPES_PER_PAGE)
        html = render_template('_recipe_list_items.html', **page_data)
    else:
        results = recipes.search(query)
        html = render_template('_search_results_fragment.html',
            recipe_list=results, query=query)

    # Check if this is a Datastar request (has datastar query param)
    if 'datastar' in request.args:
        def generate():
            yield SSE.patch_elements(html, selector='#recipe-list', mode='inner')
        return Response(generate(), mimetype=SSE_MIMETYPE)

    # Regular HTML response
    return html

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
   