# L4-fellowship

This folder is a self-contained, build-free study page for the Level 4 Data Analyst apprenticeship. Follow the repository root instructions as well as this file. Change only this project when working here.

## Run and architecture

Open `index.html` directly, or run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder. Deployment uses the repository's GitHub Pages path. Do not add a framework, backend, account system or required build step.

- `index.html`: shell, CSS and plain JavaScript application. Existing routes remain stable; additional routes are `#readiness`, `#project` and the six `#project-planning` / preparation / analysis / validation / communication / reflection stages. Lesson jumps are local controls, not new global hash routes.
- `curriculum.js`: complete trusted public records on `window.L4_CURRICULUM`; loaded as a relative, versioned script so file opening works and a new release does not mix new code with stale curriculum. Contains 37 guided answers, 111 initial/follow-up/probing prompts, themes, targets, source status and the complete worked project.
- `solutions.md`: canonical answer content. Preserve explicit `ksb-*` anchors and the short explanation, example, mistake, probe and full-answer blocks. `worked-project.md` is the canonical fictional portfolio, with six stages, eight artefacts and per-KSB rationales. The compiler regenerates the curriculum from both Markdown sources using an authoring-only Python-Markdown dependency.
- `design.md`: specification and implementation record. `README.md`: running and user data guidance.
- `tests/browser_smoke.py`: meaningful end-to-end flows, persistence, imports, dataset reconciliation, responsive layouts and failure states. Screenshots/results go to a temporary directory.
- `tests/browser_enhancements.py`: guided navigation, readiness actions, v1 compatibility, project annotations, portfolio downloads and actual SQL executed against the downloadable fixtures.
- `learning-activities.json`: authored assumptions/prompts for three labs and the three scenario decision graphs. The 30 misconception questions and explanations are canonical in the answer-key appendix of `solutions.md`. The compiler validates question coverage, graph reachability/cycles and links, then embeds all activity data into `curriculum.js` with its third source hash.
- `tests/browser_learning_tools.py`: independent Python statistics/regression and SQLite join checks; scenario branching and persistence; quiz dates/resume; new backup validation/merge; responsive checks.

## State and invariants

Keep the exact storage key `l4-fellowship.v1` and numeric schema version `1`. Never rename a shipped key or silently discard data. State includes settings, KSB records, evidence, unfinished evidence draft, attempts, an unfinished practice session and an unfinished study session.

Every storage read/write must stay guarded. Corrupt data is preserved; failed writes switch to temporary memory with an export option. Another-tab changes disable writes in the stale tab. Restore validates and normalises data before mutation, previews conflicts, retains current values by default and only replaces after explicit confirmation. On restore persistence failure, keep existing state intact.

Keep the 37 KSB IDs and their order stable: K1–K15, S1–S15, B1–B7. Preserve solution anchors and the case-sensitive `L4-fellowship` folder name. Calendar dates use local `YYYY-MM-DD`; timer timestamps use elapsed time. Independent recall suggests seven days, then fourteen after consecutive independent recall; partial suggests three and help suggests one. Manual dates override suggestions.

Personal response, confidence, learning, recall, checklist coverage and evidence are separate. Do not mark evidence complete because a lesson was read or a model answer was copied. The optional AP03 filter only appears after the learner confirms applicability.

The additive `exampleConfirmed` boolean defaults to false for older v1 records; do not erase their other fields or bump the storage key. Confirmation is an explicit self-check of a genuine personal example, requires a response and clears when that response is edited or replaced. Readiness uses recall/date, this self-check and validated evidence references separately; no Pass score or automated competence claim. `probe` is an additional supported practice question type and must survive backups/resume. Visiting the worked project changes no KSB completion or evidence.

The example dashboard derives its values from `datasetRows`, the same generator as the CSV downloads. Preserve its independent monthly-series caveat. SQL in the fictional portfolio must reconcile with the fixtures and the explicitly approved example lookup. Never resolve real conflicting values by assuming the fictional approval applies.

The new practice routes are `#labs`, `#labs-statistics`, `#labs-joins`, `#labs-forecast`, `#scenarios`, the three `#scenarios-<id>` routes, and `#quiz`. They remain children of Practice in the main navigation. There is no audio capture or personal-portfolio authoring feature in this change.

`learningTools` is an additive v1 state section: lab assumptions, per-scenario trails/drafts, per-question quiz counters/review dates and an independent unfinished quiz set. Missing sections in older backups receive empty defaults without changing other progress. Preserve question IDs Q01–Q30 and scenario/node/choice IDs; graph changes that invalidate stored trails require a migration. Validate imported paths by replaying the authored graph and validate question IDs with own-property checks. Never trust an imported outcome, score or graph transition.

Quiz checks do not update KSB recall, learning, confidence, personal-example confirmation or evidence. A wrong answer schedules one day; a correct answer seven days, then fourteen after consecutive correct responses. Recorded feedback is idempotent through reload. Scenario routes require a choice and justification; replay explicitly replaces only that scenario's current route. Do not silently overwrite another unfinished exercise. Every activity record belongs in JSON backup/restore and must retain conflict-safe merging.

Lab results must come from the actual controls: statistics distinguishes observed/imputed/excluded data; join modes preserve cardinality and NULL semantics; UNION compares compatible rows; forecast fitting uses only the selected initial months and RMSE uses only later known actuals. Future projections must not enter error metrics. These are synthetic learning examples, not operational forecasts.

Imported and user-entered text is untrusted. Escape it before inserting into HTML; never execute imported Markdown, HTML, code or URLs. Curriculum HTML is trusted authored content, generated from the public source. No sensitive workplace material or personal browser data belongs in commits. Tests use clearly synthetic data only.

## Design and interaction

The visual system uses cool paper `#F2F5F8`, white surfaces, ink `#172A3A`, muted `#4B5D6B`, blue `#174EA6` and green `#176B52`. Typography uses local Trebuchet MS and Calibri/Segoe UI fallback stacks. Keep the 37-cell KSB index, quiet reading surfaces, readable line lengths and explicit status text.

Check 390px and 320px first, then tablet and desktop. Use semantic controls, visible focus, non-colour status cues, reduced-motion support and accessible tables/charts. Essential content must not require network services. The S13 chart distinguishes actuals and held-out forecasts; future projections remain separately explained. The synthetic monthly series is independent of the 300-row request fixture.

## Checks

After code changes, run JavaScript syntax checks and all eight browser checks against a localhost server. Inspect desktop/mobile screenshots and fix observed errors. After content edits, regenerate curriculum, verify 37 guided records, 30 question IDs, graph integrity, project mappings and all six source hashes, and preserve source caveats. Do not claim a full accessibility audit from smoke checks. Keep [tests/VERIFICATION.md](./tests/VERIFICATION.md) current with checks actually performed.

## Further reasoning tools

`reasoning-activities.json` contains four correction challenges, six method decisions, three six-part annotated answer structures, four notebook sections and nine KSB connections. The compiler embeds these as `C.reasoning`, validates their stable IDs/references and all-37 connection coverage, and stores `reasoningSha256`. `solutions.md` remains the core answer/quiz source.

The routes are `#repairs`, `#methods`, `#workshop`, `#organisation`, `#connections` and their validated focused suffixes. The four practice tools stay under Practice; organisation context stays under Plan and sources and in relevant lessons. Never represent the connection paths as official assessment mappings.

`studyTools` is an additive v1 section with `repairs`, `methods`, `workshops`, `organisation` and `connections` dictionaries. Its records belong in all backups, per-record conflict-safe merges and the Markdown summary. Keep its IDs stable. Unknown IDs, invalid choices/dates/checklists and revealed responses without explanation must be rejected before mutation. User text and reference IDs remain escaped/inert. Older backups must receive empty defaults without erasing new records on merge.

Workshop drafts are distinct from KSB responses. Editing clears workshop self-checks. Copying into an existing different KSB response needs explicit in-app confirmation and clears `exampleConfirmed`; it must not set recall, coverage or evidence. Notebook notes are local personal data, never public curriculum. Their verification date is entered by the learner. Connection evidence comes from actual saved per-KSB mappings.

Run `tests/browser_reasoning_tools.py` alongside the three existing suites. It checks explanation gating, all ten correction/method cases, notebook escaping, workshop replacement, connected evidence, state validation/merge, direct file opening, mobile layout and keyboard selection. Inspect desktop and mobile screenshots; record only completed checks.

## Rehearsal and offline release

`rehearsal-activities.json` supplies three changed-assumption cases and two synthetic/one personal briefing scenarios for two audiences. The compiler validates and embeds them in `C.rehearsal` with the fifth source hash, `rehearsalSha256`. Routes: `#uncertainty`, `#calibration`, `#changes[-<id>]`, `#briefing`, `#retrieval[-<ksb>]` and `#offline`. Keep phone Practice navigation as a labelled native selector.

The additive `rehearsal` state stores bounded uncertainty controls and seed, latest rated comparisons per quiz question, changed-case responses, scenario/audience briefing drafts, per-KSB retrieval records and `lastBackupOn`. Missing old-v1 fields receive defaults. Quiz certainty is recorded before feedback and is optional; unrated answers do not invent ratings. Do not overwrite another quiz when revisiting calibration. The new records require conflict-safe merge, exports and strict input validation. Deleted evidence references remain recoverable as dangling IDs; never delete their rehearsal explanations or mark evidence complete automatically. The backup date records requesting a JSON download, not guaranteed file retention.

The uncertainty lab deliberately assumes independent normal populations with equal known standard deviations and equal per-group n. Use SE = sigma*sqrt(2/n), matching normal critical values and two-sided p-values. Do not label this as a general-purpose t-test. Distinguish statistical thresholds, practical thresholds and repeated-sampling coverage. Validate formulas independently and reconcile all 100 interval rows.

The PWA uses `manifest.webmanifest`, two PNG icons and generated `sw.js`, scoped to this folder. After any cached asset changes, run `python3 tests/build_offline.py` last. Its hashes must match the files committed in the same release. Worker installation validates all public files before caching; a failed/mixed release must never replace a working one. Keep navigation and versioned curriculum paired. Do not force a waiting update or automatically reload other tabs. Save before explicit application and block reload if storage is unsafe; temporary sessions remain exportable. Never cache personal records, backups or another project's files. Retain prior versioned caches for older open tabs.

Run `tests/browser_rehearsal.py` and `tests/browser_offline.py` as well as the four existing browser suites. The offline test requires a localhost server on port 8001 rooted at its disposable fixture parent. It copies public files into that fixture and simulates valid/invalid updates there; never run release-mutation tests against the user's project files. Verify real offline reloads, scoped caching, failure recovery and persistence. Native OS installation UI is not covered by headless Chromium.

## Practice rewards

`gamification.js` is a required relative trusted script with pure date/scoring functions, reward definitions and SVG badge art. It has no dependencies. Include its versioned URL in the offline manifest and retain matching older versions for older open tabs. New routes are `#habits`, `#quests`, `#rewards` and `#habit-settings`; these are reached from Today/Plan without adding another crowded global navigation.

Keep the `game` v1 section additive: settings, dated events, deletion IDs and one tracked block. All XP, streaks, levels, badge dates and quest steps derive from validated events. Preserve IDs across reload/backup/merge. Quiz identities and optional weekly-rehearsal fields are additive; default older imports safely. Do not infer historical visits from the old latest-result fields or grant rewards merely for opening/copying/downloading.

The first Recall/Apply/Explain completion per local date earns 20 XP each plus 40 for all three (100 maximum). More completed blocks still support check-ins/history. Each event records actual time, offset, local date, window and boundaries; validate their agreement and preserve old assignments when settings change. Three-window dates and daily trios are separate. Calendar arithmetic must handle DST. Awards describe self-recorded practice and must never mark EPA readiness, knowledge, personal examples or evidence complete.

Manual activities require tracking, a subsequent interaction, source completion/feedback, a reflection and an explicit review. Workshop completion needs all six self-checks. Starting a different tracked block with an unfinished reflection requires confirmation; existing activity text stays saved. Recall outcome actions and advancing after five quiz feedback reviews create records idempotently. A quiz block requires its distinct supporting question review IDs; deleting supporting history removes its scoring. Mistake recovery requires correct answers on later answer dates, not the same day.

Merge settings/active blocks and event conflicts explicitly; retain current values by default. Union removed IDs and filter removed records so old backups cannot resurrect them. Removal/undo recalculates rewards without altering original answers/evidence. Imported text stays escaped. Keep a limited, validated schema; unknown types, forged date/window combinations, duplicate IDs and unsupported targets must fail before mutation.

Keep rewards cosmetic, local and inspectable. The 37-KSB badge requires explicit recall/workshop/retrieval targets. Replays only show actual records, pause on navigation/visibility/source changes and use manual controls under reduced motion. Celebrate only new completions, not reloads/imports. Calendar export is a local floating-time .ics download with three 90-day recurrences, not a promise of background web notifications.

Run `node tests/gamification_core.cjs` and `tests/browser_gamification.py` alongside the previous six suites. Test XP caps, source prerequisites, time boundaries, DST, stable history/imports, removal/undo, actual task completions, awards, reminders, normal/reduced-motion replay, mobile and direct-file support. The offline suite must retain newly earned practice records through disconnected use and verified updates. Update the design/verification record and rebuild `sw.js` after cached-file changes.

## KSB visual memory cues

`ksb-visuals.json` maps exactly K1–K15, S1–S15 and B1–B7 to distinct SVG bodies, cue names and mnemonic captions. The compiler validates IDs/uniqueness and a shape/attribute allowlist, embeds `item.visual` and stores `visualSha256` as the sixth source hash. Keep the cue-to-KSB associations stable and preserve full KSB titles/IDs beside the images. These cues are available learning aids, not earned badges or assessment claims.

The runtime helper `ksbVisual` uses trusted compiled shapes only, with escaped text captions. Inline SVG artwork is decorative (`aria-hidden`, not focusable); links retain meaningful topic text and the map/lessons show mnemonic sentences. Reuse the same body at every size rather than substituting platform emoji. Do not accept SVG, image URLs or cue changes from a personal backup. No new saved fields are required.

`#visual-map` is part of the library and supports a complete printable memory sheet. Library search matches cue names/captions. Keep the index's 37 cells and status markers, mobile readability, lesson navigation, native text-only selects and existing keyboard flows. The versioned curriculum and canonical JSON are in the offline manifest; rebuild `sw.js` after changes.

Run `tests/browser_visual_cues.py` alongside the existing seven suites and the scoring/date checks. Verify all 37 unique cues and captions, identity across index/library/lessons/practice/readiness/connections, no progress or reward changes while browsing, search, keyboard links, phone/tablet layouts, print/PDF, direct-file support and offline reload. Inspect the actual artwork at large and small sizes.
