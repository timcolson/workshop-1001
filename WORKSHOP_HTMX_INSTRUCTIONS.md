# HTMX Reference: hx-boost vs hx-get/hx-post

This document covers when to use `hx-boost` versus `hx-get`/`hx-post` - a common decision point when building HTMX applications.

> **Note**: Step-by-step workshop instructions are in [workshop-docs/](workshop-docs/).

## What is hx-boost?

`hx-boost` is an HTMX attribute that converts regular navigation links into AJAX requests. It's a "progressive enhancement shortcut" that:

- Intercepts normal link clicks
- Makes AJAX requests instead of full page loads
- Swaps the entire `<body>` content
- Updates the browser URL
- Adds history entries (back button works)

## Decision Matrix

| Use Case | Use `hx-boost` | Use `hx-get`/`hx-post` |
|----------|----------------|------------------------|
| Navigation between pages with same layout | YES | Overkill |
| Pagination (replacing whole page) | YES | More code |
| Master-detail split view | NO | YES |
| Updating a specific section | NO | YES |
| Modal/dialog content | NO | YES |
| Infinite scroll | NO | YES |
| Form submissions that redirect | YES | Either works |
| Need history/back button | YES | No history |
| DON'T want history | NO | YES |

## Why hx-boost Doesn't Work for Split-Panel UX

For the recipe detail feature (list on left, details on right), `hx-boost` is NOT the right choice:

### 1. Wrong Target Element

`hx-boost` always targets the entire `<body>`. We need to target `#recipe-details`:

```html
<!-- hx-boost would replace ENTIRE body, losing the split layout -->
<a href="/recipe/5" hx-boost="true">Recipe Name</a>

<!-- What we need - replaces ONLY the details panel -->
<a href="#" hx-get="/recipe/5" hx-target="#recipe-details">Recipe Name</a>
```

### 2. URL Behavior

- `hx-boost` updates the browser URL to `/recipe/5`
- We want to stay at `/` (the homepage)
- Details are a "preview", not navigation

### 3. History Entries

- `hx-boost` creates browser history for each click
- Clicking 10 recipes = 10 back button clicks to return
- Our feature shouldn't pollute history

## What Happens Under the Hood

### With hx-boost="true"

```text
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

### With hx-get and hx-target

```text
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

## When hx-boost Shines

**Scenario**: Existing multi-page app, want to make it feel faster with minimal changes.

```html
<!-- Before (traditional) -->
<nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
</nav>

<!-- After (with hx-boost) -->
<nav hx-boost="true">
    <a href="/">Home</a>
    <a href="/about">About</a>
</nav>
```

**What you get:**

- No page reloads (AJAX instead)
- Preserves URL changes
- Back button still works
- **Zero server changes**
- Header/footer don't flash on navigation

## The Golden Rule

**Use `hx-boost`** when:

- You want the link to behave like navigation (URL changes, history added)
- You want to replace the whole page content
- You want minimal code changes to existing markup
- Server already returns full HTML pages

**Use `hx-get`/`hx-post`** when:

- You want to update a specific element
- You DON'T want URL/history changes
- You want server to return just a fragment
- You need precise control (custom targets, swap strategies)
