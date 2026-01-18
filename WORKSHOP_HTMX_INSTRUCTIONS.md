# Workshop Instructions: Show Recipe Details with HTMX

## Goal

Transform the recipe browser from a traditional multi-page app into a dynamic single-page experience where:

- The recipe list stays on the left side (scrollable for hundreds of recipes)
- Recipe details appear on the right side when clicked
- No page reloads or navigation away from the list
- The main window doesn't scroll when viewing details

## Important Note About CSS

The [static/style.css](static/style.css) file is designed to work for **both** the traditional multi-page app and the HTMX split-panel version:

- **Without HTMX changes**: The CSS provides standard single-column layout styling
- **With HTMX changes**: When you add the `.container` div, the CSS automatically activates the split-panel layout

This means **you won't need to modify CSS** during the workshop - focus on the HTMX functionality!

## The Problem with the Current App
Right now, clicking a recipe navigates to `/recipe/<id>`, which:
- Loads a completely new page
- Loses your position in the recipe list
- Requires clicking "Back" to browse more recipes
- Poor UX for exploring multiple recipes

## The HTMX Solution
With HTMX, clicking a recipe will:
1. Send a request to the server for that recipe's details
2. Receive HTML for just the details section
3. Swap that HTML into a details panel on the page
4. All without JavaScript or page navigation

---

## Step 1: Add HTMX to Your Layout

First, include the HTMX library in your [layout.html](templates/layout.html).

Add this script tag in the `<head>` section, right after the stylesheet link:

```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

Your head section should now look like:

```html
<head>
    <title>{% block title %}Basic Recipe Browser{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
```

---

## Step 2: Create a Split-Panel Layout

Update [layout.html](templates/layout.html) to wrap the content in a two-column container.

Change the `<body>` section from this:

```html
<body>
    {% block content %}{% endblock %}
</body>
```

To this:

```html
<body>
    <div class="container">
        <div class="recipe-list-panel">
            {% block content %}{% endblock %}
        </div>
        <div id="recipe-details" class="recipe-details-panel empty">
            <p>Select a recipe to view details</p>
        </div>
    </div>
</body>
```

**What changed?**
- Added a `.container` wrapper with two panels
- Left panel (`.recipe-list-panel`) will hold the recipe list
- Right panel (`#recipe-details`) will hold the recipe details
- Each panel scrolls independently
- The CSS already handles all the styling (check out [static/style.css](static/style.css)!)

---

## Step 3: Update the Home Page for HTMX

Modify [home.html](templates/home.html) to use HTMX attributes instead of regular links.

Replace the recipe list section with:

```html
<ul class="recipe-list">
    {% for recipe in page_recipes %}
    <li>
        <img src="{{ recipe.get_image_url() }}" alt="{{ recipe.name }}" width="200" height="200">
        <a href="#"
           hx-get="{{ url_for('recipe_detail', recipe_id=recipe.index) }}"
           hx-target="#recipe-details"
           hx-swap="innerHTML">
            {{ recipe.name }}
        </a>
    </li>
    {% endfor %}
</ul>
```

**What's happening here?**
- `hx-get`: Tells HTMX to make a GET request to the recipe detail URL
- `hx-target="#recipe-details"`: Tells HTMX where to put the response (the right panel)
- `hx-swap="innerHTML"`: Replace the contents of the target element
- `href="#"`: Fallback for when JavaScript is disabled

---

## Step 4: Create a Recipe Details Fragment Template

Create a new template file that returns ONLY the recipe details HTML (no layout wrapper).

Create [templates/recipe_detail_fragment.html](templates/recipe_detail_fragment.html):

```html
<h1>{{ recipe.name }}</h1>

<div class="recipe-meta">
    <p><strong>Author:</strong> {{ recipe.author }}</p>
    <p>{{ recipe.description }}</p>
</div>

<div class="section">
    <h2>Ingredients</h2>
    <ul class="ingredients">
        {% for ingredient in recipe.ingredients %}
        <li>{{ ingredient }}</li>
        {% endfor %}
    </ul>
</div>

<div class="section">
    <h2>Method</h2>
    <ol class="method">
        {% for step in recipe.method %}
        <li>{{ step }}</li>
        {% endfor %}
    </ol>
</div>

<div class="source">
    <p><a href="{{ recipe.url }}" target="_blank">View original recipe source</a></p>
</div>
```

**Why a fragment?**
- HTMX will receive ONLY this HTML
- No `<html>`, `<head>`, or layout wrapper
- Just the content to inject into the details panel

---

## Step 5: Update the Server Route

Modify the `recipe_detail` function in [server.py](server.py) to detect HTMX requests and return the fragment.

Replace the existing `recipe_detail` function (around line 61) with:

```python
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
```

**How does this work?**
- HTMX automatically adds an `HX-Request` header to its requests
- If it's an HTMX request, return just the fragment
- If someone navigates directly to `/recipe/42`, they still get the full page
- Graceful degradation!

---

## Step 6: Test It Out

1. Start your server:
   ```bash
   python server.py
   ```

2. Open http://localhost:8000

3. Try clicking different recipes:
   - Details appear on the right
   - List stays in place on the left
   - No page reload
   - Both panels scroll independently

---

## Understanding What Just Happened

### Traditional Multi-Page Flow:
1. User clicks link
2. Browser navigates to new URL
3. Server renders entire page
4. Browser loads and displays new page
5. User must click back to return

### HTMX Flow:
1. User clicks link with `hx-get`
2. HTMX intercepts the click
3. HTMX sends AJAX request with `HX-Request` header
4. Server detects header, returns HTML fragment
5. HTMX swaps fragment into `#recipe-details`
6. User stays on same page, list position preserved

---

## Understanding hx-boost: When to Use It (And When Not To)

### What is hx-boost?

`hx-boost` is an HTMX attribute that converts regular navigation links into AJAX requests. It's a "progressive enhancement shortcut" that:
- Intercepts normal link clicks
- Makes AJAX requests instead
- Swaps the entire `<body>` content
- Updates the browser URL
- Adds history entries (back button works)

### The Simple Example: Pagination with hx-boost

**WHERE `hx-boost` WOULD WORK:**

If you kept the traditional multi-page structure (no split panels), you could boost the pagination links:

```html
<!-- In home.html -->
<div class="pagination" hx-boost="true">
    {% if page > 1 %}
    <a href="{{ url_for('home', page=page-1) }}">Previous</a>
    {% endif %}

    <span class="current">Page {{ page }} of {{ total_pages }}</span>

    {% if page < total_pages %}
    <a href="{{ url_for('home', page=page+1) }}">Next</a>
    {% endif %}
</div>
```

This would:
- Turn page navigation into AJAX requests
- Replace the entire body content
- Keep the URL in sync (`/?page=2`)
- No server changes needed!

### Why hx-boost DOESN'T Work for Our Recipe Details Feature

`hx-boost` is **NOT the right choice** for the split-panel recipe detail feature because:

#### 1. Wrong Target Element
- `hx-boost` always targets the entire `<body>`
- We need to target `#recipe-details` (a specific div)
- No way to customize the target with boost

```html
<!-- This with hx-boost: -->
<a href="/recipe/5" hx-boost="true">Recipe Name</a>
<!-- Would replace the ENTIRE body, losing the split layout -->

<!-- What we need: -->
<a href="#" hx-get="/recipe/5" hx-target="#recipe-details">Recipe Name</a>
<!-- Replaces ONLY the details panel -->
```

#### 2. URL Behavior
- `hx-boost` updates the browser URL to `/recipe/5`
- We want to stay at `/` (the homepage)
- We're showing details as a "preview", not navigation

#### 3. History Entries
- `hx-boost` creates browser history for each click
- Clicking 10 recipes = 10 back button clicks to return
- Our feature shouldn't pollute history

#### 4. Server Response Required
- `hx-boost` expects the server to return a full page with `<body>` tags
- Then extracts just the body content
- Our fragment approach is cleaner (no parsing needed)

### Decision Matrix: hx-boost vs hx-get/hx-post

Use this table to decide:

| Use Case | Use `hx-boost` | Use `hx-get`/`hx-post` |
|----------|----------------|------------------------|
| Navigation between pages with same layout | ✅ YES | ❌ Overkill |
| Pagination (replacing whole page) | ✅ YES | ❌ More code |
| Master-detail split view | ❌ NO | ✅ YES |
| Updating a specific section | ❌ NO | ✅ YES |
| Modal/dialog content | ❌ NO | ✅ YES |
| Infinite scroll | ❌ NO | ✅ YES |
| Form submissions that redirect | ✅ YES | ⚠️ Either works |
| Need history/back button | ✅ YES | ❌ No history |
| DON'T want history | ❌ NO | ✅ YES |

### When hx-boost Shines: The "Quick Win" Scenario

**Scenario**: You have an existing traditional multi-page app and want to make it feel faster with minimal changes.

**Before** (traditional):
```html
<nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
</nav>
```

**After** (with hx-boost):
```html
<nav hx-boost="true">
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
</nav>
```

**What you get:**
- No page reloads (AJAX instead)
- Preserves URL changes
- Back button still works
- **Zero server changes**
- Entire header/footer don't flash on navigation

### Real-World Example: When to Use Each

#### Good hx-boost Use Case: Blog Navigation
```html
<body hx-boost="true">
    <header>
        <nav>
            <a href="/blog">Blog</a>
            <a href="/blog/category/tech">Tech</a>
            <a href="/blog/category/food">Food</a>
        </nav>
    </header>

    <main>
        <!-- Blog posts here -->
    </main>
</body>
```
- Each page has same header/footer
- Navigation just changes the main content
- URL should change
- History should be preserved

#### Good hx-get Use Case: Blog Post Comments (Our Recipe Scenario)
```html
<article>
    <h1>Blog Post Title</h1>
    <p>Content...</p>
</article>

<aside id="comments-section">
    <h2>Comments</h2>
    <button hx-get="/post/123/comments"
            hx-target="#comments-list"
            hx-swap="innerHTML">
        Load Comments
    </button>
    <div id="comments-list"></div>
</aside>
```
- Specific section updates
- URL shouldn't change
- No history pollution
- Precise control over what updates

### Technical Deep Dive: What Happens Under the Hood

#### With hx-boost="true"
```
User clicks: <a href="/recipe/5" hx-boost="true">
    ↓
HTMX intercepts click
    ↓
GET /recipe/5 with HX-Request header
    ↓
Server returns: <html><head>...</head><body>...full page...</body></html>
    ↓
HTMX extracts <body> content
    ↓
Replaces current <body> innerHTML
    ↓
Updates URL to /recipe/5
    ↓
Pushes history state
```

#### With hx-get="/recipe/5" hx-target="#recipe-details"
```
User clicks: <a hx-get="/recipe/5" hx-target="#recipe-details">
    ↓
HTMX intercepts click
    ↓
GET /recipe/5 with HX-Request header
    ↓
Server returns: <h1>Recipe</h1><div>...just fragment...</div>
    ↓
HTMX finds #recipe-details
    ↓
Replaces #recipe-details innerHTML
    ↓
URL unchanged (still at /)
    ↓
No history entry
```

### Key Insight: hx-boost is for "Enhanced Navigation"

Think of it this way:
- **hx-boost**: "Make my traditional navigation faster"
  - You're still navigating between pages
  - Just with AJAX instead of full page loads
  - URL bar should reflect where you are

- **hx-get/hx-post**: "Update part of the page dynamically"
  - You're staying on the same "page"
  - Just changing a component or section
  - URL bar stays the same

### For Our Recipe App

Our feature is **definitely an "update part of the page"** scenario:
- User is browsing recipes (staying on homepage)
- Details panel is a "preview" not a "destination"
- Similar to clicking a file in VS Code's sidebar (shows preview, doesn't navigate away)
- No history needed (wouldn't make sense to hit back 50 times after viewing 50 recipes)

**Correct approach**: `hx-get` with `hx-target="#recipe-details"`

### Could You Use hx-boost Anywhere Else in This App?

**Maybe for pagination** (if you kept it):
```html
<!-- Before: traditional pagination -->
<a href="/?page=2">Next Page</a>

<!-- With hx-boost: smoother pagination -->
<div hx-boost="true">
    <a href="/?page=2">Next Page</a>
</div>
```

This would make pagination feel faster without changing the fundamental behavior.

**Not recommended for recipe links** because you'd lose the split-panel UX.

### Summary: The Golden Rule

**Use `hx-boost`** when:
- ✅ You want the link to behave like navigation (URL changes, history added)
- ✅ You want to replace the whole page content
- ✅ You want minimal code changes to existing markup
- ✅ Server already returns full HTML pages

**Use `hx-get`/`hx-post`** when:
- ✅ You want to update a specific element
- ✅ You DON'T want URL/history changes
- ✅ You want server to return just a fragment
- ✅ You need precise control (custom targets, swap strategies)

For our recipe detail panel feature, `hx-get` with `hx-target` is definitely the right choice!

---

## Next Steps / Challenges

Once you have this working, try these enhancements:

1. **Loading Indicator**: Show a spinner while loading
   ```html
   <span class="htmx-indicator">Loading...</span>
   ```

2. **Highlight Selected Recipe**: Add styling to show which recipe is currently displayed
   - Hint: Use `hx-target` and CSS classes

3. **Keyboard Navigation**: Add arrow key support to browse recipes
   - Hint: Use HTMX events and JavaScript

4. **Remove Pagination**: Load ALL recipes and let the list scroll
   - Better UX since details are in a separate panel
   - Just remove the pagination logic from the server

5. **Add Animations**: Use CSS transitions for smooth swapping
   - Try `hx-swap="innerHTML swap:0.5s"`

---

## Common Issues & Solutions

**Problem**: Details don't appear when clicking recipes
- Check browser console for errors
- Verify HTMX script loaded (check Network tab)
- Confirm `recipe_detail_fragment.html` exists

**Problem**: Entire page is appearing in the details panel
- Server isn't detecting HTMX request
- Check that you're using the `HX-Request` header check
- Make sure you created the fragment template

**Problem**: Panels aren't side-by-side
- Check that you updated `layout.html` with the new CSS
- Verify the `.container` and panel divs are present

**Problem**: Can't scroll the recipe list
- Make sure `.recipe-list-panel` has `overflow-y: auto`
- Check that `body` has `overflow: hidden`

---

## Bonus: Remove Pagination Entirely

Since details appear in a side panel, users don't lose their place in the list. Remove pagination and show all recipes:

In [server.py](server.py):
```python
@app.route('/')
def home():
    """Home page with all recipes"""
    return render_template(
        'home.html',
        page_recipes=RECIPES,  # All recipes
        total_recipes=len(RECIPES)
    )
```

In [home.html](templates/home.html), remove the entire pagination div.

Now you have a truly infinite scrolling list with instant details!

---

## Key Takeaways

1. **No JavaScript needed**: HTMX handles all the AJAX for you
2. **Server stays simple**: Just return HTML fragments
3. **Progressive enhancement**: Still works if JavaScript is disabled
4. **Better UX**: No page reloads, maintain context
5. **Hypermedia-driven**: Server controls the UI via HTML

This is the power of HTMX - dynamic web apps with minimal complexity!
