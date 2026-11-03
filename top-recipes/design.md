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

Use short, welcoming copy: “A few favourites, a week of good meals.” Recipe illustrations or photographs can be added later; the layout should look complete without them. Avoid oversized decoration that pushes recipes or the planner down the page.

## Page structure

The desktop page uses a centred layout with a maximum width of roughly 1280 px. A compact header introduces the collection, followed by two areas: a recipe library on the left and the larger weekly planner on the right. Keep the recipe library within reach while planning. On narrow screens, stack the library above the planner and give both sections direct navigation links.

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

### Recipe library

- Show all recipes initially, with search by title, ingredient and tag, plus meal filters.
- Each card displays the name, meal category, short description, servings and timing. Overnight chilling must be visible on the oats card.
- Clicking the recipe title or “View recipe & ingredients” opens its details. A separate Add button starts meal placement, avoiding ambiguity between viewing and planning.
- Cards have a visible drag handle on devices with a pointer. Dragging the handle must not interfere with clicking the recipe or selecting text.
- When a search has no results, show “No recipes found” and a Clear filters action.

### Recipe details and shopping ingredients

Open details in a side panel on desktop and a full-screen dialog on phones. Show the title, servings, timings, description, **Ingredients — what to buy**, numbered method and recipe notes, in that order. Opening details must not reset the plan or scroll position.

Ingredients appear as readable quantities with checkboxes. Checking an ingredient means “Already have / bought” and strikes it through; optional ingredients are labelled. Group ingredients by recipe component where provided, such as filling and pastry. Include an Add to week button and a Copy ingredients button that copies a plain-text shopping checklist. If clipboard access fails, show selectable text to copy manually.

Store checked ingredients locally by recipe ID and ingredient ID. Include Reset ingredient checks, and make clear that these checkboxes belong to this recipe's list. This first version shows each recipe's stated batch quantities and yield. A combined weekly shopping list can be added later once portion and leftover rules are defined.

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
| `meal_types` | One or more of `breakfast`, `lunch`, `dinner` |
| `servings` | Positive whole number describing the batch yield |
| `prep_minutes`, `cook_minutes`, `wait_minutes` | Non-negative whole numbers; display total as their sum |
| `tags` | A YAML list, which may be empty |

The recipe title comes from its level-two heading. Every ingredient row has a unique, stable ID within that recipe, a display quantity, an ingredient name and a component group. Quantities are readable strings, such as `40 g` or `To taste`; this version does not attempt to add quantities across recipes or scale them automatically.

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
- Clicking each recipe reveals its complete quantities, ingredients and method, including the overnight wait for oats.
- Search, filters, shopping checkboxes and Copy ingredients work, including empty results and clipboard failure.
- All 21 slots accept recipes. Library drops copy; grid moves and swaps preserve the intended meals; replacement, Remove and Clear week can be undone.
- The same planning tasks work with a mouse, touch and keyboard, with readable focus and announcements.
- Each week retains its own plan after refresh. Renamed, removed and invalid recipe data and unavailable local storage have understandable outcomes.
- Screenshot view contains all seven days and three meals, the date range and complete starter recipe names. Verify at 390 × 844 and at a smaller phone viewport, with no horizontal clipping.
- Screenshot controls can be hidden and restored. Returning to edit mode preserves the plan. Print preview uses a single portrait page for the starter content.
- Check normal text contrast against WCAG AA and ensure keyboard focus, reduced motion and touch targets remain usable.
