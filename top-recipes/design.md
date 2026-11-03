# Top Recipes — page design

Status: implemented as a build-free static website in this folder. This document records the visual and interaction specification; see [README.md](README.md) for run commands, recipe editing and verification details.

## Purpose

A personal collection of favourite recipes with a weekly meal planner. Readers can explore a dish, see what to buy, and arrange breakfast, lunch and dinner from Monday to Sunday. A clean screenshot view turns the plan into a useful reference to keep on a phone.

All recipe content lives in [recipes.md](recipes.md). The page generates its cards and ingredient lists from that file, so adding a recipe never requires editing the interface.

## Starting collection

| Meal | Recipe | Stable recipe ID |
| --- | --- | --- |
| Breakfast | Overnight oats | `overnight-oats` |
| Lunch | Chicken and leek pie | `chicken-and-leek-pie` |
| Dinner | Moussaka | `moussaka` |

“Leek” and “moussaka” are the display spellings for the requested chicken and leak pie and musaka. Quantities and methods in the recipe file are suggested starting versions, ready to replace with personal favourites.

## Visual direction

Think of a well-kept kitchen notebook: warm, calm and inviting, with enough colour and movement to make planning enjoyable.

| Element | Direction |
| --- | --- |
| Page background | Warm cream, `#FAF7F0` |
| Cards and recipe panels | Soft white, `#FFFFFF` |
| Main text | Deep charcoal, `#252A24` |
| Primary buttons and links | Dark olive, `#36513E`; white button text |
| Secondary accent | Terracotta, `#8F422D`, used sparingly |
| Breakfast / lunch / dinner | Pale oat, sage and clay fills, always paired with written labels |
| Headings | Georgia or a similar readable serif |
| Body and controls | System sans-serif, 16 px minimum for ordinary reading |
| Shape and spacing | 12–16 px card corners; generous spacing based on an 8 px rhythm |
| Motion | Brief hover and placement feedback; respect reduced-motion preferences |

Use short, welcoming copy: “A few favourites, a week of good meals.” Each recipe has its own small food illustration, using soft colours and simple outlines to match the original oats, chicken pie and moussaka drawings. Images depict the named dish: soup bowls, fish fillets, coiled banitsa, layered lasagna, pancakes and the other meals. Keep the original three illustrations assigned to their dishes. Avoid oversized decoration that pushes recipes or the planner down the page.

## Page structure

The desktop page uses a centred layout with a maximum width of roughly 1280 px. A compact header introduces the collection, followed by two areas: a recipe library on the left and the larger weekly planner on the right. Keep the recipe library within reach while planning. On phones and tablets up to 960 px, stack the library above the planner and start the entire collection collapsed, so reaching the plan never requires scrolling through every recipe. Keep both sections' direct navigation links.

```text
TOP RECIPES                         Recipes · Weekly plan
A few favourites, a week of good meals.

YOUR RECIPES                     YOUR WEEK
[Search recipes…]                [Previous] Week of 2 Nov [Next]
[All] [Breakfast] [Lunch]         [Choose week] [Screenshot view]
[Dinner]
                                  Mon Tue Wed Thu Fri Sat Sun
Overnight oats          [Add]    B [ ] [ ] [ ] [ ] [ ] [ ] [ ]
Breakfast · 1 serving            L [ ] [ ] [ ] [ ] [ ] [ ] [ ]
[View recipe & ingredients]      D [ ] [ ] [ ] [ ] [ ] [ ] [ ]

Chicken and leek pie    [Add]    Drag a recipe into a meal slot,
Lunch · 4 servings               or select a slot to choose a dish.
[View recipe & ingredients]

Moussaka                [Add]
Dinner · 6 servings
[View recipe & ingredients]
```

The B/L/D abbreviations above are only for this wireframe; the actual interface displays Breakfast, Lunch and Dinner in full.

### Collapsible recipe library

- Keep a compact, cream collection header visible with the serif title, total recipe count, and an explicit Show recipes / Hide recipes button with a rotating chevron. Use the existing olive and cream design system. The button has a 44 px touch target, `aria-expanded`, and `aria-controls` pointing to the complete collection body.
- Start closed on phones and tablets, and open on the desktop's two-column layout. A direct `#recipes` link opens the collection. Preserve the user's explicit choice through responsive changes during the page visit.
- Collapse the search, meal filters, cards and footer together with the native `hidden` attribute. Keep their DOM and state intact so reopening restores the search and filters. Display the total collection count in the header and the filtered result count within the expanded body.
- Keep the expanded collection header sticky while scrolling through recipes, so Hide recipes remains available. Include Hide recipes and plan my week after the last card, returning focus and scroll to the planner. Closing a sticky header after a long scroll must bring the compact header back into view rather than leave the user stranded at the bottom of the page.
- The Recipes navigation link opens the collection; Weekly plan collapses it in the stacked mobile layout. When the collection is closed on desktop, place the compact header above a full-width planner.
- Within the open collection, show all recipes initially, with search by title, ingredient and tag, plus meal filters.
- Each card displays the name, meal category, short description, servings and timing. Overnight chilling must be visible on the oats card.
- Clicking the recipe title or “View recipe & ingredients” opens its details. A separate Add button starts meal placement, avoiding ambiguity between viewing and planning.
- Cards have a visible drag handle on devices with a pointer. Dragging the handle must not interfere with clicking the recipe or selecting text.
- When a search has no results, show “No recipes found” and a Clear filters action.

### Recipe details and shopping ingredients

Open details in a side panel on desktop and a full-screen dialog on phones. Show the title, servings, timings, description, **Ingredients — what to buy**, numbered method and recipe notes, in that order. Opening details must not reset the plan or scroll position.

Ingredients appear as readable quantities with checkboxes. Checking an ingredient means “Already have / bought” and strikes it through; optional ingredients are labelled. Group ingredients by recipe component where provided, such as filling and pastry. Include an Add to week button and a Copy ingredients button that copies a plain-text shopping checklist. If clipboard access fails, show selectable text to copy manually.

Store checked ingredients locally by recipe ID and ingredient ID. Include Reset ingredient checks, and make clear that these checkboxes belong to this recipe's list. Recipe details show each recipe's stated batch quantities and yield. The separate weekly shopping list combines ingredients from the plan and has its own per-week selections.

## Weekly planner

### Grid and week selection

- Provide exactly 21 slots: Monday through Sunday, each with Breakfast, Lunch and Dinner.
- On desktop, show seven day columns and three meal rows. On phones, use seven day rows and three meal columns so the whole week needs no horizontal scrolling.
- Initialise the week to the current local Monday, including Monday's date in the heading and dates beside each day. Previous, Next and Choose week navigate between independently saved weeks; any chosen date resolves to its Monday.
- Start with an empty plan and an inviting prompt, “Choose a recipe to start your week.” Do not silently populate a sample plan.
- One slot holds one recipe. The same recipe may appear in multiple slots. Meal categories guide browsing but do not restrict placement.

### Drag-and-drop rules

1. Drag a recipe handle from the library; all slots become valid targets and the hovered target gains a border and a label such as “Add to Monday breakfast”.
2. Drop onto an empty slot to add a copy of that recipe. The library card stays available for other days.
3. Drop onto an occupied slot to replace its recipe. Show a brief status message and Undo action.
4. Drag a planned meal into an empty slot to move it. Dropping onto another planned meal swaps the two recipes, preserving both choices.
5. Dropping outside a slot or pressing Escape cancels the drag and leaves the plan unchanged.
6. A planned meal has separate View recipe, Change and Remove actions. Clear week provides an inline Undo action and only affects the selected week.

Undo restores the state before the most recent placement, move, swap, removal or clear action. Announce the outcome, for example “Moussaka moved to Tuesday dinner.” Preserve that undo state until another edit or week navigation.

### Touch and keyboard alternatives

Drag-and-drop is an enhancement, never a requirement. Selecting an empty slot opens a searchable recipe picker, while Add on a recipe opens a day-and-meal picker. Selecting Change on a filled slot opens the same recipe picker. These controls provide all placement and replacement functions with taps or a keyboard; moving a meal is also available through a Move to control.

Use buttons and selects with visible focus, meaningful labels and at least 44 px touch targets. Return focus to the initiating control when a picker closes. Announce updates through a polite live region. Detail dialogs need focus containment, Escape to close, and focus restoration. Do not rely on colour alone to communicate meal categories or drop targets.

### Saving and resilience

Save immediately after every edit to browser local storage. Plans stay on the current browser and device after refreshing or closing the page. They do not automatically sync to a phone; the screenshot is the intended portable copy.

Use a versioned key such as `top-recipes:planner:v1`. Save weeks by their local Monday date as `YYYY-MM-DD`, and identify each slot with a weekday and meal key. Store stable recipe IDs rather than copies of recipes:

```json
{
  "schemaVersion": 1,
  "weeks": {
    "2026-11-02": {
      "monday": { "breakfast": "overnight-oats", "lunch": null, "dinner": null },
      "tuesday": { "breakfast": null, "lunch": "chicken-and-leek-pie", "dinner": null },
      "wednesday": { "breakfast": null, "lunch": null, "dinner": "moussaka" },
      "thursday": { "breakfast": null, "lunch": null, "dinner": null },
      "friday": { "breakfast": null, "lunch": null, "dinner": null },
      "saturday": { "breakfast": null, "lunch": null, "dinner": null },
      "sunday": { "breakfast": null, "lunch": null, "dinner": null }
    }
  }
}
```

This JSON illustrates the storage shape, not a preloaded plan. Validate stored data on load. If storage is unavailable, continue in memory and display “This plan will last until you close the page.” If a recipe is removed from the source file, preserve its slot as “Recipe unavailable” with Change and Remove actions. A renamed recipe keeps its plan placements when its ID stays unchanged. Malformed saved data should produce a visible recovery message and an explicit Reset saved plan action, rather than silently discarding it.

## Weekly shopping list

A Shopping list button beside the planner's Screenshot view opens a separate dialog for the selected week. It scales recipes to household and individual meal portions, combines linked leftover servings into the source cooking batch, and groups ingredients by grocery aisle. Without a household setting, existing plans keep the authored recipe servings.

- Combine matching ingredients with matching units, converting kilograms to grams and litres to millilitres. Keep different foods and incompatible units on separate lines. Preserve original quantities and preparation notes in a Recipe amounts disclosure.
- Each row has a tick box, editable numeric quantity and 44 px minus/plus controls, with its unit displayed. All items start selected; untick what is already in the cupboard or unwanted. Label optional-only ingredients.
- Whole items round up for purchasing. “To taste”, pinches and unspecified amounts start at one pack to check in the cupboard. Zero quantities do not appear in screenshots.
- Save edits for each local Monday in the existing planner storage as optional `shoppingWeeks` data, preserving old plans and storage keys. Selections persist across changes to the plan; quantity overrides persist only while the calculated total is unchanged.
- Provide Select all, Untick all and Reset list. Reset list restores calculated quantities and selections for this week without editing the plan or per-recipe checkboxes.
- Empty plans explain that meals must be added first. An unavailable recipe produces an explicit missing-ingredients message while the remaining ingredients still load.
- Screenshot view uses the existing portrait capture dialog, showing only selected positive-quantity items, a week/date heading and page number. Use a viewport-based budget of 5–10 row heights, reserving space for aisle headings; keep page boundaries stable when hiding controls. Previous/Next page controls and keyboard arrows browse the pages.
- Screenshot rows show an empty or bought checkbox, ingredient name and quantity, under aisle headings. Omit editing controls. Close returns to the still-open shopping list. Printing includes the entire selected list.

## Faster planning and shopping

- On screens up to 960 px, fix a three-button navigation bar to the bottom: Weekly plan, Recipes and Shopping list. Reserve bottom safe-area space and keep notifications above the bar. Navigation is hidden in dialogs, captures and print. Recipes opens and focuses the collection; Weekly plan collapses it and returns to the planner.
- The visual meal picker initially shows suitable meal types, with All recipes, Pinned and Recent shortcuts. Search spans the collection while ranking suitable recipes first. Use separate 44 px star buttons to pin recipes without selecting them. Keep pins and the last 12 placed recipes in the existing browser storage.
- Place Copy last week and Saved weeks beside the week controls. Save a named snapshot of meals, portions and leftover links; applying replaces the current week with Undo. Shopping overrides and bought marks are never copied. Limit saved weeks to 50. Empty previous weeks leave the current plan intact and explain why.
- Cooking for sets a household size once, with Recipe servings as the compatibility default. Each meal can use the default or a specific serving count. A later meal can link to an earlier fresh slot of the same dish. Show a live total-to-cook preview: two servings now plus two leftover servings means four servings in the original batch. Display portions and a written Leftovers label in both the grid and capture.
- Carry portions and leftover links when meals move or swap. If a source is removed, replaced, or moved later than its leftovers, make remaining affected meals fresh cooking and announce the change. Replacing a dish resets that slot’s individual settings. Undo restores settings alongside recipe placements.
- Organise groceries into Fruit & vegetables, Meat & fish, Dairy & eggs, Bakery & pastry, and Cupboard & other. Unknown ingredients stay in the final group. Keep source recipes and authored amounts available in editing mode.
- Start shopping switches to large Bought checkboxes with progress and Hide bought items. Edit list restores inclusion ticks and quantity controls. Include and Bought are independent. Changed calculated totals clear bought marks; Reset list clears all shopping edits for that week. Screenshots retain all selected items with bought marks, grouped by aisle, even when the shopping view hides bought items. Keep page boundaries stable while controls are hidden, and print the complete selected list.

## Screenshot view

The Screenshot view button opens a dedicated, uncluttered view of the selected week's current plan. The user can take a normal device screenshot and save or send it to their phone.

- Use a portrait layout with seven day rows and three labelled meal columns, with a narrow day/date column on the left.
- Include “My weekly meal plan”, the week's date range and a discreet Top Recipes footer.
- Hide the library, drag handles, editing controls, ingredient lists and empty-slot prompts. Use an em dash for an empty meal.
- Keep full recipe names readable, wrapping across lines without ellipses. Use restrained borders and a solid cream background.
- Offer Comfortable and Fit to screen sizes. Fit to screen measures the available viewport and reduces spacing before text size; the starter recipes and all 21 slots should fit within a typical phone viewport such as 390 × 844 CSS pixels.
- Set a readability floor for long future names; allow vertical scrolling and suggest a full-page screenshot if a plan cannot fit legibly. Never hide a day to force a fit.
- Put Close and size controls above the capture area. Tapping the capture area enters a controls-hidden state; Escape, a subsequent tap, or browser Back restores controls. Instructions appear before controls are hidden and must not appear in the captured plan.
- Include print styles using the same layout on one portrait page, with browser headers and footers disabled by the user if necessary.

Screenshot view is a presentation of saved state, not a separate editable copy. Closing it returns to the same week and planning position. A direct Download PNG action is an optional later enhancement; it is not necessary for ordinary screenshots.

## Recipe content and implementation foundation

### Single source of recipe content

Keep all authored recipes in `recipes.md`. Each recipe is a level-two heading followed by a fenced YAML metadata block, a short description, an Ingredients table, a numbered Method section and optional Notes. The file includes editing instructions, and this design provides a blank template below.

The metadata contract is:

| Field | Required format |
| --- | --- |
| `id` | Unique permanent lowercase slug; keep it when renaming a dish |
| `image` | Optional local path under `assets/`, such as `assets/recipes/pizza.svg`; SVG, PNG, JPEG, WebP and AVIF are supported |
| `meal_types` | One or more of `breakfast`, `lunch`, `dinner` |
| `servings` | Positive whole number describing the batch yield |
| `prep_minutes`, `cook_minutes`, `wait_minutes` | Non-negative whole numbers; display total as their sum |
| `tags` | A YAML list, which may be empty |

The recipe title comes from its level-two heading. Every ingredient row has a unique, stable ID within that recipe, a display quantity, an ingredient name and a component group. Quantities are readable strings, such as `40 g` or `To taste`. Recipe details preserve these strings; weekly shopping totals combine compatible amounts, scaled to household and individual meal portions. Linked leftovers contribute to the earlier cooking batch.

Image assignments live in the same recipe metadata and are shared by cards, detail panels and meal pickers. New recipes need no hard-coded image mapping in JavaScript. If an image is omitted or fails to load, show a neutral place setting. Never substitute a picture of another dish based on breakfast, lunch or dinner. Load list thumbnails lazily to keep mobile browsing light.

### Suggested implementation

Use static HTML, CSS and small JavaScript files with no application build step. The page fetches `recipes.md` directly, parses Markdown tokens with the local Marked distribution and YAML metadata with the local js-yaml distribution, then validates the collection before rendering. This follows the VibeProjects repository's GitHub Pages setup and build-free project rules. The libraries are checked in with their licenses, so a CDN is not required.

The interface derives the library, details and planner labels from the parsed data. Recipe text is inserted through safe text nodes. Failed requests or content validation show a retry control and an actionable error without overwriting saved plans. When opened directly from disk, an Open recipes.md file picker gives the browser permission to read the local recipe collection.

Scripts load in dependency order using `defer`, keep their variables in individual function scopes, and expose shared helpers through `globalThis.TopRecipes`. Files remain separate because the planner, content validation, details and screenshot interactions are substantial enough to benefit from clear boundaries.

```text
top-recipes/
  AGENTS.md                   Project conventions and live URL
  README.md                   Run, publish and editing instructions
  design.md                   This specification
  recipes.md                  Single source of recipe content
  index.html                  Page shell and script order
  styles.css                  Responsive and screenshot styles
  assets/                     Local illustrations and site mark
  vendor/                     Marked, js-yaml and licenses
  src/
    content.js                Markdown/YAML parsing and validation
    app.js                    Library, dialogs and planner coordination
    recipes.js                Recipe details and shopping checklists
    shopping.js               Scaled totals, aisles, selections and bought marks
    experience.js             Saved weeks and meal portions/leftover controls
    planner.js                Calendar, placement, move and swap logic
    storage.js                Versioned browser persistence
    capture.js                Screenshot and print presentation
    ui.js                     Shared DOM helpers
  tests/                      Development-only npm tools and checks
```

Validation identifies the recipe and field for duplicate IDs, missing metadata, unknown meal types, invalid timings or servings, malformed ingredient tables, duplicate or missing ingredient IDs, empty descriptions, and empty methods. Invalid content never overwrites browser plans.

### Adding or changing a recipe later

1. Copy an existing recipe section or the blank template below into `recipes.md`.
2. Give a new recipe a new permanent ID and fill in its metadata, description, ingredients and method. Keep the existing ID when editing a saved recipe.
3. Give each ingredient a stable ID so its shopping checkbox survives wording changes. The `Group` column can use `Main` if no grouping is needed.
4. Refresh the page using a static server, or commit and push to `main` and wait for GitHub Pages to publish. A valid new recipe appears automatically in search, filters, details and the planner picker.
5. Recipe edits are read directly from Markdown after publishing and refreshing; no rebuild is required. Browser-local plan changes save immediately.

````markdown
## New recipe name

```yaml
id: new-recipe-name
image: assets/recipe-placeholder.svg
meal_types: [dinner]
servings: 2
prep_minutes: 15
cook_minutes: 30
wait_minutes: 0
tags: []
```

A short description of the dish.

### Ingredients

| ID | Quantity | Ingredient | Group |
| --- | --- | --- | --- |
| example-ingredient | 200 g | Example ingredient | Main |

### Method

1. Describe the first step.
2. Describe the next step.

### Notes

Optional serving, preparation or substitution notes.
````

## Acceptance checks

- The three starter recipes load directly from `recipes.md`. Adding a fourth valid recipe requires no interface code changes.
- At phone width the complete recipe collection starts collapsed. Show/Hide remains keyboard accessible, preserves filtering and saved data, and lets the user return to the planner without scrolling through the full recipe collection. Check default desktop expansion and direct Recipes links.
- Clicking each recipe reveals its complete quantities, ingredients and method, including the overnight wait for oats.
- Search, filters, shopping checkboxes and Copy ingredients work, including empty results and clipboard failure.
- All 21 slots accept recipes. Library drops copy; grid moves and swaps preserve the intended meals; replacement, Remove and Clear week can be undone.
- The same planning tasks work with a mouse, touch and keyboard, with readable focus and announcements.
- Each week retains its own plan after refresh. Renamed, removed and invalid recipe data and unavailable local storage have understandable outcomes.
- Screenshot view contains all seven days and three meals, the date range and complete starter recipe names. Verify at 390 × 844 and at a smaller phone viewport, with no horizontal clipping.
- Screenshot controls can be hidden and restored. Returning to edit mode preserves the plan. Print preview uses a single portrait page for the starter content.
- Shopping list totals match scaled portions, linked leftovers and compatible unit conversions. Copy/apply include meal settings and support Undo. Pins, recent meals, saved weeks and bought marks survive reload without rewriting legacy data on page load. Tick choices and quantity overrides survive refresh independently by week. Shopping screenshot pages include every selected positive-quantity item exactly once, and printing includes all pages.
- Check normal text contrast against WCAG AA and ensure keyboard focus, reduced motion and touch targets remain usable.
