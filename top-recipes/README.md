# Top Recipes

A warm recipe notebook and Monday–Sunday meal planner, served directly by GitHub Pages.

**Live page:** https://nikolaspanayotov-jpg.github.io/VibeProjects/top-recipes/

## Open locally

No installation or application build is needed. From this folder, run:

```sh
python3 -m http.server 8000
```

Open **http://localhost:8000/**. Alternatively, serve the VibeProjects repository root and open **http://localhost:8000/top-recipes/**.

You can also open `index.html` directly from disk. Because browsers block automatic access to neighbouring local files, select **Open recipes.md** to choose your recipe collection. Once selected, recipes and planning work normally. On HTTP and GitHub Pages, recipes load automatically.

## Use the page

- On phones and tablets, the recipe collection starts collapsed so the weekly planner is close to the top. Use **Show recipes** to browse and **Hide recipes** to close the whole collection. Its header stays visible while browsing, and **Hide recipes and plan my week** at the bottom returns you to the planner. The desktop collection starts open; collapsing it gives the planner the full width.
- The fixed phone navigation takes you straight to **Weekly plan**, **Recipes** or **Shopping list**. It disappears while a dialog or screenshot is open.
- Search by recipe name, ingredient or tag, or filter by meal. Open a recipe to see quantities and method; tick ingredients you have and copy the checklist.
- Drag a recipe's grip into any of the 21 meal slots, use its Add button, or tap an empty slot. Any recipe can go in any slot.
- The visual meal picker starts with suitable recipes, with **All recipes**, **★ Pinned** and **Recent** shortcuts. Search includes the entire collection, and any recipe can still go in any meal slot. Tap **☆** to pin a dish; **★** unpins it. Pins and the last 12 recipes you placed save in this browser.
- Open a planned meal to read it. Its `···` menu offers **Portions & leftovers**, Change, Move and Remove. Moving into an occupied slot swaps the meals. Adding from the library replaces the target.
- Undo reverses the last edit, including Clear week. Undo stays beside Clear week if you dismiss its notification. Changing weeks ends the previous week's undo history.
- Previous, Next, This week and Choose week select separately saved weeks. Dates use the browser's local calendar, beginning on Monday.
- **Copy last week** copies the previous calendar week into the selected week. **Saved weeks** lets you name and save up to 50 reusable plans, then apply or delete them. Both copy and apply include individual portions and leftover links and can be undone. Household size remains your current setting; shopping edits and bought marks stay with their original week.
- **Cooking for** sets household size once for all weeks. Leave **Recipe servings** selected to keep the original full-batch amounts. A meal’s **Portions & leftovers** controls can override its servings or link it to an earlier fresh cooking of the same dish.
- **Shopping list** opens the selected week's ingredients. Shared items combine when their units match, with kilograms converted to grams and litres to millilitres. Untick items you have or want to skip, and use the minus/plus buttons or type a quantity. Screenshot view includes only selected items with positive quantities, with Previous/Next page controls for long lists. Hide controls for a clean screenshot; returning to the list keeps your edits.
- **Start shopping** turns the grouped list into large **Bought** checkboxes. These are separate from the editing checkboxes that choose what to buy. Use **Hide bought items** to see what remains, **Clear bought marks** to start again, or **Edit list** to adjust quantities. Screenshots include all selected items, with bought marks, even if bought items are hidden in shopping mode.
- Screenshot view shows the complete week as a portrait plan. Tap the plan or select Hide controls, take a screenshot, then tap again or press Escape to restore controls. Comfortable mode gives more room; Print uses a portrait page. For long names, use a full-page screenshot when needed.

Showing or hiding recipes preserves your search, filters and saved data. The Recipes navigation link opens the collection; Weekly plan closes it on phones and tablets. Your explicit show/hide choice stays in place through screen-size changes during the current page visit.

Plans, saved weeks, pins, recent recipes, portion settings, shopping edits, bought marks and recipe ingredient checks save in this browser on this device; they do not sync between devices. Shopping lists save separately for each week. If browser storage is unavailable, the page stays usable for the session. Malformed saved data is preserved until you explicitly choose Reset saved data, which clears all saved page data.

Shopping quantities scale each recipe by the servings needed. With no household size selected, each meal uses the recipe’s stated servings, preserving existing plans. Linked leftover meals add their portions to the earlier cooking batch. For example, a recipe for four serving a household of two on Monday and two as leftovers on Wednesday needs one four-serving batch. The portions field describes what is eaten at that meal; the preview states the total batch to cook. If a source is removed, replaced or moved after its leftovers, affected remaining meals become fresh cooking and a message explains the change. Whole items round up, while “to taste”, pinches and unspecified amounts start at one pack to check in your cupboard. The Recipe amounts disclosure preserves the source quantities, preparation notes and batch scaling. Ingredients are grouped into fruit and vegetables, meat and fish, dairy and eggs, bakery and pastry, and cupboard items. Optional ingredients are labelled. Different foods and incompatible units stay on separate lines; plain flour and self-raising flour are distinct.

Tick choices persist as the plan changes. A manually changed quantity stays while its calculated recipe total is unchanged; if that total changes, the amount refreshes from the plan and its bought mark clears so an increased requirement is not silently marked complete. Reset list restores the calculated quantities, selects every ingredient and clears bought marks for that week. Weekly shopping choices are independent of the “already have / bought” checkboxes inside individual recipes.

## Update and publish recipes

1. Edit [recipes.md](recipes.md). Copy a complete recipe section to add a dish.
2. Give a new dish a unique slug `id`. Keep an existing dish's ID when renaming it so saved plans keep working. Ingredient IDs should also remain stable. Change the copied `image` field to the new dish's artwork, or remove it to use a neutral place setting.
3. Keep the YAML metadata, Ingredients table columns and numbered Method section.
4. Commit and push the updated file to the VibeProjects repository's `main` branch. GitHub Pages publishes the folder; refresh the page after deployment.

There is no generated data file or rebuild command. The browser reads and validates `recipes.md` directly using local Markdown and YAML libraries. The same file drives cards, search, ingredients and meal pickers. Errors identify the recipe and field; saved plans are retained if content cannot load. Text is rendered without executing authored HTML.

Each current recipe has its own image assigned in its YAML metadata, for example `image: assets/recipes/pizza.svg`. The original oats, chicken pie and moussaka illustrations remain assigned to those three dishes; the other dishes have individual matching SVG illustrations in `assets/recipes/`. To replace an image, add a local SVG, PNG, JPEG, WebP or AVIF file under `assets/` and update that recipe's `image` path. Names may use letters, numbers, hyphens and underscores. The cards, details and meal picker all use that same assignment. Missing or unassigned pictures use a neutral place-setting illustration rather than a different dish. Library and picker thumbnails load lazily.

Quantities describe each recipe's stated batch size. The starter quantities and methods are suggestions, ready to replace with your own. Shopping totals scale those quantities to household and individual meal portions, combining linked leftovers into their original batch. Recipe details continue to show the authored batch amounts.

## Development checks

Only the test harness uses npm. With Node.js 22.8 or newer:

```sh
npm ci --prefix tests
npm test --prefix tests
```

Checks cover Markdown parsing, content validation, calendar calculations, persistence, the actual shipped scripts' DOM interactions and project-relative asset paths. Native dragging, visual layout, screenshot fit and print pagination require real-browser checks when browser infrastructure is available.

## Source map

| File | Purpose |
| --- | --- |
| `recipes.md` | All authored recipe content |
| `design.md` | Visual and interaction specification |
| `index.html`, `styles.css`, `assets/` | Page shell, responsive styles and local illustrations |
| `src/content.js` | Markdown-token and YAML validation |
| `src/app.js` | Library, dialogs, planner controls and drag-and-drop |
| `src/recipes.js` | Safe recipe rendering and shopping checklists |
| `src/shopping.js` | Scaled ingredient totals, aisle groups, quantities, selection and bought marks |
| `src/experience.js` | Reusable weeks and per-meal portions/leftover controls |
| `src/planner.js`, `src/storage.js` | Calendar calculations, immutable edits and validated persistence |
| `src/capture.js`, `src/ui.js` | Screenshot view and shared interface helpers |
| `vendor/` | Local Marked and js-yaml browser files and licenses |
| `tests/` | Development-only dependencies and automated checks |

The page uses system fonts and local SVG illustrations. No external services or CDN requests are required. Scripts are ordinary deferred scripts, so the project needs no framework, bundler, server-side code or application package.json.
