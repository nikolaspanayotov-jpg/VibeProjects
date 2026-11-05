# Data Fellowship study desk

A personal study page for the Level 4 Data Analyst apprenticeship, covering all 37 Knowledge, Skills and Behaviours.

Open `index.html` in a browser, keeping `curriculum.js` beside it. There is no installation, build step, account or backend. For a local server, run from this folder:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8000/`. The same relative paths work under the GitHub Pages project subpath, `VibeProjects/L4-fellowship/`.

## What is included

- All 37 complete answer guides, each with a concise 60-second explanation, a worked example, a common mistake and a probing question. Expand the full definitions/calculations when needed; use the mobile Learn / Worked example / My answer / Practise navigation to jump between tasks.
- A six-stage fictional service-capacity project with eight annotated artefacts, reproducible SQL, an interactive join comparison, numerical/qualitative dashboard views and a downloadable portfolio. Its artefacts map to every KSB and never count as personal evidence automatically.
- A readiness matrix separating recall, explicitly self-checked personal examples and evidence. Its next three actions open the relevant explanation, probing practice, personal response or evidence form.
- Search and combined filters; learning, confidence, recall and evidence tracked separately; local-date review scheduling.
- Evidence references with per-KSB rationales, review notes, editable reflections, draft recovery and deletion undo.
- Quick recall, follow-ups, probing questions, project walkthroughs, weak-topic review and mixed discussion, with answer reveal, an optional timer and resumable sessions.
- Three interactive analysis labs under Practice: outliers/missing values, joins/unions and forecast windows/baselines. Controls change the actual calculations and exact-value tables using synthetic data.
- Three branching workplace scenarios with required justifications, consequences, alternative routes, saved drafts and reflection prompts.
- Thirty misconception questions with explanations after submission, a previously-missed queue, review dates and resumable question sets. Question results stay separate from KSB recall and evidence.
- S12 stakeholder worksheets, an S13 forecast/mining worksheet and an accessible synthetic forecast plot/table.
- Six practical exercises and four downloadable synthetic CSV datasets with data dictionaries, worked approaches and self-checks.
- Four “find and fix” challenges with diagnoses, decision impacts and explained corrections.
- Six method-selection decisions covering t-tests, association, regression and forecasting, with assumptions and alternatives.
- An answer workshop for all 37 KSBs: three annotated example structures, independent drafts and six self-review checks.
- A private organisation notebook for policy references, tools, architecture and stakeholder context, displayed in related lessons.
- Nine interactive KSB connections covering all 37 topics, with combined discussion prompts and your matching evidence rationales.
- A weekly study plan, optional assessment settings, conditional AP03 route filters, JSON backup/restore, a Markdown study summary and print styles.

New tools open at `#repairs`, `#methods`, `#workshop`, `#organisation` and `#connections`. Focused links include `#repairs-duplicate-join`, `#methods-paired-change`, `#workshop-k8`, `#organisation-policies` and `#connections-quality`.

## Personal progress

Progress stays in browser storage under `l4-fellowship.v1`. Storage is specific to the device, browser and origin: opening the file, using localhost and visiting GitHub Pages can have different saved progress. Use the JSON backup and restore controls to move it. Merge retains conflicting current records by default and lets you choose imported records explicitly; replacement requires confirmation.

When storage fails, the page retains an exportable in-memory session. Corrupt saved data is left untouched and can be downloaded for recovery. If another tab changes the same progress, the current tab stops writing so it cannot silently overwrite those changes.

Use sanitised reflections and approved reference IDs. This public repository and browser storage are not approved storage for sensitive workplace evidence. Keep original material in its authorised location. Model answers, synthetic tasks and self-recorded coverage do not constitute assessor approval or a guaranteed Pass. Confirm your applicable assessment plan with the provider.

## Files and content maintenance

`solutions.md` is the canonical public answer bank, including the short explanations, examples, mistakes and probes. `worked-project.md` is the fictional portfolio source; `design.md` records the page specification. `curriculum.js` contains the authored sources compiled into browser-ready records with source hashes and stable KSB anchors. `index.html` contains the application HTML, CSS and JavaScript. No runtime Markdown parser, external fonts, chart library or analytics service is used.

`solutions.md` also contains the human-readable misconception answer key. `learning-activities.json` is the authored lab/scenario source; the compiler validates its decision graphs and embeds it with the questions into the same local curriculum file. Learning tools are available at `#labs`, `#scenarios` and `#quiz`, with focused links such as `#labs-forecast`.

`reasoning-activities.json` is the canonical authored source for the five further tools. It is compiled into the same curriculum, validated for KSB/choice links and covered by `reasoningSha256`. The additive `studyTools` section holds each exercise, workshop draft, organisation note and connected explanation. Backups include these records; merge retains conflicting current work by default. The workshop only copies a draft into a KSB response when you choose that action, and confirms replacement of an existing different answer.

Lab assumptions, scenario routes and quiz records use an additive `learningTools` section inside the existing version-1 backup. Older progress remains readable. Merge keeps existing conflicting tool records unless you choose otherwise; replacement still requires confirmation. Wrong quiz answers are suggested for the following day, correct answers for seven days, or fourteen after consecutive correct responses. These are study defaults, not assessment rules.

When changing the answer bank, the optional authoring utility regenerates the checked-in curriculum:

```bash
python3 -m pip install Markdown
python3 tests/compile_curriculum.py
```

This utility is for maintainers; the shipped page runs directly without it. Preserve the KSB identifiers, solution anchors, project path and storage key.

## Verification

See [the verification record](./tests/VERIFICATION.md). The browser smoke check exercises the main user flows, storage recovery, imports and responsive layouts. To run it with Playwright installed and a local server running:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 tests/browser_smoke.py --url http://127.0.0.1:8000/ --output /tmp/l4-qa
python3 tests/browser_enhancements.py --url http://127.0.0.1:8000/ --output /tmp/l4-enhancements-qa
python3 tests/browser_learning_tools.py --url http://127.0.0.1:8000/ --output /tmp/l4-learning-tools-qa
python3 tests/browser_reasoning_tools.py --url http://127.0.0.1:8000/ --output /tmp/l4-reasoning-qa
```

The output folder contains screenshots and a JSON result report; it is not committed. Browser testing is not a complete WCAG conformance audit, and offline reload of a hosted page is not promised. Direct file opening works with both application files present.
