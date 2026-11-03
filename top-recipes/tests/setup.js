import { readFile } from "node:fs/promises";
import { runInThisContext } from "node:vm";

// Exercise exactly the classic scripts shipped to Pages, including the vendored parsers.
export async function runScript(path) {
  const url = new URL(`../${path}`, import.meta.url);
  runInThisContext(await readFile(url, "utf8"), { filename: url.pathname });
}
for (const path of [
  "vendor/marked.umd.js",
  "vendor/js-yaml.min.js",
  "src/planner.js",
  "src/storage.js",
  "src/ui.js",
  "src/content.js",
  "src/recipes.js",
  "src/shopping.js",
  "src/capture.js",
  "src/experience.js",
])
  await runScript(path);
export const api = globalThis.TopRecipes;
