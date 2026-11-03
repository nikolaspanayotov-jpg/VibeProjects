# Anthropic IPO guide

Independent investor briefing built from `key-points-summary.md`, the SpaceX research in `../SpaceX-ipo/`, and the reviewed design documents in this folder. The page is a dated research snapshot, not a live market feed or an official Anthropic publication.

GitHub Pages: https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/

Private mirror: https://anthropic-ipo-briefing-20261030.jazzychord256.chatgpt.site — the November refresh is prepared but not deployed there. Automatic approval review rejected transferring its live repository credential through terminal input. Do not bypass that rejection; use a supported protected credential connection before pushing the prepared source and publishing. The private mirror retains its earlier October publication until then.

## Run

Open `index.html` in a browser, or run `python -m http.server 8765 --bind 127.0.0.1` from this directory. The execution environment's browser policy may block `file://`; serving over HTTP works. There is no installation, build step or backend.

## Files and architecture

- `index.html`: complete HTML, CSS, inline ledger data and JavaScript. Embedded Archivo/Source Sans 3 font subsets and their SIL Open Font Licenses are included in the file. There are no runtime font, script, API or cross-project requests.
- `design-and-content-plan.md`, `design-review.md`, `build-plan.md`: design decisions, second-pass review and implementation sequence. Preserve them with the research.
- `tests/browser_smoke.py`: native Chromium/Playwright checks. Requires an already available Playwright installation and `/usr/bin/chromium`; any test dependencies belong in `tests/`.
- `tests/VERIFICATION.md`: actual validation evidence, screenshot review and limitations.

The inline `ledger-data` JSON uses integer USD millions and a fixed maximum of 18,000. `renderLedger` derives costs, signed results, margin, per-$100 expenses and bar widths. The default is Q3 2026 after the 2 November amendment, checked 3 November. The switch retains historical H1 and Q2; all three periods remain in the exact table. Validate both GAAP and adjusted reconciliations from one dataset. `updateNavigation` tracks the reading line using one scheduled animation frame. Print handlers open and restore details, with a CSS fallback. There is no persisted state.

The reading experience changes are specified in `reading-experience-plan.md`. The ledger also derives operating margin and rounded operating expenses per $100 revenue from the same inputs; these are accounting measures, not cash-flow estimates. Keep `briefing`, `driver-demand`, `driver-compute`, and `driver-valuation` anchors stable. The three other driver themes and seven-event chronology remain available through native disclosures and print.

`source-preview-data` contains dated provenance and explicitly labeled research notes. One short original cover excerpt is verified; contextual MD&A notes are summaries, not quotations. The 22 entries distinguish current amended disclosures from the original S-1 and historical H1 figures. Preserve ordinary links, modified-click behavior, native-dialog focus containment, Escape/Close restoration without article scroll, an explicit index handoff, and no-JavaScript fallbacks. Never fetch sources at runtime.

The `financial-views` panels now cover the nine months ended 30 September 2026, independently of the ledger selection. Cash/securities use the September balance sheet. The Q3 `operating-reconciliation` shows −567 + 1,070 + 1,960 = 2,463 million and preserves the economic qualifications around excluded costs. Keep periods explicit when updating either component.

`commitment-data` holds the company-reported $895.4bn aggregate, $447.5bn expected before year-end 2030, $69.8bn expected payments in the twelve months after September, and $213.8bn subject to pre-commencement conditions/termination rights. Timing views overlap. The $319.993bn maturity schedule has narrower scope. Never add either view or the historical partner examples to the aggregate. Preserve the distinctions between expected incurrence and payments, conditions, ceilings and minimums.

The `dilution-example` remains hypothetical: indices start at 100, with per-share index = company-value index / economic-share index × 100. Its native sliders support gains, losses and reset; the default 120/125=96 illustration survives without JavaScript. These are never Anthropic valuation inputs or targets. Retain the dated roadmap, first-use glossary and chapter aids.

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
- Keep the matched H1 SpaceX comparison and 29 October price cutoff explicitly historical. Do not compare nine-month Anthropic numbers directly with SpaceX H1 values.
- Preserve `key-points-summary.md` as the original October research. Current inputs and amendment scope are recorded in `amendment-2026-11-02-summary.md`.
- Net revenue retention excludes Pro, Max and Ultra subscribers in the amendment. Do not invent the still-blank run-rate revenue or IPO terms.

## Design

Use the six base variables `--paper`, `--ink`, `--muted`, `--accent`, `--tailwind` and `--headwind`. Archivo headings and Source Sans 3 body use fallback stacks. Maintain 390px-first layouts, visible focus, reduced motion, readable contrast and no whole-page horizontal scrolling. Desktop uses a static masthead and sticky contents rail; smaller screens use one sticky header with native Contents. The operating ledger is the principal visual.

## Verification and publication

Serve the page and run `python tests/browser_smoke.py`. Set `ANTHROPIC_TEST_URL` when using another local port. Inspect screenshots after changes to hierarchy or layout; check affected periods and sources after factual changes. Record actual checks rather than claiming unrun tests. Before publication refresh the source status or clearly retain the historical snapshot.

The canonical source is maintained in `nikolaspanayotov-jpg/VibeProjects` at `Anthropic-ipo/`. Keep future commits limited to this project. The private Sites copy is a viewing export; its hosting workspace is `/workspace/sites/anthropic-ipo-briefing`. Copy this exact `index.html` into that workspace's `dist/` only after validation. Hosting credentials must never enter project files.

Generated screenshots and PDFs are retained in the execution workspace and can be regenerated by the browser checks; they are ignored in Git. The test script, recorded results, and verification notes are versioned.
