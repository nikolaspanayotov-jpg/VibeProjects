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

async function setup({ width = 390, hash = "" } = {}) {
  const browser = new Window({
    url: `https://nikolaspanayotov-jpg.github.io/VibeProjects/top-recipes/${hash}`,
    settings: {
      disableCSSFileLoading: true,
      disableJavaScriptFileLoading: true,
    },
  });
  browser.innerWidth = width;
  browser.document.write(html);
  const week = api.emptyWeek();
  week.sunday.dinner = "wine-kebab";
  const saved = JSON.stringify({
    schemaVersion: 1,
    weeks: { [api.mondayKey()]: week },
    shoppingWeeks: {
      [api.mondayKey()]: {
        "milk|ml": { baseline: 250, quantity: 300, selected: false },
      },
    },
  });
  browser.localStorage.setItem(api.PLAN_KEY, saved);
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
      configurable: true,
      writable: true,
    });
  }
  await runScript("src/app.js");
  await settle();
  return {
    browser,
    saved,
    $: (selector) => browser.document.querySelector(selector),
    all: (selector) => [...browser.document.querySelectorAll(selector)],
  };
}

test("mobile starts with the whole recipe collection collapsed and the planner available", async () => {
  const ui = await setup();
  try {
    assert.equal(ui.$("#recipes-content").hidden, true);
    assert.equal(
      ui.$("#recipes-toggle").getAttribute("aria-expanded"),
      "false",
    );
    assert.equal(
      ui.$("#recipes-toggle").getAttribute("aria-controls"),
      "recipes-content",
    );
    assert.equal(ui.$("#recipes-toggle-label").textContent, "Show recipes");
    assert.equal(
      ui.$("#recipe-count").textContent,
      `${recipes.length} recipes`,
    );
    assert.equal(ui.all(".slot").length, 21);
    assert.equal(ui.$("#shopping-open").disabled, false);
    assert.equal(
      ui.$(".workspace").classList.contains("recipes-collapsed"),
      true,
    );
    assert.equal(ui.browser.localStorage.getItem(api.PLAN_KEY), ui.saved);
  } finally {
    await settle();
    ui.browser.close();
  }
});

test("show/hide preserves searching, recipe details, saved meals and shopping edits", async () => {
  const ui = await setup();
  const { $, browser } = ui;
  try {
    $("#recipes-toggle").click();
    assert.equal($("#recipes-content").hidden, false);
    assert.equal($("#recipes-toggle").getAttribute("aria-expanded"), "true");
    const search = $("#recipe-search");
    search.value = "salmon";
    search.dispatchEvent(new browser.Event("input", { bubbles: true }));
    assert.equal(ui.all(".recipe-card").length, 1);
    assert.equal($("#recipe-count").textContent, `${recipes.length} recipes`);
    assert.equal(
      $("#recipe-results").textContent,
      `1 of ${recipes.length} recipes`,
    );
    $(".recipe-title").click();
    assert.equal($("#recipe-dialog").open, true);
    assert.equal($("#detail-title").textContent, "Salmon");
    $('[data-close="recipe-dialog"]').click();
    search.focus();
    $("#recipes-toggle").click();
    assert.equal(browser.document.activeElement, $("#recipes-toggle"));
    assert.equal($("#recipes-content").hidden, true);
    $("#recipes-toggle").click();
    assert.equal($("#recipe-search").value, "salmon");
    assert.equal($(".recipe-title").textContent, "Salmon");
    assert.equal(browser.localStorage.getItem(api.PLAN_KEY), ui.saved);
  } finally {
    await settle();
    browser.close();
  }
});

test("the bottom close control returns focus and scroll to the weekly planner", async () => {
  const ui = await setup();
  try {
    const scrolls = [];
    ui.$("#weekly-plan").scrollIntoView = (options) => scrolls.push(options);
    ui.$("#recipes-toggle").click();
    ui.$("#recipes-close").focus();
    ui.$("#recipes-close").click();
    await settle();
    assert.equal(ui.$("#recipes-content").hidden, true);
    assert.equal(ui.browser.document.activeElement, ui.$("#planner-heading"));
    assert.equal(scrolls.length, 1);
    assert.equal(scrolls[0].block, "start");
  } finally {
    await settle();
    ui.browser.close();
  }
});

test("mobile navigation opens recipes and collapses them when returning to the plan", async () => {
  const ui = await setup();
  try {
    ui.$("#recipes-nav-link").click();
    await settle();
    assert.equal(ui.$("#recipes-content").hidden, false);
    ui.$("#planner-nav-link").click();
    await settle();
    assert.equal(ui.$("#recipes-content").hidden, true);
    ui.$("#recipes-nav-link").click();
    await settle();
    assert.equal(ui.$("#recipes-content").hidden, false);
  } finally {
    await settle();
    ui.browser.close();
  }
});

test("a direct recipes link opens the collection on mobile", async () => {
  const ui = await setup({ hash: "#recipes" });
  try {
    assert.equal(ui.$("#recipes-content").hidden, false);
    assert.equal(ui.$("#recipes-toggle").getAttribute("aria-expanded"), "true");
  } finally {
    await settle();
    ui.browser.close();
  }
});

test("desktop defaults open, adapts before interaction and preserves an explicit collapse across resizes", async () => {
  const ui = await setup({ width: 1200 });
  const { $, browser } = ui;
  try {
    assert.equal($("#recipes-content").hidden, false);
    browser.innerWidth = 390;
    browser.dispatchEvent(new browser.Event("resize"));
    assert.equal($("#recipes-content").hidden, true);
    browser.innerWidth = 1200;
    browser.dispatchEvent(new browser.Event("resize"));
    assert.equal($("#recipes-content").hidden, false);
    $("#recipes-toggle").click();
    assert.equal($(".workspace").classList.contains("recipes-collapsed"), true);
    browser.innerWidth = 390;
    browser.dispatchEvent(new browser.Event("resize"));
    browser.innerWidth = 1200;
    browser.dispatchEvent(new browser.Event("resize"));
    assert.equal($("#recipes-content").hidden, true);
    $("#recipes-toggle").click();
    $("#planner-nav-link").click();
    await settle();
    assert.equal($("#recipes-content").hidden, false);
  } finally {
    await settle();
    browser.close();
  }
});
