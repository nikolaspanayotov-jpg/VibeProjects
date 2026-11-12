# Forty additional tests

Baseline: main `91489947ab91fbb5be38ed2a91b4fc6568b6da74`.

Add T11–T50, each with ten eight-option questions and three or four correct selections. T11–T47 focus on the 37 individual KSBs; T48–T50 use mixed workplace cases. New questions use authored scenarios and source-checked concept/decision statements from the detailed guides. Repeated principles reinforce learning in different contexts; do not count a reordered option set or a reworded original question as a new question. Validate 400 new stems and distinct complete option sets, with specific explanations and coherent combined answers.

Retain the first ten tests, their wording, IDs, keys, revision and stored results byte-for-byte. Append four bounded public data packs rather than replacing the original bank. Compile each pack to relative JS so all fifty tests work by direct file opening and offline. Preserve the storage key/schema and existing score semantics. Expand the per-test draft bound to fifty and submitted history to five hundred, with current export, removal, conflict and tombstone protections.

Keep Tests accessible from the main menu. Add search by test title, topic and KSB, a New tests view, and ten-card paging. Search/paging is transient UI state; selecting a test or restoring a backup must not replace a draft. Display truthful totals of 50 tests/500 questions, retain KSB cues, and provide clear empty and page-boundary states.

Verify every correct set plus missing/extra variants, the original content hashes and real legacy records. Run a complete browser submission for each new test, check catalogue navigation/search, old/new draft coexistence, restored history, strict new-ID validation, direct-file and 320/390/768/1440px layouts. Run all existing suites and an expanded offline lifecycle check preserving a new test's draft/result through an update. Rebuild the cache manifest last, publish only this project using verified bounded blobs and an expected-head lease, then verify deployed hashes and live flows. Keep private authoring/checkpoint/test artefacts out of GitHub.

## Completion record

Implemented T11–T50 and the catalogue controls. All fifteen browser suites and four pure suites passed, including actual submission of every new test, original-release state preservation and offline update continuity. Full checks are recorded in tests/VERIFICATION.md. The original ten-test bank and compiled base file remain byte-for-byte unchanged.
