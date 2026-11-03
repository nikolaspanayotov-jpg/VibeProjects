import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { api } from "./setup.js";

const {
  parseShoppingQuantity,
  shoppingName,
  buildShoppingList,
  applyShoppingEdits,
  createPersistence,
  validPlanner,
  emptyWeek,
  assignMeal,
  PLAN_KEY,
  parseRecipes,
} = api;
const recipes = parseRecipes(
  await readFile(new URL("../recipes.md", import.meta.url), "utf8"),
);
const getRecipe = (id) => recipes.find((recipe) => recipe.id === id);

test("shopping amounts handle weights, volumes, fractions, counts and pantry quantities", () => {
  const cases = [
    ["1 kg", 1000, "g"],
    ["1.5 litres", 1500, "ml"],
    ["2 cloves", 2, "clove"],
    ["Half a medium", 0.5, "item"],
    ["½", 0.5, "item"],
    ["1½ tbsp", 1.5, "tbsp"],
    ["3/4 tsp", 0.75, "tsp"],
    ["4, about 140 g each", 4, "item"],
    ["1 ready-rolled sheet, about 320 g", 1, "sheet"],
    ["1 small handful", 1, "handful"],
    ["To taste", 1, "pack"],
    ["1 pinch", 1, "pack"],
  ];
  for (const [source, quantity, unit] of cases) {
    const parsed = parseShoppingQuantity(source);
    assert.equal(parsed.quantity, quantity, source);
    assert.equal(parsed.unit, unit, source);
  }
});

test("shared ingredients sum across meals and repeated batches, with compatible volume conversion", () => {
  let week = assignMeal(
    emptyWeek(),
    { day: "monday", meal: "breakfast" },
    "overnight-oats",
  );
  week = assignMeal(
    week,
    { day: "tuesday", meal: "breakfast" },
    "overnight-oats",
  );
  week = assignMeal(
    week,
    { day: "wednesday", meal: "breakfast" },
    "macaroni-bake",
  );
  const list = buildShoppingList(week, getRecipe);
  assert.equal(list.mealCount, 3);
  assert.equal(list.recipeCount, 2);
  assert.equal(list.items.find((item) => item.name === "Milk").quantity, 700);
  assert.equal(
    list.items.find((item) => item.name === "Rolled oats").quantity,
    80,
  );
  const fake = (id) => ({
    id,
    title: id,
    ingredients: [
      {
        id: "stock",
        name: "Chicken stock",
        quantity: id === "a" ? "1 litre" : "250 ml",
      },
    ],
  });
  const converted = buildShoppingList(
    assignMeal(
      assignMeal(emptyWeek(), { day: "monday", meal: "lunch" }, "a"),
      { day: "monday", meal: "dinner" },
      "b",
    ),
    fake,
  );
  assert.equal(converted.items.length, 1);
  assert.equal(converted.items[0].quantity, 1250);
});

test("prepared onions and eggs merge while different flours, stocks and incompatible units stay distinct", () => {
  let week = assignMeal(
    emptyWeek(),
    { day: "monday", meal: "lunch" },
    "meatballs-soup",
  );
  week = assignMeal(week, { day: "monday", meal: "breakfast" }, "pancakes");
  week = assignMeal(week, { day: "tuesday", meal: "dinner" }, "wine-kebab");
  week = assignMeal(week, { day: "wednesday", meal: "dinner" }, "moussaka");
  const { items } = buildShoppingList(week, getRecipe);
  assert.equal(items.find((item) => item.name === "Onions").quantity, 4);
  assert.equal(items.find((item) => item.name === "Eggs").quantity, 3);
  assert.equal(
    items.find((item) => item.name === "Self-raising flour").quantity,
    200,
  );
  assert.equal(items.filter((item) => item.name === "Plain flour").length, 2);
  assert.equal(
    items.filter((item) => item.name.includes("vegetable stock")).length,
    2,
  );
  assert.equal(items.find((item) => item.name === "Salt").quantity, 1);
  assert.equal(
    shoppingName({ id: "milk", name: "Coconut milk" }),
    "Coconut milk",
  );
  assert.equal(
    shoppingName({
      id: "chicken",
      name: "Boneless, skinless chicken thighs, cut into pieces",
    }),
    "Chicken thighs",
  );
});

test("missing recipe slots are reported and optional-only ingredients retain their label", () => {
  let week = assignMeal(
    emptyWeek(),
    { day: "monday", meal: "breakfast" },
    "overnight-oats",
  );
  week = assignMeal(week, { day: "monday", meal: "dinner" }, "deleted-recipe");
  const list = buildShoppingList(week, getRecipe);
  assert.equal(list.missingCount, 1);
  assert.equal(list.mealCount, 2);
  assert.equal(
    list.items.find((item) => item.name === "Chia seeds").optional,
    true,
  );
  assert.equal(list.items.find((item) => item.name === "Milk").optional, false);
});

test("quantity edits persist for unchanged totals, while plan changes refresh amounts and keep selections", () => {
  const original = [
    { key: "milk|ml", name: "Milk", quantity: 450, unit: "ml" },
  ];
  const edits = {
    "milk|ml": { baseline: 450, quantity: 600, selected: false },
  };
  assert.deepEqual(applyShoppingEdits(original, edits)[0], {
    ...original[0],
    baseline: 450,
    quantity: 600,
    selected: false,
    bought: false,
  });
  const changed = applyShoppingEdits(
    [{ ...original[0], quantity: 550 }],
    edits,
  )[0];
  assert.equal(changed.quantity, 550);
  assert.equal(changed.selected, false);
  assert.equal(original[0].quantity, 450);
});

test("old saved plans load unchanged and shopping edits save independently for each week", () => {
  const oldPlan = {
    schemaVersion: 1,
    weeks: {
      "2026-11-02": assignMeal(
        emptyWeek(),
        { day: "monday", meal: "breakfast" },
        "pancakes",
      ),
    },
  };
  const data = new Map([[PLAN_KEY, JSON.stringify(oldPlan)]]);
  const storage = {
    getItem: (key) => data.get(key) ?? null,
    setItem: (key, value) => data.set(key, value),
  };
  const saved = createPersistence(storage);
  assert.equal(saved.issue, null);
  assert.deepEqual(saved.shoppingWeek("2026-11-02"), {});
  const edits = {
    "milk|ml": { baseline: 250, quantity: 300, selected: false },
  };
  saved.saveShoppingWeek("2026-11-02", edits);
  saved.check("pancakes", "egg", true);
  const loaded = createPersistence(storage);
  assert.deepEqual(loaded.shoppingWeek("2026-11-02"), edits);
  assert.deepEqual(loaded.shoppingWeek("2026-11-09"), {});
  assert.equal(loaded.week("2026-11-02").monday.breakfast, "pancakes");
  assert.equal(loaded.isChecked("pancakes", "egg"), true);
  loaded.reset();
  assert.deepEqual(loaded.shoppingWeek("2026-11-02"), {});
});

test("invalid shopping values are rejected and unavailable storage keeps shopping edits in memory", () => {
  const saved = createPersistence(null);
  const edits = { "milk|ml": { baseline: 250, quantity: 0, selected: false } };
  saved.saveShoppingWeek("2026-11-02", edits);
  assert.deepEqual(saved.shoppingWeek("2026-11-02"), edits);
  assert.equal(saved.issue, "unavailable");
  for (const quantity of [-1, Infinity, NaN, 1e10]) {
    assert.throws(() =>
      saved.saveShoppingWeek("2026-11-02", {
        "milk|ml": { ...edits["milk|ml"], quantity },
      }),
    );
  }
  assert.equal(
    validPlanner({
      schemaVersion: 1,
      weeks: {},
      shoppingWeeks: { "2026-11-02": { bad: { quantity: 10 } } },
    }),
    false,
  );
});
