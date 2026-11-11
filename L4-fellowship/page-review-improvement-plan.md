# Fellowship page review and improvement plan

11 November 2026. Baseline: main `d3da021abd42948db6002236ed289943ac7c1e04` (the fellowship project matches release `15c7c0c`).

## Review

Reviewed 40 primary views and the lesson/library/assessment source, with desktop and phone screenshots. No page errors or desktop page overflow occurred. The existing practice, evidence and reward flows work together; this change concentrates on access to learning content and visual recall.

The full answer is a plain disclosure below assessment context, a diagram, a mistake and an example. The useful 60-second explanation has much stronger hierarchy. Assessment pages repeat a large provenance block before the activity, groups show IDs without topic names, and 254 source prompts are navigated through one long select. Source criteria are traceable and differentiated correctly; preserve that work.

## Implement

1. **Make deeper reading obvious.** Keep the 60-second explanation. Add a prominent Definitions and detail study-step button, move the existing detailed-answer disclosure directly below the short explanation and style it as a substantial reading invitation. Use a book symbol, clear opening affordance and a short description. Preserve native keyboard toggling, focus, printing and the existing detail anchor. Do not mark anything learned by opening it.
2. **Refine all 37 visual cues.** Keep every existing name, mnemonic and topic association. Redraw the artwork with simpler silhouettes, balanced geometry, rounded strokes and two-tone fills. Preserve blue Knowledge, green Skills and amber Behaviours, with category text and KSB IDs. Reuse the same SVG at every size; no network images or animation. Inspect the full gallery, tiny index, print sheet and individual lessons.
3. **Make assessment content actionable.** Add a concise, authored Explain / Show / Discuss study brief for each of the 30 groups. Label these as derived coaching, retaining exact source criteria and provider guidance independently. Include readable topic names and explicit expand/collapse affordances in group summaries. Keep the eight distinction rows and all source references unchanged.
4. **Make the question bank easier to use.** Add local prompt search and Previous/Next navigation with a position indicator. Search works alongside existing method/group filters and never edits saved responses. No-result states offer a clear reset. Keep existing prompt IDs, wording, revision snapshots, source mocks and reveal gating. Condense provenance to a short visible attribution with expandable details; do not remove limitations or source links.

## Verify and publish

Keep storage key/schema v1, KSB IDs/order, numeric coverage targets, all old quiz/source question records and existing draft/evidence/reward data. New briefs do not alter criteria or invalidate old self-reviews. Verify all source hashes and mappings. Run all twelve existing browser suites, three pure suites and a focused review suite covering new navigation/search, all 37 drawings and all 30 briefs, safe input, keyboard use, saved answers, printing, direct-file use and 320/390/768/1440px layouts. Visually inspect the output.

Regenerate curriculum and the offline manifest after cached assets are final. Verify real offline reloads and explicit updates with retained progress. Record actual checks in tests/VERIFICATION.md. Upload bounded verified blobs, create a project-only commit, update main with an expected-head lease and verify GitHub Pages hashes and live flows. Exclude private source, local release files and test artefacts.

## Implementation record

Implemented the four changes above. The detailed-answer content and native disclosure remain intact; only access and hierarchy changed. All 30 derived coaching briefs link to their source group/cells, and all 37 new SVGs retain their established mnemonic identity. Runtime verification and release evidence are recorded in tests/VERIFICATION.md.
