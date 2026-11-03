import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { Window } from "happy-dom";
import { api, runScript } from "./setup.js";

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const markdown = await readFile(
  new URL("../recipes.md", import.meta.url),
  "utf8",
);
const recipes = api.parseRecipes(markdown);
const settle = () => new Promise((resolve) => setTimeout(resolve, 20));
async function setup(saved) {
  const browser = new Window({
    url: "https://nikolaspanayotov-jpg.github.io/VibeProjects/top-recipes/",
    settings: {
      disableCSSFileLoading: true,
      disableJavaScriptFileLoading: true,
    },
  });
  browser.innerWidth = 390;
  browser.innerHeight = 667;
  browser.document.write(html);
  if (saved)
    browser.localStorage.setItem(
      api.PLAN_KEY,
      typeof saved === "string" ? saved : JSON.stringify(saved),
    );
  for (const [key, value] of Object.entries({
    window: browser,
    document: browser.document,
    navigator: browser.navigator,
    history: browser.history,
    requestAnimationFrame: (callback) => setTimeout(callback, 0),
    fetch: async () => ({ ok: true, text: async () => markdown }),
  }))
    Object.defineProperty(globalThis, key, {
      value,
      writable: true,
      configurable: true,
    });
  await runScript("src/app.js");
  await settle();
  const $ = (selector) => browser.document.querySelector(selector);
  const all = (selector) => [...browser.document.querySelectorAll(selector)];
  return {
    browser,
    $,
    all,
    change(node, value, event = "change") {
      node.value = value;
      node.dispatchEvent(new browser.Event(event, { bubbles: true }));
    },
    submit(form) {
      form.dispatchEvent(
        new browser.Event("submit", { bubbles: true, cancelable: true }),
      );
    },
    saved: () => JSON.parse(browser.localStorage.getItem(api.PLAN_KEY)),
    chooseText(text) {
      const control = all("#picker-content button").find(
        (node) => node.textContent === text,
      );
      assert.ok(control, text);
      control.click();
    },
    slot: (day, meal) => $(`.slot[data-day="${day}"][data-meal="${meal}"]`),
    async close() {
      await settle();
      browser.close();
    },
  };
}

test("mobile navigation, suitable recipes, pins, search and recently used meals work together and reload", async () => {
  const ui = await setup();
  let saved;
  try {
    ui.$("#mobile-recipes").click();
    assert.equal(ui.$("#recipes-content").hidden, false);
    assert.equal(ui.$("#mobile-recipes").getAttribute("aria-current"), "page");
    ui.$('[data-favourite="pancakes"]').click();
    assert.equal(
      ui.$('[data-favourite="pancakes"]').getAttribute("aria-pressed"),
      "true",
    );
    ui.$("#mobile-plan").click();
    assert.equal(ui.$("#recipes-content").hidden, true);
    ui.slot("monday", "breakfast").querySelector("button").click();
    assert.ok(ui.$('[aria-label="Choose Pancakes for Monday breakfast"]'));
    assert.equal(
      ui.$('[aria-label="Choose Lasagna for Monday breakfast"]'),
      null,
    );
    ui.$('[data-shortcut="favourites"]').click();
    assert.equal(ui.all(".picker-recipe").length, 1);
    ui.$(".picker-recipe").click();
    assert.equal(
      ui.saved().weeks[api.mondayKey()].monday.breakfast,
      "pancakes",
    );
    ui.slot("tuesday", "breakfast").querySelector("button").click();
    ui.$('[data-shortcut="recent"]').click();
    assert.equal(ui.all(".picker-recipe").length, 1);
    assert.match(ui.$(".picker-recipe").textContent, /Pancakes/);
    ui.$('[data-shortcut="suggested"]').click();
    ui.change(ui.$('#picker-content input[type="search"]'), "salmon", "input");
    assert.ok(ui.$('[aria-label="Choose Salmon for Tuesday breakfast"]'));
    ui.$('[data-close="picker-dialog"]').click();
    ui.$("#mobile-shopping").click();
    assert.equal(ui.$("#shopping-dialog").open, true);
    assert.equal(ui.$("#mobile-shopping").getAttribute("aria-current"), "page");
    ui.$('[data-close="shopping-dialog"]').click();
    assert.equal(ui.$("#mobile-plan").getAttribute("aria-current"), "page");
    saved = ui.saved();
  } finally {
    await ui.close();
  }
  const reloaded = await setup(saved);
  try {
    assert.equal(
      reloaded.$('[data-favourite="pancakes"]').getAttribute("aria-pressed"),
      "true",
    );
    reloaded.slot("tuesday", "breakfast").querySelector("button").click();
    reloaded.$('[data-shortcut="recent"]').click();
    assert.match(reloaded.$(".picker-recipe").textContent, /Pancakes/);
  } finally {
    await reloaded.close();
  }
});

test("copying weeks and applying templates include settings, support Undo and leave shopping edits untouched", async () => {
  const key = api.mondayKey();
  const previous = api.emptyWeek();
  previous.monday.dinner = previous.wednesday.lunch = "moussaka";
  const current = api.emptyWeek();
  current.monday.breakfast = "pancakes";
  const settings = {
    "monday-dinner": { servings: 2 },
    "wednesday-lunch": { servings: 2, leftoverOf: "monday-dinner" },
  };
  const shoppingEdits = {
    "milk|ml": { baseline: 250, quantity: 300, selected: false },
  };
  const ui = await setup({
    schemaVersion: 1,
    weeks: { [key]: current, [api.weekOffset(key, -1)]: previous },
    mealSettings: { [api.weekOffset(key, -1)]: settings },
    shoppingWeeks: { [key]: shoppingEdits },
  });
  let saved;
  try {
    ui.$("#copy-last-week").click();
    assert.deepEqual(ui.saved().weeks[key], previous);
    assert.deepEqual(ui.saved().mealSettings[key], settings);
    ui.$("#undo-inline").click();
    assert.deepEqual(ui.saved().weeks[key], current);
    assert.deepEqual(ui.saved().mealSettings[key], {});
    ui.$("#copy-last-week").click();
    ui.$("#templates-open").click();
    ui.change(ui.$('[name="template-name"]'), "Family favourites", "input");
    ui.submit(ui.$(".template-form"));
    assert.equal(ui.saved().templates[0].title, "Family favourites");
    ui.$('[data-close="picker-dialog"]').click();
    ui.$("#next-week").click();
    ui.$("#templates-open").click();
    ui.chooseText("Use week");
    const next = api.weekOffset(key, 1);
    assert.deepEqual(ui.saved().weeks[next], previous);
    assert.deepEqual(ui.saved().mealSettings[next], settings);
    ui.$("#undo-inline").click();
    assert.deepEqual(ui.saved().weeks[next], api.emptyWeek());
    assert.deepEqual(ui.saved().shoppingWeeks[key], shoppingEdits);
    saved = ui.saved();
  } finally {
    await ui.close();
  }
  const reloaded = await setup(saved);
  try {
    reloaded.$("#templates-open").click();
    assert.match(reloaded.$(".template-list").textContent, /Family favourites/);
    reloaded.chooseText("Delete");
    assert.deepEqual(reloaded.saved().templates, []);
  } finally {
    await reloaded.close();
  }
});

test("household servings, individual portions and leftovers change shopping totals and appear in captures", async () => {
  const key = api.mondayKey();
  const week = api.emptyWeek();
  week.monday.dinner = week.wednesday.lunch = "moussaka";
  const ui = await setup({ schemaVersion: 1, weeks: { [key]: week } });
  try {
    ui.change(ui.$("#household-size"), "2");
    assert.equal(ui.saved().preferences.householdSize, 2);
    assert.match(ui.slot("monday", "dinner").textContent, /2 servings/);
    ui.slot("wednesday", "lunch").querySelector(".slot-more").click();
    ui.chooseText("Portions & leftovers");
    assert.ok(ui.$('[name="leftover-source"] option[value="monday-dinner"]'));
    ui.$('[name="use-default"]').click();
    ui.change(ui.$('[name="servings"]'), "1");
    ui.change(ui.$('[name="leftover-source"]'), "monday-dinner");
    assert.match(ui.$(".portion-help").textContent, /3 servings.*2 meals/);
    ui.submit(ui.$(".portion-form"));
    assert.deepEqual(ui.saved().mealSettings[key]["wednesday-lunch"], {
      servings: 1,
      leftoverOf: "monday-dinner",
    });
    assert.match(
      ui.slot("wednesday", "lunch").textContent,
      /Leftovers · 1 serving/,
    );
    ui.$("#shopping-open").click();
    const getRecipe = (id) => recipes.find((recipe) => recipe.id === id);
    const expected = api.buildShoppingList(week, getRecipe, {
      householdSize: 2,
      mealSettings: ui.saved().mealSettings[key],
    });
    const meat = expected.items.find((item) => item.unit === "g");
    const row = ui
      .all(".shopping-item")
      .find((node) => node.dataset.shoppingKey === meat.key);
    assert.equal(
      Number(row.querySelector('[type="number"]').value),
      meat.quantity,
    );
    ui.$('[data-close="shopping-dialog"]').click();
    ui.$("#screenshot-open").click();
    assert.match(ui.$("#capture-grid").textContent, /Leftovers · 1 serving/);
    ui.$("#capture-close").click();
    await settle();
    ui.$("#undo-inline").click();
    assert.deepEqual(ui.saved().mealSettings[key], {});
    assert.doesNotMatch(ui.slot("wednesday", "lunch").textContent, /Leftovers/);
  } finally {
    await ui.close();
  }
});

test("shopping mode has independent Bought marks, aisle headings, hide-bought controls and saved screenshot checks", async () => {
  const key = api.mondayKey();
  const week = api.emptyWeek();
  week.monday.breakfast = "pancakes";
  const ui = await setup({ schemaVersion: 1, weeks: { [key]: week } });
  let saved;
  try {
    ui.$("#shopping-open").click();
    assert.ok(ui.all(".shopping-aisle h3").length >= 2);
    const berries = ui
      .all(".shopping-item")
      .find((node) => node.dataset.shoppingKey === "berries|g");
    berries.querySelector(".shopping-check input").click();
    ui.$("#shopping-mode").click();
    assert.equal(ui.$("#shopping-bulk-actions").hidden, true);
    assert.equal(
      ui
        .all(".shopping-item")
        .find((node) => node.dataset.shoppingKey === "berries|g").hidden,
      true,
    );
    const freshMilk = ui
      .all(".shopping-item")
      .find((node) => node.dataset.shoppingKey === "milk|ml");
    freshMilk.querySelector(".shopping-bought-check input").click();
    assert.equal(ui.saved().shoppingWeeks[key]["milk|ml"].bought, true);
    assert.equal(ui.saved().shoppingWeeks[key]["milk|ml"].selected, true);
    assert.match(ui.$("#shopping-summary").textContent, /1 of .* bought/);
    ui.$("#shopping-hide-bought").click();
    assert.equal(
      ui
        .all(".shopping-item")
        .find((node) => node.dataset.shoppingKey === "milk|ml").hidden,
      true,
    );
    ui.$("#shopping-screenshot").click();
    ui.browser.dispatchEvent(new ui.browser.Event("beforeprint"));
    assert.ok(ui.all(".shopping-capture-aisle").length >= 2);
    const capturedMilk = ui
      .all(".shopping-capture-row")
      .find((node) => node.dataset.shoppingKey === "milk|ml");
    assert.equal(
      capturedMilk.querySelector(".shopping-capture-box").textContent,
      "☑",
    );
    assert.equal(
      ui
        .all(".shopping-capture-row")
        .some((node) => node.dataset.shoppingKey === "berries|g"),
      false,
    );
    ui.browser.dispatchEvent(new ui.browser.Event("afterprint"));
    ui.$("#capture-close").click();
    await settle();
    saved = ui.saved();
  } finally {
    await ui.close();
  }
  const reloaded = await setup(saved);
  try {
    reloaded.$("#shopping-open").click();
    assert.equal(reloaded.$('[aria-label="Bought Milk"]').checked, true);
    reloaded.$("#shopping-mode").click();
    reloaded.$("#shopping-unbuy-all").click();
    assert.equal(reloaded.$('[aria-label="Bought Milk"]').checked, false);
    assert.equal(
      reloaded.saved().shoppingWeeks[key]["berries|g"].selected,
      false,
    );
  } finally {
    await reloaded.close();
  }
});
