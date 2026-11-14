# Valuation and position-planning review — 14 November 2026

Implements the uploaded research handoff; refreshed sources, access limits, model conventions and differences are recorded in [valuation-and-position-plan-2026-11-14.md](../valuation-and-position-plan-2026-11-14.md). New modules distinguish published fair values, reported bank forecasts, author forward sensitivities and a finite hypothetical position. The initial review handoff left main/public HTML unchanged; the user subsequently approved publishing this reviewed implementation.

## Actual validation

```sh
node tests/position_math.mjs
ANTHROPIC_TEST_URL=http://127.0.0.1:8824/ python tests/position_planner.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8824/ python tests/browser_smoke.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8824/ python tests/reading_tools.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8824/ python tests/november_refresh.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8824/ python tests/participation_update.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8824/ python tests/uk_pricing.py
node --check /tmp/position-all-inline.js
```

**124 checks passed**: 15 independent arithmetic cases, 10 new browser decision-tool checks and 99 existing regression checks (66 general, 14 reading tools, 6 November refresh, 6 participation, 7 UK pricing). One existing direct-file check remains unverified because administrator browser policy blocks file URLs. Full numerical assertions include $1,480 consideration; $360 gross gain / $160 loss at different entries; $71.78/$68.45 averages after additions; the $853.50 downside; $1,017.50 staged receipts / $277.50 realised gain; £130.29 FX-sensitive gain; $91.60 forward value / $83.27 with 10% more shares; and the 9.8012× forecast-revenue ratio. Further cases cover currency-specific charges, per-sale fees, zero/partial allocation, finite reviews, overselling, full exit, unknown costs, fractional/empty/non-finite inputs and contribution/share-cap breaches.

The final general and new-browser suites were rerun after the mobile GBP-column refinement and final horizon/entry-discipline copy. The other suites passed on the same implementation before these confined refinements; no unnecessary blanket rerun is claimed. Three executable script blocks pass syntax checking. Original `ledger-data`, `entry-return-data` and `commitment-data` JSON were compared with the prior main source and are unchanged. All 56 source previews and 15 first-use definitions passed keyboard/focus checks.

New controls retain no-runtime-request/no-persistence behaviour. Unknown fees stay visibly not supplied; the default outputs are before costs, not net profit. Optional additions and sales start off, and changing a price never enables a purchase. An explicit transfer action is required to use a forward or custom reference in the position planner. No brokerage login, application, order or trade was performed.

## Visual, print and link review

Actual mobile/desktop captures inspected include `position-mobile-forward-results.png`, both mobile and desktop `position-…-position-results.png`, the initial independent-valuation and planner mobile captures, and the updated brief's second page. The final mobile results table keeps USD and GBP amounts visible together. Advanced controls use native disclosures; wider exact tables have a local scroll hint and keyboard-focusable regions. At 320, 390, 768 and 1440px, expanded content has no whole-page horizontal overflow. An additional direct-link session verified all four new main anchors clear the mobile header, plus enlarged-text reflow.

Both brief PDFs remain exactly **two A4 pages**, with and without JavaScript. Full-guide outputs are **60 pages with JavaScript and 59 without**. Actual full-guide forward-matrix page 40 and planner page 44 were rasterised and inspected. Text extraction retains dates, author/source labels, model assumptions, exact cash flows and fee/tax qualifications. No-JavaScript examples retain the five entry rows, nine forward combinations and default position ledger.

Verification limits: Chromium only; no screen-reader/other-engine session, authenticated broker preview, live price/FX feed or tax computation. Morningstar direct retrieval returned 403; indexed article text was available, not the full company report. The final note distinguishes the newly verified 11 November published $25/$188 cases from the older equity scenarios and our author illustrations.

## Review handoff

The initial implementation was provided as a project-only patch and standalone review bundle against main `21cbfafd4a30cc16b0615fe5dabc363dddcb1c1f`. The user reviewed it and explicitly approved publication to main. Before publication, both HTML files and all other reviewed files matched the review manifest exactly; only publication-status documentation was subsequently updated. No code or HTML changed after the recorded checks. Public-source metadata is retained; private hosting identifiers, credentials and personal portfolio data are excluded.

## Publication

Published to `main` in implementation commit [`119ce59fea36391585a6790609503b9a8f6a8bc2`](https://github.com/nikolaspanayotov-jpg/VibeProjects/commit/119ce59fea36391585a6790609503b9a8f6a8bc2), with exactly 13 changed files, all within `Anthropic-ipo/`. [GitHub Pages run 43596859776](https://github.com/nikolaspanayotov-jpg/VibeProjects/actions/runs/43596859776) completed successfully for that exact commit.

At **2026-11-14 12:53:02 UTC**, both ordinary public URLs returned HTTP 200 and hashes matching the reviewed, tested HTML, without query strings or authentication:

- [Full guide](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/): 530,127 bytes; SHA-256 `0a351b7b56b89b322413860a6593804b41f1604714faa3df4d2cebc794367908`.
- [Two-page brief](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/investment-brief.html): 95,311 bytes; SHA-256 `d5e786a0f3079d22c6cabac7b5897caee829920cd923160e898e561cc48772b7`.

This publication receipt updates documentation only. The deployed HTML is unchanged from the version that passed the recorded 124 checks. No new code tests were required for the subsequent publication-status edits.

---

# UK/European IPO price and IBKR funding verification — 14 November 2026

The focused source review and implementation plan are in [uk-europe-pricing-2026-11-14.md](../uk-europe-pricing-2026-11-14.md). The new `uk-ipo-costs` section explains common issuer pricing, the amendable EEA/Swiss ceiling, UK GBP/CDI and USD routes, and a maximum-20-share IBKR currency-cost comparison. Four primary/company/broker source previews were added (48 total). General FX rates remain conditional; unknown account-specific IPO fees are not represented as zero or replaced with secondary-market commissions.

## Actual validation

```sh
ANTHROPIC_TEST_URL=http://127.0.0.1:8820/ python tests/uk_pricing.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8820/ python tests/browser_smoke.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8820/ python tests/reading_tools.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8820/ python tests/november_refresh.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8820/ python tests/participation_update.py
node --check /tmp/uk-inline.js
```

**99 checks passed**: 66 general regression, 14 reading tools, 6 November refresh, 6 participation and 7 focused UK pricing checks. One direct-file check remains unverified because browser administrator policy blocks file URLs. New checks cover equal issuer prices versus local costs, regional cap amendment, unchanged default/static calculations, reduced allocations, the manual FX minimum and percentage tiers, correct basis-point conversion, invalid/empty/fractional/above-cap inputs, tiny nonzero labels, keyboard reset/announcement, source provenance and focus restoration, direct/reloaded section and generated search-passage links, 320/390/768/1440px reflow, no-JavaScript parity and printed assumptions. No page/console errors or runtime third-party requests were observed. All 48 source previews passed the general regression check.

An additional reload check exposed browser scroll restoration overriding a generated passage anchor inside the new closed disclosure. A non-cached `pageshow` handoff now reapplies that anchor; back/forward-cache pages retain their saved reading position. The focused UK, general browser and reading-tool suites were rerun after the fix.

The `ledger-data`, `entry-return-data` and `commitment-data` JSON were compared with the prior implementation and are unchanged. The assumed $74 midpoint and invented 1.25 USD/GBP rate do not become a live quote or final offer terms.

## Visual and print review

Actual captures inspected: `uk-mobile-uk-ipo-costs.png`, `uk-mobile-uk-cost-calculator.png`, `uk-desktop-uk-cost-results.png`; the updated brief's second A4 page; and the full-guide printed funding comparison (page 36). The new result columns preserve their fee exclusions and conditional automatic-FX wording.

Both brief PDFs are exactly **two A4 pages**, with and without JavaScript. The full guide prints to **50 pages with JavaScript and 49 without**. Extracted print text preserves the common-price explanation, amendment qualification, 20-share assumptions and currency-only funding figures. Generated images/PDFs remain ignored local QA artifacts.

Verification used Chromium only, with no authenticated IBKR account, trade/application submission, screen-reader session or other browser engine. The broker's advertised UK offer URL redirected to its homepage; the page does not claim the user's eligibility, account cutoff, exact IPO application fee or FX workflow were verified. Public notes omit private hosting metadata and credentials.

## Publication

Published to `main` in implementation commit [`6531cd342ad7ab86d4a10833360db44d9f107e8e`](https://github.com/nikolaspanayotov-jpg/VibeProjects/commit/6531cd342ad7ab86d4a10833360db44d9f107e8e), with exactly ten project-only changed files. [GitHub Pages run 43584764424](https://github.com/nikolaspanayotov-jpg/VibeProjects/actions/runs/43584764424) completed successfully for that commit.

At **2026-11-14 10:21:49 UTC**, both ordinary public URLs returned HTTP 200, with hashes matching the validated files and no query strings or authentication:

- [Full guide](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/): 453,359 bytes; SHA-256 `2beaa441a030670a0dc6b87b76e7cbcdcd85897094317ae79f6e9be0392446d5`.
- [Two-page brief](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/investment-brief.html): 94,602 bytes; SHA-256 `63c4c33b54264ac5c29f9194885d85b6c74cae5cf5fdac55a02a2ffae291e4db`.

The owned local preview server was stopped after verification. This documentation receipt leaves the published HTML unchanged.

---

# 14 November IPO participation and timetable verification

The update follows [ipo-update-2026-11-14.md](../ipo-update-2026-11-14.md), which records the source review and plan. The page and brief now distinguish the unchanged 10 November preliminary terms from newer FWPs, expected company dates, regional conditions and attributed order-book reports.

## Actual validation

```sh
ANTHROPIC_TEST_URL=http://127.0.0.1:8814/ python tests/browser_smoke.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8814/ python tests/reading_tools.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8814/ python tests/november_refresh.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8814/ python tests/participation_update.py
node --check /tmp/n14-inline.js
```

**92 checks passed**: 66 general regression, 14 reading-tool, 6 November-financial-refresh and 6 new participation/timeline checks. One direct-file check remains unverified because browser administrator policy blocks file URLs. The new checks cover expected EST dates versus completed/final terms; five FWPs and their issuer/SEC/review dates; regional scope, application cutoffs, $120 maximum versus the U.S. range; AEDT/EST timetable labels; source-preview keyboard restoration; order-book attribution and limits; company-defined efficiency measurement; 320/390/768/1440px reflow and no-JavaScript evidence. All 44 source previews were exercised. No page/console errors or runtime third-party requests were observed.

The `ledger-data`, `entry-return-data` and `commitment-data` JSON match the prior page exactly. The calculator, economic share counts and historical SpaceX prices have not been replaced with reported forecasts or a book-coverage-derived return assumption.

## Visual and print review

Actual captures inspected: `nov14-mobile-overview.png`, `nov14-mobile-regional-access.png`, `nov14-desktop-order-book.png`; both rasterised pages of the two-page brief; and full-guide print pages containing the demand panel and regional disclosure. Layouts retain readable status/date labels, distinct reported-versus-analytical treatment and visible regional price/cutoff qualifications.

Both `investment-brief.pdf` and `investment-brief-nojs.pdf` are **exactly two A4 pages**. The full guide prints to **46 pages with JavaScript and 45 without**. Extracted print text retains the timetable, price-ceiling distinction, regional time labels, reported book coverage and source dates. After the final copy-only amendment/FWP wording and timetable-citation correction in the brief, affected PDFs were regenerated and text/page-count checked. No full regression rerun is claimed after that copy-only correction.

Generated screenshots/PDFs remain ignored local QA artifacts. Verification is Chromium-only, with no screen-reader/other-engine session, exhaustive legal eligibility audit or independent company-claim validation. The full roadshow video was not reviewed; relevant text exhibits, official FAQ and listed regional sections were read. A printed schedule, source publication or dated event listing is not proof of an allocation, new revenue or an effective/completed IPO.

## Publication

Published to `main` in implementation commit [`5126255b957975ebbc62935b19fcbfccd5e807b5`](https://github.com/nikolaspanayotov-jpg/VibeProjects/commit/5126255b957975ebbc62935b19fcbfccd5e807b5), limited to `Anthropic-ipo/`. [GitHub Pages run 43579516118](https://github.com/nikolaspanayotov-jpg/VibeProjects/actions/runs/43579516118) completed successfully for that exact commit.

At **09:14:44 UTC on 14 November**, both ordinary public URLs returned HTTP 200 and hashes matching the validated HTML, with no query strings or authentication:

- [Full guide](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/): 431,852 bytes; SHA-256 `76dcf03cf32a3931d293636fcae16f5f69b931569884cb197060e53334a97443`.
- [Two-page brief](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/investment-brief.html): 94,534 bytes; SHA-256 `89e94e22d3fd5829fb2ef3c3221bda8f33739386c79e33acb3ebb1fcd6185371`.

The owned preview server was stopped after verification. This documentation receipt does not change the published HTML. Public notes exclude private hosting metadata and credentials.

---

# 10 November IPO-source refresh verification

The guide and printable brief incorporate the latest amendment and material official/reported developments since 2 November. Scope, source locations, limitations and old/new values are recorded in [ipo-update-2026-11-10.md](../ipo-update-2026-11-10.md).

## Checks run

```sh
ANTHROPIC_TEST_URL=http://127.0.0.1:8810/ python tests/browser_smoke.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8810/ python tests/reading_tools.py
ANTHROPIC_TEST_URL=http://127.0.0.1:8810/ python tests/november_refresh.py
node --check /tmp/nov10-inline.js
```

**86 checks passed**: 66 regression checks, 14 reading-tool checks and 6 targeted offering/source-refresh checks. One direct-file regression remains unverified because administrator policy blocks file URLs. Tests verify 36 source previews, the updated commitment dataset/bar scale, both midpoint share-count calculations, original financial reconciliations, both revenue bases, search, keyboard/source focus, expected retail allocation versus individual access, eligible versus freely tradable shares, no-JavaScript content and 320/390/768/1440px reflow. No page/console errors or runtime third-party requests were observed. Ledger and historical SpaceX JSON were compared with the prior page and are unchanged.

The final brief source-citation edit was followed by targeted PDF generation and text/page-count verification; no full regression rerun was claimed for that copy-only edit. Both brief print paths are exactly **two A4 pages**. Full-guide print outputs are **41 pages with JavaScript and 40 without**. Extracted text retains current terms, scope/conditions and original source links.

Actual screenshots inspected: `nov10-mobile-offering-terms.png`, `nov10-desktop-offering-terms.png` and `nov10-mobile-share-supply.png`. Both brief PDF pages were rasterised and inspected, as were the full-guide roadshow and compensation/contingency print pages. Files are local ignored QA artifacts. Chromium only; no screen-reader/other-engine session. A4 counts assume embedded fonts, 100% scale and browser headers/footers off.

The updated SEC HTML was downloaded successfully and compared with 2 November. Some web-reader requests to the new filing/roadshow returned internal errors; the actual SEC HTML supplied primary evidence, while the official newsroom supplied the roadshow announcement listing. The model/science/inference pages, event schedule and syndicated Reuters report were read through the web connector. No inaccessible full article is claimed as read. The event was still scheduled at the pre-livestream review.

## Publication

Published on `main` in implementation commit [`fc9d95ef91db6c5d4fa5178dcef065fb3e6ebfbb`](https://github.com/nikolaspanayotov-jpg/VibeProjects/commit/fc9d95ef91db6c5d4fa5178dcef065fb3e6ebfbb), with changes confined to `Anthropic-ipo/`. [GitHub Pages run 42838806038](https://github.com/nikolaspanayotov-jpg/VibeProjects/actions/runs/42838806038) completed successfully for that commit at 14:58 UTC on 10 November.

At **14:58:35 UTC on 10 November**, both ordinary public URLs returned HTTP 200 and exact SHA-256 matches to the validated HTML:

- [Full guide](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/): 418,379 bytes; `6b4d19b6e207bc6b391dd4a7dc87aa8d28e92f56f57e3c2035f0401e6630de36`.
- [Two-page brief](https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/investment-brief.html): 93,865 bytes; `b6ce9ea5f2ad1b4361769b0a686487a92470eef7ff0d61c8b3f8a269d8436f82`.

The owned local preview server was stopped. This documentation receipt leaves the served HTML unchanged. Public notes contain no private hosting metadata or credentials.

---

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
