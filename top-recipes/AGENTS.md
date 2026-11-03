# Top Recipes

Live URL: https://nikolaspanayotov-jpg.github.io/VibeProjects/top-recipes/

This project is a recipe notebook and Monday–Sunday planner. Follow the repository's root AGENTS.md and frontend-design skill. Keep all changes inside `top-recipes/`.

## Run and publish

There is no application build step. Serve this folder, or the repository root, with any static server. `python3 -m http.server 8000` is enough. GitHub Pages publishes this folder from `main` at the URL above. Keep the folder name and all asset URLs relative.

Opening `index.html` from disk loads the classic scripts normally. Local browser security blocks fetching Markdown automatically from disk, so use Open recipes.md to select the collection. On HTTP and GitHub Pages, the page fetches recipes.md automatically.

## Architecture

- `recipes.md` is the sole recipe content source. Edits appear after publishing and refreshing; no generated recipe JSON exists.
- `vendor/` contains local Marked 15.0.12 and js-yaml 4.1.0 browser distributions with their licenses.
- `src/content.js` validates Marked tokens and YAML metadata. Never render authored content as HTML.
- Classic scripts load with `defer`, in the order in index.html. They expose helpers through `globalThis.TopRecipes`; each file has its own function scope.
- `src/app.js` coordinates the library, pickers and planner. `planner.js` contains pure calendar and meal-edit functions; `storage.js` validates persisted data; `recipes.js` renders ingredients and recipes; `capture.js` manages screenshot mode and print.
- `src/shopping.js` totals one full batch per planned meal, merges equivalent ingredient names with matching units, converts kg/g and l/ml, and exposes weekly tick selections and quantity controls. Preparation notes remain available through Recipe amounts. Do not combine different foods or convert volume to weight without ingredient-specific data. Pantry quantities (“to taste”, pinches, unspecified amounts) default to one pack; whole items round up.
- `styles.css` contains the cream/olive/terracotta visual system, mobile planner and portrait capture layout. Fonts and illustrations are local or system-provided.

Do not rename shipped storage keys `top-recipes:planner:v1` or `top-recipes:ingredients:v1`, recipe IDs or ingredient IDs. Preserve malformed saved data until the user explicitly resets it. Calculate dates in local time. Moving a grid meal into an occupied slot swaps the meals; adding from the library replaces the target. Undo remains available beside Clear week even if its toast is dismissed.

Shopping edits live in the existing planner JSON as optional `shoppingWeeks[localMonday][ingredientKey]` records `{ baseline, quantity, selected }`. Accept old planner records without this field. Preserve selections when the plan changes, and keep manual quantities only while their calculated baseline is unchanged. Reset list affects one week's shopping edits; it does not alter meal placements or recipe checkboxes. The existing capture dialog supports both the meal grid and selected shopping items, paginating shopping screenshots to 5–10 rows according to viewport height. Hiding controls must not change page boundaries. Printing the shopping capture includes every selected item.

## Verification

Development dependencies belong only in `tests/`: run `npm ci --prefix tests`, then `npm test --prefix tests`. The tests load the same vendored parsers and classic scripts that ship to Pages. Verify the page, script, stylesheet and recipes.md URLs after publication. Check 390 px and desktop layouts in a real browser when preview infrastructure is available; DOM tests do not prove visual fit or native gesture behavior.

Commit messages start with `top-recipes:`. Only push to main after the relevant checks pass.
