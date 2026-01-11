#!/usr/bin/env python3
"""
Simple Recipe Web Server - Zero Dependencies
Workshop 1001: HTMX & Datastar with Python
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


# Load recipe data at startup
with open('data/recipes.json', 'r') as f:
    RECIPES = json.load(f)

RECIPES_PER_PAGE = 10


# HTML Templates using string formatting
HOME_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Recipe Browser</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .recipe-list {{ list-style: none; padding: 0; }}
        .recipe-list li {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .recipe-list a {{ text-decoration: none; color: #0066cc; font-size: 18px; }}
        .recipe-list a:hover {{ text-decoration: underline; }}
        .pagination {{ margin: 20px 0; text-align: center; }}
        .pagination a {{ margin: 0 5px; padding: 5px 10px; border: 1px solid #ddd; text-decoration: none; color: #0066cc; }}
        .pagination a:hover {{ background: #f0f0f0; }}
        .pagination .current {{ font-weight: bold; background: #0066cc; color: white; padding: 5px 10px; }}
    </style>
</head>
<body>
    <h1>Recipe Browser</h1>
    <p>Browse {total_recipes} delicious recipes</p>

    <ul class="recipe-list">
        {recipe_items}
    </ul>

    <div class="pagination">
        {pagination}
    </div>
</body>
</html>"""


RECIPE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>{name} - Recipe Browser</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .back-link {{ margin-bottom: 20px; }}
        .back-link a {{ text-decoration: none; color: #0066cc; }}
        .recipe-meta {{ color: #666; margin-bottom: 20px; }}
        .section {{ margin: 20px 0; }}
        .section h2 {{ color: #555; font-size: 20px; }}
        .ingredients {{ list-style: disc; padding-left: 20px; }}
        .method {{ list-style: decimal; padding-left: 20px; }}
        .method li {{ margin: 10px 0; }}
        .source {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="back-link">
        <a href="/">← Back to Recipe List</a>
    </div>

    <h1>{name}</h1>

    <div class="recipe-meta">
        <p><strong>Author:</strong> {author}</p>
        <p>{description}</p>
    </div>

    <div class="section">
        <h2>Ingredients</h2>
        <ul class="ingredients">
            {ingredients}
        </ul>
    </div>

    <div class="section">
        <h2>Method</h2>
        <ol class="method">
            {method}
        </ol>
    </div>

    <div class="source">
        <p><a href="{url}" target="_blank">View original recipe source →</a></p>
    </div>
</body>
</html>"""


class RecipeHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler with route dictionary"""

    def do_GET(self):
        """Handle GET requests using route dictionary"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Route dictionary - maps paths to handler methods
        routes = {
            '/': self.handle_home,
            '/recipe': self.handle_recipe,
        }

        # Check for exact match first
        if path in routes:
            routes[path](query_params)
        # Check for recipe route with ID
        elif path.startswith('/recipe/'):
            self.handle_recipe_detail(path)
        else:
            self.send_404()

    def handle_home(self, query_params):
        """Handle home page with recipe list and pagination"""
        # Get page number from query params (default to 1)
        page = int(query_params.get('page', ['1'])[0])
        page = max(1, page)  # Ensure page is at least 1

        # Calculate pagination
        total_recipes = len(RECIPES)
        total_pages = (total_recipes + RECIPES_PER_PAGE - 1) // RECIPES_PER_PAGE
        page = min(page, total_pages)  # Ensure page doesn't exceed total

        start_idx = (page - 1) * RECIPES_PER_PAGE
        end_idx = start_idx + RECIPES_PER_PAGE
        page_recipes = RECIPES[start_idx:end_idx]

        # Generate recipe list HTML
        recipe_items = []
        for idx, recipe in enumerate(page_recipes, start=start_idx):
            recipe_items.append(
                f'<li><a href="/recipe/{idx}">{recipe["Name"]}</a></li>'
            )

        # Generate pagination HTML
        pagination_links = []
        if page > 1:
            pagination_links.append(f'<a href="/?page={page-1}">← Previous</a>')

        pagination_links.append(f'<span class="current">Page {page} of {total_pages}</span>')

        if page < total_pages:
            pagination_links.append(f'<a href="/?page={page+1}">Next →</a>')

        # Render template
        html = HOME_TEMPLATE.format(
            total_recipes=total_recipes,
            recipe_items='\n        '.join(recipe_items),
            pagination=' '.join(pagination_links)
        )

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def handle_recipe_detail(self, path):
        """Handle individual recipe detail page"""
        try:
            # Extract recipe ID from path
            recipe_id = int(path.split('/')[-1])

            if recipe_id < 0 or recipe_id >= len(RECIPES):
                self.send_404()
                return

            recipe = RECIPES[recipe_id]

            # Generate ingredients HTML
            ingredients = '\n            '.join(
                f'<li>{ing}</li>' for ing in recipe.get('Ingredients', [])
            )

            # Generate method/steps HTML
            method = '\n            '.join(
                f'<li>{step}</li>' for step in recipe.get('Method', [])
            )

            # Render template
            html = RECIPE_TEMPLATE.format(
                name=recipe.get('Name', 'Unknown Recipe'),
                author=recipe.get('Author', 'Unknown'),
                description=recipe.get('Description', 'No description available.'),
                ingredients=ingredients,
                method=method,
                url=recipe.get('url', '#')
            )

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

        except (ValueError, IndexError):
            self.send_404()

    def handle_recipe(self, query_params):
        """Legacy recipe handler (redirects to detail page)"""
        recipe_id = query_params.get('id', ['0'])[0]
        self.send_response(301)
        self.send_header('Location', f'/recipe/{recipe_id}')
        self.end_headers()

    def send_404(self):
        """Send 404 Not Found response"""
        html = """<!DOCTYPE html>
<html>
<head><title>404 Not Found</title></head>
<body>
    <h1>404 - Page Not Found</h1>
    <p><a href="/">Return to Recipe List</a></p>
</body>
</html>"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        """Override to provide cleaner log output"""
        print(f"{self.address_string()} - {format % args}")


def run_server(port=8000):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, RecipeHandler)
    print(f"🍳 Recipe Server starting on http://localhost:{port}")
    print(f"📚 Loaded {len(RECIPES)} recipes")
    print(f"Press Ctrl+C to stop the server\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
