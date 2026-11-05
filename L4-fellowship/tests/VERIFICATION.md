# Implementation verification

Date: 3 November 2026. Result: **passed** in Playwright Chromium.

The page was exercised from a localhost server scoped to `L4-fellowship`, and separately by opening `index.html` directly from disk. All runtime content is local; no required external network requests or JavaScript page errors were observed.

## Browser checks performed

- Clean first visit: all 37 index links, no fabricated completion, no assumed assessment date.
- Search by topic/identifier, combined filters, clearing filters and empty results.
- All 37 complete lesson views, answer guides, personal response forms, preparation targets and source links.
- Response, confidence, learning and coverage persistence through reload; text containing HTML remains plain text.
- Review scheduling: help/partial/independent outcomes, seven-to-fourteen-day progression and manual dates. A Pacific/Kiritimati browser at a UTC date boundary confirmed local calendar dates.
- S12's two stakeholder slots and S13's forecast/mining worksheet persist; the S13 plot has an accessible description and the documented exact-value table.
- Evidence validation, two-KSB rationales, linked/reviewed states, edit, delete/undo and unfinished draft recovery.
- Practice: guidance hidden before reveal, pause/reload/resume, timer expiry preserves the response, ratings schedule reviews and mixed discussion contains K/S/B topics.
- Study plan, priority topics and conditional AP03 filters, reconciling 17 project-route and 20 discussion-route KSBs.
- Six practical exercises and all four CSV downloads. Fixtures reconcile to 300 requests, 30 missing completion dates, four missing service IDs, eight unmatched S99 records and 357 rows after the deliberately flawed join. Monthly series: 12 observations; feedback: 36 comments.
- JSON export; malformed, unsupported-version and unknown-KSB import rejection; import preview; default conflict retention; non-conflicting additions; explicit replacement confirmation.
- Corrupt storage remains untouched and downloadable. Simulated quota failure leaves an exportable temporary session.
- All main views checked for horizontal page overflow at 320, 390, 768 and 1280px. Desktop screenshots use 1440px. The tablet KSB index breakpoint was corrected after an observed overflow.
- Keyboard entry through the skip link, focus into main content and the next study action; reduced-motion mode and print navigation suppression.
- Direct file opening loads the full curriculum and synthetic forecast without `fetch()` or a server.

JavaScript syntax checks passed for the application and curriculum. The curriculum compiler checks the 37-item set and preserves the complete answers, examples, templates, evidence prompts and follow-ups. The source hash is embedded in `curriculum.js`.

## Visual inspection and limits

Desktop and mobile screenshots were inspected for hierarchy, legibility, reading surfaces, index layout and overflow. Test output and screenshots are saved under `/tmp/l4-qa` during this session and are not application data or committed assets.

This is focused browser verification, not a complete WCAG conformance audit or cross-browser certification. Provider-specific assessment requirements and detailed current-law/source verification remain as described in `solutions.md`. No real workplace evidence, model result or stakeholder feedback is asserted by the synthetic examples. Hosted-page offline reload and cloud synchronisation are not implemented; direct file opening and JSON transfer are supported.

## Guided lessons, worked project and readiness — 3 November 2026

Both the existing smoke check and `browser_enhancements.py` passed after the improvements. No page errors were observed. Enhancement screenshots/results are kept under `/tmp/l4-enhancements-qa`; the regression output is under `/tmp/l4-regression-qa` in this session.

- All 37 KSBs contain the short explanation, worked example, common mistake and probing question, while retaining the complete original guide and evidence prompts.
- Mobile Learn / Worked example / My answer / Practise jumps open and focus the correct content. Detailed guidance remains expandable, and sticky navigation does not cover the response field.
- Genuine-personal-example confirmation persists, clears on edits and stays separate from evidence and confidence. A legacy v1 record retains its response, confidence, gap note and settings while defaulting the new confirmation to false.
- The readiness matrix filters correctly. A seeded combination of partial recall, a draft example and missing evidence produces the expected three distinct actions and routes each to the matching KSB. User-entered markup stays plain text.
- Probing practice questions use their own question type, preserve responses across pause/reload and remain compatible with backup validation.
- The worked project has six navigable stages, eight annotated artefacts, links covering all 37 KSBs and a downloadable Markdown portfolio. Its approved example lookup downloads five unique reference rows.
- The portfolio's four SQL queries execute against the actual downloaded fixtures: duplicate S2 count two, flawed join 357 rows, approved join 300 rows, and missing/unmatched counts four/eight.
- The dashboard derives 300 requests, 270 completed, 30 open and median eight days from the same fixture generator as the CSV downloads. Service counts reconcile to 300. Feedback totals are 42 theme assignments across 36 comments, with explicit multiple-theme and sampling caveats.
- Project navigation/downloads do not create personal evidence, mark learning complete or copy fictional experience into a personal response. “Write my own example” opens the relevant empty/previously saved response without filling it from the case.
- New views reflow without page overflow at 320, 390, 768 and 1280px; enlarged reading text, keyboard jumps and direct file opening also work. Phone/desktop screenshots were inspected for the short lesson, readiness and project layouts.

## Analysis labs, branching scenarios and misconception quizzes — 4 November 2026

The existing smoke and guided-study checks passed with the new tools. The focused `browser_learning_tools.py` check also passed; its results and screenshots are under `/tmp/l4-learning-tools-qa` for this session. These are Chromium checks, not a complete accessibility or cross-browser certification.

- The statistics lab's outlier, observed-value exclusion and three missing-value treatments agree with independent Python mean/median calculations. Keyboard range interaction, reload persistence and lab-only reset were exercised.
- All four join types, with and without a duplicate lookup key, agree with actual SQLite output counts, distinct request IDs and sums. UNION/UNION ALL retain their different duplicate semantics and use compatible request tables.
- Twenty-four forecast configurations agree with independent regressions and RMSE calculations. Only available post-training observations enter error; beyond-history projections stay separate. Narrow-screen axis labels were simplified after visual inspection found an overlap; the check asserts visible month-label bounds do not overlap.
- All three scenarios follow their authored decision graphs. The check exercises risky and defensible routes, validates nonempty justifications, recovers drafts/outcomes through reload and verifies that imported paths cannot invent transitions. Restart affects one scenario only.
- The 30-question bank covers all KSB identifiers as conceptual revision material. Feedback is hidden until submission, recorded once through reload, and includes an explanation. The previously-missed and due queues, next-day incorrect review, correct-answer spacing and paused-set recovery were exercised.
- Lab, scenario and quiz work does not modify KSB recall, learning, confidence, personal-example confirmation or evidence automatically.
- JSON backups include new tool progress and unfinished sets. Merge preserves conflicting current settings and adds new records; old v1 imports preserve newer tool work. Invalid identifiers (including prototype-like keys), values and graph paths are rejected without changing state. Explicit replacement restores the complete tool state.
- New views reflow at 320, 390, 768 and 1280px, with enlarged reading text and direct file opening supported. Phone and desktop screenshots were inspected for lab results, question feedback and scenario choices. No JavaScript page errors were observed.

Question answers are canonical in the `solutions.md` appendix. The compiler validates 30 stable question IDs, KSB coverage, scenario reachability, acyclic paths, the saved-route length limit and the third authored-source hash. The question counts are practice information, not an EPA Pass prediction or verified workplace competence.

## 5 November 2026 — reasoning tools, notebook and connections

All four browser suites passed against the updated local page in headless Chromium (Playwright 1.64.1). JavaScript syntax checks passed for the application and curriculum. The authoring compiler passed ID, choice, KSB reference, annotation and coverage checks; all four source hashes were verified alongside the 37 lessons and 30 misconception questions.

Commands used in this environment:

```bash
PYTHONPATH=/tmp/l4-authoring python3 tests/compile_curriculum.py
node --check /tmp/extend-app.js
node --check curriculum.js
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_smoke.py --url http://127.0.0.1:8000/ --output /tmp/l4-core-regression
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_enhancements.py --url http://127.0.0.1:8000/ --output /tmp/l4-guided-regression-new
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_learning_tools.py --url http://127.0.0.1:8000/ --output /tmp/l4-learning-regression-new
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_reasoning_tools.py --url http://127.0.0.1:8000/ --output /tmp/l4-reasoning-qa
```

`/tmp/extend-app.js` was extracted from the shipped inline script. The new suite exercises all four correction challenges and six method decisions, required justifications, feedback hiding/reveal and reload persistence. Its SQLite calculation independently confirms the join example's five rows / total 90 versus source total 60. It checks six-part K/S/B example annotations, per-KSB drafts, clearing self-checks on edit, cancellation/acceptance of personal-response replacement and preservation of evidence/recall/coverage.

Notebook summaries, approved reference strings and manual verification dates persist and appear in the linked lessons and workshop. Malicious-looking note HTML and `javascript:` reference text stay inert. All nine connections collectively cover 37 KSBs, filter correctly and display actual matching evidence with its rationales. Combined responses save separately.

Synthetic records round-trip in JSON and the Markdown summary. Conflicts keep current records unless imported records are chosen. Old v1 backups retain the new sections on merge. Unknown/prototype-like IDs, invented choices, incomplete revealed responses, duplicate self-checks and impossible dates are rejected without changing saved state. The original three suites also passed their existing recovery, cross-device restore, lifecycle, data reconciliation and legacy compatibility checks.

All new views were checked at 320, 390, 768 and 1280 pixels, with enlarged text, keyboard radio selection and direct file opening. No page errors were recorded. Desktop connections and correction feedback, the mobile connection flow and the mobile answer workshop were visually inspected. Test screenshots, downloads and synthetic personal progress stay outside the repository. These browser checks are not a full accessibility conformance audit.
