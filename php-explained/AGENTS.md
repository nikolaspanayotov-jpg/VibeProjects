# PHP explained

A standalone, interactive guide to the October 2026 PHP2Shell disclosures, written for non-technical readers. Its repository path is `php-explained/`; keep that folder name stable. Hosting follows the repository's GitHub Pages configuration.

## Running

Open `index.html` in a full browser, or serve this folder with `python3 -m http.server 8000`. No build, framework or runtime dependencies. GitHub's source viewer and some embedded file previews do not execute page JavaScript. When JavaScript is disabled or initialisation fails, the written guide and native expandable sections remain usable, and a notice explains how to access the interactive version. The stories, quiz, copy and print controls are revealed only after their handlers initialise.

## Architecture

All page HTML, CSS and JavaScript are inline in `index.html`. The `notes` and `repairs` objects hold the original and repaired story steps. `mode`, `step` and `patched` hold the viewer state, rendered by `render()`.

- The story cards (`oom`, `stale`) select a story and restart it in Original PHP.
- The always-visible `original` and `repaired` buttons change the version while preserving the current step and keeping keyboard focus on the selected button.
- `next` and `back` move between four steps. The final step replaces Next with `patch`, which replays the other version from step one. `reset` restarts the current version.
- `changeStory()` updates the scene in place. It must never scroll the page or focus the story heading. The active control keeps focus; when Next/Replay is hidden or Previous becomes disabled, focus transfers to the available primary action with `preventScroll: true`.
- `prepareStorySizing()` creates invisible intrinsic size reserves for every story copy, illustration and outcome. CSS overlays these reserves in grid cells so changing a story, step or version cannot move the navigation. The reserves are `aria-hidden` and `inert`; keep their typography and spacing identical to the visible content. They adapt to viewport width and font sizing without resize handlers or scroll restoration.
- Separate handlers power audience guidance, version guidance, quiz, copy and print. Quiz feedback identifies the correct answer with both text and colour. No persistence, network scanning or backend.

## Design and copy

Use British English (`en-GB`), British date order, and plain language throughout the visitor-facing copy. Keep technical identifiers, PHP settings and CSS syntax intact. The user requested removal of disclaimer copy from the page; retain factual explanations, source links and functional instructions such as enabling JavaScript.

The stories lead the page after a compact introduction. Their dark ink surround, two illustrated story selectors, inset navigation tray and prominent rust/green version signs make them the centrepiece. Original PHP uses rust; Repaired PHP uses green. Chapter panels use clear borders, soft surfaces, small accent rules and serif headings on a warm paper background. Omit decorative section numbering, including duplicate digits on story cards; retain the useful step and quiz counters. The takeaway chapter uses dark green. All palette values are on `:root`; use system sans-serif and Georgia without external font dependencies.

The mobile layout wraps navigation, uses two story cards side by side, places narration above the scene and gives the primary action its own full-width row. Story updates must preserve the reader’s scroll position and keep controls stationary. Grid and select content may shrink. Reduced-motion support disables scene animation and smooth scrolling. Preserve citations and distinguish the 23 October follow-up from the 21 October pair. Security facts are dated 24 October 2026 and need review before future updates.

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

The Playwright check covers both stories, comparison between Original and Repaired PHP at every step, and repaired replays, back/restart, every quiz answer, scoring and retry, all audience and version choices, expandable sections, copy success and denial, print dispatch, internal links, keyboard navigation, reduced motion, and JavaScript-disabled fallback. It asserts state changes, safe control focus, unchanged scroll position/navigation position after story actions, and no horizontal overflow at 320px, 390px and 1280px, fails on page errors, and takes screenshots. Inspect those screenshots as well. Clipboard and print APIs are stubbed: native clipboard permissions and the native print dialog still require a manual check.

## Current verification limits

On 24 October 2026, JavaScript syntax checks and interaction checks against HTML parsed with LinkeDOM passed. The DOM checks exercised every button and dropdown, all quiz answer paths, copy success/denial and print dispatch. Story regression checks also assert zero scroll API calls, `preventScroll` on focus transfers, and removal of decorative section numbers. Browser-specific focus/scroll APIs were instrumented; these checks do not verify layout, native focus behaviour or accessibility announcements.

The real Playwright launch still fails in this environment before loading the page (`setsockopt: Operation not permitted` from Chromium). Browser interaction checks and screenshots have therefore not passed. Do not claim mobile layout or full browser verification is complete. Keep changes off the deployment branch until the required browser checks and screenshot review can run.
