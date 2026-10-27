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

Browser tests have **not passed and runtime behaviour has not been verified**. No mobile or desktop screenshots were captured or inspected. No successful browser check of search, filters, disclosures, hashes, copying, printing, keyboard focus, reduced motion, overflow, zoom, file URLs or HTTP hosting is claimed.

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
