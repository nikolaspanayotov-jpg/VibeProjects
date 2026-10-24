# PHP explained

A standalone, interactive guide to the October 2026 PHP2Shell disclosures, written for nontechnical readers. Its repository path is `php-explained/`; keep that folder name stable. Hosting follows the repository's GitHub Pages configuration.

## Running

Open `index.html` in a full browser, or serve this folder with `python3 -m http.server 8000`. No build, framework or runtime dependencies. GitHub's source viewer and some embedded file previews do not execute page JavaScript. When JavaScript is disabled or initialization fails, the written guide and native expandable sections remain usable, and a notice explains how to access the interactive version. The stories, quiz, copy and print controls are revealed only after their handlers initialize.

## Architecture

All page HTML, CSS and JavaScript are inline in `index.html`. The `notes` data and `render()` drive two four-step stories; `mode`, `step` and `patched` hold their state. `changeStory()` updates the scene and moves focus to the step heading so hiding the final Next button does not strand keyboard users. At phone widths it also brings the changed scene into view. Separate handlers power audience guidance, version guidance, quiz, copy and print. No persistence, network scanning or backend.

## Design and constraints

Paper and green colors, warm warning colors, serif headings and system body text. Color variables are defined on `:root`. Navigation wraps on phones; grid children and selects may shrink to their container. Reduced-motion support disables scene animation and smooth scrolling. The desk is a teaching analogy, not a working exploit. Preserve citations and distinguish the October 23 follow-up from the October 21 pair. Security facts are dated October 24, 2026 and need review before future updates.

## Checking changes

The app itself needs no installation. `qa/buttons.cjs` is an optional Playwright check. It resolves `../index.html` relative to the test, so the working directory and checkout location do not matter. It uses Playwright's installed Chromium by default. Set `CHROMIUM_EXECUTABLE` to use a system browser. Screenshots go to a temporary directory printed on successful completion; no absolute workspace paths are committed.

With Playwright already available, run `node qa/buttons.cjs`. Otherwise, from this project folder, install test-only tooling:

```sh
npm install --prefix qa --no-save --package-lock=false playwright linkedom
./qa/node_modules/.bin/playwright install chromium
node qa/dom.mjs
node qa/buttons.cjs
```

Do not commit generated `qa/node_modules` or other dependency artifacts. There is no application build step.

`qa/dom.mjs` provides fast regression checks against parsed HTML using the test-only LinkeDOM package. It can run without a browser; focus and scrolling are instrumented and layout is not checked.

The Playwright check covers both stories and repaired replays, back/restart, every quiz answer, scoring and retry, all audience and version choices, expandable sections, copy success and denial, print dispatch, internal links, keyboard navigation, reduced motion, and JavaScript-disabled fallback. It asserts state changes, focus and no horizontal overflow at 390px and 1280px, fails on page errors, and takes screenshots. Inspect those screenshots as well. Clipboard and print APIs are stubbed: native clipboard permissions and the native print dialog still require a manual check.

## Current verification limits

On October 24, 2026, JavaScript syntax checks and interaction checks against HTML parsed with LinkeDOM passed. The DOM checks exercised every button and dropdown, all quiz answer paths, copy success/denial and print dispatch. Browser-specific focus/scroll APIs were instrumented; these checks do not verify layout, native focus behavior or accessibility announcements.

The real Playwright launch still fails in this environment before loading the page (`setsockopt: Operation not permitted` from Chromium). Browser interaction checks and screenshots have therefore not passed. Do not claim mobile layout or full browser verification is complete. Keep changes off the deployment branch until the required browser checks and screenshot review can run.
