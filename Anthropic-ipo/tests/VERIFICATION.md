# Implementation verification — 30 October 2026

The standalone [page](../index.html) implements the reviewed design using both the Anthropic and SpaceX research documents. Those research documents were preserved. The page clearly identifies the 30 October research snapshot, the preliminary 26 October filing, and historical SpaceX observations through 29 October. It has no live quote feed.

## Current reading experience revision

All five improvements approved by the user are implemented. See [reading-experience-plan.md](../reading-experience-plan.md) for the accepted scope.

- Three numbered opening questions pair filed facts with visible qualifications, citations, and onward links.
- The ledger leads with the signed GAAP result. Operating margin and rounded operating expenses per $100 revenue are derived from the same integer data as the bars: **H1 −$693m, −4.3%, about $104; Q2 +$974m, +8.4%, about $92**. Formulas and both periods remain available in the exact-data table without JavaScript. Operating expenses are explicitly distinguished from cash spending.
- Demand quality, compute economics, and valuation/dilution lead the driver section, with the editorial priorities labeled as analysis. All six original paired themes remain available; products, partners, and trust are grouped in a native supporting disclosure.
- Three dated SpaceX observations are paired with Anthropic investment questions. The seven-event chronology remains available in a disclosure. Limits of inference and differences between the businesses are visible.
- All **20 source entries** have local previews with provenance, dates, source-index research notes, original links, and verified excerpts where available. Seven short excerpt variants across five source entries were checked verbatim against the retained original filing text after whitespace normalization. Customer, financial, and compute citations choose the relevant MD&A excerpt. Other text is labeled as a research note. Market-data dates describe observations/cutoffs rather than invented publication dates. The filed Customer B concentration and Bloomberg identification have separate labels.

### Current checks and evidence

`python tests/browser_smoke.py` completed with **38 checks passed and one direct-file check unverified because administrator policy blocks file URLs**. The current [machine-readable results](browser-results.json) supersede the initial run below.

The browser tests cover the opening questions; three primary and three supporting themes; paired lessons and chronology; H1/Q2 results, margin, per-$100 values and fixed scale; all 20 previews; contextual excerpts; dates/provenance; original links; keyboard activation; forward/backward Tab containment; Escape and explicit Close; focus and article-scroll restoration; source-list handoff; and 320px preview scrolling to its actions. Existing 320/390/768/1440px reflow, mobile navigation, table, reduced-motion, increased-text, no-JavaScript, font-fallback, console, runtime-request, and print checks also passed.

Actual screenshots inspected in the local `screenshots/` directory: `mobile-briefing.png`, `mobile-economics.png`, `mobile-source-preview.png`, `desktop-briefing.png`, `desktop-drivers.png`, `desktop-spacex.png`, `desktop-source-preview.png`, `mobile-spacex-implication.png`, and `mobile-supporting-drivers.png`. The composition preserves the existing type, palette, financial-bar scale and native disclosure conventions.

The initial keyboard check exposed native Tab navigation reaching browser chrome at the edge of the preview. Explicit first/last-control wrapping corrected this; the full browser suite then passed. Print inspection exposed a split introduction and stranded exact-table header. Print CSS now starts the economics section on a new page, keeps its introduction together, and keeps the exact ledger table together. Only the affected print checks were repeated after that print-only correction.

The regenerated local PDFs contain **21 A4 pages with JavaScript** and **20 without JavaScript**. Text extraction verified the opening brief, derived values, supporting themes, all seven dated events, customer attribution, commitments and original SEC URLs in both. The economics introduction, result and full ledger were confirmed on page 2; that printed page was visually inspected after correction. The source-preview modal is excluded from print; the complete source index remains.

Remaining limits from the initial record still apply: Chromium only, no screen-reader session, no exhaustive external-link/source refresh, and direct-file loading blocked by environment policy. The 720px/doubled-body-text check does not establish every browser's 200% zoom behavior. Research dates and historical-price qualifications have not been advanced.

Canonical page SHA-256 for this revision:

```text
db0822c0c86692fc5e6268c259c58bf948bfe23fe6b69a93b61b81991dd08ed8
```

The revised private publication returned **`succeeded`** at 10:36:21 UTC on 30 October 2026, at the unchanged URL: https://anthropic-ipo-briefing-20261030.jazzychord256.chatgpt.site

- Pushed hosting commit: `476654aeccdc511209d026cf245c624e2ae078b2`.
- Saved version: `appgprj_6ae463759fc48191915e2a0679c838bb~appgver_ae169ba619488191857f214ef66fb997`.
- Deployment: `appgdep_6ae4731962d08191a14002f99d1e6364`.
- Canonical HTML and the pushed hosting export have the identical SHA-256 above. Site identity and owner-only audience were retained. The source archive was built from the pushed export; no credential was persisted.
- The same canonical source and supporting text records are maintained in GitHub under `VibeProjects/Anthropic-ipo/` on `main`. Generated PDFs/screenshots remain local and ignored.

## Initial implementation record (historical)

The entries below describe the first publication. Current results, PDFs, and captures have been refreshed for the revision above; original commit/deployment identifiers are retained as history.

## Result

**Private page:** https://anthropic-ipo-briefing-20261030.jazzychord256.chatgpt.site

The Sites deployment returned `succeeded`. Its generated desktop screenshot was downloaded and visually inspected; the expected title, filing-status panel, typography, and preliminary terms rendered correctly. The capture is retained locally as `screenshots/published-preview.jpeg`.

Canonical repository folder: https://github.com/nikolaspanayotov-jpg/VibeProjects/tree/main/Anthropic-ipo

The HTML, research, reviewed plans, maintenance notes, test script, results, and this verification record are versioned in GitHub. Generated screenshot and PDF artifacts remain in the execution workspace and are ignored in Git; their paths below are local evidence references.

## Browser checks actually run

The page was served with `python -m http.server 8765 --bind 127.0.0.1` from the project folder. Tests ran with the available Python Playwright installation and `/usr/bin/chromium` (Chromium 154):

```sh
python tests/browser_smoke.py
```

The initial run recorded **26 checks passed; one direct-file check was unverified because of browser administrator policy.** The linked JSON now contains the current revision's results.

- HTTP 200, visible preliminary offer terms, and default H1 content.
- Every internal citation and navigation target exists.
- Integer financial reconciliation: H1 expenses $16,979m and operating result −$693m; Q2 expenses $10,581m and operating result +$974m.
- H1/Q2 switching updates the period, figures, sign, live announcement, and bar geometry on the same 0–18bn scale.
- Native radio arrow-key operation and focus retention.
- Mobile Contents closes after navigation; the target clears the sticky header. Desktop active navigation tracks the reading position.
- No page-wide horizontal overflow at 320, 390, 768, and 1440 CSS pixels, including expanded exact-data tables. Wide tables scroll within their labeled region.
- Expense segments have visible height at mobile, tablet, and desktop widths.
- Reduced-motion mode, JavaScript disabled, and embedded-font fallback preserve readable content. Without JavaScript, the non-working period switch is hidden and both periods remain in the exact-data table.
- Reflow with a 720px viewport and doubled body text. This is the specific increased-text check performed; it is not a claim of testing every browser's 200% zoom behavior.
- No page errors, console errors, or third-party runtime requests during the test.
- JavaScript-enabled and JavaScript-disabled print PDFs generated successfully.

## Visual review and corrections

Actual captures inspected included `screenshots/mobile-top.png`, `screenshots/mobile-economics.png`, `screenshots/desktop-top.png`, `screenshots/desktop-economics.png`, and `screenshots/desktop-spacex.png`. Full-page captures and additional fallback states are also retained locally in `screenshots/`.

The review led to these corrections:

- Adjusted headline wrapping to avoid an isolated final word.
- Corrected anchor offsets and current-section tracking.
- Removed a conflicting percentage-height rule that collapsed the desktop expense bar. Added a meaningful visibility regression check.
- Outlined light chart segments and strengthened their legend boundaries.
- Increased small supporting text to at least 14px.
- Kept the financial ledger together in print after inspecting a split card.

The complete browser suite passed after the bar correction. The final print-only pagination change was checked by regenerating both PDFs and inspecting the affected printed ledger.

## Print

The initial PDFs each contained **18 A4 pages**; current artifacts have been regenerated as described above. Print CSS expands supporting details, removes sticky controls, and exposes source URLs. Text extraction confirmed supporting figures and original SEC URLs survived in both initial versions. Printed pages were visually inspected, including the complete financial ledger after the pagination correction. The embedded font licenses are present in the HTML source and intentionally do not print as page content.

## Content and source boundaries

The page was checked against the research and reviewed design, including financial arithmetic, matched H1 periods, price types, contract ceilings/cancellation terms, and the distinction between filed Customer B concentration and Bloomberg's reported identification. The original Anthropic S-1 cover was reopened before publication and still specified no final offer price or trading date. The page retains an explicitly dated snapshot rather than asserting live offering status.

All internal citation targets were tested. This was not an exhaustive reachability audit of every external link, a fresh independent audit of every filing claim, or a causal attribution of every SpaceX price change. Market explanations remain qualified analysis.

## Remaining limitations

- Direct `file://` navigation returned `ERR_BLOCKED_BY_ADMINISTRATOR` in this environment. It is recorded as unverified; the policy was not bypassed. Static HTTP serving works, and the page has no external runtime dependencies.
- No assistive-technology screen-reader session was available. Native semantics, keyboard radio operation, focus retention, and the live-region update were checked, but this is not a full accessibility certification.
- Browser evidence uses Chromium; Safari and Firefox were not run.
- The research snapshot must be refreshed before representing the page as current after 30 October 2026.

## Exact publication record

The canonical HTML and the Sites `dist/index.html` export have the same SHA-256:

```text
a6a5a2b9631bb8d1c9107fd3fcbec90be38bc44bda2214f547a7d6c14bdd2f93
```

- Hosting workspace: `/workspace/sites/anthropic-ipo-briefing`
- Pushed hosting source commit: `0b1ca666311a5256157550156f3f3197bf119198`
- Project: `appgprj_6ae463759fc48191915e2a0679c838bb`
- Saved version: `appgprj_6ae463759fc48191915e2a0679c838bb~appgver_b270d4188fb8819199e0a6999f23992e`
- Deployment: `appgdep_6ae467ccdc8881919d9a8acaacfc4a96`
- Deployment status: `succeeded`, 30 October 2026 at 09:48:50 UTC.
- Sites audience: private. The GitHub repository is public and its source publication is separate from Sites access controls.

The source archive was built from the pushed state with `.openai/hosting.json` and `dist/index.html`. No hosting credential was written into project files or Git configuration. The repository's Frontend Design skill guided implementation; Sites provided the private publication.
