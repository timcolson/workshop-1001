# Workshop 1001 - Intro to HTMX & Datastar with Python

Want to make a dynamic web app without JavaScript or React complexity?

With [HTMX](https://htmx.org/) or [Datastar](https://data-star.dev/), your server-side Python sends HTML to dynamically update the view. This workshop teaches the model for building reactive websites using hypermedia frameworks.

## Workshop Documentation

Full instructions are in the **[workshop-docs/](workshop-docs/)** folder, built with Astro Starlight.

```bash
cd workshop-docs
npm install
npm run dev
# Open http://localhost:4321
```

## Quick Start (Recipe App)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install flask
flask run --app app.py
# Open http://127.0.0.1:5000
```

## What You'll Learn

| Part | Topic |
|------|-------|
| **I** | Baseline HTML Recipes Web App |
| **II** | Upgrade to Dynamic App with HTMX |
| **III** | Datastar Alternative (optional) |

## Recipe Data

The workshop uses ~1,600 recipes from BBC as JSON. See [workshop-docs](workshop-docs/) for attribution and alternative public domain sources.

## License

Workshop content and code are provided for educational purposes.