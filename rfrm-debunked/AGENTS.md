# rfrm debunked

A public, critical evidence guide to the user-supplied Economic Rescue Plan. It covers exactly 64 numbered measures and 37 unnumbered supporting claims, reviewed 27 October 2026. Expected hosting path: `/rfrm-debunked/` in this repository’s existing GitHub Pages site. No deployment is performed by the app.

## Run

Open `index.html` directly, or run `python3 -m http.server 8000` from this folder. No installation, build, API, storage, authentication or network request is needed to read/search the page. External source links only navigate when selected.

## Architecture and updates

- `index.html`: complete generated static document, inline CSS and focused DOM-derived JavaScript.
- `authoring/template.html`: page structure, styles and interactions.
- `authoring/{energy,housing,infrastructure,deregulation,tax,support}.json`: reviewed article/source content. Article fields: id, number (null for supporting), category, page, title, proposal, counter, critique, sourceIds, related, evidenceLabel, optional evidencePanels and dependencies. Source fields: id, publisher, title, date, URL, accessed, finding.
- `authoring/highlights.json`: eight static headline panels: three initial findings and five inside a native overview disclosure. These do not add to the 101 policy result count. The 64-number index is also a native disclosure.
- `authoring/audit.json`: all 20 policy lines reaching an absolute £1bn in any forecast year, tested against six disclosure dimensions. Display as 20 native disclosures with six labelled checks; shared full notes may be linked from a common-notes glossary. Keep unknown disclosure separate from falsity.
- `authoring/updates.json`: verified official provenance and additional source records.
- `authoring/tables.json`: literal source table strings, including blank cells and parentheses. Never infer zero from blank or silently reconcile rounded totals.
- `authoring/generate.py`: optional Python3 authoring helper; run `python3 authoring/generate.py` after edits. It validates content lengths/references, writes static `index.html` and the coverage/source audit in `RESEARCH.md`. Readers need no build.
- `economic-rescue-plan-summary.md`: preserved source notes. Do not edit to fit the critique. Original SHA256: 6bd56fc035838ee613067efd673beaf0c02a8c3ae5893e38e489ac0d5ac76c8f.
- `PLAN.md`: approved brief. `RESEARCH.md`: provenance/evidence limitations, summary/table inventory and exact source register.

Keep the folder name, `measure-01`…`measure-64` and descriptive `claim-*` IDs permanent; published links depend on them. Original numbering/order/category grouping must survive edits. Never add a measure 65. Every substantive addition needs a real opened source with publisher/title/date (or explicitly unknown), URL, access date and supported finding. Check jurisdiction, legal commencement and forecast vintage. Attributed source assertions are not automatically verified facts. The official publisher-hosted plan and launch were verified on 27 October 2026; preserve the scoped version comparison in RESEARCH.md. Do not claim byte-for-byte identity or independent certification of the in-house fiscal model.

All articles are static HTML and native details. Search indexes headings, proposals, counterarguments, analysis, evidence labels, worked examples and dependency text directly from the DOM, including closed details. Headline panels and the audit do not become policy search results. The four everyday shortcuts in `generate.py` collect explicit existing categories/entries; shortcut, search and original topic combine with AND. Repeating a shortcut removes it; Clear all filters and policy fragments clear shortcut, topic, query and evidence-label filters. Search and topic combine with AND; #12 is an exact measure query. Hash navigation clears filters and opens/focuses the article. Before/after-print handlers temporarily reveal/open all then restore state. Clipboard failure reveals/selects the permanent URL.

## Design

Apply the repository frontend-design skill and approved brief. Tokens: --bg #F4F6FA, --surface #FFF, --ink #172033, --muted #526079, --accent #234BB5, --analysis #71345D. Georgia major headings, system sans body 18px/1.65, 68ch reading measure. Restrained rules and original numbering carry the hierarchy. Sidebar 220px/sticky, stack below 900px; touch targets 44px, visible focus and no global overflow. No truth score, stock imagery, decorative charts, framework or runtime Markdown fetch.

Evidence panels and dependencies stay inside each native analysis expansion and remain searchable. Each expansion ends with Back to results, preserving filters. The opening overview includes accessible UC arithmetic and paired annual NI/levy bars generated from existing source-backed notes/table data; do not imply predicted effects or omit taper assumptions. On phones the enhanced sticky reading bar shows the current filter view and returns focus to topic/search; retain scroll clearance and hide it without JavaScript and in print. Print snapshots include shortcut state and every native disclosure.

## Checks

Run `python3 tests/static_audit.py`. With Python Playwright and Chromium installed, run `python3 tests/browser_smoke.py`; it uses a temporary local static server and also exercises file://. Screenshots/results are written under `tests/artifacts/` (generated review artefacts, not required hosting files). Inspect 390px and 1440px screenshots. Browser tests cover searches, AND filters/reset, multiple disclosures, initial/changed/filtered hashes, copy denial fallback, print/restoration, 320px overflow, 200% layout, reduced motion, keyboard and no-JavaScript. Read the latest actual results; do not infer tests passed merely from their existence.

`tests/control_runtime.mjs` runs the actual page script against LinkeDOM with explicitly modelled browser APIs. Install the test-only dependency with `npm install --prefix tests`, then run `npm test --prefix tests`. For an existing standalone LinkeDOM worker, use `LINKEDOM_WORKER_PATH=/path/to/worker.mjs node tests/control_runtime.mjs`. These checks exercise event handlers and DOM state, including every copy button and topic control, nested fragment recovery, and print restoration. They do not establish native clicks, keyboard defaults, layout, or actual clipboard/print permission behavior. The browser suite separately clicks every disclosure and copy button when browser execution is available. Neither test dependency is needed by readers.

Fragment handling must reveal nested citations and audit disclosures, including repeated fragment links, without resetting topic-filter clicks. Copy retries clear stale feedback and previous fallback fields. Printing waits for `afterprint` in non-blocking browsers; failures restore state and show recovery text.

Only modify this project. Keep the app build-free and all project resources relative. Publishing/committing is handled after integration review.

`python3 tests/mobile_review.py` runs real Chromium touch/viewport checks at 320, 375, 390, 430, 768, 844 landscape and 1440 CSS pixels, with screenshots/results in `tests/artifacts/mobile-review/`. Both browser scripts use a temporary loopback HTTP server. The smoke suite records file-URL checks as skipped only when managed browser policy explicitly blocks them. Preserve genuine failures; do not bypass browser policies. The 28 October real-browser review passed HTTP, native disclosure, keyboard, touch, no-JavaScript and print checks; see tests/VERIFICATION.md for exact scope. No Safari or physical-device coverage is implied.

Active chips remove one AND filter at a time using textContent, never query HTML; removal returns focus to the relevant visible input or explorer heading. The six-label evidence select participates in reset/hash and print snapshots. The static funding route links levy → employer NI → sequencing assumptions with previous/next navigation. Six native glossary definitions use existing sources and explicit contextual links without rewriting article or quotation text. Correction actions only open prefilled GitHub issue drafts; HTTP(S) uses the current article URL, while file:// and no-JavaScript retain a public repository reference and never include local paths. Editorial dates distinguish the 27 October evidence review from 28 October interface changes.
