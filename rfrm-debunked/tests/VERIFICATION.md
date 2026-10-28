# Verification record

Recorded 27 October 2026 for the completed static page.

## Checks completed

- `python3 tests/static_audit.py` passed: exactly 64 numbered measures in original order, 37 supporting entries, ten original numbered categories, unique HTML IDs, valid internal fragments and related links, sources for every article, and critiques within 120–200 words.
- The static audit confirmed complete financial-table structure, selected critical blank/negative cells, and the unchanged source-summary SHA-256.
- The supplied page 22 and page 31 table images were visually compared with `authoring/tables.json`; the complete fiscal table includes all source years and blank cells.
- The generated inline JavaScript passed `node --check` after extraction to a temporary file.
- The authoring generator and both Python test scripts passed Python syntax compilation.
- Calculated WCAG contrast ratios for ink, muted text, accent and analysis colours against both background and white surface all exceed 4.5:1. The lowest tested ratio was 5.87:1.
- The final page was regenerated and the static audit rerun successfully.

These checks establish static integrity and syntax. They do not establish browser behaviour or visual accessibility.

## Browser verification limitation

Browser tests have **not passed and real-browser behaviour has not been verified**. No mobile or desktop screenshots were captured or inspected. No successful browser check of search, filters, disclosures, hashes, copying, printing, keyboard focus, reduced motion, overflow, zoom, file URLs or HTTP hosting is claimed. The later DOM/event checks below execute the application script with modelled browser APIs; they do not remove this limitation.

The managed execution sandbox denied local socket creation when the browser smoke test attempted to start its temporary HTTP server (`PermissionError: [Errno 1] Operation not permitted`). An installed Chromium browser was subsequently found at `/usr/bin/chromium`; the root agent also encountered sandbox socket restrictions during browser launch. Attempts to run with additional network permission were aborted. They are not test results and are not treated as approvals or successful checks.

## Run the remaining browser checks

On a machine that permits local server sockets and browser launch, with Python Playwright and Chromium installed, run from this project folder:

```bash
python3 tests/static_audit.py
python3 tests/browser_smoke.py
```

The browser script uses `CHROMIUM_EXECUTABLE` when set, otherwise an installed `chromium` or `chromium-browser`, otherwise Playwright’s default Chromium. For example:

```bash
CHROMIUM_EXECUTABLE=/usr/bin/chromium python3 tests/browser_smoke.py
```

It exercises HTTP and file URLs, case-insensitive and collapsed-analysis search, exact measure queries, combined topic filtering, reset and empty results, multiple disclosures, initial and changed article hashes, clipboard-denial fallback, print-state restoration and printed citation URLs, keyboard focus, reduced motion, no JavaScript, and narrow layouts. It records a 720px layout as a 200% zoom-equivalent of a 1440px desktop; actual browser zoom should also be checked manually.

Successful runs write results and 320px, 390px and 1440px screenshots to `tests/artifacts/`. Inspect those screenshots, check real 200% browser zoom, and record observed results before claiming runtime or visual verification. Generated artefacts and Python bytecode are excluded by the project `.gitignore`.

## Feedback revision review — 27 October 2026

- The extended static audit passed: all 101 policy entries, 64 original numbers, eight headline panels, 101 evidence labels, valid unique fragment links, and all 20 eligible major costing lines against six disclosure questions.
- Python source and generated inline JavaScript passed syntax checks. The browser smoke test has been extended for the new panels and search text but has not been executed successfully in this environment.
- The published NI-cut and migrant-levy rows were compared directly: matching magnitudes of £7.14bn, £6.96bn, £6.76bn and £6.77bn from 2028/29 to 2031/32. The critique treats this as a funding assumption needing behavioural evidence, not an arithmetic impossibility.
- The illustrative UC calculation was checked: £486 × 55% = £267.30 less UC, leaving £218.70, conditional on full taper exposure and sufficient remaining entitlement. The page states the assumptions and excludes other interactions.
- The original financial-table data and source summary retain their prior checksums. No supplied financial values were rewritten to support the critique.
- New evidence was checked against the official Reform policy page, PDF and dated launch announcement; Tax Policy Associates; IFS; Parliament; government EUSS and Withdrawal Agreement guidance; the European Commission; and MoneyHelper. The page distinguishes publication provenance from independent verification of costings.
- The May overtime estimate is explicitly distinguished from the October fiscal profile. EUSS and payroll treatment are framed as legal-compatibility questions. EU-importer CBAM obligations and possible commercial effects on UK exporters are distinguished. Higher interest costs are not subtracted twice from Reform's headroom.

The browser verification limitation above continues to apply to this revision. No successful screenshot, layout, interaction or accessibility check is claimed.

## Mobile layout and disclosure audit revision — 27 October 2026

The shared container now owns safe-area-aware horizontal gutters; the headline section sets only block padding. Section headings use restrained rules instead of filled bands. The major costing audit now uses 20 native disclosures with six labelled checks each. Repeated full notes appear once in a linked common-notes glossary; all original statuses, notes, profiles and underlying audit data remain available. The two financial tables retain their semantic table structure.

Static checks verify all 120 check statuses and note content (including linked notes), each compact summary, 20 audit disclosures and exactly two financial tables. Browser coverage now explicitly checks both container and reading gutters at 320px/390px, 44px numbered links, audit keyboard disclosure, phone overflow and print visibility without JavaScript. These browser additions have not been run in this socket-restricted environment; the browser limitation above still applies.

The final scanability refinement keeps collapsed audit rows to policy name, published profile and “View disclosure details”; all six checks remain in each expansion. The number index uses six columns from 350px through 1000px and four below 350px, retaining 44px cells. Static audit and syntax checks passed after regeneration; browser coverage includes the 350px and 950px boundaries but remains unrun.

## Control regression review — 27 October 2026

The previous topic-filter selector matched both navigation links and every policy article because both carried `data-topic`. The handler called `preventDefault()` on clicks bubbling through an article, cancelling native summary and link actions and unexpectedly applying its topic filter. It now selects only `.topic-nav a[data-topic]`.

Other fixes reveal and focus nested citation, heading and audit fragment targets; preserve topic filtering on repeated fragment clicks; clear stale copied feedback and older manual-copy fields; and restore state with visible recovery guidance when opening print throws. Normal print restoration still waits for `afterprint`, including browsers whose print call returns immediately. Modern closed-disclosure print styling also includes `::details-content`.

The actual inline application JavaScript passed `tests/control_runtime.mjs` using Node and LinkeDOM 0.18.12. Eight regression groups cover:

- Initial control visibility and all 101 entries.
- Summary, permanent-link and source-link events in all 101 articles retain their default action and do not change the selected topic.
- Form submission, exact-number and evidence searches, combined filters, empty-state reset and clear-all.
- Every topic navigation link and select option.
- All 64 measure fragments and repeated-fragment recovery.
- Nested and initial citation fragments, topic and main navigation, malformed fragments and all 20 audit targets.
- All 101 copy handlers, with successful and denied clipboard API responses, correct per-entry URLs, selected manual fallback and stale-feedback recovery.
- Print preparation, non-blocking completion, exact filter/disclosure restoration, failed-print recovery and clearing an earlier error on retry.

These tests parse the real HTML and dispatch events to the real application handlers. Location, animation frames, focus/selection, reflected disclosure state, clipboard and printing are explicitly modelled. They verify handler logic and DOM state; they do not verify browser rendering, native click/keyboard activation, actual clipboard permissions, or operating-system print dialogs.

The regression test was also run against the inline script from commit `d88519d58f3c4bfc232a8b7834f8166254feacc8`. It failed with `Analysis summary click must keep its native disclosure default`, confirming that the test detects the original click-cancellation bug.

Command used in this environment:

```bash
LINKEDOM_WORKER_PATH=/tmp/rfrm-linkedom-0.18.12.mjs node tests/control_runtime.mjs
```

The standalone worker was fetched from the upstream `WebReflection/linkedom` 0.18.12 GitHub source; SHA-256 `38824d3d2933bd753456e7e87558121cfd31c1c08dedcd72ef4be9a75907322c`. It is a temporary test dependency, not a site asset. Elsewhere, install the pinned test dependency with `npm install --prefix tests` and run `npm test --prefix tests`.

The static audit and Python/JavaScript syntax checks passed after the fixes. The browser suite now includes actual clicks on every summary and copy button, every desktop/mobile topic control, the Search button, deep links and print recovery. A browser run was attempted again but stopped at local server startup with `PermissionError: [Errno 1] Operation not permitted`. None of its browser checks executed. The browser verification limitation above therefore still applies.


## Reading and navigation revision — 28 October 2026

Implemented the five requested improvements: a Start here overview with three initial findings and five native expansions; an expandable original-number index; four everyday shortcuts; two sourced arithmetic figures in the opening overview; compact entries with supplementary evidence inside analyses; and phone reading controls with a Back to results link in every expansion.

Shortcut membership is explicit in the authoring generator and leaves the original article order/categories untouched. Shortcuts, search and original topics combine with AND; repeating a shortcut removes it. Clear-all, empty-state reset and policy-fragment recovery clear shortcut state. Printing snapshots and restores shortcuts along with query/topic and all native disclosures.

The UC figure retains the full existing annual £486 tax-saving example, £267.30 UC deduction and £218.70 retained amount, with full 55% taper exposure, sufficient entitlement, work-allowance and unchanged-NI assumptions and the existing exclusions. The four pairs of annual NI/levy bars are derived from the unchanged fiscal table: £7.14bn, £6.96bn, £6.76bn and £6.77bn in 2028/29–2031/32. Labels show costs/receipts as magnitudes on a shared zero-based scale and explicitly distinguish published funding assumptions from predicted behavioural effects. Existing source links accompany both figures. No new external source claims or JSON edits were introduced.

Completed checks:

- `python3 tests/static_audit.py` passed, including 3+5 overview structure, the 64-number disclosure, compact evidence placement, source-backed figure amounts/years/labels, all prior content/source/table integrity checks and unchanged summary hash.
- `LINKEDOM_WORKER_PATH=/tmp/rfrm-linkedom-0.18.12.mjs node tests/control_runtime.mjs` passed all ten regression groups. New coverage checks each shortcut’s expected categories/entries, query/topic intersections, repeat-toggle, clear-all/empty reset, policy-hash recovery, filter-preserving return links, overview fragment expansion, native-summary defaults, reading-control focus, and shortcut restoration after printing.
- The pinned upstream LinkeDOM worker was restored via the GitHub connector after the temporary dependency disappeared during environment refresh. It remains a temporary test dependency, not a hosting asset.
- The authoring generator and both Python tests passed syntax compilation; generated inline JavaScript passed `node --check`.

The browser smoke suite was updated for native overview/index expansion, shortcut navigation, moved evidence panels, phone toolbar focus/clearance and no-JavaScript/print visibility. It was **not rerun** because of the previously established socket restrictions. No new screenshots were captured or inspected. Sticky positioning, overflow, actual native interaction, keyboard defaults, mobile/desktop layout and print rendering remain unverified in a real browser; the existing browser limitation above continues to apply.


## Topic navigation return — 28 October 2026

Every Browse the plan topic link, including All topics, now applies its filter and then focuses and scrolls to the explorer heading through the same helper used by everyday shortcuts. The runtime test checks heading focus and the scroll target for every topic link; browser coverage checks focus but remains unrun under the existing restriction. Static audit and all ten DOM/runtime regression groups passed after regeneration.
