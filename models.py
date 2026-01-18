"""Recipe data model"""


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
