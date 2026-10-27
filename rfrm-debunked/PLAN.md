# Approved implementation brief

Build “rfrm debunked”: a searchable public evidence page examining the supplied Economic Rescue Plan for a general UK audience, in plain British English. This is an implementation handoff, approved before construction; implementation is local pending repository review.

## Scope and content

- Preserve the source summary unchanged. Cover exactly 64 numbered measures, in their original order and ten original categories, with permanent IDs `measure-01` through `measure-64`.
- Add unnumbered supporting claims for all headline, tax, bill, welfare, spending, education, health, pension and fiscal proposals. Record a coverage inventory in RESEARCH.md; duplicate proposals link to their numbered analysis.
- Every article carries the attributed proposal, original number where applicable, category and printed PDF page, one visible counterargument, and a native details disclosure labelled “Debunked” with 120–200 words of analysis, relevant sources and related articles.
- Research real sources and record publisher, title, date, exact URL, access date and supported finding. Prefer UK primary evidence, verify jurisdiction and legal status, separate forecast from fact and trade-off. Do not imply the supplied PDF has independently verified official provenance.
- Include complete, faithful transcriptions of the savings table on printed page 22 and fiscal table on page 31. Preserve every year, value and empty cell; explain nominal £bn, parentheses, cash versus accounting, gross versus net, current deficit versus borrowing, and unverified model assumptions.

## Design and access

Use the reviewed repository frontend design skill: calm contemporary public-policy reference, original measure numbering as its memorable device, restrained dividers and left-aligned reading. Tokens: background #F4F6FA, surface #FFFFFF, ink #172033, muted #526079, accent #234BB5, analysis #71345D. Georgia headings and system sans body at 18px/1.65; text about 68ch. Spacing 8/16/24/32/48px. Desktop maximum 1200px with sticky 220px topic sidebar; stack below 900px and show a labelled native topic select. No decorative imagery, charts, excess motion, truth scores or blanket false verdicts.

## Behaviour

All article content is static HTML, readable without JavaScript. Hide enhanced controls until initialisation. Search title, proposal, counterargument and collapsed analysis case-insensitively, with exact `#12` queries. Combine search AND topic. Sync desktop and mobile filters, announce result count, hide empty headings, provide clear/reset and no-results states. Keep focus stable and preserve original order. Baseline topic links work without JavaScript.

Permanent article hashes clear conflicting filters, reveal their article, open its disclosure and focus its heading. Copy links provide a selectable URL fallback. Print reveals all articles and analyses, includes citation URLs, and restores filters and disclosures afterwards. Support file:// and ordinary static HTTP hosting, keyboard navigation, 320/390px mobile, desktop and 200% zoom, reduced motion and no global overflow.

## Files and delivery

Work only inside this project. Use vanilla HTML/CSS/JS with one runtime index.html, inline styles/scripts, no framework, backend, dependencies, runtime Markdown fetch or AI service. Authoring helpers and structured content may generate the committed static page; readers need no build. Add project AGENTS.md, RESEARCH.md, this PLAN.md, and meaningful browser/static tests within tests/. Do not mutate the remote repository until integration review.

## Acceptance

Check exact numbering/category/page/coverage, article lengths and citations, table transcription and fiscal treatment. Exercise title and collapsed-text search, #12, AND topic, empty/reset, multiple disclosures, initial/changed hashes including filtered targets, copy fallback, print/restoration, file and HTTP, JavaScript disabled, keyboard focus, reduced motion, 320/390/1440 widths, 200% zoom, screenshots and browser errors. Report only checks actually run and any evidence limitations.
