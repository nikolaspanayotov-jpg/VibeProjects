# Anthropic IPO guide

Independent investor briefing built from `key-points-summary.md`, the SpaceX research in `../SpaceX-ipo/`, and the reviewed design documents in this folder. The page is a dated research snapshot, not a live market feed or an official Anthropic publication.

GitHub Pages: https://nikolaspanayotov-jpg.github.io/VibeProjects/Anthropic-ipo/


## Run

Open `index.html` in a browser, or run `python -m http.server 8765 --bind 127.0.0.1` from this directory. The execution environment's browser policy may block `file://`; serving over HTTP works. There is no installation, build step or backend.

## Files and architecture

- `index.html`: complete HTML, CSS, inline ledger data and JavaScript. Embedded Archivo/Source Sans 3 font subsets and their SIL Open Font Licenses are included in the file. There are no runtime font, script, API or cross-project requests.
- `design-and-content-plan.md`, `design-review.md`, `build-plan.md`: design decisions, second-pass review and implementation sequence. Preserve them with the research.
- `tests/browser_smoke.py`: native Chromium/Playwright checks. Requires an already available Playwright installation and `/usr/bin/chromium`; any test dependencies belong in `tests/`.
- `tests/VERIFICATION.md`: actual validation evidence, screenshot review and limitations.

The inline `ledger-data` JSON uses integer USD millions and a fixed maximum of 18,000. `renderLedger` derives costs, signed results, margin, per-$100 expenses and bar widths. The default is Q3 2026 after the 2 November amendment, checked 4 November. The switch retains historical H1 and Q2; all three periods remain in the exact table. Validate both GAAP and adjusted reconciliations from one dataset. `updateNavigation` tracks the reading line using one scheduled animation frame. Print handlers open and restore details, with a CSS fallback. There is no persisted state.

The reading experience changes are specified in `reading-experience-plan.md`. The ledger also derives operating margin and rounded operating expenses per $100 revenue from the same inputs; these are accounting measures, not cash-flow estimates. Keep `briefing`, `driver-demand`, `driver-compute`, and `driver-valuation` anchors stable. The three other driver themes and seven-event chronology remain available through native disclosures and print.

`source-preview-data` contains dated provenance and explicitly labeled research notes. One short original cover excerpt is verified; contextual MD&A notes are summaries, not quotations. The 44 entries distinguish current amended disclosures, the SEC register, company announcements/research, a scheduled event, third-party retail reporting, the original S-1 and historical H1 figures. Preserve ordinary links, modified-click behavior, native-dialog focus containment, Escape/Close restoration without article scroll, an explicit index handoff, and no-JavaScript fallbacks. Never fetch sources at runtime.

The `financial-views` panels now cover the nine months ended 30 September 2026, independently of the ledger selection. Cash/securities use the September balance sheet. The Q3 `operating-reconciliation` shows −567 + 1,070 + 1,960 = 2,463 million and preserves the economic qualifications around excluded costs. Keep periods explicit when updating either component.

The 4 November additions are specified in `content-and-reading-update-2026-11-04.md`. `what-changed` distinguishes an amended filing, newly incorporated context and unresolved terms. The 4 November register check did not find a later filing; it must not become a claimed new filing date. `renderComputeTrend` derives the fixed Q2/Q3 compute/revenue comparison, quarterly growth and percentage-point change from `ledger-data`. This chart does not switch with the ledger. Static values must match the dataset.

`commercial-evidence` separates filed enterprise spending from the 27 October government announcement and 4 November company research. Each scorecard identifies evidence, analytical opportunity and an unanswered question. Preserve the government discount/no-minimum qualification, preprint/commercial limits and the distinction between a scheduled product event and an IPO milestone. Do not imply that adoption resolves separate legal restrictions.

`ownership-map` separates economic participation, voting/board control and tradable supply. Class F has no economic rights; converting existing Class N into Class A must not count as new economic shares. `entry-return-data` stores integer-cent SpaceX prices and one 29 October endpoint. Entry indices start at 100 on a fixed 0–120 scale. The selected June high is a close, not the intraday peak. Preserve the price-return exclusions, hindsight limitations and source links. Complete static calculations remain available without JavaScript. Check signed labels fit inside the chart in print.

`retail-access` is specified in `retail-access-update-2026-11-05.md`. Its six platform groups stay visible; an optional native disclosure preserves the full names in the 2 November retail passage. Named participation is prospective; do not imply open applications, verified individual eligibility or a guaranteed allocation. The 10 November amendment expects overall retail allocation up to 20%, based on demand; the final price, actual allocation and platform requirements still require confirmation. Keep the two entry routes and ordinary links to/from `entry-comparison`. The possible demand/volatility effects are analysis, not a price forecast. `source-a-retail` is now the 10 November filing; `source-retail-barrons` is 4 November reporting. The current register check is 14 November; prior company-research/event review dates remain separate.

`commitment-data` holds the company-reported $900.9bn aggregate, $451.6bn expected before year-end 2030, $70.7bn expected payments in the twelve months after September, and $186.2bn subject to pre-commencement conditions/termination rights. Timing views overlap. The $319.993bn maturity schedule has narrower scope. Never add either view or the historical partner examples to the aggregate. Preserve the distinctions between expected incurrence and payments, conditions, ceilings and minimums.

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
- Net revenue retention excludes Pro, Max and Ultra subscribers in the amendment. Run-rate revenue is now disclosed at approximately $81bn for 31 October in the 10 November amendment. Preserve its annualisation definition; final IPO pricing and completion remain unconfirmed; the company FAQ now expects 18/19 November EST pricing/trading, subject to clearance.

## Design

Use the six base variables `--paper`, `--ink`, `--muted`, `--accent`, `--tailwind` and `--headwind`. Archivo headings and Source Sans 3 body use fallback stacks. Maintain 390px-first layouts, visible focus, reduced motion, readable contrast and no whole-page horizontal scrolling. Desktop uses a static masthead and sticky contents rail; smaller screens use one sticky header with native Contents. The operating ledger is the principal visual.

## Verification and publication

Serve the page and run `python tests/browser_smoke.py`. Set `ANTHROPIC_TEST_URL` when using another local port. Inspect screenshots after changes to hierarchy or layout; check affected periods and sources after factual changes. Record actual checks rather than claiming unrun tests. Before publication refresh the source status or clearly retain the historical snapshot.

The canonical source is maintained in `nikolaspanayotov-jpg/VibeProjects` at `Anthropic-ipo/`. Keep future commits limited to this project. Public project notes must omit private hosting URLs, internal deployment identifiers, export paths and credentials.

Generated screenshots and PDFs are retained in the execution workspace and can be regenerated by the browser checks; they are ignored in Git. The test script, recorded results, and verification notes are versioned.

## Approved reading tools and concise brief

`reading-tools-update-2026-11-05.md` specifies the five additions. `reading-toolbox` contains local passage search; `findPassages`, `showSearchResults` and `revealSearchHash` index current DOM text and open native disclosures. Generated `passage-*` IDs must be deterministic across reloads. Preserve text-only query rendering, pagination, keyboard focus, anchor clearance and no persistence/network calls. Search controls are excluded from print and reading estimates.

`valuation-calculator` / `renderValuation` use explicitly hypothetical price/share inputs and either reported nine-month revenue ($33.242bn) or explicitly hypothetical 12-month revenue. Price × billions of economic shares yields billions of equity value; divide by billions of selected revenue. The grid varies price ±20% and shares ±10%. Never auto-annualise reported revenue, call the result enterprise value, or substitute unknown offering terms with zero. Keep invalid-input hiding, adaptive small-value labels, reset, static example and all share-count qualifications. Mobile result visibility must not obstruct controls.

`partner-map` uses native disclosures for five selected relationships; opening a card spans the grid on screen. Preserve filed facts versus analysis and the non-exhaustive scope. `evidence-tracker` enhances the existing three scenarios; statuses are analysis and dates refer to the retained evidence snapshot. Strengthening a downside scenario must not be styled as a favourable investment signal.

`investment-brief.html` is a second standalone page, reusing embedded fonts. It prints to two A4 pages at 100% scale, with browser headers/footers off. Keep the summary and dates aligned with the full guide; its print button only invokes the browser dialog. The ordinary no-JavaScript version remains printable. `tests/reading_tools.py` checks new behavior and both two-page print paths; run it alongside `tests/browser_smoke.py` after relevant changes. Generated PDFs/screenshots remain ignored.

## 10 November source refresh

Current evidence and old/new differences are recorded in `ipo-update-2026-11-10.md`. The latest source is Amendment No. 2, accession `0001628280-26-072484`. All current primary citations use it; original S-1, Amendment No. 1 and historical H1 sources remain separately labelled. There are 36 preview entries.

`offering-terms` distinguishes 825m base public shares (801,351,354 primary plus 23,648,646 secondary), the 123,750,000 company option, the conditional $26bn private placement and estimated $84.6bn net company proceeds at $74 with no option. The $3.8bn RSU tax use is distinct from the $14.2bn expected cumulative compensation expense. Google and AMD placement purchases consume existing funding commitments; never add them twice.

`valuation-bases` and the calculator’s two preset buttons use the same $74 midpoint, with 13,086,672,591 offering-summary A+N shares or 18,012,993,379 expanded-worksheet economic columns. Exclude non-economic T/F, explain fund-held shares, options, awards and rollover notes, and do not label either a final diluted valuation. The calculator still starts with the original clearly hypothetical example and divides by nine-month GAAP revenue, not the $81bn run-rate. `share-supply` keeps the selected relative release schedule, eligibility/actual selling distinction and restricted private shares explicit.

The commitment chart now uses a fixed $0–$1,000bn scale; timing views overlap. The $319.993bn maturity table retains its narrower September scope. The additional $150bn–$175bn estimate without fixed dollar commitments and developer/power guarantees must not be mechanically added to the chart. `new-financing-exposures` explains accounting and contingent exposures.

`november-developments` labels company product/research evidence and dated Reuters sentiment reporting. Event outcomes were not available at the pre-livestream review; do not turn a schedule or RSU vesting date into an IPO date. Run `tests/november_refresh.py` alongside the two existing browser scripts after a relevant refresh. Keep the separate two-page brief synchronised.

## 14 November timetable, FWP and participation update

`ipo-update-2026-11-14.md` records the source review and implementation plan. The register lists five additional FWPs with filingDate 12 November; issuer dates are 10 or 11 November and must not be conflated with filing/review dates. The latest S-1/A remains 10 November. There are 44 source previews. The official IPO FAQ expects pricing 18 November and trading 19 November EST, subject to clearance and market conditions. These are not confirmed pricing or a completed listing.

`regional-access` adds UK/EEA/Swiss/Australian/Canadian/Japanese document handoffs without claiming universal eligibility. The $120 EEA/Swiss maximum is a regional ceiling, not a new U.S. range; $70–$78 remains indicative. UK intermediaries set their own cutoffs; covered EEA/Swiss expected close is 18 November at 16:00 CET / 10:00 ET, subject to change. Australian indicative dates use AEDT and must not be treated as contradictory to the U.S. EST dates. Regional tranches are not incremental shares to add to the global offer.

`order-book` keeps Reuters/Bloomberg attribution and dates; six-times reported coverage is not an allocation probability, revenue demand or return forecast. No bank forecasts were adopted as model inputs. `roadshow-evidence` distinguishes selected customer/issuer claims and the long-period revenue-to-compute-expense ratio from the Q2–Q3 chart. The 10 November event is now a past listed date; do not infer contracts/outcomes from a schedule. All three financial/historical JSON datasets remain unchanged.

Run `tests/participation_update.py` for the new date, regional, attribution, native-disclosure and reflow checks, alongside the existing browser suites. The brief remains a two-page A4 document; keep its source links and date/status language in sync.
