import { api, runScript } from "./setup.js";
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { Window } from "happy-dom";
const { parseRecipes } = api;
const { mondayKey, emptyWeek } = api;
const { PLAN_KEY } = api;

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const markdown = await readFile(
  new URL("../recipes.md", import.meta.url),
  "utf8",
);
const recipes = parseRecipes(markdown);
const settle = () => new Promise((resolve) => setTimeout(resolve, 20));

async function setup({ failFetch = false, savedPlan = null, fileMode = false } = {}) {
  const browser = new Window({
    url: fileMode ? 'file:///recipes/index.html' : "https://nikolaspanayotov-jpg.github.io/VibeProjects/top-recipes/",
    settings: {
      disableCSSFileLoading: true,
      disableJavaScriptFileLoading: true,
    },
  });
  browser.document.write(html);
  let fail = failFetch;
  if (savedPlan)
    browser.localStorage.setItem(PLAN_KEY, JSON.stringify(savedPlan));
  for (const [key, value] of Object.entries({
    window: browser,
    document: browser.document,
    navigator: browser.navigator,
    history: browser.history,
    requestAnimationFrame: (callback) => setTimeout(callback, 0),
    fetch: async () => {
      if (fail) throw new Error("Offline");
      return { ok: true, text: async () => markdown };
    },
  }))
    Object.defineProperty(globalThis, key, {
      value,
      configurable: true,
      writable: true,
    });
  await runScript("src/app.js");
  await settle();
  return {
    browser,
    $: (selector) => browser.document.querySelector(selector),
    all: (selector) => [...browser.document.querySelectorAll(selector)],
    recover: () => {
      fail = false;
    },
    input: (node, value) => {
      node.value = value;
      node.dispatchEvent(new browser.Event("input", { bubbles: true }));
    },
    submit: (form) =>
      form.dispatchEvent(
        new browser.Event("submit", { bubbles: true, cancelable: true }),
      ),
    close: () => browser.close(),
  };
}

test("the page supports a complete recipe-to-week workflow through DOM controls", async (t) => {
  const ui = await setup();
  const { $, all, browser, input, submit } = ui;
  const slot = (day, meal) =>
    $(`.slot[data-day="${day}"][data-meal="${meal}"]`);
  const textButton = (selector, text) =>
    all(selector).find((node) => node.textContent === text);
  const savedWeek = () =>
    JSON.parse(browser.localStorage.getItem(PLAN_KEY)).weeks[mondayKey()];
  try {
    await t.test("loads all recipe cards and exactly 21 empty slots", () => {
      assert.equal(all(".recipe-card").length, recipes.length);
      assert.equal(all(".slot").length, 21);
      assert.equal(all(".slot-empty").length, 21);
      assert.equal($("#clear-week").disabled, true);
    });

    await t.test(
      "searches ingredients, filters meals and recovers from empty results",
      () => {
        input($("#recipe-search"), "aubergine");
        assert.equal(all(".recipe-card").length, 1);
        assert.equal($(".recipe-title").textContent, "Moussaka");
        input($("#recipe-search"), "no-such-dish");
        assert.match($("#recipe-list").textContent, /No recipes found/);
        $("#recipe-list .text-button").click();
        assert.equal(all(".recipe-card").length, recipes.length);
        $('[data-filter="lunch"]').click();
        assert.equal($(".recipe-title").textContent, "Chicken and leek pie");
        assert.equal(
          $('[data-filter="lunch"]').getAttribute("aria-pressed"),
          "true",
        );
        $('[data-filter="all"]').click();
      },
    );

    await t.test(
      "opens ingredients, remembers checks and falls back when copying is unavailable",
      async () => {
        $(".recipe-title").click();
        assert.equal($("#recipe-dialog").open, true);
        assert.equal($("#detail-title").textContent, "Overnight oats");
        assert.match($(".detail-timings").textContent, /Wait 8 hr/);
        const check = $('[data-ingredient="rolled-oats"]');
        check.click();
        assert.equal(check.checked, true);
        $('[data-close="recipe-dialog"]').click();
        $(".recipe-title").click();
        assert.equal($('[data-ingredient="rolled-oats"]').checked, true);
        Object.defineProperty(browser.navigator, "clipboard", {
          value: undefined,
          configurable: true,
        });
        textButton(".detail-actions button", "Copy ingredients").click();
        await settle();
        assert.equal($(".copy-fallback").hidden, false);
        assert.match(
          $(".copy-fallback textarea").value,
          /\[x\] 40 g Rolled oats/,
        );
        $('[data-close="recipe-dialog"]').click();
      },
    );

    await t.test(
      "adds by recipe button and by tapping a slot, then saves independently by week",
      async () => {
        $(".add-recipe").click();
        assert.equal($("#picker-dialog").open, true);
        assert.equal($('.picker-form select[name="meal"]').value, "breakfast");
        submit($(".picker-form"));
        await settle();
        assert.equal(
          slot("monday", "breakfast").querySelector(".planned-title")
            .textContent,
          "Overnight oats",
        );
        slot("monday", "lunch").querySelector(".slot-empty").click();
        all(".picker-recipe")
          .find((node) => node.textContent.includes("Chicken and leek pie"))
          .click();
        await settle();
        assert.equal(savedWeek().monday.lunch, "chicken-and-leek-pie");
        $("#next-week").click();
        assert.equal(all(".slot-empty").length, 21);
        $("#previous-week").click();
        assert.equal(all(".slot.filled").length, 2);
      },
    );

    await t.test(
      "moves into an occupied slot by swapping, then supports undo, removal and clearing",
      async () => {
        slot("monday", "breakfast").querySelector(".slot-more").click();
        textButton(".meal-actions button", "Move to another slot").click();
        $('.picker-form select[name="meal"]').value = "lunch";
        submit($(".picker-form"));
        await settle();
        assert.equal(savedWeek().monday.breakfast, "chicken-and-leek-pie");
        assert.equal(savedWeek().monday.lunch, "overnight-oats");
        $("#undo").click();
        assert.equal(savedWeek().monday.breakfast, "overnight-oats");
        slot("monday", "lunch").querySelector(".slot-more").click();
        textButton(".meal-actions button", "Remove meal").click();
        await settle();
        assert.equal(savedWeek().monday.lunch, null);
        $("#undo").click();
        assert.equal(savedWeek().monday.lunch, "chicken-and-leek-pie");
        $("#clear-week").click();
        assert.equal(all(".slot-empty").length, 21);
        $("#dismiss-toast").click();
        assert.equal($("#undo-inline").hidden, false);
        $("#undo-inline").click();
        assert.equal(all(".slot.filled").length, 2);
      },
    );

    await t.test(
      "supports library drag-copy, grid drag-swap and Escape cancellation",
      async () => {
        const transfer = { setData() {}, effectAllowed: "", dropEffect: "" };
        const drag = (node, type) => {
          const event = new browser.Event(type, {
            bubbles: true,
            cancelable: true,
          });
          Object.defineProperty(event, "dataTransfer", { value: transfer });
          node.dispatchEvent(event);
          return event;
        };
        const libraryHandle = all(".recipe-card .drag-handle")[2];
        drag(libraryHandle, "dragstart");
        assert.equal(
          drag(slot("tuesday", "dinner"), "dragover").defaultPrevented,
          true,
        );
        drag(slot("tuesday", "dinner"), "drop");
        await settle();
        assert.equal(savedWeek().tuesday.dinner, "moussaka");
        assert.equal(all(".recipe-card").length, recipes.length);
        drag(
          slot("tuesday", "dinner").querySelector(".drag-handle"),
          "dragstart",
        );
        drag(slot("monday", "breakfast"), "drop");
        await settle();
        assert.equal(savedWeek().monday.breakfast, "moussaka");
        assert.equal(savedWeek().tuesday.dinner, "overnight-oats");
        const before = JSON.stringify(savedWeek());
        drag(libraryHandle, "dragstart");
        browser.document.dispatchEvent(
          new browser.KeyboardEvent("keydown", {
            key: "Escape",
            bubbles: true,
          }),
        );
        drag(slot("friday", "lunch"), "drop");
        assert.equal(JSON.stringify(savedWeek()), before);
      },
    );

    await t.test(
      "shows a complete capture plan and restores controls after hiding them",
      async () => {
        $("#screenshot-open").click();
        assert.equal($("#capture-dialog").open, true);
        assert.equal(all(".capture-row").length, 8);
        assert.equal(all('.capture-cell[role="cell"]').length, 21);
        assert.match($("#capture-grid").textContent, /Chicken and leek pie/);
        assert.equal($("#capture-sheet").querySelector("button"), null);
        $("#capture-sheet").click();
        assert.equal(
          $("#capture-dialog").classList.contains("controls-hidden"),
          true,
        );
        const cancel = new browser.Event("cancel", { cancelable: true });
        $("#capture-dialog").dispatchEvent(cancel);
        await settle();
        assert.equal(
          $("#capture-dialog").classList.contains("controls-hidden"),
          false,
        );
        $("#capture-close").click();
        await settle();
        assert.equal($("#capture-dialog").open, false);
        assert.equal(all(".slot.filled").length, 3);
        browser.dispatchEvent(new browser.Event("beforeprint"));
        assert.equal(all('.capture-cell[role="cell"]').length, 21);
      },
    );

    await t.test(
      "recipe rendering treats authored titles as text",
      async () => {
        const { createRecipeViews } = api;
        const views = createRecipeViews({
          persistence: {},
          openPlacement() {},
          makeDraggable() {},
          notify() {},
          storageChanged() {},
        });
        const maliciousTitle = "<img src=x onerror=alert(1)>";
        const card = views.card({ ...recipes[0], title: maliciousTitle });
        assert.equal(
          card.querySelector(".recipe-title").textContent,
          maliciousTitle,
        );
        assert.equal(card.querySelectorAll("img").length, 1);
      },
    );
  } finally {
    await settle();
    ui.close();
  }
});

test("a failed recipe request can retry without losing a previously saved meal", async () => {
  const week = emptyWeek();
  week.sunday.dinner = "moussaka";
  const ui = await setup({
    failFetch: true,
    savedPlan: { schemaVersion: 1, weeks: { [mondayKey()]: week } },
  });
  try {
    assert.match(ui.$("#recipe-list").textContent, /could not be opened/);
    assert.equal(ui.all(".slot.filled").length, 1);
    ui.recover();
    ui.$("#recipe-list .text-button").click();
    await settle();
    assert.equal(ui.all(".recipe-card").length, recipes.length);
    assert.equal(
      ui.$('.slot[data-day="sunday"][data-meal="dinner"] .planned-title')
        .textContent,
      "Moussaka",
    );
  } finally {
    await settle();
    ui.close();
  }
});

test('opening from disk can load the Markdown collection through the local file picker', async () => {
  const ui = await setup({ failFetch: true, fileMode: true });
  try {
    assert.match(ui.$('#recipe-list').textContent, /Choose your recipes.md/);
    const transfer = new ui.browser.DataTransfer();
    transfer.items.add(new ui.browser.File([markdown], 'recipes.md', { type: 'text/markdown' }));
    const input = ui.$('#recipe-list input[type="file"]');
    input.files = transfer.files;
    input.dispatchEvent(new ui.browser.Event('change', { bubbles: true }));
    await settle();
    assert.equal(ui.all('.recipe-card').length, recipes.length);
    assert.equal(ui.all('.slot').length, 21);
  } finally { await settle(); ui.close(); }
});
