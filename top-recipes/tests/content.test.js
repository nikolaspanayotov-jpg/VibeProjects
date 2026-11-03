import { api, runScript } from "./setup.js";
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
const { parseRecipes } = api;

const markdown = await readFile(
  new URL("../recipes.md", import.meta.url),
  "utf8",
);

test("compiles the authored recipes, preserving quantities, components and timing", () => {
  const recipes = parseRecipes(markdown);
  assert.deepEqual(
    recipes.map((recipe) => recipe.id),
    [
      "overnight-oats", "chicken-and-leek-pie", "moussaka",
      "chicken-with-rice", "cottage-pie", "lasagna", "spaghetti-bolognese",
      "sausages", "salmon", "chicken-soup", "meatballs-soup", "filled-peppers",
      "pancakes", "macaroni-bake",
      "tuna", "chicken-kavarma", "wine-kebab",
      "pizza", "potato-and-leek-soup", "banitsa", "spanish-omelette", "egg-sandwich",
      "roast-dinner", "roast-turkey-with-potatoes", "french-toast",
      "chicken-pineapple-stir-fry", "turkey-soup",
    ],
  );
  assert.equal(recipes[0].waitMinutes, 480);
  assert.equal(recipes[0].ingredients[0].quantity, "40 g");
  assert.deepEqual(
    recipes.slice(0, 3).map((recipe) => recipe.ingredients.length),
    [6, 14, 17],
  );
  assert.equal(recipes[1].ingredients.at(-1).group, "Pastry lid");
  assert.equal(recipes[2].method.length, 7);
  assert.ok(recipes[0].description.startsWith("Creamy oats"));
  assert.deepEqual(
    recipes.filter(recipe => recipe.mealTypes.includes("breakfast")).map(recipe => recipe.id),
    ["overnight-oats", "pancakes", "macaroni-bake", "banitsa", "spanish-omelette", "egg-sandwich", "french-toast"],
  );
});

test("adding a recipe section automatically creates an additional data record", () => {
  const oats = markdown.slice(
    markdown.indexOf("## Overnight oats"),
    markdown.indexOf("## Chicken and leek pie"),
  );
  const extra = oats
    .replace("## Overnight oats", "## Berry breakfast")
    .replace("id: overnight-oats", "id: berry-breakfast");
  const recipes = parseRecipes(`${markdown}\n${extra}`);
  assert.equal(recipes.length, parseRecipes(markdown).length + 1);
  assert.equal(recipes.at(-1).title, "Berry breakfast");
  assert.equal(recipes.at(-1).id, "berry-breakfast");
});

test("content errors identify the affected recipe and field", async (t) => {
  const cases = [
    [
      "duplicate recipe",
      markdown.replace("id: moussaka", "id: overnight-oats"),
      /Moussaka → id: duplicate/,
    ],
    [
      "unknown category",
      markdown.replace("meal_types: [breakfast]", "meal_types: [snack]"),
      /Overnight oats → meal_types/,
    ],
    [
      "negative wait",
      markdown.replace("wait_minutes: 480", "wait_minutes: -1"),
      /Overnight oats → wait_minutes/,
    ],
    [
      "zero servings",
      markdown.replace("servings: 1", "servings: 0"),
      /Overnight oats → servings/,
    ],
    [
      "duplicate ingredient",
      markdown.replace("| milk | 100 ml", "| rolled-oats | 100 ml"),
      /Overnight oats → ingredients: invalid or duplicate/,
    ],
    [
      "missing quantity",
      markdown.replace("| rolled-oats | 40 g", "| rolled-oats | "),
      /Overnight oats → ingredients/,
    ],
    [
      "wrong columns",
      markdown.replace(
        "| ID | Quantity | Ingredient | Group |",
        "| ID | Amount | Ingredient | Group |",
      ),
      /Overnight oats → ingredients/,
    ],
    [
      "empty method",
      markdown.replace(
        /### Method\n[\s\S]*?### Notes/,
        "### Method\n\n### Notes",
      ),
      /Overnight oats → method/,
    ],
    [
      "missing description",
      markdown.replace(/Creamy oats prepared[^\n]+\n/, ""),
      /Overnight oats → description/,
    ],
    [
      "malformed YAML",
      markdown.replace(
        "tags: [make-ahead, no-cook, vegetarian]",
        "tags: [broken",
      ),
      /Overnight oats → metadata/,
    ],
  ];
  for (const [name, input, expected] of cases)
    await t.test(name, () =>
      assert.throws(() => parseRecipes(input), expected),
    );
});
