# Anthropic IPO guide

Independent investor briefing built from `key-points-summary.md`, the SpaceX research in `../SpaceX-ipo/`, and the reviewed design documents in this folder. The page is a dated research snapshot, not a live market feed or an official Anthropic publication.

Private viewing URL: https://anthropic-ipo-briefing-20261030.jazzychord256.chatgpt.site

## Run

Open `index.html` in a browser, or run `python -m http.server 8765 --bind 127.0.0.1` from this directory. The execution environment's browser policy may block `file://`; serving over HTTP works. There is no installation, build step or backend.

## Files and architecture

- `index.html`: complete HTML, CSS, inline ledger data and JavaScript. Embedded Archivo/Source Sans 3 font subsets and their SIL Open Font Licenses are included in the file. There are no runtime font, script, API or cross-project requests.
- `design-and-content-plan.md`, `design-review.md`, `build-plan.md`: design decisions, second-pass review and implementation sequence. Preserve them with the research.
- `tests/browser_smoke.py`: native Chromium/Playwright checks. Requires an already available Playwright installation and `/usr/bin/chromium`; any test dependencies belong in `tests/`.
- `tests/VERIFICATION.md`: actual validation evidence, screenshot review and limitations.

The inline `ledger-data` JSON uses integer USD millions and a fixed maximum of 18,000. `renderLedger` derives costs, signed operating results and bar widths. The default is H1 2026. The radio switch affects only this panel; the complete exact table always includes H1 and Q2. `updateNavigation` tracks the section at the reading line using a single scheduled animation frame. Print lifecycle handlers open and then restore details; print CSS also supports the no-JavaScript case. There is no persisted state.

The reading experience changes are specified in `reading-experience-plan.md`. The ledger also derives operating margin and rounded operating expenses per $100 revenue from the same inputs; these are accounting measures, not cash-flow estimates. Keep `briefing`, `driver-demand`, `driver-compute`, and `driver-valuation` anchors stable. The three other driver themes and seven-event chronology remain available through native disclosures and print.

`source-preview-data` contains dated provenance and only verified original excerpts. Other preview text is explicitly a research note taken from the source index. MD&A excerpts follow the customer/compute/financial citation context. All 20 source entries retain ordinary links; JavaScript enhances those links with a native dialog where supported. Preserve modified-click behavior, focus containment, Escape/Close restoration without article scroll, an explicit source-index handoff, and the no-JavaScript anchor fallback. Never fetch sources or new quotes at runtime.

The second reading revision adds the fixed H1 `financial-views` panels (independent of the ledger's selected period), the hypothetical `dilution-example`, the dated `roadmap`, first-use glossary links, and chapter reading aids. The dilution example starts each index at 100 and computes per-share index as company-value index / economic-share index × 100. Its two native sliders support gains, losses and reset; the complete default 120/125=96 illustration survives without JavaScript. These are illustrative indices, never Anthropic valuation inputs or price targets.

`term-help-data` supplies the Anthropic-specific explanation; definitions come from the single glossary at `glossary`, with stable `definition-*` IDs. Term links fall back to that native disclosure and are enhanced by `term-preview` when supported. Preserve both dialog families' focus and keyboard behavior. Closing a definition must keep the reading position; its explicit glossary link opens the disclosure and focuses the chosen definition.

`measureReading` estimates five main chapters at 200 words/minute; total minutes equal their rounded chapter estimates. It excludes sources, closed detail bodies, visually hidden descriptions, the controls and reading-time labels themselves. Opened supporting detail adds time. `updateReadingProgress` measures article position, not proof of reading; it does not persist state. Keep mobile chapter-strip height, section padding, anchor offsets and focus clearance consistent. Reading controls and dialogs are excluded from print; printed examples retain current displayed values.

## Stable conventions

- Preserve the directory name and capitalization `Anthropic-ipo`, explicitly requested and already shared.
- Keep the page self-contained and compatible with GitHub Pages at `/Anthropic-ipo/`. Do not import SpaceX files at runtime; embed selected facts and original sources.
- Preserve section IDs `overview`, `economics`, `drivers`, `commitments`, `spacex`, `watchlist` and `sources`, plus source IDs used by citations.
- Keep dates as civil date strings; avoid timezone conversion of market dates.
- Keep periods, units and source status beside material figures. Do not turn unspecified IPO terms into zero or guessed values.
- Distinguish operating profit, net income and cash flow; new economic issuance and resale supply; and filing data versus reported attribution.
- Do not sum the mixed compute-arrangement rows. Preserve the ceiling, ramp and cancellation terms around SpaceXAI amounts.
- Customer B's 34.5% concentration is filed; the Anthropic identification is attributed to Bloomberg.
- SpaceX events are selected dated observations with price types. Do not interpolate a daily series or imply an unlock determines price direction.

## Design

Use the six base variables `--paper`, `--ink`, `--muted`, `--accent`, `--tailwind` and `--headwind`. Archivo headings and Source Sans 3 body use fallback stacks. Maintain 390px-first layouts, visible focus, reduced motion, readable contrast and no whole-page horizontal scrolling. Desktop uses a static masthead and sticky contents rail; smaller screens use one sticky header with native Contents. The operating ledger is the principal visual.

## Verification and publication

Serve the page and run `python tests/browser_smoke.py`. Set `ANTHROPIC_TEST_URL` when using another local port. Inspect screenshots after changes to hierarchy or layout; check affected periods and sources after factual changes. Record actual checks rather than claiming unrun tests. Before publication refresh the source status or clearly retain the historical snapshot.

The canonical source is maintained in `nikolaspanayotov-jpg/VibeProjects` at `Anthropic-ipo/`. Keep future commits limited to this project. The private Sites copy is a viewing export; its hosting workspace is `/workspace/sites/anthropic-ipo-briefing`. Copy this exact `index.html` into that workspace's `dist/` only after validation. Hosting credentials must never enter project files.

Generated screenshots and PDFs are retained in the execution workspace and can be regenerated by the browser checks; they are ignored in Git. The test script, recorded results, and verification notes are versioned.
