# Workshop 1001 - Intro to HTMX & Datastar with Python

**Subject**: Introduction to HTMX and Datastar with a Python backend
  
Want to make a dynamic web app, without a bunch of JavaScript or React?

With [HTMX](https://htmx.org/) or [Datastar](https://data-star.dev/), your server side Python can send HTML to dynamically update the view for your users. By the end of this hour long workshop, you will understand the model for building reactive, dynamic web sites using two popular hypermedia frameworks.

Recipe Source - ~1600 recipes as a single JSON file, scraped from BBC:  

- [Scraped data at frosch.cosy.sbg.ac.at](https://frosch.cosy.sbg.ac.at/datasets/json/recipes/-/blob/main/recipes.json?ref_type=heads)  

Recipe Source - 13,582 recipes scraped from Epicurious; plus 200MB of small images.
  
- [Kaggle dataset 'pes12017000148' - food-ingredients-and-recipe-dataset-with-images](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images?resource=download)  

Recipe Source - public domain repository; data in markdown files with frontmatter & Hugo
 - [github.com/ronaldl29 - public-domain-recipes](https://github.com/ronaldl29/public-domain-recipes)

----

## Part I: Start with an HTML Recipes Web App (10 min)

Before you can add upgrades, you need a working example webapp! The workshop provides  code for a crude recipe webapp.

The app consists of the following features:

1. Web server using Flask and Jinja2 to browse, view, and search recipes.  
2. Server will load recipe data from files (JSON, CSV, markdown) for simplicity, not scalability! In production, obviously you would add the complexity of a database.
3. Home page that shows a list of 10 recipe titles at a time with pagination.  
4. Template files to separate the HTML views from your code.
5. Links from the browse list to a recipe details page.

**To set up your environment and run the webapp**

Pre-requisites: Python 3.10+ (tested with 3.14)

1. Check out this repository.
2. Create a virtual environment and add dependencies. For details, see [W3Schools venv](https://www.w3schools.com/python/python_virtualenv.asp).
   1. `python -m venv venv`
   2. `source venv/bin/activate` (macOS) or `venv\Scripts\activate` (Windows)
   3. `pip install flask`
3. Run the webapp: `python server.py`
4. Open the app in your browser!

Congratulations! You should have a running recipe webapp.

Ugly, right? Not a great UX. Why???

- *Ask for reasons….(2 min)*
- *Page loads*
- *Paging*
- *???* 

**Consider upgrading to a dynamic app… reasons why? (3 min)**  

- *Ask for thoughts on upgrades…*
  
- *Better UX* — show the recipe details inline, without a separate page load  
- *Infinite scroll* without “pages”  
- *Dynamic Search* with server-side index and dynamic results as you type.  
  
**3 minutes of “theory”**  

- Show the model for the web.  
- Show the model for SPA (Single Page Application)  
- Show the model for HTMX  
- Show the model for Datastar  
  
Explain that HTMX and Datastar do roughly the same thing, but how they do it is different.  
  
## Part II: Upgrade to Dynamic App - HTMX

Next, you will add updgrade three features in the app, to show recipe details inline, scroll the browse list without "pages", and produce a list of live search results.

### Upgrade 1 - Inline recipe details  (10 min)  

Showing the recipe details inline on the page would be a big improvement. When a user selects a recipe, they expect to see it without delay. Viewing another recipe should not involve the back button.

What you want is to send the selected recipe ID to the server, get back the selected recipe details, and show them in a second column. The CSS already has a second column, so you need to connect to the server for the details HTML:

1. Send the ID to the server
2. Get back the recipe details
3. Display the recipe details in the #recipe-details div

**To send the ID to the server**

1. Open `templates/home.html`
2. Find the recipe detail link: `href="{{ url_for('recipe_detail', recipe_id=recipe.index) }}`
3. Replace the href value with `#`, and add the following `hx-` attributes:
```html
href="#"
hx-get="{{ url_for('recipe_detail', recipe_id=recipe.index) }}"
hx-target="#recipe-details"
```

Refresh your browser and select a recipe!

Wow! With only those three changes, you should see dynamic loading of recipe details! The result isn't perfect yet, but we'll get to fixing in a minute.

**What is happening!?!**
When you select the link now, HTMX handles the request. HTMX calls the server and puts the results into the `target` div. The problem is the server is still sending an entire page, wrapped in `layout.html` which includes HTML that you don't need. 

All you need now is the recipe_details fragment.

**To update the server to send details fragment**

1. Open server.py
2. Replace `return render_template('recipe.html', recipe=recipe)` with the following:

```# Check if this is an HTMX request
    if request.headers.get('HX-Request'):
        # Return just the fragment for HTMX
        return render_template('recipe_detail_fragment.html', recipe=recipe)
    else:
        # Return full page for direct navigation
        return render_template('recipe.html', recipe=recipe)
```
3. Stop and restart the server.

Refresh your browser and select a recipe. 

### Upgrade 2 - Infinite scroll for recipe list (15 min)

Instead of 10 at a time as “pages”, load more when a user scrolls.

### Upgrade 3 - Live search results (15 min)  

1. Send search text (debounce) to server
2. Get result list - titles & links.  
3. Repeat as search text changes.  

**Part III: Upgrade to Dynamic App - Datastar**  

Explain that HTMX and Datastar do roughly the same thing, but how they do it is different. Return to the base app, re-apply the three upgrades.

## Summary

- You added dynamic elements…without the complexity of React components.  
- Comparison between HTMX and Datastar  
- What would you like to explore further?  
  
——  

## Ideas / Optional side quests

- Add a “star” to favorite a recipe, have that show up in a favorites list. (Complexity here because need to save a users preferences. No DB currently.
- Some feature that uses SSE to push updates to the client… ???  
  - Maybe… multiple users on the same server
    - Setting a Favorite updates their friends?
      Whenever Alvin favorites a recipe, Becky would see that update in real-time?  
    - Editing the category on a recipe that is "uncategorized", flags the recipe as "Being edited by NAME", and upon save, moves the recipe into the given category. (Main, Desert, Beverage)


## Troubleshooting

- `Access to 127.0.0.1 was denied` - `chrome://net-internals/#sockets` Flush socket pools 