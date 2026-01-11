# Workshop 1001 - Intro to HTMX & Datastar with Python

Subject: Introduction to HTMX and Datastar with a Python backend
  
Want to make a dynamic web app, without a bunch of JavaScript or React?

With [HTMX](https://htmx.org/) or [Datastar](https://data-star.dev/), your server side Python can send HTML to dynamically update the view for your users. By the end of this hour long workshop, you will understand the model for building reactive, dynamic web sites using two popular hypermedia frameworks.

Recipe Source - ~1600 JSON from BBC:  

- [https://frosch.cosy.sbg.ac.at/datasets/json/recipes/-/blob/main/recipes.json?ref_type=heads](https://frosch.cosy.sbg.ac.at/datasets/json/recipes/-/blob/main/recipes.json?ref_type=heads)  

Recipe Source - 13,582 recipes scraped from Epicurious; plus 200MB of small images.
  
- [https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images?resource=download](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images?resource=download)  

**Build an HTML Recipes Web App (15 min)**  

1. Simple web server — zero dependencies, but use a Dict to look up routes (no if/else trees)  
2. Load recipe data from JSON or CSV file. (For simplicity, not scalability)  
3. Home page of the Recipe Site lists 10 recipes per page (just recipe titles).  
4. Create a separate recipe_details page (using templates).  
5. Link from the browse list to the details page.  
  
Done! Ugly, right? Not a great UX. Why?

- Ask for reasons….(2 min)
  
**Consider upgrading to a dynamic app… reasons why? (3 min)**  

- Ask for thoughts on upgrades…
  
- *Better UX* — show the recipe details inline, without a separate page load  
- *Infinite scroll* without “pages”  
- *Dynamic Search* with server-side index and dynamic results as you type.  
  
**3 minutes of “theory”**  

- Show the model for the web.  
- Show the model for SPA (Single Page Application)  
- Show the model for HTMX  
- Show the model for Datastar  
  
Explain that HTMX and Datastar do roughly the same thing, but how they do it is different.  
  
**Upgrade to Dynamic App**  
Show recipe details inline (10 min)  

1. Show how with HTMX
2. Show how with Datastar
  
Infinite scroll (15 min)  
Instead of 10 at a time as “pages”, load more when a user scrolls.  

1. Show how with HTMX  
2. Show how with Datastar  
  
Live search results (15 min)  

1. Send search text (debounce) to server
2. Get result list - titles.  
3. Repeat as search text changes.  
  
**Summary**  

- You added dynamic elements…without the complexity of React components.  
- Comparison between HTMX and Datastar  
- What would you like to explore further?  
  
——  
**Ideas / Optional side quests**  

- Add a “star” to favorite a recipe, have that show up in a favorites list. (Complexity here because need to save a users preferences. No DB currently.
- Some feature that uses SSE to push updates to the client… ???  
  - Maybe… multiple users on the same server
    - Setting a Favorite updates their friends?
      Whenever Alvin favorites a recipe, Becky would see that update in real-time?  
    - Editing the category on a recipe that is "uncategorized", flags the recipe as "Being edited by NAME", and upon save, moves the recipe into the given category. (Main, Desert, Beverage)  
-
