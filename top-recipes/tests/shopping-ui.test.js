import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { Window } from "happy-dom";
import { api, runScript } from "./setup.js";

const { emptyWeek, mondayKey, PLAN_KEY } = api;
const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const markdown = await readFile(
  new URL("../recipes.md", import.meta.url),
  "utf8",
);
const settle = () => new Promise((resolve) => setTimeout(resolve, 20));

async function setup(plan) {
  const browser = new Window({
    url: "https://nikolaspanayotov-jpg.github.io/VibeProjects/top-recipes/",
    settings: {
      disableCSSFileLoading: true,
      disableJavaScriptFileLoading: true,
    },
  });
  browser.innerHeight = 667;
  browser.document.write(html);
  if (plan) browser.localStorage.setItem(PLAN_KEY, plan);
  for (const [key, value] of Object.entries({
    window: browser,
    document: browser.document,
    navigator: browser.navigator,
    history: browser.history,
    requestAnimationFrame: (callback) => setTimeout(callback, 0),
    fetch: async () => ({ ok: true, text: async () => markdown }),
  })) {
    Object.defineProperty(globalThis, key, {
      value,
      writable: true,
      configurable: true,
    });
  }
  await runScript("src/app.js");
  await settle();
  return {
    browser,
    $: (selector) => browser.document.querySelector(selector),
    all: (selector) => [...browser.document.querySelectorAll(selector)],
  };
}

test("shopping list supports selection, quantities, screenshot pages and reload without changing meals", async (t) => {
  const week = emptyWeek();
  week.monday.breakfast = "overnight-oats";
  week.tuesday.breakfast = "overnight-oats";
  week.wednesday.breakfast = "pancakes";
  const ui = await setup(
    JSON.stringify({ schemaVersion: 1, weeks: { [mondayKey()]: week } }),
  );
  const { $, all, browser } = ui;
  const row = (key) =>
    all(".shopping-item").find((node) => node.dataset.shoppingKey === key);
  let persisted;
  try {
    await t.test(
      "opens from the planner and combines ingredients from all planned meals",
      () => {
        assert.equal($("#weekly-plan #shopping-open").disabled, false);
        $("#shopping-open").click();
        assert.equal($("#shopping-dialog").open, true);
        assert.equal(
          row("milk|ml").querySelector('input[type="number"]').value,
          "450",
        );
        assert.match($("#shopping-summary").textContent, /3 planned meals/);
        assert.equal(all(".slot.filled").length, 3);
      },
    );
    await t.test(
      "plus, minus, typed amounts and item selection update the saved list",
      () => {
        const milk = row("milk|ml");
        const quantity = milk.querySelector('input[type="number"]');
        milk.querySelector('[aria-label="Increase Milk quantity"]').click();
        assert.equal(quantity.value, "500");
        milk.querySelector('[aria-label="Decrease Milk quantity"]').click();
        assert.equal(quantity.value, "450");
        quantity.value = "600";
        quantity.dispatchEvent(new browser.Event("change", { bubbles: true }));
        row("berries|g").querySelector('input[type="checkbox"]').click();
        assert.equal(row("berries|g").classList.contains("excluded"), true);
        const saved = JSON.parse(browser.localStorage.getItem(PLAN_KEY));
        assert.equal(saved.shoppingWeeks[mondayKey()]["milk|ml"].quantity, 600);
        assert.equal(
          saved.shoppingWeeks[mondayKey()]["berries|g"].selected,
          false,
        );
        assert.deepEqual(saved.weeks[mondayKey()], week);
      },
    );
    await t.test(
      "screenshot pages contain selected items and quantities with controls hidden",
      async () => {
        const expected = all(".shopping-item")
          .filter(
            (node) => node.querySelector('input[type="checkbox"]').checked,
          )
          .map((node) => node.dataset.shoppingKey);
        $("#shopping-screenshot").click();
        assert.equal($("#capture-dialog").open, true);
        assert.equal($("#shopping-dialog").open, true);
        assert.equal($("#capture-grid").hidden, true);
        assert.match($("#capture-title").textContent, /shopping/);
        assert.ok(
          $("#capture-dates").textContent.includes(
            String(api.parseLocalDate(mondayKey()).getFullYear()),
          ),
        );
        assert.equal(
          $("#capture-shopping").querySelector("button,input"),
          null,
        );
        const found = [];
        while (true) {
          found.push(
            ...all(".shopping-capture-row").map(
              (node) => node.dataset.shoppingKey,
            ),
          );
          assert.ok(all(".shopping-capture-row").length <= 8);
          if ($("#capture-next-page").disabled) break;
          $("#capture-next-page").click();
        }
        assert.deepEqual(found.sort(), expected.sort());
        assert.equal(found.includes("berries|g"), false);
        $("#capture-previous-page").click();
        assert.match($("#capture-shopping").textContent, /600 ml/);
        $("#capture-hide").click();
        assert.equal(
          $("#capture-dialog").classList.contains("controls-hidden"),
          true,
        );
        $("#capture-dialog").dispatchEvent(
          new browser.Event("cancel", { cancelable: true }),
        );
        await settle();
        assert.equal(
          $("#capture-dialog").classList.contains("controls-hidden"),
          false,
        );
        browser.dispatchEvent(new browser.Event("beforeprint"));
        assert.equal(all(".shopping-capture-row").length, expected.length);
        browser.dispatchEvent(new browser.Event("afterprint"));
        assert.ok(all(".shopping-capture-row").length <= 8);
        $("#capture-close").click();
        await settle();
        assert.equal($("#capture-dialog").open, false);
        assert.equal($("#shopping-dialog").open, true);
        assert.equal(
          row("milk|ml").querySelector('input[type="number"]').value,
          "600",
        );
      },
    );
    await t.test(
      "unticking everything disables screenshots, then selection can be restored",
      () => {
        $("#shopping-clear-selection").click();
        assert.equal($("#shopping-screenshot").disabled, true);
        $("#shopping-select-all").click();
        assert.equal($("#shopping-screenshot").disabled, false);
        row("berries|g").querySelector('input[type="checkbox"]').click();
        persisted = browser.localStorage.getItem(PLAN_KEY);
      },
    );
  } finally {
    await settle();
    browser.close();
  }

  const reloaded = await setup(persisted);
  try {
    reloaded.$("#shopping-open").click();
    const milk = reloaded
      .all(".shopping-item")
      .find((node) => node.dataset.shoppingKey === "milk|ml");
    assert.equal(milk.querySelector('input[type="number"]').value, "600");
    assert.equal(
      reloaded
        .all(".shopping-item")
        .find((node) => node.dataset.shoppingKey === "berries|g")
        .querySelector("input").checked,
      false,
    );
    reloaded.$("#shopping-reset").click();
    assert.equal(
      reloaded
        .all(".shopping-item")
        .find((node) => node.dataset.shoppingKey === "milk|ml")
        .querySelector('input[type="number"]').value,
      "450",
    );
    reloaded.$('[data-close="shopping-dialog"]').click();
    reloaded.$("#next-week").click();
    reloaded.$("#shopping-open").click();
    assert.equal(reloaded.all(".shopping-item").length, 0);
    assert.equal(reloaded.$("#shopping-screenshot").disabled, true);
    assert.match(reloaded.$("#shopping-items").textContent, /Plan a few meals/);
  } finally {
    await settle();
    reloaded.browser.close();
  }
});
