# Budget 26 verification

Edition: 28 October 2026. The page, copy revision and reader improvements were pushed to GitHub in commits a751c66, 5d9f210 and 380a119. The checks below assess the local implementation under a nested static-hosting path; they do not establish production deployment status.

## Passed

- `python3 tests/static_audit.py`: all 48 policy entries retain the original inventory/order and numerical values across the combined summary, comparisons, metadata and expanded prose, in the approved six groups. Summaries and expanded prose are edited for clarity rather than compared verbatim with the source. Six takeaways, twenty timeline rows and eight OBR assessment points are present. Both forecast tables match the markdown cell for cell. IDs are unique; fragments and local-document references resolve; source citations remain present. The four reading routes/twelve links, three comparison panels, worked-example arithmetic/assumptions, six focusable definitions and key timeline dates/event labels are checked.
- `node --check` on the extracted inline script: JavaScript syntax passes.
- `BUDGET26_LINKEDOM_PATH=/tmp/budget26-linkedom-worker.mjs node tests/control_runtime.mjs`: eleven groups of checks pass against the actual page script. These exercise initialisation; multi-word closed-detail search and topic AND combinations; all topic counts and synchronisation; filtered/repeated/nested/invalid fragments; all twelve audience links recovering filtered targets; search within comparison values and closed worked examples; deep links into examples; all six glossary links and repeated return-to-origin focus including closed/filtered policy recovery; six table-derived chart series; denied/successful clipboard paths including every copy button; full print-state restoration and failure recovery; and mobile Contents Escape/focus behaviour. Anchor navigation and hashchange delivery are explicitly modelled in the DOM suite.
- Structural inspection with lxml confirms all 48 native policy disclosures contain their copy controls and source references. Inputs have associated labels.
- Palette text contrast passes WCAG AA for ink, muted text and accent against both white and the page background, including white text on the accent.
- The copy review found ten exact summary/detail duplicates and 35 expanded paragraphs starting with their full summary. Both counts are now zero. All 15 lowercase summary openings were corrected. Three short measures use source-only disclosures; all 48 disclosures retain citations and copy controls. Qualitative source fidelity was also reviewed separately, because numerical checks cannot prove meaning is preserved.

The optional DOM test dependency was obtained from WebReflection/linkedom's standalone worker.js, Git blob `31bb78a1d7c77d689ddaf3048b22b7b51a47b59e`. It is stored temporarily outside the project, not bundled with the webpage.

## Native browser checks completed

`python3 tests/browser_smoke.py` completed in Chromium **154.0.8037.57** on 28 October 2026: **20 scenarios passed, one skipped, zero page/console errors**. The managed runner still needed additional network permission for its loopback HTTP server and Chromium; earlier socket restrictions are no longer blocking this HTTP-based suite.

- The actual page loads under `/budget26/`, with the optional Google Fonts stylesheet replaced by empty CSS to exercise the system-font fallback.
- All twelve audience links recover filtered policies and focus their headings. Searches find closed detail, comparison values and worked examples. Topic counts and combined filters are correct.
- The 24%/44%/49% explanation sits immediately after the property-income entry, following the savings-income entry. It remains visible for either related tax, disappears for pension-only searches, and is included/restored correctly during print. Desktop/mobile placement screenshots are recorded as desktop-tax-context.png and mobile-tax-context.png.
- Every native policy disclosure and all 48 copy controls work. The denied-permission fallback and success feedback pass; a separate unmodified Clipboard API check writes and reads the correct URL with Chromium clipboard permissions granted.
- All six glossary links focus their definitions and return to the original passage. Changed, repeated, nested and malformed fragments are handled. All six charts reproduce their source table values and year types.
- Layouts fit **320, 390, 768 and 1440 CSS pixels**, including checks with policy disclosures open. The mobile menu closes on selection/Escape. Keyboard skip navigation, visible focus, reduced-motion preference and **200% CSS zoom** pass.
- A **390 × 844** Chromium context with mobile/touch emulation and a 3× device scale exercises taps through the reading routes, comparison, both worked examples, glossary return and timeline.
- Reading routes, comparisons, worked examples, definitions and native disclosures remain available with JavaScript disabled.
- Print/PDF reveals all policies, restores the exact filter/disclosure state and handles a simulated print failure. The generated **25-page A4 PDF** contains all 48 policy titles and the worked-example amounts. Page margins, heading breaks and source-link wrapping were corrected after visual review.

Screenshots were produced and visually inspected for the desktop hero/routes/policies, mobile hero/OBR, touch-mobile reading routes/comparison/examples/glossary/timeline, 200% CSS zoom, and sample print pages. They are local ignored artifacts under `tests/artifacts/`; `results.json` records completion, browser version, passes, skips and errors. The native suite now waits for scheduled fragment focus before asserting another control's focus and installs the print-failure stub without accidentally invoking it.

## Remaining limits

The **file://** navigation check is skipped because this Chromium runtime reports `ERR_BLOCKED_BY_ADMINISTRATOR`. The test records that exact policy block; other file-loading errors still fail. Static HTTP hosting and no-JavaScript reading passed. No attempt was made to disable the browser administrator policy.

Testing used headless Chromium and touch/mobile emulation, not physical phones, Safari, Firefox or screen-reader software. Screenshots use the system-font fallback; remote Google Font loading was not tested. CSS zoom is not a physical device or browser-UI zoom test. These checks do not establish complete accessibility conformance.

Run `python3 tests/browser_smoke.py` from the project folder on a runtime with Python Playwright, Chromium and local socket access. Screenshots and a print PDF are written under `artifacts/`; inspect the images as well as the exit status and recorded skips.
