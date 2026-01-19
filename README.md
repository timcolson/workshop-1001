# Workshop 1001 - Intro to HTMX & Datastar with Python

**Subject**: Introduction to HTMX and Datastar with a Python backend
  
Want to make a dynamic web app, without a bunch of JavaScript or React?

With [HTMX](https://htmx.org/) or [Datastar](https://data-star.dev/), your server side Python can send HTML to dynamically update the view for your users. By the end of this hour long workshop, you will understand the model for building reactive, dynamic web sites using two popular hypermedia frameworks.

***Disclaimer:*** Some concepts might not be explained correctly. We are all learning. If you have corrections, submit them as bugs. Remember: Be kind.

Recipe Source - ~1600 recipes as a single JSON file, scraped from BBC:  

- [Scraped data at frosch.cosy.sbg.ac.at](https://frosch.cosy.sbg.ac.at/datasets/json/recipes/-/blob/main/recipes.json?ref_type=heads)  
- Note: After building code for the workshop using this dataset, Tim realized the original data source might be copyright by the BBC. Plan is to replace with another dataset that is in the public domain. If links and attribution are not sufficient, we'll remove said dataset immediately upon request.

Recipe Source - 13,582 recipes scraped from Epicurious; plus 200MB of small images.
  
- [Kaggle dataset 'pes12017000148' - food-ingredients-and-recipe-dataset-with-images](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images?resource=download)  

Recipe Source - public domain repository; data in markdown files with frontmatter & Hugo

 - [github.com/ronaldl29 - public-domain-recipes](https://github.com/ronaldl29/public-domain-recipes)
 - Plan to switch to this data source. Time constraint for a local Python meetup, and format difference are limiting factors. Submit a patch if you have time!

----

## Part I: Baseline HTML Recipes Web App (10 min)

Before you can add upgrades, you need a working example webapp! The workshop provides code for a crude recipe webapp.

The app consists of the following features:

- Flask webapp to browse, view, and search recipes.
- Static data in files (JSON) for simplicity.
- Template files to separate HTML views from code.
  
**To set up your environment and run the webapp**

Pre-requisites: Python 3.10+ (tested with 3.14)

1. Check out the workshop repository: <https://github.com/timcolson/workshop-1001>
2. Create a virtual environment and add dependencies. For more info on venv, see [W3Schools venv](https://www.w3schools.com/python/python_virtualenv.asp).
   1. `python -m venv venv`
   2. `source venv/bin/activate` (macOS) or `venv\Scripts\activate` (Windows)
   3. `pip install flask`
3. Run the webapp: `flask run --app app.py`
4. Open the app in your browser!

***Congratulations!*** You should have a working recipe webapp.

Browse the list of recipes. View some recipe details. Navigate back to the list. Go to the next page in the list. Run a search.

The app works, but it's not a great experience (UX) is it? Why not???

- *What are some reasons the UX is not enjoyable... (2 min)*
- *Separate page loads*
- *Paging*
- *???*

**Consider upgrading to a dynamic app… reasons why? (3 min)**  

- *List three ways you might upgrade the app to be more fluid...*
  
- *Better UX* — show the recipe details inline, without a separate page load  
- *Infinite scroll* without “pages”  
- *Dynamic Search* with server-side index and dynamic results as you type.  
  
**3 minutes of “theory”**  

In the beginning (circa 1990), the World Wide Web consisted entirely of the following model:

- Web 1.0 : User -> Request (HTTP) -> Server -> Response (HTML)

Fast forward 15 years to 2005, and AJAX ushered in asynchronous dynamic web sites. Single Page Applications (SPA) took hold. Google Mail was one of the first examples. In the SPA model, JavaScript (JS) makes requests on behalf of the user: 

- SPA : User -> Request (HTTP) -> Server -> SPA (HTML + JS) -> Request from App -> Response (**JSON**) -> repeat *ad infinitum*

Skip ahead another 15 years to 2020. JavaScript is ubiquitous . Web front ends are amazing but also complex.

Users want dynamic webapps. Developers struggle with the complexity of front ends. Sometimes, you just need dyanmic HTML.

With HTMX and Datastar, the model moves back slightly closer to the original Web 1.0: 

- HTMX: User -> Request (HTTP) -> Server -> (HTML + HTMX) -> Request from App -> Partial Response (**HTML**) -> repeat *ad infinitum*
- Datastar: User -> Request (HTTP) -> Server -> (HTML + Datastar) -> Server Sent Event (SSE) -> Signal to patch DOM **) -> repeat *ad infinitum*

Both HTMX and Datastar feature a *hypermedia first* approach. With HTMX, you use additional HTML attributes to create requests from your App to the server. With Datastar, you modify your app state with events sent from the server.

HTMX example : click invokes a get action, server sends back HTML

```html
<a href="#"
    hx-get="{{ url_for('endpoint', recipe_id=recipe.index) }}"
    hx-target="#recipe-details">Recipe 1</a>
```

Datastar example : click invokes a get action, server sends an event back with data:

```html
<button data-on:click="@get('/endpoint')">
    Open the pod bay doors, HAL.
</button>
<div id="hal"></div>
```

HTMX and Datastar focus on *hypermedia*, using HTML and HTTP to create dynamic applications. Both rely on JavaScript (JS) to do their thing, but JavaScript is somewhat hidden from you, the developer. HTMX adds new `hx-` prefixed attributes to existing HTML tags. Datastar extends HTML through the use of `data-` prefixed attributes that use the HTML `data-*` standard attributes (hence the name "data star").

We'll explore the similarities and differences later, but let's dive into some upgrades with HTMX!

## Part II: Upgrade to Dynamic App with HTMX

You will upgrade the app to dynamically show recipe details, return live search results, and infinitely scroll the recipe list.

Before you make changes, you need to see how the app is currently structured. We've kept the scope small, so it'll only take a minute.

The recipe app is built with [Flask](https://flask.palletsprojects.com/en/stable/) which is a well known web framework for Python. The main entry point is `app.py` which relies on `models.py` to provide a *Recipe* data model and repository which can fetch a single recipe or a list of recipes. The model class encapsulates pagination and search.

The main `app.py` file contains `routes` for the home page, the recipe list, recipe details, and search. Open and review the file. You might notice `Status304Filter` which is there to simplify the log output by **not** recording *not modified* entries for static assets, such as the CSS file.

In this workshop, you'll modify the `routes` and the `templates`. Each route retrieves data and renders a template. Standalone page templates (home.html, recipe.html, search.html) can include re-usable *fragments*. Whole pages extend a common `layout.html` template, which includes CSS and JavaScript.

Depending on your needs, a route can return a full HTML page wrapped in the layout, or a route can return a smaller chunk of HTML. That flexibility will be important for making dynamic upgrades to the webapp.

Enough background! let's start making this app dynamic with HTMX...

### Upgrade - Inline recipe details  (10 min)  

When a user selects a recipe, they expect to see it without delay. Viewing another recipe should not required the back button.

Displaying recipe details inline on the page, without a separate page load, would be a big improvement

How? Imagine you could send the selected recipe ID to the server, get back recipe details, and show the recipe in a second column. 

You're in luck! The CSS already defines two flex-columns, called `recipe-list-panel` & `recipe-details-panel`.  

Take the following steps to connect to the server for the details:

1. Add the HTMX library to the layout
2. Send the recipe ID to the server for details
3. Display recipe details in #recipe-details div

#### Step 1 - Add HTMX to the project

You can load HTMX in the layout template which is used for all full pages.

1. Open `templates/layout.html`
2. In the `<head>` section, add the script:

```javascript
<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js" integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz" crossorigin="anonymous"></script>
```

You're going to need a place for the recipe details to be displayed.

In the layout template, replace the contents of `<body>` with the following HTML:

```html
<div class="container">
    <div class="recipe-list-panel">
        {% block content %}{% endblock %}
    </div>
    <div id="recipe-details" class="recipe-details-panel empty">
        <p>Select a recipe to view details</p>
    </div>
</div>
```

#### Step 2 - Get recipe details from the server

1. Open `templates/recipe_list_fragment.html`
2. Find the recipe detail link: `href="{{ url_for('recipe_detail', recipe_id=recipe.index) }}`
3. Replace the href value with `#`, and add the following `hx-` attributes:

```html
href="#"
hx-get="{{ url_for('recipe_detail', recipe_id=recipe.index) }}"
hx-target="#recipe-details"
```

Refresh your browser and select a recipe!

**Wow!** You should already see **dynamic loading** of recipe details!
(The result isn't perfect, but we'll fix that in the next step.)

**How is this working!?!** The new recipe link invokes HTMX to handle the request. HTMX calls the server and puts the results into the `target` div.

The server is still sending an **entire page** wrapped in `layout.html`. So, you're getting extra HTML that you don't need. 

What you need is just the recipe details fragment.

#### Step 3 - Update route to only send details fragment**

In this step, you will add logic to the server side to return partial HTML for HTMX requests.

1. Open app.py
2. In recipe_detail() function, add the following **before** the return statement:

```html
    if request.headers.get('HX-Request'):
        return render_template('recipe_detail_fragment.html', recipe=recipe)
```
3. Stop and restart the server.

Refresh your browser and select a recipe. You should now see only **recipe details** dynamically loading.

For requests from HTMX, the **HX-Request** header is present. With that info, your server action can choose a different template. In this case, the route will return only the HTML produced by the recipe_detail_fragment.

At this point, the format is still a bit wrong. Turns out, the CSS is applying a centered style when the details panel is `EMPTY`, and that style is still being applied.

#### Fix the formatting - remove `empty` style

You can use another HTMX attribute `hx-on::after-request` to evaluate inline JavaScript to remove the `empty` class.

1. Open `templates/recipe_list_fragment.html`
2. Add another attribute to the detail link:
`hx-on::after-request="this.closest('body').querySelector('#recipe-details').classList.remove('empty')"`

Refresh the page, then select a recipe. The recipe details should be looking pretty good now! :)

HTMX provides many more attributes which you can review in the [HTMX Reference - Core Attributes](https://htmx.org/reference/#attributes).

Note: HTMX also applies a CSS class (`htmx-indicator`) while a request is ongoing. That might be useful for updates that take a few seconds. You could display a "Loading..." message during the request. 

### Upgrade - Live search results (15 min)  

Wouldn't it be cool if the search results were dynamic? You're going to make that happen now!

1. Send search text (debounce) to server
2. Get result list - titles & links.  
3. Repeat as search text changes.  

#### Step 1 - Add a dynamic search box

1. Open `templates/home.html`
2. Replace the search-box div with the following HTMX code:
```html
<div class="search-box">
    <input type="search"
           name="q"
           placeholder="Search recipes..."
           hx-get="{{ url_for('search_recipes') }}"
           hx-trigger="input changed delay:300ms, search"
           hx-target="#recipe-list">
</div>```

#### Step 2 - Update server response - fragment

Similar to before, you're going to update the server 
1. Open `app.py`
2. Replace render_template with the search results fragment 

```html
return render_template('search_results_fragment.html', recipes=results, query=query)
```
3. Create a new template file : `search_results_fragment.html`
4. Add the following template content:
```html
{% if query %}
<p class="search-info">Found {{ recipes|length }} result{% if recipes|length != 1 %}s{% endif %} for "{{ query }}"</p>
{% endif %}

{% if recipes %}
<ul class="recipe-list">
    {% for recipe in recipes %}
    <li>
        <img src="{{ recipe.get_thumbnail_image_url() }}" alt="{{ recipe.name }}" width="50" height="50" />
        <a href="#"
           hx-get="{{ url_for('recipe_detail', recipe_id=recipe.index) }}"
           hx-target="#recipe-details"
           hx-on::after-request="this.closest('body').querySelector('#recipe-details').classList.remove('empty')">
            {{ recipe.name }}
        </a>
    </li>
    {% endfor %}
</ul>
{% elif query %}
<p class="no-results">No recipes found matching "{{ query }}"</p>
{% endif %}
```

***Congratulations!!!*** You should now have dynamic search results!


### Upgrade: Infinite scroll for recipe list (15 min)

Instead of 10 at a time as “pages”, wouldn't it be better to load more recipes into the list when the user scrolls to the bottom?

**Optional Side Quest:** Before you get started with infinite scroll, you might want to try upgrading the **Next** and **Previous** links to use HTMX. Right now, choosing those buttons re-loads the full page, which clears the currently selected recipe detail. If you convert to HTMX, the page of results could target the recipe_list column. We won't go through the detailed steps, because they are similar to what you've already done. Doing is learning, right? :) 


***TODO*** -- Add a trigger that loads and appends the next page of recipes into the recipe list. Hint: You'll use the [hx-on*](https://htmx.org/attributes/hx-on/) attributes.



## Part III: Upgrade to Dynamic App - Datastar

NOTE: If the workshop authors have the time, we'll build this section. If not, well, we only promised an introduction. 

The authors of Datastar agree that hypermedia is a great way to build dynamic apps. They take a different approach to how to make dynamic updates.

The following table compares features of the two frameworks:

| Feature | HTMX | Datastar |
| ---- | ---- | ---- |
| Philosophy | Adds to existing HTML specification; minimal and unopinionated | Combines features of HTMX and Alpine.js, aiming for high-performance live updates; minimal and more opinionated |
| Response Type | Primarily expects HTML fragments in response | Can send HTML fragments, JSON, or JavaScript |
| Update Logic | Client-driven: logic scattered across HTML attributes that trigger requests | Server-driven: server decides what should change, keeping logic in one place |
| Primary Comm. Protocol | AJAX (HTTP requests) | Server-Sent Events (SSE) (server "pushes" updates) |
| Real-time Updates | Requires polling or writing custom WebSocket code | Built-in real-time updates via SSE |
| Client-side Reactivity | No built-in state management; often paired with Alpine.js for reactivity | Built-in reactive signals (similar to Alpine.js) |

TODO: Return to the base app, re-apply the upgrades using Datastar.


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