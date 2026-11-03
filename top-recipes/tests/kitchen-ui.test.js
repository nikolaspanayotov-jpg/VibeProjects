import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { Window } from "happy-dom";
import { api, runScript } from "./setup.js";
import { imageCanvas } from "./image-canvas.js";

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const markdown = await readFile(
  new URL("../recipes.md", import.meta.url),
  "utf8",
);
const recipes = api.parseRecipes(markdown);
const settle = () => new Promise((resolve) => setTimeout(resolve, 25));

async function setup({
  saved,
  nativeCanvas = false,
  share = null,
  canShare = true,
} = {}) {
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
  if (saved) browser.localStorage.setItem(api.PLAN_KEY, JSON.stringify(saved));
  const downloads = [];
  browser.document.addEventListener("click", (event) => {
    const link = event.target.closest?.("a[download]");
    if (!link) return;
    event.preventDefault();
    downloads.push({ href: link.href, name: link.download });
  });
  if (nativeCanvas) {
    const create = browser.document.createElement.bind(browser.document);
    browser.document.createElement = (name, ...args) =>
      name.toLowerCase() === "canvas" ? imageCanvas() : create(name, ...args);
  }
  if (share) {
    Object.defineProperty(browser.navigator, "share", {
      value: share,
      configurable: true,
    });
    Object.defineProperty(browser.navigator, "canShare", {
      value: () => canShare,
      configurable: true,
    });
  }
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
    downloads,
    saved: () => JSON.parse(browser.localStorage.getItem(api.PLAN_KEY)),
    change(node, value, event = "change") {
      node.value = value;
      node.dispatchEvent(new browser.Event(event, { bubbles: true }));
    },
    submit(form) {
      form.dispatchEvent(
        new browser.Event("submit", { bubbles: true, cancelable: true }),
      );
    },
    row(key) {
      return all(".shopping-item").find(
        (node) => node.dataset.shoppingKey === key,
      );
    },
    async ready() {
      for (let i = 0; i < 50 && $("#capture-save").disabled; i++)
        await settle();
      assert.equal(
        $("#capture-save").disabled,
        false,
        $("#capture-export-status").textContent,
      );
    },
    async close() {
      if ($("#cook-dialog").open) $("#cook-dialog").close();
      if ($("#capture-dialog").open) $("#capture-close").click();
      await settle();
      await browser.happyDOM.abort();
      browser.close();
    },
  };
}

test("extra groceries can be added without a plan, edited, checked, captured, removed, undone and reloaded", async () => {
  const key = api.mondayKey();
  const ui = await setup({ saved: { schemaVersion: 1, weeks: {} } });
  let saved;
  try {
    ui.$("#shopping-open").click();
    ui.$("#shopping-extra").open = true;
    ui.change(ui.$('[name="extra-name"]'), "Coffee");
    ui.change(ui.$('[name="extra-quantity"]'), "2");
    ui.change(ui.$('[name="extra-unit"]'), "pack");
    ui.submit(ui.$("#shopping-extra-form"));
    assert.match(ui.$("#shopping-extra-status").textContent, /Coffee added/);
    const item = ui.saved().customShoppingWeeks[key][0];
    assert.equal(item.quantity, 2);
    assert.equal(item.aisle, "Cupboard & other");
    const rowKey = `extra:${item.id}|pack`;
    assert.equal(
      ui.row(rowKey).querySelector(".shopping-extra-label").textContent,
      "Extra item",
    );
    ui.row(rowKey)
      .querySelector('[aria-label="Increase Coffee quantity"]')
      .click();
    assert.equal(ui.saved().customShoppingWeeks[key][0].quantity, 3);
    ui.row(rowKey)
      .querySelector('[aria-label="Edit extra item Coffee"]')
      .click();
    ui.change(ui.$('[name="extra-name"]'), "Ground coffee");
    ui.change(ui.$('[name="extra-aisle"]'), "Cupboard & other");
    ui.submit(ui.$("#shopping-extra-form"));
    ui.$("#shopping-mode").click();
    ui.row(rowKey).querySelector(".shopping-bought-check input").click();
    assert.equal(ui.saved().customShoppingWeeks[key][0].bought, true);
    ui.$("#shopping-screenshot").click();
    assert.match(ui.$("#capture-shopping").textContent, /Ground coffee/);
    assert.match(ui.$("#capture-shopping").textContent, /3 packs/);
    assert.equal(ui.$(".shopping-capture-box").textContent, "☑");
    ui.$("#capture-close").click();
    await settle();
    ui.$("#shopping-mode").click();
    ui.row(rowKey)
      .querySelector('[aria-label="Remove extra item Ground coffee"]')
      .click();
    assert.deepEqual(ui.saved().customShoppingWeeks[key], []);
    ui.$("#shopping-extra-undo").click();
    assert.equal(ui.saved().customShoppingWeeks[key][0].name, "Ground coffee");
    ui.$("#shopping-reset").click();
    assert.equal(ui.saved().customShoppingWeeks[key][0].bought, false);
    assert.equal(ui.saved().customShoppingWeeks[key][0].quantity, 3);
    assert.deepEqual(ui.saved().weeks, {});
    saved = ui.saved();
    ui.$('[data-close="shopping-dialog"]').click();
    ui.$("#next-week").click();
    ui.$("#shopping-open").click();
    assert.equal(ui.all(".custom-item").length, 0);
    assert.equal(ui.$("#shopping-extra-undo").hidden, true);
  } finally {
    await ui.close();
  }
  const reloaded = await setup({ saved });
  try {
    reloaded.$("#shopping-open").click();
    assert.equal(reloaded.all(".custom-item").length, 1);
    assert.match(reloaded.$("#shopping-items").textContent, /Ground coffee/);
  } finally {
    await reloaded.close();
  }
});

test("extra groceries keep their amounts when recipe portions change and their text is rendered safely", async () => {
  const key = api.mondayKey();
  const week = api.emptyWeek();
  week.monday.breakfast = "pancakes";
  const name = '<img src=x onerror="alert(1)">';
  const ui = await setup({
    saved: {
      schemaVersion: 1,
      weeks: { [key]: week },
      customShoppingWeeks: {
        [key]: [
          {
            id: "extra-milk",
            name,
            quantity: 500,
            unit: "ml",
            aisle: "Dairy & eggs",
            selected: false,
            bought: true,
          },
        ],
      },
    },
  });
  try {
    ui.change(ui.$("#household-size"), "3");
    ui.$("#shopping-open").click();
    const row = ui.row("extra:extra-milk|ml");
    assert.equal(row.querySelector("img"), null);
    assert.ok(row.textContent.includes(name));
    assert.equal(row.querySelector('[type="number"]').value, "500");
    assert.equal(row.querySelector(".shopping-check input").checked, false);
    assert.equal(
      row.querySelector(".shopping-bought-check input").checked,
      true,
    );
    assert.equal(ui.saved().weeks[key].monday.breakfast, "pancakes");
  } finally {
    await ui.close();
  }
});

test("cooking mode follows steps, keeps preparation ticks separate, runs timers and pauses on close", async (t) => {
  let now = 1000;
  t.mock.method(Date, "now", () => now);
  const key = api.mondayKey();
  const week = api.emptyWeek();
  week.monday.breakfast = "pancakes";
  const ui = await setup({
    saved: { schemaVersion: 1, weeks: { [key]: week } },
  });
  try {
    ui.$("#mobile-recipes").click();
    ui.all(".recipe-title")
      .find((node) => node.textContent === "Pancakes")
      .click();
    ui.$("#recipe-start-cooking").click();
    const recipe = recipes.find((recipe) => recipe.id === "pancakes");
    assert.equal(ui.$("#cook-dialog").open, true);
    assert.equal(ui.$("#recipe-dialog").open, true);
    assert.equal(ui.$("#cook-step-text").textContent, recipe.method[0]);
    ui.$("#cook-step-done").click();
    ui.$("#cook-next").click();
    assert.equal(ui.$("#cook-step-text").textContent, recipe.method[1]);
    ui.$("#cook-previous").click();
    assert.equal(ui.$("#cook-step-done").checked, true);
    ui.$("#cook-ingredient-list input").click();
    assert.equal(ui.$("#recipe-detail .ingredient-row input").checked, false);
    ui.change(ui.$("#cook-timer-name"), "Rice");
    ui.change(ui.$("#cook-timer-minutes"), "1");
    ui.submit(ui.$("#cook-timer-form"));
    assert.equal(ui.$(".cook-timer-time").textContent, "1:00");
    now = 31000;
    ui.browser.document.dispatchEvent(new ui.browser.Event("visibilitychange"));
    assert.equal(ui.$(".cook-timer-time").textContent, "0:30");
    ui.$("#cook-close").click();
    await settle();
    assert.equal(ui.$("#cook-dialog").open, false);
    assert.equal(ui.browser.document.activeElement.id, "recipe-start-cooking");
    now = 900000;
    ui.$("#recipe-start-cooking").click();
    assert.equal(ui.$(".cook-timer-time").textContent, "0:30");
    assert.equal(ui.$("#cook-step-done").checked, true);
    assert.equal(ui.$("#cook-ingredient-list input").checked, true);
    ui.$('[data-action="toggle"]').click();
    now += 31000;
    ui.browser.document.dispatchEvent(new ui.browser.Event("visibilitychange"));
    assert.equal(ui.$(".cook-timer-time").textContent, "0:00");
    assert.equal(ui.$(".cook-timer-finished").hidden, false);
    assert.match(ui.$("#cook-status").textContent, /Rice: time’s up/);
    for (let index = 0; index < recipe.method.length; index++) {
      ui.change(ui.$("#cook-step-select"), String(index));
      if (!ui.$("#cook-step-done").checked) ui.$("#cook-step-done").click();
    }
    assert.equal(ui.$("#cook-complete").hidden, false);
    assert.equal(ui.$("#cook-progress").value, recipe.method.length);
    assert.deepEqual(ui.saved().weeks[key], week);
  } finally {
    await ui.close();
  }
});

test("screen awake is optional and released when leaving cooking mode", async () => {
  const ui = await setup();
  let released = false;
  try {
    const lock = new ui.browser.EventTarget();
    lock.release = async () => {
      released = true;
      lock.dispatchEvent(new ui.browser.Event("release"));
    };
    Object.defineProperty(ui.browser.navigator, "wakeLock", {
      value: { request: async () => lock },
      configurable: true,
    });
    ui.$(".recipe-title").click();
    ui.$("#recipe-start-cooking").click();
    assert.equal(ui.$("#cook-awake-label").hidden, false);
    ui.$("#cook-awake").click();
    await settle();
    assert.match(ui.$("#cook-awake-status").textContent, /stay awake/);
    ui.$("#cook-close").click();
    await settle();
    assert.equal(released, true);
  } finally {
    await ui.close();
  }
});

test("PNG buttons save and natively share the current plan and shopping page", async () => {
  const key = api.mondayKey();
  const week = api.emptyWeek();
  week.monday.breakfast = "pancakes";
  week.monday.dinner = "moussaka";
  const shared = [];
  const ui = await setup({
    saved: { schemaVersion: 1, weeks: { [key]: week } },
    nativeCanvas: true,
    share: async (data) => shared.push(data),
  });
  try {
    ui.$("#screenshot-open").click();
    await ui.ready();
    assert.equal(ui.$("#capture-share").hidden, false);
    ui.$("#capture-save").click();
    assert.equal(ui.downloads[0].name, `top-recipes-plan-${key}.png`);
    ui.$("#capture-share").click();
    await settle();
    assert.equal(shared[0].files[0].type, "image/png");
    const bytes = new Uint8Array(await shared[0].files[0].arrayBuffer());
    assert.deepEqual([...bytes.slice(0, 8)], [137, 80, 78, 71, 13, 10, 26, 10]);
    ui.$("#capture-close").click();
    await settle();
    ui.$("#shopping-open").click();
    ui.$("#shopping-screenshot").click();
    await ui.ready();
    assert.match(ui.$("#capture-export-status").textContent, /page shown/);
    ui.$("#capture-next-page").click();
    await ui.ready();
    ui.$("#capture-share").click();
    await settle();
    assert.equal(
      shared[1].files[0].name,
      `top-recipes-shopping-${key}-page-2.png`,
    );
    ui.$("#capture-save").click();
    assert.equal(
      ui.downloads[1].name,
      `top-recipes-shopping-${key}-page-2.png`,
    );
  } finally {
    await ui.close();
  }
});

test("share cancellation and unsupported image export leave screenshots usable", async () => {
  const ui = await setup({
    nativeCanvas: true,
    share: async () => {
      throw new DOMException("Cancelled", "AbortError");
    },
  });
  try {
    ui.$("#screenshot-open").click();
    await ui.ready();
    ui.$("#capture-share").click();
    await settle();
    assert.match(
      ui.$("#capture-export-status").textContent,
      /Sharing cancelled/,
    );
    assert.equal(ui.$("#capture-save").disabled, false);
  } finally {
    await ui.close();
  }
  const unsupported = await setup();
  try {
    unsupported.$("#screenshot-open").click();
    await settle();
    assert.equal(unsupported.$("#capture-save").disabled, true);
    assert.match(
      unsupported.$("#capture-export-status").textContent,
      /screenshot or use Print/,
    );
    unsupported.$("#capture-hide").click();
    assert.equal(
      unsupported.$("#capture-dialog").classList.contains("controls-hidden"),
      true,
    );
  } finally {
    await unsupported.close();
  }
});
