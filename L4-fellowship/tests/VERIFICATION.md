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

## 5 November 2026 — six further additions and offline lifecycle

All six browser suites passed on the final application in headless Chromium with Playwright 1.64.1. JavaScript syntax checks passed for the inline application, curriculum and service worker. Five content hashes, 37 KSB records, 30 quiz IDs and every precached public-asset hash were independently verified.

The four established suites passed again with outputs in `/tmp/l4-final-core`, `/tmp/l4-final-guided`, `/tmp/l4-final-learning` and `/tmp/l4-final-reasoning`. They retain the earlier coverage of storage failure, corrupt-data recovery, legacy backups, evidence status, numerical fixtures and guided study. The initial keyboard check caught the backup reminder preceding the primary study action; the reminder was moved below that action and the final check passed.

New commands (alongside the four existing suite commands):

```bash
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_rehearsal.py --url http://127.0.0.1:8000/ --output /tmp/l4-final-rehearsal
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_offline.py --url http://127.0.0.1:8001/L4-fellowship/ --fixture /tmp/l4-pwa-fixture/L4-fellowship --output /tmp/l4-offline-qa
```

The offline suite used a second localhost server rooted at `/tmp/l4-pwa-fixture`; it only changed its copied fixture to simulate releases. The test accounts for SimpleHTTPServer's whole-second Last-Modified validation when changing worker files. This fixture timing adjustment does not weaken the production SHA-256 asset checks.

Activity results:

- Eight combinations of n, known standard deviation, difference and confidence level matched independent Python `NormalDist` intervals and `math.erfc` p-values. All 100 interval rows reconciled with their displayed coverage and width; settings and simulation seed persisted.
- Confidence ratings survived unfinished quizzes, were recorded once before feedback and did not change KSB states. Unrated attempts were excluded; revisiting a question preserved an unfinished quiz.
- All three changed-condition cases required a choice/reason, explained changed versus retained assumptions and retained drafts/review state.
- Briefing drafts remained separate by scenario/audience, displayed tailored examples, escaped untrusted preview text and downloaded the actual draft and reference.
- Evidence rehearsal required support, contribution and limits, displayed saved rationales after review, supported explicit gaps and preserved explanations when an evidence reference was removed.
- New state round-tripped through JSON; conflicting imports retained current records by default; older v1 data retained new records during merge. Invalid IDs, confidence labels and numerical controls were rejected without mutation.

Offline results:

- Manifest scope/start URL and 192/512 PNG dimensions were checked. Registration and all cached URLs stayed under the project subpath; the cache contained only public assets.
- Actual offline reloads succeeded across lessons and new activities, public source guides were fetchable offline and edits survived disconnection/reload.
- A deliberately mismatched HTML/curriculum release failed installation. The previous complete copy and progress remained available.
- A valid release waited for explicit application. Simulated storage failure blocked reload; the temporary draft could be exported and restored, then survived activation and another offline reload.

New views were checked at 320, 390, 768 and 1280 pixels, with mobile activity selection, enlarged text and direct file opening. No page errors were recorded. Desktop briefing/statistics views and mobile statistics/offline views were visually inspected; the interval plot's mobile labels were enlarged and spaced for legibility. Screenshots and synthetic backups remain under `/tmp`. Headless Chromium does not test native OS installation dialogs, and these checks are not a complete WCAG conformance audit.

## 5 November 2026 — daily missions, dated rewards and quest history

All seven browser suites passed on the release application, plus `node tests/gamification_core.cjs`. JavaScript syntax checks passed for the inline app, `gamification.js`, curriculum and service worker. The five curriculum source hashes, 37 KSB records, 30 misconception IDs and all 12 cached public-asset hashes were verified. The new reward helper is included in the atomic offline release.

Release commands used:

```bash
node tests/gamification_core.cjs
node --check /tmp/habit-app.js
node --check gamification.js
node --check curriculum.js
node --check sw.js
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_smoke.py --output /tmp/l4-habit-release-core
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_enhancements.py --output /tmp/l4-habit-release-guided
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_learning_tools.py --output /tmp/l4-habit-release-learning
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_reasoning_tools.py --output /tmp/l4-habit-release-reasoning
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_rehearsal.py --output /tmp/l4-habit-release-rehearsal
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_gamification.py --output /tmp/l4-habit-release-game
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_offline.py --output /tmp/l4-habit-release-offline
```

`/tmp/habit-app.js` was extracted from the shipped inline script. The app suites used the project-local server on port 8000; the offline lifecycle suite used the disposable project-subpath fixture on port 8001. All test dates, reflections, backups and screenshots are synthetic and remain outside the project.

Pure calculations covered: 20/20/20 plus 40 daily XP and its cap; first qualifying badge dates; quest receipts; removal recalculation; current/best streaks across gaps; local dates and both sides of a DST fallback; exact time-window boundaries; supporting quiz-review prerequisites; same-day versus later-day mistake recovery; explicit 37-topic coverage; two audiences for the same scenario; and three linked discussion attempts.

The new browser suite completed real Recall, Apply and Explain tasks at three controlled local times, earning exactly 100 XP and the quality quest. It verified that unfinished reflections survive reload, a block cannot finish before interaction/source completion, and application/evidence-gap practice leaves KSB/evidence state separate. Further practice respected the daily cap. Badges showed their qualifying day, pinned correctly and exported local SVG cards; the desk's lamp unlocked. Selecting another quest changed actual mission suggestions.

Five reviewed quiz questions created one supported block; reloading did not duplicate records. The optional mixed rehearsal recorded three distinct K/S/B attempts and its cosmetic milestone. Time settings rejected invalid boundaries, retained historical window assignments and exported three 90-day calendar recurrences with alarms, stable IDs, floating local times and RFC-style folded lines of at most 75 bytes. The structural calendar checks do not assert delivery by an external calendar application.

Removal/undo recalculated XP and badges. Merging an older backup preserved removal IDs, identical imports did not duplicate rewards, and conflicting practice records required explicit imported-record selection. Older v1 data retained the new history during merge. Duplicate IDs, unknown/prototype-like types, invalid dates/offsets/windows, invalid schedules and unsupported tracked contexts were rejected without mutation. Full reward history round-tripped into a fresh browser context.

Weekly replay used actual records. Normal-motion playback advanced and paused when the document became hidden; reduced motion retained manual controls. Markdown recaps and SVG weekly cards reconciled with the recorded week. All new routes reflowed at 320, 390, 768 and 1280 pixels, enlarged text fit, and direct file opening loaded the required helper without page errors. Desktop reward/mission views and mobile missions/quest paths were visually inspected. The initial regression run exposed a hidden Resume practice button in the collapsed broader study plan; unfinished sessions now open that section and both existing resume checks passed.

The offline suite additionally earned a new practice record while disconnected and verified that the same game events survived temporary-memory recovery, verified service-worker activation and offline reload. It retained its checks for project scope, public-only caches and rejection of mismatched releases. These checks are not a complete accessibility audit and do not cover native OS installation dialogs or calendar alert delivery.

## 5 November 2026 — distinct visual memory cues for every KSB

All eight browser suites passed, alongside the scoring/date checks and JavaScript syntax checks. The new compiler validation passed for exactly 37 known IDs, unique names and SVG bodies, bounded captions and an SVG shape/attribute allowlist. All six content-source hashes, 37 guided records, 30 quiz IDs and 13 offline asset hashes were verified.

The existing core, guided, learning-tools, reasoning, rehearsal and gamification suites passed against the icon-enabled application, with outputs under `/tmp/l4-visual-core`, `guided`, `learning`, `reasoning`, `rehearsal` and `game`. The added suite and final offline check used:

```bash
PYTHONPATH=/tmp/l4-authoring python3 tests/compile_curriculum.py
python3 tests/build_offline.py
node --check /tmp/visual-app.js
node --check curriculum.js
node --check sw.js
node tests/gamification_core.cjs
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_visual_cues.py --output /tmp/l4-visual-release-cues
PYTHONPATH=/tmp/l4-authoring PLAYWRIGHT_BROWSERS_PATH=/tmp/l4-browsers python3 tests/browser_offline.py --output /tmp/l4-visual-release-offline
```

`/tmp/visual-app.js` was extracted from the shipped inline script. The visual suite inspected every cue in the map and index, then opened all 37 lessons and checked that each used exactly the same artwork and caption as its map card. Names and geometry were distinct. Browsing all pictures left personal KSB state, evidence and reward records unchanged. SVGs were decorative/non-focusable, with visible ID/title/caption text and keyboard-accessible links.

Library search located B2 through its “roadblock” cue. Readiness contained all 37 matching topic illustrations; the quality connection used K8/S6/B5; discussion practice showed the correct K1 picture and mnemonic; related-topic chips used the same art. Native text selects and existing KSB-ID text remained usable. The 37-picture memory map worked by opening the file directly, printed with all images present and generated a substantial A4 PDF through the browser print engine.

The new route, index, library, lesson headings, practice, readiness, connections and quests were checked at 320, 390, 768 and 1280 pixels, including enlarged text. No page errors were recorded. The complete desktop gallery was visually inspected for all 37 associations, along with desktop K1 and mobile S13/gallery layouts. Pictures retained readable sizes in the map and scaled down consistently for repeated cues. The K4 caption explicitly notes that data types can overlap and sensitivity is a separate question.

The offline suite reloaded `#visual-map` while disconnected and verified all 37 cards, in addition to its source-guide, scope, mismatch rejection, safe update and personal-progress preservation checks. The canonical visual JSON and the matching new curriculum version are covered by the atomic cache manifest. No new personal-data fields or reward rules were introduced. Test screenshots/PDFs remain under `/tmp`; these checks are not a complete accessibility conformance audit.

## 5 November 2026 — visible shortcuts and fading success feedback

All eight existing browser suites passed against the updated page, along with the scoring/date checks and JavaScript syntax checks. Outputs are under `/tmp/l4-feedback-core`, `guided`, `learning`, `reasoning`, `rehearsal`, `game`, `visuals` and `offline`. The additional `tests/browser_feedback.py` suite passed with output under `/tmp/l4-feedback-qa`.

The focused suite exercised all four shortcut destinations by keyboard, visible focus, touch targets and responsive layouts at 320, 390, 768 and 1440 pixels without changing saved progress. It submitted unanswered, incorrect and correct quiz questions; checked that focus stayed on the answer feedback; observed the actual CSS fade and eventual hiding; and verified repeat correct answers and no replay after reload. Correction, method and changed-assumption questions also received success feedback only after the authored correct choice and required explanation.

The same three-step weekly quest was completed through real Recall, correction and retrieval workflows in two separate weeks. Both completions displayed congratulations, including the second week after the original badge had already been earned. Incomplete quests and reloads did not display congratulations. The suite also checked static reduced-motion feedback, saved opt-out/re-enable behaviour and ordinary status toasts above the success message. The existing offline checks passed through disconnected use, rejection of a mismatched release, explicit verified update and preservation of personal records.

Desktop shortcut and correct-answer screenshots and phone shortcut/quest-completion screenshots were visually inspected. The buttons are prominent and the success message fits near the bottom with readable contrast. Synthetic screenshots and exported data remain outside the project under `/tmp`. No personal state schema or reward rules changed. These checks are not a complete accessibility audit.

## 5 November 2026 — seven guided-study improvements

All ten browser suites passed. The existing core, guided-learning, learning-tools, reasoning, rehearsal, gamification, visual-cue and feedback outputs are under `/tmp/l4-seven-core`, `guided`, `learning`, `reasoning`, `rehearsal`, `game`, `visuals` and `feedback`. The final expanded offline suite passed under `/tmp/l4-seven-offline-final`; the added `tests/browser_guided_study.py` passed under `/tmp/l4-seven-new`. The compiler regenerated 37 guided records, the complete project and activities with all six verified source hashes. JavaScript syntax checks passed for the inline app, curriculum, reward helper and generated worker. The pure scoring/date checks passed. All 13 cached-asset hashes matched the final offline manifest.

The new suite verified that the phone shortcuts fit in the first viewport with 44px touch targets and keyboard activation; all 13 original activities remain reachable from the grouped practice navigation; the recommended recall session lasts five minutes; and a completed tracked activity has a visible nearby finish action which uses the original reflection dialog. It exercised ten-row readiness paging, KSB search, disclosure expansion, all-37 mode and inert search markup. During development it caught a blur/change rerender which could swallow disclosure activation; the duplicate change handler was removed and the complete flow then passed.

Visual sessions for K1, S8 and B5 were completed through actual UI. Unfinished visual text survived reload and restoration in a separate browser context; the new question type retained existing strict v1 validation. The guide stayed hidden until reveal, and independent evidence/personal-example checks were not completed automatically. All 37 KSBs retain their authored scenarios, with the shared memory-cue suite verifying the existing illustrations. Lifecycle, join and statistics diagrams were checked.

A saved assessment date of 20 November 2026, preferred Monday/Wednesday/Friday study days and K13 priority produced the expected first day and topic, paged across weeks and stopped on the deadline. Past dates produced an actionable empty state and browsing did not change KSB records. Every new application challenge was answered, explanation-gated, revealed and reloaded. Chart tables matched their authored values. The weighted-mean and held-out RMSE keys were independently calculated. Backups restored all eight new records and the selected new quest in a separate context. All six quests were present and selectable.

The expanded offline suite reloaded the new chart/calculation routes, readiness, plan and quests while disconnected, alongside its original guide, scope, mismatched-release rejection, explicit update, memory-recovery and persistence checks. Responsive checks covered 320, 390, 768 and 1440 pixels and direct file opening of a new chart challenge. Desktop and phone screenshots of navigation, recommendations, readiness, charts and planning were visually inspected. Test data and screenshots remain synthetic and outside the project under `/tmp`. These checks are not a full accessibility audit or a prediction of EPA success.
