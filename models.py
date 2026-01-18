"""Recipe data model"""
import json


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

    def get_thumbnail_image_url(self):
        """Generate placeholder image URL"""
        return f"https://static.photos/food/200x200/{self.index}"


class RecipeRepository:
    """Repository for recipe data access"""

    def __init__(self, data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
            self.recipes = [Recipe(d, i) for i, d in enumerate(data)]

    def get_by_id(self, recipe_id):
        """Get recipe by ID, or None"""
        if 0 <= recipe_id < len(self.recipes):
            return self.recipes[recipe_id]
        return None

    def get_page(self, page, per_page=10):
        """Get paginated recipe data"""
        page = max(1, page)
        total = len(self.recipes)
        total_pages = (total + per_page - 1) // per_page
        page = min(page, total_pages)
        start = (page - 1) * per_page

        return {
            'recipe_list': self.recipes[start:start + per_page],
            'page': page,
            'total_pages': total_pages,
            'total_recipes': total
        }

    def search(self, query, limit=42):
        """Search by name or description"""
        q = query.strip().lower()
        if not q:
            return []
        results = []
        for r in self.recipes:
            if q in r.name.lower() or (r.description and q in r.description.lower()):
                results.append(r)
                if len(results) >= limit:
                    break
        return results
