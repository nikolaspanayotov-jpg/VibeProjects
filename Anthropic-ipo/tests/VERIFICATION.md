# Reading-tools implementation verification — 5 November 2026

All five approved additions are complete: local article search, a hypothetical valuation calculator and nine-cell sensitivity table, three scenario evidence trackers, five expandable partner relationships, and a separate two-page printable brief. Scope and source notes: [reading-tools-update-2026-11-05.md](../reading-tools-update-2026-11-05.md).

## Actual validation

```sh
ANTHROPIC_TEST_URL=http://127.0.0.1:8806/ python tests/browser_smoke.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8806/ python tests/reading_tools.py
node --check /tmp/anthropic-tools-inline.js
```

**80 checks passed:** 66 existing browser checks and 14 new reading-tool checks. One existing direct-file check remains unverified because the browser's administrator policy blocks file URLs; no bypass was attempted. See [browser-results.json](browser-results.json) and [reading-tools-results.json](reading-tools-results.json).

The new checks cover search pagination, punctuation, empty/unknown queries, literal markup input, opening collapsed evidence, focus and reloadable passage links; independent valuation and nine-cell arithmetic; both revenue bases; blank/zero/negative/large inputs; tiny-positive rounding; reset; mobile keyboard clearance; all partner source-preview paths; scenario evidence disclosures; 320/390/768/1440px reflow; the separate print action; no-JavaScript content and both brief print paths. No page/console errors or runtime third-party requests were observed. The final new-tool run includes the last mobile workbench layout adjustment. The broader 66-check regression preceded that confined layout adjustment; affected new behavior and both full-guide PDFs were then checked again.

The `ledger-data`, `entry-return-data`, `commitment-data` and `source-preview-data` JSON datasets match the pre-change page exactly. Original research and the SpaceX historical cutoff remain intact. Primary partner roles were re-read in the amended prospectus. This implementation did not perform a new general news sweep or refresh the old market-price snapshot.

## Visual and print review

Actual mobile and desktop captures inspected in `tests/screenshots/`: `tools-mobile-search.png`, `tools-mobile-valuation.png`, `tools-mobile-sensitivity.png`, `tools-mobile-evidence.png`, `tools-desktop-valuation.png` and `tools-desktop-partners.png`. Review changes made expanded partner cards span the available row, shortened redundant decimal formatting in the sensitivity grid, used neutral scenario-signal colours and kept the mobile valuation result visible while editing. Its sticky scope ends with the input workbench so it does not cover the sensitivity table. Keyboard traversal keeps the controls clear of it.

Both pages of `investment-brief.pdf` were rasterised and inspected. It and `investment-brief-nojs.pdf` are **exactly two A4 pages** at 100% scale with browser headers/footers off. Text extraction verifies dates, retail qualifications, spending/concentration figures, the cash-flow distinction and the historical SpaceX entry examples. The brief remains readable on screen and printable without JavaScript. The full guide prints to **37 pages with JavaScript and 36 without**; partner and calculator print layouts were inspected, and final PDF text retains the new evidence/assumptions. Generated PDFs and screenshots remain local, ignored and reproducible.

Verification limits: Chromium only; no screen-reader or other-engine session. Print page counts assume the documented A4 settings and embedded fonts. No new exhaustive legal/broker eligibility review or causal market study.

Validated files:

- `index.html`: 395,366 bytes; SHA-256 `d0000c5406888677fb32a928525a2d6ff56f851aa038fe282213ea35d32aefde`.
- `investment-brief.html`: 93,276 bytes; SHA-256 `f5583083c76663e3fe7f5ce43944ca5e514310e2c19ab154c03f8f85993fcb8c`.

## Publication

Published to `nikolaspanayotov-jpg/VibeProjects` main, limited to `Anthropic-ipo/`, in commit `5126ab4a7dbea3d2590a1c49e21ddb0533295f17`. The [Pages workflow](https://github.com/nikolaspanayotov-jpg/VibeProjects/actions/runs/42127942131) completed successfully for that exact commit.

At **23:14:48 UTC on 5 November 2026**, both ordinary public URLs returned HTTP 200 and SHA-256 hashes matching the validated local files above, without query strings or authentication:

- [Full guide](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/): 395,366 bytes.
- [Two-page investment brief](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/investment-brief.html): 93,276 bytes.

The owned local preview server was stopped after verification. This final documentation receipt does not change the validated HTML.

Public project notes omit private hosting URLs, internal identifiers and export paths. Earlier validation history remains available in the repository's commit history. Automatic approval review rejected an upload containing historical private hosting metadata; the public record was narrowed to the current validation and GitHub publication evidence before retrying. No private credential transfer or deployment was attempted.
