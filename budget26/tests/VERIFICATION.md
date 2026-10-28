# Budget 26 verification

Edition: 28 October 2026. The page and its copy revision were pushed to GitHub in commits a751c66 and 5d9f210. The checks below assess the implementation and subsequent audience/comparison/example/glossary/timeline additions, not live hosting or deployment.

## Passed

- `python3 tests/static_audit.py`: all 48 policy entries retain the original inventory/order and numerical values across the combined summary, comparisons, metadata and expanded prose, in the approved six groups. Summaries and expanded prose are edited for clarity rather than compared verbatim with the source. Six takeaways, twenty timeline rows and eight OBR assessment points are present. Both forecast tables match the markdown cell for cell. IDs are unique; fragments and local-document references resolve; source citations remain present. The four reading routes/twelve links, three comparison panels, worked-example arithmetic/assumptions, six focusable definitions and key timeline dates/event labels are checked.
- `node --check` on the extracted inline script: JavaScript syntax passes.
- `BUDGET26_LINKEDOM_PATH=/tmp/budget26-linkedom-worker.mjs node tests/control_runtime.mjs`: eleven groups of checks pass against the actual page script. These exercise initialisation; multi-word closed-detail search and topic AND combinations; all topic counts and synchronisation; filtered/repeated/nested/invalid fragments; all twelve audience links recovering filtered targets; search within comparison values and closed worked examples; deep links into examples; all six glossary links and repeated return-to-origin focus including closed/filtered policy recovery; six table-derived chart series; denied/successful clipboard paths including every copy button; full print-state restoration and failure recovery; and mobile Contents Escape/focus behaviour. Anchor navigation and hashchange delivery are explicitly modelled in the DOM suite.
- Structural inspection with lxml confirms all 48 native policy disclosures contain their copy controls and source references. Inputs have associated labels.
- Palette text contrast passes WCAG AA for ink, muted text and accent against both white and the page background, including white text on the accent.
- The copy review found ten exact summary/detail duplicates and 35 expanded paragraphs starting with their full summary. Both counts are now zero. All 15 lowercase summary openings were corrected. Three short measures use source-only disclosures; all 48 disclosures retain citations and copy controls. Qualitative source fidelity was also reviewed separately, because numerical checks cannot prove meaning is preserved.

The optional DOM test dependency was obtained from WebReflection/linkedom's standalone worker.js, Git blob `31bb78a1d7c77d689ddaf3048b22b7b51a47b59e`. It is stored temporarily outside the project, not bundled with the webpage.

## Browser checks not completed

Chromium could not launch within the execution sandbox: socket operations were rejected with `Operation not permitted`. A request for the additional runtime network permission was cancelled before the browser suite ran. A subsequent in-sandbox launch with Chromium's crash reporting disabled still failed on a socket shutdown operation.

The latest browser-suite attempt failed before browser launch: opening the loopback HTTP server socket raised `PermissionError: [Errno 1] Operation not permitted`. The suite now includes the new reading routes, comparison/example search, glossary return path, labelled timeline and no-JavaScript reading aids, but these native browser checks have not run successfully.

No mobile/desktop screenshots were produced or visually reviewed. Native keyboard/control behaviour, actual clipboard permissions, real print/PDF rendering, responsive layout, 200% zoom and font-failure browser behaviour remain unverified. The LinkeDOM checks use explicit stand-ins for focus, selection, scrolling, layout dimensions, window events and clipboard; they do not establish browser or accessibility conformance.

The complete browser smoke suite is provided as `browser_smoke.py`. On a machine that can launch Chromium, run `python3 tests/browser_smoke.py` from the project folder. It serves the actual page under /budget26/, also tests file:// and no-JavaScript reading, writes screenshots and a print PDF under artifacts/, and fails on page/console errors. Inspect the images after a successful run.
