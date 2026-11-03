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

- Search by recipe name, ingredient or tag, or filter by meal. Open a recipe to see quantities and method; tick ingredients you have and copy the checklist.
- Drag a recipe's grip into any of the 21 meal slots, use its Add button, or tap an empty slot. Any recipe can go in any slot.
- Open a planned meal to read it. Its `···` menu offers Change, Move and Remove. Moving into an occupied slot swaps the meals. Adding from the library replaces the target.
- Undo reverses the last edit, including Clear week. Undo stays beside Clear week if you dismiss its notification. Changing weeks ends the previous week's undo history.
- Previous, Next, This week and Choose week select separately saved weeks. Dates use the browser's local calendar, beginning on Monday.
- Screenshot view shows the complete week as a portrait plan. Tap the plan or select Hide controls, take a screenshot, then tap again or press Escape to restore controls. Comfortable mode gives more room; Print uses a portrait page. For long names, use a full-page screenshot when needed.

Plans and ingredient checks save in this browser on this device; they do not sync between devices. If browser storage is unavailable, the page stays usable for the session. Malformed saved data is preserved until you explicitly choose Reset saved data, which clears plans and ingredient checks.

## Update and publish recipes

1. Edit [recipes.md](recipes.md). Copy a complete recipe section to add a dish.
2. Give a new dish a unique slug `id`. Keep an existing dish's ID when renaming it so saved plans keep working. Ingredient IDs should also remain stable.
3. Keep the YAML metadata, Ingredients table columns and numbered Method section.
4. Commit and push the updated file to the VibeProjects repository's `main` branch. GitHub Pages publishes the folder; refresh the page after deployment.

There is no generated data file or rebuild command. The browser reads and validates `recipes.md` directly using local Markdown and YAML libraries. The same file drives cards, search, ingredients and meal pickers. Errors identify the recipe and field; saved plans are retained if content cannot load. Text is rendered without executing authored HTML.

Quantities describe each recipe's stated batch size. The starter quantities and methods are suggestions, ready to replace with your own. Automatic portion scaling and combined weekly shopping quantities are outside this version.

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
| `src/planner.js`, `src/storage.js` | Calendar calculations, immutable edits and validated persistence |
| `src/capture.js`, `src/ui.js` | Screenshot view and shared interface helpers |
| `vendor/` | Local Marked and js-yaml browser files and licenses |
| `tests/` | Development-only dependencies and automated checks |

The page uses system fonts and local SVG illustrations. No external services or CDN requests are required. Scripts are ordinary deferred scripts, so the project needs no framework, bundler, server-side code or application package.json.
