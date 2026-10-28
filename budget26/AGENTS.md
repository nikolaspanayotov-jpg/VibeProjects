# Budget 26

A neutral, public Budget explainer for the 28 October 2026 edition. Intended static-hosting path: `/budget26/`. Apply the VibeProjects root rules and shared frontend-design skill.

## Run and architecture

Open `index.html` directly, or run `python3 -m http.server 8000` in this folder. The runtime is one HTML file with inline CSS and JavaScript. No build, package installation, API, account or storage is required. An optional Public Sans Google Fonts stylesheet has system-font fallbacks.

- `key-budget-points.md` is the editorial source of truth; preserve it and the original PDF in `sources/`.
- `build-plan.md` records the approved design and behaviour.
- `index.html` contains all 48 policy entries, six topic groups, twenty timeline rows, eight OBR assessment points and both forecast tables as static HTML. There is no runtime Markdown parser or committed authoring generator. Give the main announcement in the summary and additional eligibility, exclusions, dates or caveats in Details and sources. If no extra explanation is needed, use a Sources disclosure with citations and the copy control; do not repeat the summary.
- Chart values are read from the two HTML tables. Do not duplicate their numerical data in JavaScript.

## Content and public links

Keep the folder name, policy IDs and main section fragments stable. Check citations, geographical scope, dates, amounts and consultation qualifications when editing. The edition is historical; do not turn its planned dates into claims of enactment. Preserve the distinction between OBR forecasts and government policy. PDF citations use printed pages; add six for PDF page anchors. Keep the Annex A access limitation visible in Sources.

Search indexes all words across titles, summaries, dates, geography and complete source detail. Search and one selected topic combine with AND. The 48 policy entries are the result count; overview, forecasts, timeline and sources are not policy results. Initial, changed and repeated fragments reveal filtered articles, open disclosures and focus the target. Clipboard failures expose a selected URL. Print snapshots reveal all content and restore the reader's filters and disclosure states afterwards.

The shared explanation of the 24%/44%/49% rates belongs immediately after the property-income entry, following both affected taxes. Its data-related-policies attribute keeps it visible when savings or property income is shown, and hides it for unrelated search results. Printing reveals it with all policies and then restores the filtered state.

Four audience reading routes contain twelve ordinary policy links. They curate a reading path, not an entitlement determination. Three comparison panels replace repeated numerical summary prose and are indexed by search. The two worked examples show qualifying 2027–28 mileage (£6,200 for 12,000 miles) and a qualifying £10,000 LISA withdrawal (£500 lower charge); preserve their assumptions and reimbursement/tax-relief distinction. Six dotted-underlined terms link to static, focusable glossary definitions. JavaScript remembers only the last term link in memory; the glossary return button navigates to its stable read-term-* fragment and restores focus. Normal links and definitions remain readable without JavaScript.

Timeline labels Starts, Relief ends and Planned describe the announced schedule, not enacted status. Keep month-only dates at month precision. The 30 June 2027 relief expiry, 1 July fuel-duty change, 1/6 April 2027 split, 2 January 2028 private-hire measure and separate pension/carer dates are deliberate.

## Design and accessibility

Public Sans/system sans; teal #006B63, ink #162D3A, muted #526674, background #F4F7F8, white #FFFFFF and lines #CDD8DE. The calendar rail is the main visual device. Keep text left aligned and avoid decorative imagery, counters or motion. At 960px use a 220px sticky sidebar; below it use a native topic select. Preserve keyboard focus, 44px controls, reduced-motion support, no-JavaScript reading and no global overflow. The forecast tables may scroll inside their labelled containers.

## Verification

Run `python3 tests/static_audit.py` and `python3 tests/browser_smoke.py`. Browser tests require Python Playwright and Chromium; use `/usr/bin/chromium` by default or set `BUDGET26_CHROMIUM` to another executable. Test-only tooling is not required by readers. Generated screenshots and results go in `tests/artifacts/` and are ignored by Git. Inspect the mobile and desktop screenshots before reporting success. Do not infer tests passed just because their scripts exist.

The browser suite also exercises 390px touch emulation, no-JavaScript reading, native clipboard permission, print/PDF and 200% CSS zoom. Its result record distinguishes completed checks, skips and errors. A Chromium administrator-policy block on file:// is recorded as a specific skip; other navigation errors fail. HTTP-hosted tests must still pass. Print styles provide 14mm vertical/12mm horizontal page margins, keep headings with following content and wrap source URLs as ordinary block links.

`tests/control_runtime.mjs` executes the actual page script against LinkeDOM with explicitly modelled browser-only APIs. Run with an installed `linkedom` package or set `BUDGET26_LINKEDOM_PATH` to a standalone worker module, e.g. `BUDGET26_LINKEDOM_PATH=/tmp/budget26-linkedom-worker.mjs node tests/control_runtime.mjs`. It tests DOM state and handlers, not native clicks, layout, clipboard permissions or visual rendering. See tests/VERIFICATION.md for the checks actually completed.

Only change this project. Building and checking locally does not publish the page; repository updates and deployment are separate actions.
