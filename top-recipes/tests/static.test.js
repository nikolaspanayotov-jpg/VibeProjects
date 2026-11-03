import test from "node:test";
import assert from "node:assert/strict";
import { readFile, access } from "node:fs/promises";
import { Window } from "happy-dom";
import { api } from "./setup.js";

test("the project runs directly under its GitHub Pages subdirectory with local assets", async () => {
  const html = await readFile(
    new URL("../index.html", import.meta.url),
    "utf8",
  );
  const browser = new Window({
    url: "https://nikolaspanayotov-jpg.github.io/VibeProjects/top-recipes/",
    settings: {
      disableCSSFileLoading: true,
      disableJavaScriptFileLoading: true,
    },
  });
  browser.document.write(html);
  try {
    for (const node of browser.document.querySelectorAll(
      "script[src], link[href], img[src]",
    )) {
      const target = node.getAttribute("src") || node.getAttribute("href");
      assert.ok(
        target.startsWith("./"),
        `Asset must be project-relative: ${target}`,
      );
      await access(new URL(`../${target}`, import.meta.url));
      assert.ok(
        new URL(target, browser.document.baseURI).pathname.startsWith(
          "/VibeProjects/top-recipes/",
        ),
      );
    }
    assert.equal(browser.document.querySelector('script[type="module"]'), null);
    assert.equal(
      new URL("./recipes.md", browser.document.baseURI).pathname,
      "/VibeProjects/top-recipes/recipes.md",
    );
    const recipes = api.parseRecipes(
      await readFile(new URL("../recipes.md", import.meta.url), "utf8"),
    );
    for (const recipe of recipes) {
      if (!recipe.image) continue;
      assert.ok(
        api.validRecipeImagePath(recipe.image),
        `Invalid image path for ${recipe.title}`,
      );
      await access(new URL(`../${recipe.image}`, import.meta.url));
      assert.ok(
        new URL(recipe.image, browser.document.baseURI).pathname.startsWith(
          "/VibeProjects/top-recipes/assets/",
        ),
      );
    }
    await assert.rejects(access(new URL("../package.json", import.meta.url)));
  } finally {
    browser.close();
  }
});
