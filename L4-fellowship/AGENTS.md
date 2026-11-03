# L4-fellowship

This folder is a self-contained, build-free study page for the Level 4 Data Analyst apprenticeship. Follow the repository root instructions as well as this file. Change only this project when working here.

## Run and architecture

Open `index.html` directly, or run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder. Deployment uses the repository's GitHub Pages path. Do not add a framework, backend, account system or required build step.

- `index.html`: shell, CSS and plain JavaScript application. Hash routes are `#today`, `#library`, `#ksb-k1` through `#ksb-b7`, `#evidence`, `#practice`, `#plan` and `#studio`.
- `curriculum.js`: complete trusted public content records on `window.L4_CURRICULUM`; loaded as a relative script so file opening works. Contains 37 answers, 74 initial/follow-up prompts, themes, target checklists and source status.
- `solutions.md`: canonical answer content. Preserve explicit `ksb-*` anchors. `tests/compile_curriculum.py` can regenerate the curriculum after content edits using Python-Markdown as an authoring-only dependency.
- `design.md`: specification and implementation record. `README.md`: running and user data guidance.
- `tests/browser_smoke.py`: meaningful end-to-end flows, persistence, imports, dataset reconciliation, responsive layouts and failure states. Screenshots/results go to a temporary directory.

## State and invariants

Keep the exact storage key `l4-fellowship.v1` and numeric schema version `1`. Never rename a shipped key or silently discard data. State includes settings, KSB records, evidence, unfinished evidence draft, attempts, an unfinished practice session and an unfinished study session.

Every storage read/write must stay guarded. Corrupt data is preserved; failed writes switch to temporary memory with an export option. Another-tab changes disable writes in the stale tab. Restore validates and normalises data before mutation, previews conflicts, retains current values by default and only replaces after explicit confirmation. On restore persistence failure, keep existing state intact.

Keep the 37 KSB IDs and their order stable: K1–K15, S1–S15, B1–B7. Preserve solution anchors and the case-sensitive `L4-fellowship` folder name. Calendar dates use local `YYYY-MM-DD`; timer timestamps use elapsed time. Independent recall suggests seven days, then fourteen after consecutive independent recall; partial suggests three and help suggests one. Manual dates override suggestions.

Personal response, confidence, learning, recall, checklist coverage and evidence are separate. Do not mark evidence complete because a lesson was read or a model answer was copied. The optional AP03 filter only appears after the learner confirms applicability.

Imported and user-entered text is untrusted. Escape it before inserting into HTML; never execute imported Markdown, HTML, code or URLs. Curriculum HTML is trusted authored content, generated from the public source. No sensitive workplace material or personal browser data belongs in commits. Tests use clearly synthetic data only.

## Design and interaction

The visual system uses cool paper `#F2F5F8`, white surfaces, ink `#172A3A`, muted `#4B5D6B`, blue `#174EA6` and green `#176B52`. Typography uses local Trebuchet MS and Calibri/Segoe UI fallback stacks. Keep the 37-cell KSB index, quiet reading surfaces, readable line lengths and explicit status text.

Check 390px and 320px first, then tablet and desktop. Use semantic controls, visible focus, non-colour status cues, reduced-motion support and accessible tables/charts. Essential content must not require network services. The S13 chart distinguishes actuals and held-out forecasts; future projections remain separately explained. The synthetic monthly series is independent of the 300-row request fixture.

## Checks

After code changes, run a JavaScript syntax check and the existing browser smoke check against a localhost server. Inspect desktop/mobile screenshots and fix observed errors. After answer edits, regenerate curriculum, verify all 37 records and source links, and preserve source caveats. Do not claim a full accessibility audit from smoke checks. Keep [tests/VERIFICATION.md](./tests/VERIFICATION.md) current with checks actually performed.
