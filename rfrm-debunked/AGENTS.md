# rfrm debunked

A public, critical evidence guide to the user-supplied Economic Rescue Plan. It covers exactly 64 numbered measures and 37 unnumbered supporting claims, reviewed 27 October 2026. Expected hosting path: `/rfrm-debunked/` in this repository’s existing GitHub Pages site. No deployment is performed by the app.

## Run

Open `index.html` directly, or run `python3 -m http.server 8000` from this folder. No installation, build, API, storage, authentication or network request is needed to read/search the page. External source links only navigate when selected.

## Architecture and updates

- `index.html`: complete generated static document, inline CSS and focused DOM-derived JavaScript.
- `authoring/template.html`: page structure, styles and interactions.
- `authoring/{energy,housing,infrastructure,deregulation,tax,support}.json`: reviewed article/source content. Article fields: id, number (null for supporting), category, page, title, proposal, counter, critique, sourceIds, related. Source fields: id, publisher, title, date, URL, accessed, finding.
- `authoring/tables.json`: literal source table strings, including blank cells and parentheses. Never infer zero from blank or silently reconcile rounded totals.
- `authoring/generate.py`: optional Python3 authoring helper; run `python3 authoring/generate.py` after edits. It validates content lengths/references, writes static `index.html` and the coverage/source audit in `RESEARCH.md`. Readers need no build.
- `economic-rescue-plan-summary.md`: preserved source notes. Do not edit to fit the critique. Original SHA256: 6bd56fc035838ee613067efd673beaf0c02a8c3ae5893e38e489ac0d5ac76c8f.
- `PLAN.md`: approved brief. `RESEARCH.md`: provenance/evidence limitations, summary/table inventory and exact source register.

Keep the folder name, `measure-01`…`measure-64` and descriptive `claim-*` IDs permanent; published links depend on them. Original numbering/order/category grouping must survive edits. Never add a measure 65. Every substantive addition needs a real opened source with publisher/title/date (or explicitly unknown), URL, access date and supported finding. Check jurisdiction, legal commencement and forecast vintage. Attributed source assertions are not automatically verified facts. Do not claim official PDF provenance or independent certification of the in-house fiscal model.

All articles are static HTML and native details. Search indexes heading/proposal/counter/analysis text directly from the DOM, including closed details. Search and topic combine with AND; #12 is an exact measure query. Hash navigation clears filters and opens/focuses the article. Before/after-print handlers temporarily reveal/open all then restore state. Clipboard failure reveals/selects the permanent URL.

## Design

Apply the repository frontend-design skill and approved brief. Tokens: --bg #F4F6FA, --surface #FFF, --ink #172033, --muted #526079, --accent #234BB5, --analysis #71345D. Georgia major headings, system sans body 18px/1.65, 68ch reading measure. Restrained rules and original numbering carry the hierarchy. Sidebar 220px/sticky, stack below 900px; touch targets 44px, visible focus and no global overflow. No truth score, stock imagery, decorative charts, framework or runtime Markdown fetch.

## Checks

Run `python3 tests/static_audit.py`. With Python Playwright and Chromium installed, run `python3 tests/browser_smoke.py`; it uses a temporary local static server and also exercises file://. Screenshots/results are written under `tests/artifacts/` (generated review artefacts, not required hosting files). Inspect 390px and 1440px screenshots. Browser tests cover searches, AND filters/reset, multiple disclosures, initial/changed/filtered hashes, copy denial fallback, print/restoration, 320px overflow, 200% layout, reduced motion, keyboard and no-JavaScript. Read the latest actual results; do not infer tests passed merely from their existence.

Only modify this project. Keep the app build-free and all project resources relative. Publishing/committing is handled after integration review.
