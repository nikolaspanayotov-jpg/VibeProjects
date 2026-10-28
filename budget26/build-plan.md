# Budget 26 — build plan for Codex 6.1 Sol

Approved direction: a neutral, accessible Budget explainer for general UK readers, based on `key-budget-points.md`, covering the edition published 28 October 2026.

## 1. Purpose and constraints

Help readers understand the main announcements, find relevant changes, check start dates and geographical coverage, and distinguish government policy from the OBR's assessment. Use the existing markdown as the editorial source of truth. Preserve all amounts, dates, qualifications and source references.

Follow the VibeProjects root AGENTS.md and shared frontend-design skill, including its original design-principles reference. Borrow rfrm-debunked's useful reading patterns: topic navigation, searchable static content, native expandable detail, permanent links, clipboard fallback and print restoration. The Budget page is a neutral explainer, without that project's critical framing or measure numbering.

Build one runtime `index.html` containing semantic HTML, inline CSS and inline JavaScript. Preserve the source markdown and PDF. Use relative local paths; support both file:// and static hosting at /budget26/. Add project AGENTS.md and focused verification scripts. No framework, package manager, build step, backend, API, runtime markdown loading or persistent user state is required. Verify locally; publishing is a separate step.

## 2. Visual design and layout

Headline: **Budget 26: what changes, and when.**

Introduction: A plain-English guide to the 28 October 2026 Budget: taxes, bills, public spending and the OBR outlook.

Use a contemporary public-information design. The memorable element is a calendar rail connecting announcements to commencement dates. Keep the remaining composition restrained, with open policy sections and dividers. Contained panels are reserved for the opening calendar and significant OBR qualifications.

| Token | Value | Use |
| --- | --- | --- |
| Background | #F4F7F8 | Page background |
| Surface | #FFFFFF | Panels and controls |
| Ink | #162D3A | Main text |
| Muted | #526674 | Secondary text |
| Accent | #006B63 | Links, selection and focus |
| Line | #CDD8DE | Dividers |

Use Public Sans, with system-ui/sans-serif fallbacks; an optional Google Fonts stylesheet uses display=swap. External font failure must not affect functionality. Body type is 18px desktop and 17px mobile at 1.65 line-height. Headline is 38–64px, section headings 28–36px, policy headings 22–26px. Limit reading width to approximately 68ch. Use tabular numerals for figures. Spacing: 8/12/16/24/32/48/72px. Main maximum width 1220px; horizontal padding 20px mobile and 32px desktop. Controls have at least 44px touch targets, visible focus and 8px corners. Avoid decorative imagery, gradients, automatic entrance animations and counters.

Page order:

1. Sticky masthead: Budget 26 home link; Overview, Changes, OBR, Dates, Sources.
2. Opening headline, edition date, introduction, Explore the changes and Read the OBR outlook links. Calendar rail: 29 October 2026 (LISA), January 2027 (energy payments/bus cap), April 2027 (main changes).
3. Six concise overview takeaways, linked to relevant content.
4. Changes: search, six topic filters and the 48-entry policy inventory below.
5. OBR: forecast chart, complete data tables, eight assessment points.
6. Dates: an expanded twenty-entry timeline preserving the original ten rows' coverage, with exact dates, event labels and policy links.
7. Sources: original documents, editorial notes, access limitations and downloads.
8. Footer: edition date, independent explainer description and back-to-top link.

At 960px and above use a 220px topic sidebar and 40px gap. The sidebar sticks only inside the explorer and can scroll on short viewports. Below 960px use a single column and native topic select. The sticky mobile masthead has a native details Contents menu with a positioned dropdown. JavaScript closes it after a link choice or Escape; Escape returns focus to its summary. Provide adequate anchor clearance.

## 3. Content and behaviour

### Required inventory

Exactly 48 policy entries, retaining source section order:

| Topic | Entries |
| --- | --- |
| Bills and travel (8) | Household Energy Payment; domestic electricity VAT; fuel duty; bus fares; business mileage; public EV charging; food/heating-oil/fertiliser tariffs; longer-term energy reforms. |
| Tax, savings and pensions (8) | Headline taxes; savings income; property income; cash ISA; trading allowance; Pension Tax Allowance; pension death benefits; State Pension Triple Lock. |
| Work and housing (8) | Minimum wages; parental pay; Carer's Allowance; youth employment; Your First Home; social/affordable housing; LISA withdrawal charge; new First Time Buyer ISA. |
| Business and investment (11) | Corporation Tax; pub/music-venue rates relief; Small Business Rate Relief; other RHL rates; industrial electricity; Founders' Relief; BADR; employee share options; capital allowances; R&D administration; investment finance. |
| Funding and tax administration (8) | Bank surcharge; gaming machines; online marketplaces; private-hire operators; HMRC modernisation; Making Tax Digital; other duties; additional OOTLAR measures. |
| Public spending (5) | Spending discipline; defence funding; Ukraine; fiscal devolution; AI/security. |

Keep grouped measures grouped and preserve all their components. Outside the entry count retain the note explaining the additional two-point savings/property rate increases and the note explaining the prior-government baseline for £40bn/£120bn spending comparisons.

Each article has a descriptive permanent policy-* ID, linked heading, short visible explanation with its principal figure, visible When and Where information, and any implementation qualification. Preserve every original fact across the whole article. A native Details and sources disclosure adds eligibility, staged dates, exclusions or caveats that the summary has not already explained, followed by precise source references and Copy link. Do not paste the visible summary into the expanded text. For short measures with no additional explanation, label the disclosure Sources and show only the citations and Copy link. Aim for 30–60 words of visible summary where appropriate; do not pad short items. All editorial content must be in initial HTML and readable without JavaScript.

Use British English and absolute dates. Distinguish new policy, extensions, earlier policies being implemented, forecasts and consultations. Do not imply legislation passed solely because a commencement date is stated. Keep England/Great Britain/UK coverage distinct. Explain abbreviations. Retain annualised versus actual savings, annual versus multi-year spending, and investment/lending versus grants. Use clearly labelled illustrative arithmetic with explicit assumptions; do not estimate an individual reader's tax bill or determine their eligibility. Preserve the OBR debt qualification and Annex A access limitation.

### Audience routes, comparisons and explanations

Add a compact reading-routes section after the overview, with a hero shortcut and mobile Contents link. Four audiences—first-time buyers, pensioners, drivers and small-business owners—each have three ordinary links to relevant policies across topics. Keep the route links functional without JavaScript, and use existing fragment recovery with JavaScript. Routes suggest relevant reading, not universal eligibility.

Use three visible comparison panels in the trading-allowance, Business Asset Disposal Relief and cash-ISA entries. Show before/existing and announced/retained values, units and the difference. Remove repeated figures from the surrounding summary. Include comparison text in search.

Add two worked examples inside their relevant policy disclosures: 12,000 qualifying own-car/van business miles in 2027–28 gives 10,000 × 55p + 2,000 × 35p = £6,200; a qualifying £10,000 gross LISA withdrawal for a first home above £450,000 incurs a £2,000 charge at 20%, compared with £2,500 at 25%. Show the £500 reduction and £8,000/£7,500 available amounts. Preserve dates, eligibility assumptions and the distinction between a mileage reimbursement/deduction amount and resulting tax relief. Include examples in search and print.

Explain rateable value, writing-down allowance, equity loan, real terms, annualised estimates and GDP in a static glossary after the timeline. Dotted-underlined links at the point of use navigate to focusable definitions. Support ordinary keyboard/tap navigation and no-JavaScript reading. With JavaScript, offer a return button to the last originating term link; use a stable read-term-* fragment to restore context and reveal any filtered or closed containing policy. Do not rely on hover or store reading history persistently. Do not invent repayment terms for Your First Home.

### Navigation and search

Stable main anchors: overview, changes, obr, dates, sources. Policy IDs are descriptive and permanent; no original measure numbers are invented.

Desktop topic buttons and mobile select share a single selected topic. Search matches all query words case-insensitively across title, summary, dates, geography and closed detail text. Search AND topic determines results. Update while typing without moving input focus. Announce X of 48 policies shown in a polite live region; hide empty topic headings and provide Clear filters plus a useful empty state. Other page sections remain available. Topic selection moves to the explorer heading. Without JS, show ordinary topic links and all entries; reveal enhanced controls only after successful initialisation.

Initial, changed and repeated fragments reveal filtered targets, clear conflicting filters, open ancestor disclosures, focus the target heading and scroll below the masthead. Several disclosures can stay open. Copy success is announced with the policy title; clipboard failure reveals a labelled, selected, read-only URL field.

### OBR visualisation

Transcribe both markdown forecast tables exactly, preserving years, decimals and units. Render one compact SVG line chart from those HTML table values. Native metric select: GDP growth (default), CPI inflation, unemployment, borrowing £bn, borrowing % GDP, debt % GDP. Zero-based maxima are respectively 2%, 4%, 6%, £150bn, 5%, 100%. Label points and axes; distinguish calendar and financial years. Provide a textual chart summary. Hide the chart until initialisation succeeds. Both accessible tables remain in a native View all forecast data disclosure.

Identify figures as central forecasts published 28 October 2026. Include all eight assessment points from the markdown: living standards, fiscal rules, debt, tax, renters, pensions, risks and growth. Explain headroom. Display the 56% probability as attributed text.

### Timeline, sources and print

Preserve the original timeline's coverage in twenty chronological entries, with explicit Starts, Relief ends and Planned labels. Split 1 April wage changes from 6 April tax changes and include 2 January 2028 private-hire VAT. Distinguish the final relief day (30 June 2027) from the following fuel-duty change, and keep pension and Carer's Allowance dates separate. Preserve starts, expiries, consultation qualifications and month-only precision. Link each to relevant policies. Each policy disclosure links to its source and identifies printed page/paragraph or OOTLAR section. Budget PDF anchors translate printed page numbers to PDF page numbers by adding six. Source links use the existing official URLs and relative PDF location; offer the markdown for download.

Print this guide temporarily reveals all policies and opens every disclosure, then restores filters and disclosure states after printing. Hide navigation/controls in print, include all data tables and source URLs, and retain normal browser Print support.

## 4. Implementation stages

1. Build the semantic document and all content. Confirm 48 entries, six groups, six takeaways, twenty timeline entries, eight OBR assessments and exact tables before styling.
2. Apply tokens, typography, responsive layout and opening calendar; check 390px before desktop.
3. Add search, topic synchronisation, result counts/reset, fragment recovery, mobile navigation and clipboard fallback.
4. Add the table-derived forecast chart and print snapshot/restoration.
5. Validate, inspect screenshots and document operation in AGENTS.md. Keep tests inside tests/; no runtime dependencies or committed authoring generator.

Use small named functions. Interfaces introduced are the static /budget26/ page, its fragment URLs and relative document links; there are no API/database changes.

## 5. Acceptance

- Content: exact 48-entry inventory; all original details, amounts, dates, jurisdictions and caveats; six takeaways, twenty timeline entries, eight OBR points; cell-for-cell forecast tables and working citations.
- Functional: title/closed-detail search; all topic filters and AND combinations; empty/reset; desktop/mobile sync; initial/changed/repeated/nested/filtered fragments; multiple details; clipboard success/denial; six chart metrics; print/restoration.
- Runtime: file://, HTTP, nested /budget26/ path, JavaScript disabled and optional fonts unavailable.
- Visual: inspect 390px and 1440px screenshots; check 320px, 768px and 200% zoom. No global overflow; tables may scroll in labelled containers. No hidden anchor targets.
- Accessibility: semantic landmarks, logical headings, skip link, keyboard controls, visible focus, 44px targets, AA contrast, non-colour status cues and reduced motion. No browser errors or missing local assets.
- Run static audits for inventory, IDs, references and forecast values; browser tests for interactions. Report only checks actually run.

Done when a reader can grasp the headline changes, locate a policy, understand its timing/coverage, inspect its source and read the OBR qualifications on mobile and desktop.
