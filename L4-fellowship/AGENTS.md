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

After code changes, run JavaScript syntax checks and all three browser checks against a localhost server. Inspect desktop/mobile screenshots and fix observed errors. After content edits, regenerate curriculum, verify 37 guided records, 30 question IDs, graph integrity, project mappings and all three source hashes, and preserve source caveats. Do not claim a full accessibility audit from smoke checks. Keep [tests/VERIFICATION.md](./tests/VERIFICATION.md) current with checks actually performed.
