# BeeTrains

An independent, static guide to the planned integration of local rail into Greater Manchester's Bee Network. The project lives under `/BeeTrains/`; preserve this folder's capitalisation and shared station IDs.

## Running and checking

Open `index.html` in a browser, or serve the repository root with `python3 -m http.server 8000` and visit `/BeeTrains/`. There is no build step, framework, account or backend.

Run `python3 BeeTrains/tests/browser_smoke.py` from the repository root for browser checks. This requires Python Playwright and Chromium; set `CHROMIUM_PATH` if Chromium is not on PATH. The script starts its own loopback server and writes ignored screenshots and a JSON report into `tests/artifacts/`. The page has no runtime dependency on those tools.

## Files

- `index.html`: all page HTML, CSS, SVG, JavaScript and embedded Latin WOFF2 fonts.
- `FONT-LICENSES.txt`: the unmodified SIL Open Font License notices for the two embedded font families.
- `bee-network-plans.md`: research brief and source context.
- `design-and-layout.md`: approved visual and interaction brief.
- `tests/browser_smoke.py`: browser acceptance checks.
- `tests/VERIFICATION.md`: recorded checks, scope and limits.

## Content and data

The base HTML's four `[data-station-group]` lists are the single source for station records. Each entry has a stable `data-station` ID and display name. JavaScript derives search, list and share-link records from this HTML; do not introduce a second station dataset.

`PHASES` supplies milestone dates and explanatory copy. The `services` milestone is a separate December 2027 event, with no station membership. Keep service improvements, payments, station integration and accessibility completion distinct.

Station groups were checked against TfGM's live station list on 31 October 2026: 14 entries for December 2026, 15 for March 2027, 42 named entries under the December 2028 heading, and 25 for 2030. The source's December 2028 heading says 43 while its visible list has 42. Preserve the named list and avoid a headline total until TfGM reconciles the discrepancy. “Lostock Parkway” is the source's displayed name; do not infer a different date or station record from that wording.

All dates describe plans. Do not automatically mark a milestone delivered when its date passes. Confirm delivery with current evidence, then update the copy and review date together. Accessibility statements must be verified separately. The station-information link opens TfGM's official station directory, rather than a guessed per-station URL.

## Interactions and state

`setPhase`, `selectStation`, `renderSearch`, `renderList` and `renderMap` coordinate the explorer. Search covers all groups. Selecting a station chooses its integration phase; choosing an incompatible phase clears the station detail. Controls are revealed only after setup succeeds; the original narrative and station lists remain readable without JavaScript.

The `station` URL parameter uses stable IDs. Copying has a selectable-input fallback. No localStorage keys or persistent browser state are used. Keep history changes guarded for browsers that restrict history on local files.

## Visual conventions

Preserve the six CSS colour variables, Barlow Condensed headings, Source Sans 3 body text and restrained rail-atlas composition. Fonts are embedded so the page does not depend on a Google Fonts request; retain their licence notices. The SVG depicts selected corridors, not a complete travel map, fare boundary or live railway state. Complete group membership is available in the HTML station list. Supplementary diagram links have equivalent large buttons in that list.

Check mobile widths first, native keyboard interaction, visible focus, reduced motion, print and the no-JavaScript fallback after relevant changes. Keep runtime assets self-contained and source links beside factual claims.
