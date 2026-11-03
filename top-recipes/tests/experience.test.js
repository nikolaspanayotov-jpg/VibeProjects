import test from "node:test";
import assert from "node:assert/strict";
import { api } from "./setup.js";

const {
  emptyWeek,
  assignMeal,
  moveMeal,
  cleanMealSettings,
  moveMealSettings,
  cookingBatches,
  buildShoppingList,
  applyShoppingEdits,
  createPersistence,
  validPlanner,
  PLAN_KEY,
  groupShoppingItems,
  paginateShoppingItems,
} = api;
const source = { day: "monday", meal: "dinner" };
const leftover = { day: "wednesday", meal: "lunch" };
const recipe = {
  id: "chicken",
  title: "Chicken",
  servings: 4,
  ingredients: [
    { id: "chicken", name: "Chicken thighs", quantity: "600 g" },
    { id: "eggs", name: "Eggs", quantity: "2" },
  ],
};
const getRecipe = (id) => (id === recipe.id ? recipe : undefined);
const planned = () =>
  assignMeal(assignMeal(emptyWeek(), source, "chicken"), leftover, "chicken");

test("household portions and linked leftovers buy exactly the combined cooking portions", () => {
  const week = planned();
  const settings = { "wednesday-lunch": { leftoverOf: "monday-dinner" } };
  const batches = cookingBatches(week, getRecipe, settings, 2);
  assert.equal(batches.length, 1);
  assert.equal(batches[0].servings, 4);
  assert.equal(batches[0].meals, 2);
  const list = buildShoppingList(week, getRecipe, {
    mealSettings: settings,
    householdSize: 2,
  });
  assert.equal(list.batchCount, 1);
  assert.equal(list.mealCount, 2);
  assert.equal(
    list.items.find((item) => item.name === "Chicken thighs").quantity,
    600,
  );
  // Explicit portions override the household just for that meal, including leftovers.
  settings["wednesday-lunch"].servings = 1;
  const small = buildShoppingList(week, getRecipe, {
    mealSettings: settings,
    householdSize: 2,
  });
  assert.equal(
    small.items.find((item) => item.name === "Chicken thighs").quantity,
    450,
  );
  assert.equal(small.items.find((item) => item.name === "Eggs").quantity, 2);
  assert.equal(buildShoppingList(week, getRecipe).items[0].quantity, 1200);
});

test("moving cooking meals carries portions and remaps leftovers; removing a source cooks remaining meals fresh", () => {
  const week = planned();
  const settings = {
    "monday-dinner": { servings: 3 },
    "wednesday-lunch": { servings: 1, leftoverOf: "monday-dinner" },
  };
  const target = { day: "tuesday", meal: "dinner" };
  const moved = moveMeal(week, source, target);
  const next = moveMealSettings(moved, settings, source, target);
  assert.equal(next["tuesday-dinner"].servings, 3);
  assert.equal(next["wednesday-lunch"].leftoverOf, "tuesday-dinner");
  assert.equal(cookingBatches(moved, getRecipe, next, 2).length, 1);
  const removed = assignMeal(week, source, null);
  assert.deepEqual(cleanMealSettings(removed, settings), {
    "wednesday-lunch": { servings: 1 },
  });
  assert.equal(
    cookingBatches(
      removed,
      getRecipe,
      cleanMealSettings(removed, settings),
      2,
    )[0].servings,
    1,
  );
  const tooLate = { day: "sunday", meal: "dinner" };
  const lateSettings = moveMealSettings(
    moveMeal(week, source, tooLate),
    settings,
    source,
    tooLate,
  );
  assert.equal(lateSettings["wednesday-lunch"].leftoverOf, undefined);
  const replaced = assignMeal(week, source, "pancakes");
  assert.deepEqual(api.replaceMealSettings(week, replaced, settings), {
    "wednesday-lunch": { servings: 1 },
  });
  assert.equal(
    cleanMealSettings(week, {
      "monday-dinner": { leftoverOf: "wednesday-lunch" },
      "wednesday-lunch": { leftoverOf: "monday-dinner" },
    })["wednesday-lunch"],
    undefined,
  );
});

test("legacy plans gain optional preferences, meal settings and templates without losing shopping or recipe checks", () => {
  const edits = {
    "eggs|item": { baseline: 2, quantity: 4, selected: false, bought: true },
  };
  const legacy = {
    schemaVersion: 1,
    weeks: { "2026-11-02": planned() },
    shoppingWeeks: { "2026-11-02": edits },
  };
  const data = new Map([[PLAN_KEY, JSON.stringify(legacy)]]);
  const storage = {
    getItem: (key) => data.get(key) ?? null,
    setItem: (key, value) => data.set(key, value),
  };
  const state = createPersistence(storage);
  assert.deepEqual(state.preferences(), {
    householdSize: null,
    favourites: [],
    recent: [],
  });
  assert.equal(data.get(PLAN_KEY), JSON.stringify(legacy));
  const settings = {
    "wednesday-lunch": { servings: 2, leftoverOf: "monday-dinner" },
  };
  state.savePlan("2026-11-02", planned(), settings);
  state.savePreferences({
    householdSize: 2,
    favourites: ["chicken"],
    recent: ["chicken"],
  });
  state.saveTemplates([
    { id: "easy-week", title: "Easy week", week: planned(), settings },
  ]);
  state.check("chicken", "eggs", true);
  const reloaded = createPersistence(storage);
  assert.equal(reloaded.issue, null);
  assert.equal(reloaded.preferences().householdSize, 2);
  assert.deepEqual(reloaded.mealSettings("2026-11-02"), settings);
  assert.deepEqual(reloaded.shoppingWeek("2026-11-02"), edits);
  assert.equal(reloaded.isChecked("chicken", "eggs"), true);
  const template = reloaded.templates()[0];
  template.week.monday.dinner = null;
  assert.equal(reloaded.templates()[0].week.monday.dinner, "chicken");
  assert.equal(
    validPlanner({
      ...legacy,
      preferences: { householdSize: 0, favourites: [], recent: [] },
    }),
    false,
  );
  assert.equal(
    validPlanner({
      ...legacy,
      mealSettings: { "2026-11-02": { "monday-dinner": { servings: -1 } } },
    }),
    false,
  );
  assert.equal(
    validPlanner({ ...legacy, templates: [{ id: "broken" }] }),
    false,
  );
});

test("bought marks survive unchanged totals and clear when the quantity needed changes", () => {
  const items = [{ key: "milk|ml", name: "Milk", quantity: 200, unit: "ml" }];
  const edits = {
    "milk|ml": { baseline: 200, quantity: 250, selected: true, bought: true },
  };
  assert.equal(applyShoppingEdits(items, edits)[0].bought, true);
  const changed = applyShoppingEdits(
    [{ ...items[0], quantity: 300 }],
    edits,
  )[0];
  assert.equal(changed.bought, false);
  assert.equal(changed.quantity, 300);
  assert.equal(changed.selected, true);
});

test("aisles and paginated screenshots keep every selected item exactly once in aisle order", () => {
  const names = [
    "Onions",
    "Chicken thighs",
    "Milk",
    "Bread",
    "Olive oil",
    "Carrots",
    "Salmon",
    "Eggs",
    "Plain flour",
    "Lemons",
    "Stock",
    "Potatoes",
  ];
  const items = names.map((name, index) => ({
    name,
    key: `${index}|item`,
    unit: "item",
    quantity: 1,
  }));
  const groups = groupShoppingItems(items);
  assert.deepEqual(
    groups.map((group) => group.aisle),
    api.SHOPPING_AISLES,
  );
  const pages = paginateShoppingItems(items, 5);
  assert.ok(pages.length > 1);
  assert.deepEqual(
    pages.flat().map((item) => item.key),
    groups.flatMap((group) => group.items).map((item) => item.key),
  );
  assert.equal(
    new Set(pages.flat().map((item) => item.key)).size,
    items.length,
  );
  assert.ok(pages.every((page) => page.length <= 5));
});
