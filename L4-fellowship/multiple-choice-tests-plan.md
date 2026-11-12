# Multiple-choice Tests page

12 November 2026. Baseline main: `bc63f8d8ea624f7d68092407605c56cd67a28205`.

## Scope and question design

Add **Tests** to the desktop main menu and phone main-menu selector. This is the only entry point from other app sections: do not add Tests to Today shortcuts, Practice, lesson links or activity pickers. The page contains ten named tests with ten distinct questions each. Questions use checkboxes, eight meaningful options and three or four correct options. Cover all 37 KSBs, using the existing library answers and Definitions and detailed answer content. Keep each question attached to one KSB and its source anchor. Different questions revisit complementary aspects or contexts rather than repeat the same wording.

Themes: responsible data use; planning and delivery; structures and architecture; quality and integration; statistics; predictive analysis and forecasting; visuals and communication; professional behaviours; practical analytical decisions; mixed EPA revision. These are derived study tests, not official EPA papers or a substitute for explaining genuine applied work.

## Experience

Use the current paper/ink/blue design and the established KSB illustrations. The Tests landing page presents ten numbered cards, question/KSB coverage, saved-draft status and derived result summaries. Inside a test show one question at a time, all eight checkbox options, a ten-question navigator, answered count and Previous/Next controls. More than one option is always required for a correct answer; selection alone does not reveal correctness. Submit only when all ten questions have at least one selection.

After submission, award one point only for an exact match to the correct set. Missing a required option or choosing an incorrect option earns zero for that question. Give a score out of ten and explain each option, distinguishing selected correct, selected incorrect, missed correct and correctly omitted options with text. Show a coherent answer explanation and a link which opens that KSB's detailed guide. Preserve the submitted attempt and support explicit retakes. Never mark a KSB learned, evidence complete, an EPA grade or award unsupported XP. Reuse the existing success message only on a new submission containing correct answers; never replay it on reload/import.

## Content and state

Canonical public JSON holds 100 questions, eight option records per question, correct-set keys, per-option reasoning, a combined answer and source references. An authoring-only compiler checks 10×10 structure, all-37 coverage, unique IDs/text, 3–4 correct options, source anchors and hashes against the existing detailed guides, then emits a relative JS data file for direct-file/offline operation. Existing curriculum/answers are unchanged.

Keep `l4-fellowship.v1` and numeric schema version 1. Add an independent `multipleChoice` section containing per-test drafts, submitted attempts and deletion tombstones. Retain drafts for different tests, save selections and position, and support guarded storage, old-v1 defaults, strict import validation, per-record conflict choices and JSON/Markdown export. Scores derive from validated option selections, never imported score fields. Keep authored IDs/revisions immutable and retain old content versions if a future edition changes questions. History deletion must survive old-backup merges. Bound history and make export/removal actionable when full.

## Verification and release

Test every authored correct set and deliberate missing/extra-option variants, all ten actual browser submissions, multi-select interaction, withheld guidance, saved drafts/reload, history/retakes, menu-only entry, detailed-guide links, independent KSB/evidence/reward state, backup/merge/conflict/deletion/error paths and malformed imports. Check keyboard access, focus, 320/390/768/1440px reflow, print and direct-file opening; inspect screenshots. Run all thirteen existing browser suites and three existing pure suites alongside the new focused checks. Rebuild and verify offline assets last; test disconnected use and a real verified update preserving test records. Publish a project-only commit to main using bounded, checkpointed blob uploads and an expected-head lease, then verify the live files and flows. Keep private source, release checkpoints and test artefacts out of the commit.

## Implementation and verification

Implemented the dedicated Tests page and main-menu entry. The ten tests cover all 37 KSBs at least twice, with 100 distinct questions, 800 explained options and immutable source-linked keys. Existing guides, criteria and artwork remain unchanged. All fourteen browser suites, four pure suites, independent numerical checks and the final verified offline lifecycle passed; detailed evidence is in tests/VERIFICATION.md. Release publication excludes private checkpoints and test artefacts.
