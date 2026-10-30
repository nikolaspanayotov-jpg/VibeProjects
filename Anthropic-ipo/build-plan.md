---
title: "Anthropic IPO page: implementation plan"
prepared_on: "2026-10-30"
status: "Implemented, verified, and published privately on 2026-10-30"
design: "design-and-content-plan.md"
review: "design-review.md"
---

# Anthropic IPO page: implementation plan

## Starting point

Build from the revised [design and content plan](design-and-content-plan.md) and its completed [second-pass review](design-review.md). The source material is [the Anthropic summary](key-points-summary.md) and [the SpaceX hindsight analysis](../SpaceX-ipo/key-points-and-anthropic-comparison.md).

The implementation is complete in [index.html](index.html). Browser evidence, corrected findings, limitations, and publication details are recorded in [tests/VERIFICATION.md](tests/VERIFICATION.md). The original implementation sequence below is retained as the maintenance specification.

Private viewing link: https://anthropic-ipo-briefing-20261030.jazzychord256.chatgpt.site

The approved follow-up improvements are specified in [reading-experience-plan.md](reading-experience-plan.md): a 60-second opening brief, per-$100 financial explanations, three reading priorities, paired SpaceX implications, and source previews. This supplements the original implementation sequence below.

The second approved set adds three H1 financial perspectives, an indexed dilution illustration with native controls, a dated milestone roadmap, first-use definitions, and chapter reading estimates/position indicators. These remain within the standalone architecture and preserve the original dated research. The numerical illustration uses hypothetical indices rather than Anthropic valuation inputs.

Completed preparation:

- [x] Locate and read the user's Frontend Design skill in the connected VibeProjects repository.
- [x] Read root repository instructions and inspect a nearby static project.
- [x] Synthesize both research documents into a page outline and real content.
- [x] Define typography, palette, spacing, responsive structure, and interaction behavior.
- [x] Recheck the design, revise navigation and evidence qualifications, and verify ledger arithmetic and base text contrast.
- [x] Prepare the implementation sequence and acceptance conditions below.

## Architecture and file boundary

Start with one **`index.html`** containing semantic HTML, inline CSS, inline JavaScript, the approved data, and source links. It must open directly from disk and run under a basic static server. Use native controls and inline SVG where useful. No framework, bundler, backend, charting package, runtime market API, or project-root package manifest is needed.

Keep work inside `Anthropic-ipo`. Preserve the directory's case and existing research files. The intended GitHub Pages path is `/Anthropic-ipo/` under the repository's configured host; confirm the actual host before adding a canonical URL. The user explicitly requested this folder and the existing paths have been shared, so do not rename it to satisfy a new-folder convention.

```text
Anthropic-ipo/
  key-points-summary.md             existing research; preserve
  design-and-content-plan.md       reviewed design
  design-review.md                 completed specification review
  build-plan.md                    this document
  index.html                       implemented production page
  AGENTS.md                        project maintenance notes
  tests/                           verification artifacts/tools
    VERIFICATION.md                evidence from actual implementation checks
    screenshots/                   reviewed mobile/desktop captures
```

The SpaceX Markdown document is an authoring input. The deployed page must not fetch or import files from `../SpaceX-ipo/`; embed the selected facts and original source URLs locally. Markdown links between planning documents are not runtime dependencies.

If integrating these workspace artifacts into a fresh repository checkout, inspect the current tree and Git status first. Preserve both research files and unrelated projects. Do not clone over the non-empty working folder or overwrite remote content blindly. Re-read any updated root/project instructions before implementation.

## Phase 1: establish the publication dataset and copy

**Result:** a small, traceable content model and edited page copy, ready to place into the HTML.

1. Reopen the linked Anthropic filing and check for amendments or a final prospectus. Determine whether the page remains an explicitly dated snapshot or can accurately incorporate newer terms. Do the same for material SpaceX updates used in the case study. Keep historical price observations dated even if a newer quote exists.
2. Extract the precise financial inputs, commitment terms, governance descriptions, and selected SpaceX events used by the design. Link each to an original source and locator. Review the reported identification of Customer B separately from the filed concentration percentage.
3. Finalize the 1,800–2,400-word main reading path. Put further contract rows, accounting explanations, comparison metrics, definitions, and source detail into supporting disclosures. Keep material qualifications visible.
4. Retain source dates, units, periods, and status in the data. Unavailable offer fields remain unavailable; do not substitute zero, a rumored valuation, or an assumed trading date.

Suggested authoring records, kept inline in the production file rather than as a runtime-fetch requirement:

| Record | Required fields / rule |
| --- | --- |
| Source | Stable ID, publisher, title, document date, section/page locator, original URL, checked date. |
| Financial metric | Stable ID, company, period start/end, measure, units, numerical value, precision, source IDs. Distinguish flow periods from balance-sheet dates. |
| Evidence status | Filing disclosure, calculated, management outlook, third-party report, or analysis. Calculations retain their inputs and formula. |
| Commitment | Counterparty, disclosure date, amount, basis such as minimum/ceiling/estimate, term, delivery conditions, cancellation rights, and overlap note. |
| Price observation | Date, USD price, offer/open/close/intraday type, session where relevant, source IDs. Never invent observations between recorded dates. |
| Offering status | Proposed/confirmed/not specified in this filing, effective as-of date, original source. |

The 900% retention metric, any annualized revenue figure, and accounting margin definitions need attached qualifications. Treat market and filing dates as civil date strings; format the year/month/day components directly so browser timezone conversion cannot move an observation to a different day.

**Done when:** every displayed material claim has a source or is explicitly analytical; all numeric periods and units are unambiguous; and all unresolved terms have honest visible wording. This can be completed without guessing final offer terms.

## Phase 2: implement the static reading experience

**Result:** the entire page is useful before JavaScript enhancement.

Implement the seven sections and stable anchors exactly as specified: `overview`, `economics`, `drivers`, `commitments`, `spacex`, `watchlist`, and `sources`.

- Add one H1, logical H2/H3 hierarchy, `header`, `nav`, `main`, `section`, and `footer` landmarks, a skip link, and meaningful figure/table captions.
- Build the opening status list and real filing link. Add the thesis and three takeaways before supporting detail.
- Render the default H1 operating ledger and both periods' exact data in accessible tables. Preserve all four expense categories and the signed GAAP operating result.
- Group annual revenue separately from half-year revenue. Explain why net loss differs from operating loss and cash use.
- Render the six paired driver/risk themes. Each has evidence, implication, and a “Watch” statement; use native detail disclosures for added depth.
- Render commitments and ownership as separate mechanisms. The SpaceXAI ceiling, timing, and cancellation terms stay together. Avoid a combined commitments total and an unsupported ownership pie chart.
- Render the SpaceX selected-event chronology, supplier/customer relationship, lessons, and matched-period comparison. Attribute the customer identity beside the 34.5% percentage.
- Complete the offering watchlist, three conditional scenarios, definitions, and source index.

Use a single citation convention: descriptive inline links to stable local source entries, and original outbound links at those entries. Every internal citation has a valid target. Do not make the user open a disclosure merely to learn that an amount is a ceiling or a forecast.

**Done when:** keyboard and no-JavaScript readers can access all substantive content and source links, including both financial periods.

## Phase 3: apply the visual system and responsive layout

**Result:** a recognizable, readable implementation of the reviewed design at mobile and desktop sizes.

Implement the six base colors as `:root` variables, plus explicit derived surface/divider fallbacks. Use Archivo and Source Sans 3 with a resilient fallback stack, limited weights, and font display behavior that preserves visible text.

Build mobile-first at **390px**. Keep 18px gutters, readable type, at least 44px controls, and a single sticky header/Contents mechanism below the desktop breakpoint. At approximately 1100px, switch to the static masthead and a sticky contents rail. Set appropriate anchor offsets for each layout.

The operating ledger is the visual centerpiece. Use one zero point and a fixed 0–18bn axis for both views. Labels must fit outside short segments rather than shrinking into unreadable text. The complete table supplies exact values; the graphic does not depend on a tooltip. The relationship diagram and SpaceX events remain visually subordinate.

Keep essential tables compact. If detailed tables require horizontal scrolling, confine it to a labeled, keyboard-accessible region; the whole page must not scroll sideways. Avoid fixed-width children, hidden overflow that clips focus, or images that determine the page width.

**Done when:** the 390px and desktop compositions express the same hierarchy; section reading widths, table labels, the status panel, and source URLs remain usable with long text and font fallback.

## Phase 4: add the bounded interactions

**Result:** working enhancements that clarify the evidence without creating unnecessary controls.

| Interaction | Implementation behavior | Failure / fallback |
| --- | --- | --- |
| Period switch | Native radio group for H1/Q2 2026. Update only the ledger's title, bars, figures, and result. Announce one concise result through a polite live region. Keep focus on the chosen control. | Hide the switch without JavaScript; show default H1 graphic and both exact-period datasets. |
| Contents | Real anchors; native small-screen disclosure. A modest current-section indicator may use `IntersectionObserver`. | Anchors and native disclosure work without observers or scripts. |
| Details and sources | Native `<details>` / `<summary>`; expanded content adds definitions, terms, calculations, or sources. | Native browser behavior requires no custom accordion code. |
| Event details | Open a dated SpaceX event to read its context and sources. Preserve the observation type in the summary. | Core date/price/context remains a readable list. |
| Print | Print CSS reveals supporting content and source URLs, removes sticky positioning and switches, and avoids clipping figures/tables. Use print lifecycle handling only if browser behavior requires it. | The static text and exact tables are printable even without JavaScript. |

Use small plain functions, `camelCase`, `UPPER_CASE` constants, and DOM references ending in `El`. Derive the selected view from one data object; do not duplicate formula logic in several listeners. Scope CSS through component classes to avoid section/element selector conflicts.

No theme switch, valuation calculator, saved preferences, search engine, sign-up, quote feed, countdown, or automatic animation is required. The current page has no persistence requirement. If future work adds preferences, use a namespaced, versioned storage object with guarded reads and writes as the root rules require.

**Done when:** every visible control has an observable and accurate result, keyboard operation works, and no-JavaScript content remains complete.

## Phase 5: verify the implemented page and correct findings

**Result:** browser evidence and a written record of checks actually run.

Run meaningful checks appropriate to financial content and the interactions:

1. **Content and arithmetic:** reconcile the ledger totals and signed results, check displayed rounding, period labels, and citations; check that unavailable fields do not become zeros. Confirm there is no summed mixed commitments total or interpolated SpaceX price data.
2. **Matched comparison:** verify H1 company/period assignments, capex definitions, and the visible qualification. Check source attribution for Customer B and the source date for every price.
3. **Native browser behavior:** load through a static server and exercise anchors, mobile Contents, radio switching, source links, and disclosures. Check errors and console output. Verify direct-file use as well when the environment permits it.
4. **Responsive rendering:** inspect **390px** first, then approximately **1440px** desktop, plus a **320px** overflow check and 200% zoom/reflow. Capture and actually inspect screenshots. Check long source URLs, focus outlines, table wrappers, and the fixed chart scale.
5. **Accessibility:** keyboard-only traversal, native radio navigation, visible focus, useful chart description/table, semantic headings, and meaningful source-link names. Recheck actual foreground/background pairs, including tinted panels and selected/focus states. Automated checks supplement manual review.
6. **Resilience and print:** disable JavaScript, block web fonts, enable reduced motion, and inspect print/PDF output. Ensure expanded details, sources, and period labels survive. Use browser print handling only where it fixes an observed issue.

Use available browser tooling; any test-only packages belong in `tests/`, not the app root. Avoid a broad suite that simply mirrors the markup. The important regressions are factual display, period changes, unavailable data, accessible controls, and reflow.

Record viewport/browser details, commands or scenarios, inspected captures, findings, fixes, and any unavailable checks in `tests/VERIFICATION.md`. Do not describe a check as passed if the environment could not run it. Correct observed issues and repeat only the affected checks unless a fix has broader impact.

**Done when:** the implemented reading path and interactions are verified, material defects are corrected, and remaining limitations are explicit.

## Phase 6: package for the repository and later publication

**Result:** a self-contained page and maintenance notes, ready for the user's requested next action.

Create project `AGENTS.md` with purpose, local serving instructions, architecture, stable anchor/data IDs, visual tokens, source-refresh rules, and important financial distinctions. Document the intentional directory case. Explain why SpaceX data remains a historical case study and why no runtime imports reach other project folders.

The completed page was first published privately through Sites, with an exact export of the canonical HTML. The source archive, pushed hosting commit, and successful deployment are recorded in the verification document. The page and supporting text documents are maintained in the user's requested `Anthropic-ipo/` folder on the VibeProjects `main` branch. Before subsequent publication, inspect the latest repository instructions and diff, reconfirm the dated source status, and verify the configured path.

No additional stack selection or mandatory design sign-off is needed to start implementation. If final offer terms remain unavailable, the static guide can still accurately show the dated preliminary status. A numerical valuation model would be a separate extension after reliable capitalization and explicit modeling assumptions are available.

## Implementation completion checklist

- [x] Real copy from both research documents, with Anthropic as the main subject.
- [x] Sources, dates, units, and visible material qualifications.
- [x] Correct H1/Q2 ledger and a fixed scale.
- [x] Balanced drivers and risks; commitments, dilution, and control explained separately.
- [x] SpaceX events labeled by price type; no claimed deterministic unlock effect.
- [x] Customer relationship and third-party attribution handled accurately.
- [x] Native interactions and no-JavaScript/font fallbacks checked; accessibility limits recorded.
- [x] Mobile, desktop, print, keyboard, and console checks recorded.
- [x] Self-contained `index.html`, updated project instructions, preserved research documents.
- [x] Filing-status review and explicitly dated research snapshot before private publication.

Repository references: [root instructions][repo-rules], [Frontend Design skill][skill].

[repo-rules]: https://github.com/nikolaspanayotov-jpg/VibeProjects/blob/87e1fd38fccc5bae14020d99a7676fe6d4e13f21/AGENTS.md
[skill]: https://github.com/nikolaspanayotov-jpg/VibeProjects/blob/87e1fd38fccc5bae14020d99a7676fe6d4e13f21/.agents/skills/frontend-design/SKILL.md
