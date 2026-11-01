# BeeTrains

An independent, static guide to the planned integration of local rail into Greater Manchester's Bee Network. The project lives under `/BeeTrains/`; preserve this folder's capitalisation and shared station IDs.

## Running and checking

Open `index.html` in a browser, or serve the repository root with `python3 -m http.server 8000` and visit `/BeeTrains/`. There is no build step, framework, account or backend.

Run `python3 BeeTrains/tests/browser_smoke.py` from the repository root for browser checks. This requires Python Playwright and Chromium; set `CHROMIUM_PATH` if Chromium is not on PATH. The script starts its own loopback server and writes ignored screenshots and a JSON report into `tests/artifacts/`. The page has no runtime dependency on those tools.

## Files

- `index.html`: all page HTML, CSS, SVG, JavaScript and embedded Latin WOFF2 fonts.
- `FONT-LICENSES.txt`: the unmodified SIL Open Font License notices for the two embedded font families.
- `assets/piccadilly.jpg` and `assets/README.md`: a locally served, licensed archive photograph and its attribution record.
- `bee-network-plans.md`: research brief and source context.
- `design-and-layout.md`: approved visual and interaction brief.
- `tests/browser_smoke.py`: browser acceptance checks.
- `tests/VERIFICATION.md`: recorded checks, scope and limits.

The page also includes a dated roadmap comparison, a Piccadilly transfer guide, a reader-facing update history and generated station briefs. These are all part of the same build-free HTML file.

## Content and data

The base HTML's four `[data-station-group]` lists are the single source for station records. Each entry has a stable `data-station` ID, display name, verified direct facilities URL, station code, postcode where checked, access category and review date. JavaScript derives search, list, detail and share-link records from this HTML; do not introduce a second station dataset.

`PHASES` supplies milestone dates and explanatory copy. The `services` milestone is a separate December 2027 event, with no station membership. Keep service improvements, payments, station integration and accessibility completion distinct.

Station groups were checked against indexed copies of TfGM's dedicated station list on 31 October 2026: 14 entries for December 2026, 15 for March 2027, 42 named entries under the December 2028 heading, and 25 for 2030. The source's December 2028 heading says 43 while its visible list has 42. Preserve the named list and show this discrepancy beside both the 2028 explanation and its interactive list. Avoid a headline total until TfGM reconciles it. “Lostock Parkway” is the source's displayed name; do not infer a different date or station record from that wording.

All dates describe plans. Do not automatically mark a milestone delivered when its date passes. Confirm delivery with current evidence, then update the copy and review date together. Accessibility statements must be verified separately. National Rail's published station pages were fetched for 95 entries on 31 October 2026; direct URLs were resolved from its station sitemap, with explicit aliases for differently named stations. Salford Central's National Rail page returned 404, so its TfGM station page identified in indexed material is used; its live availability and access category remain unconfirmed here. Do not guess facilities links or infer an access category from planned work.

Access categories are nominal platform-access summaries, not real-time lift status or a guarantee of level boarding. Keep future access works separate from the current category. The guide gives station-specific service enhancements only for the verified Airport and Rochdale corridor examples; other results state that a station-specific change is not confirmed in this guide.

## Interactions and state

`setPhase`, `selectStation`, `renderSearch`, `renderList` and `renderMap` coordinate the explorer. Search covers all groups. Selecting a station chooses its integration phase; choosing an incompatible phase clears the station detail. Controls are revealed only after setup succeeds; the original narrative and station lists remain readable without JavaScript.

`CORRIDORS` supplies readable branch descriptions. A selected station shown on the SVG gets a separate halo; an omitted station gets an explicit explanation and a link to its full list entry. The December 2027 service phase is text-only: no shared `data-route` path may carry a `services` token, and the diagram/list switch is hidden for that milestone. Retain the preceding diagram/list choice when returning to a station group. On mobile, phase controls occupy two rows and the selected explanation comes before the diagram.

Payment copy distinguishes the October secondary reporting's target for rail-only contactless at all Greater Manchester stations by end-2028 from station integration through 2030. Journeys and ticket conditions remain unconfirmed. Rail contactless and the daily paper ticket share a planned December 2026 launch period; do not imply a sequence between them. Source context must distinguish indexed review from live link checks and delivery confirmation.

`setPayment` switches the three worked-journey panels: rail contactless, a daily paper ticket and future integrated caps. These illustrate Glossop–Piccadilly–St Peter's Square, with no assumed price or ticket validity. Without JavaScript and in print, all three explanations remain available.

The `station` URL parameter uses stable IDs. Copying has a selectable-input fallback. No localStorage keys or persistent browser state are used. Keep history changes guarded for browsers that restrict history on local files.

## Reader tools

- The static roadmap compares station integration, rail-only payment, cross-mode tickets/caps and services. Its date links select the matching explorer panel. A dash means no additional target specified here, not a guarantee that nothing changes. The comparison is a native disclosure, initially collapsed on a narrow-screen visit; it remains readable without JavaScript.
- The selected-station bar appears only when the complete result has scrolled above the header. Its native disclosure is collapsible, and its name/date update with the current selection. `updateStationContext` adjusts anchor offsets for the measured header and bar heights. Never steal focus on scroll or keep a stale station after a phase clears the selection.
- `buildStationBrief` uses the current station record and its rendered facts, so print/download content does not have a separate dataset. It retains the research date, source URLs, unknown fares and the 2028 count discrepancy where relevant. `printStationBrief` uses the browser's print dialog with a station-only print mode; `afterprint` restores the full page and title. `downloadStationBrief` creates a standalone, script-free HTML file with inline styles. No export request is sent to a server.
- Keep station briefs to one A4 page with the default print stylesheet. Browser checks cover Glossop, Flowery Field, Stockport and Salford Central, including planned works, source discrepancies and unconfirmed access.
- The update history distinguishes dates of published plans from dates of changes to this guide. Never infer an operational launch from an editorial update or automatically advance statuses when a target date passes.

## Piccadilly transfer guidance

The transfer section is based on Network Rail's accessible guide and September 2025 station map, both retrieved on 1 November 2026, plus National Rail's Passenger Assist information. It describes nominal lift routes and assistance planning, not live equipment availability or a guaranteed step-free journey. Keep TfGM alert links as external checks and retain the indexed-source limitation.

Use the current guide URL ending `/2022/08/Manchester-Piccadilly-Station-Guide-Accessible.pdf`. The older indexed `/2022/11/Manchester-Piccadilly-accessible-station-guide.pdf` returned 404 during research. Recheck source URLs before substituting either one.

## Visual conventions

Preserve the six CSS colour variables, Barlow Condensed headings, Source Sans 3 body text and restrained rail-atlas composition. Fonts are embedded so the page does not depend on a Google Fonts request; retain their licence notices. The SVG depicts selected corridors, not a complete travel map, fare boundary or live railway state. Complete group membership is available in the HTML station list. Supplementary diagram links have equivalent large buttons in that list. The Piccadilly photograph is a historical image, uploaded in 2012, and retains a visible source and CC BY-SA 3.0 credit. Do not present it as a current image of Bee Network rail services.

Check mobile widths first, native keyboard interaction, visible focus, reduced motion, print and the no-JavaScript fallback after relevant changes. Keep runtime assets self-contained and source links beside factual claims.
