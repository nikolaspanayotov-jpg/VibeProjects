---
title: "Anthropic IPO page: design and content plan"
prepared_on: "2026-10-30"
status: "Design specification; reviewed in design-review.md"
implementation_plan: "build-plan.md"
---

# Anthropic IPO page: design and content plan

## Purpose and audience

Create an independent, source-linked investor guide to Anthropic's IPO. Help a financially curious reader answer three questions: what supports the business's value, what can impair returns per share, and what SpaceX's completed IPO teaches about entry valuation and trading risk.

The reader should understand the central argument in one minute, review the evidence in five to eight minutes, and follow sources for detail. The page should support informed judgment without presenting a recommendation, target price, or implied official affiliation.

The working title is **“Anthropic's IPO: growth, compute and the price you pay.”** Anthropic remains the subject throughout. SpaceX is a substantial supporting case study, rather than a second company landing page.

This task produces the design, a second-pass review, and an implementation plan. It does not create or publish the production page.

## Inputs and repository constraints

Use both existing research documents:

- [Anthropic key points](key-points-summary.md): financials, growth drivers, risks, compute commitments, governance, dilution, proposed offering, and missing terms.
- [SpaceX hindsight and comparison](../SpaceX-ipo/key-points-and-anthropic-comparison.md): dated trading observations, contemporary explanations, unlock behavior, matched-period financials, and the commercial relationship between the companies.

Follow the repository's [Frontend Design skill][skill], its [preserved design guidance][guidance], and [root AGENTS.md][repo-rules], read from the GitHub repository at revision `87e1fd38fccc5bae14020d99a7676fe6d4e13f21`. The skill's entry-point blob is `0022fbc9f6c1e1bfaecb6cbe99c537f4aef4162e`.

The nearby Budget 26 page was inspected for repository conventions. Reuse its principle of source-linked summaries and optional detail, while giving this project its own typography, composition, and core visualization.

Build later as a self-contained, build-free `index.html` with inline HTML, CSS, and JavaScript. No framework, backend, or runtime imports from another project. Keep the existing **`Anthropic-ipo`** directory name and case: the user explicitly requested it and its paths have already been shared. The repository's preferred lowercase naming applies to future new folders, not a rename here.

The editorial baseline is the research prepared **30 October 2026**, using Anthropic's **26 October preliminary S-1** and SpaceX regular-session prices through **29 October**. This design does not assert that these are live figures. Refresh source status during implementation and before any publication.

## Editorial position

Lead with this argument:

> Anthropic's growth is exceptional. Shareholder returns will depend on the price paid, the cost of staying at the AI frontier, and how much value reaches each share.

The page must preserve five distinctions:

1. Business growth and investment returns are different measures.
2. Reported revenue, annualized activity, and contracted revenue are different measures.
3. Operating results, net income, and cash flow answer different questions.
4. New shares create economic dilution; resale of existing shares changes tradable supply.
5. SpaceX illustrates mechanisms and a realized history; its chart does not forecast Anthropic's shares.

Use sentence case and plain explanations. Introduce terms such as float, retention, and rollover notes where the reader needs them. Do not make readers learn a glossary before understanding the argument.

## Visual direction

The visual concept is **an investment briefing organized around an operating ledger**. Its distinctive element is a proportionate comparison of revenue and operating expenses, with a period switch that reveals why a profitable quarter can coexist with a loss-making half-year. The surrounding page stays quiet and readable.

Use a white ground, deep blue text, a disciplined blue accent, generous spacing, and occasional pale panels derived from the core palette. The visual language should feel analytical and approachable. It should not imitate Anthropic's brand or use space imagery to imply that SpaceX is the subject.

### Color tokens

Six base colors; component backgrounds and dividers derive from these rather than introducing unrelated accents.

| Token | Hex | Role |
| --- | --- | --- |
| `--paper` | `#FFFFFF` | Page, reading surfaces, inverse text. |
| `--ink` | `#17324D` | Main text, headings, chart labels. |
| `--muted` | `#51657B` | Secondary text and period labels. |
| `--accent` | `#2348A5` | Links, selected controls, revenue bar, keyboard focus. |
| `--tailwind` | `#14675C` | Tailwind labels and positive operating-result text, always with words/signs. |
| `--headwind` | `#A53240` | Headwind labels and negative operating-result text, always with words/signs. |

Derive `--wash` by mixing 4% ink with paper and `--line` by mixing 22% ink with paper, with literal sRGB fallbacks. Dividers are decorative; input boundaries and focus outlines use stronger colors. Status and meaning never depend on color alone.

### Typography and spacing

- **Archivo**, weights 600/700, for headings: compact, confident sans-serif shapes suitable for a financial briefing.
- **Source Sans 3**, weights 400/600, for body, controls, and financial figures. Use tabular numerals, not a separate monospace data face.
- Fallbacks: headings `Arial, sans-serif`; body `system-ui, sans-serif`. The content must remain usable if web fonts fail.
- Body 18px, line height 1.6; supporting text at least 14px. Reading width 64–70ch.
- Heading scale: mobile H1 38–44px, desktop 56–64px; H2 28–36px; H3 21–24px. Do not shrink type to force a heading onto a fixed number of lines.
- Spacing steps: 4, 8, 12, 16, 24, 32, 48, 72px. Mobile section gaps 48px; desktop 72px.
- Content width at most 1180px, with 18px gutters at 390px and 32px gutters on larger screens.
- Text is left aligned. Numeric columns are right aligned. Headings use one treatment across the complete phrase, with no isolated accent word.

Use open reading sections and comparison rows. Reserve a restrained 10px radius for grouped controls and interactive panels. Do not turn every paragraph into a matching card. Motion is limited to brief user-triggered state changes; the primary content is visible without entrance animations.

## Page architecture and content

Target 1,800–2,400 words in the main reading path. Supporting disclosures, detailed commitments, the full comparison, glossary, and sources can expand the page to roughly 4,000–5,000 words when opened. Critical qualifications remain visible beside their claims.

| Section / anchor | Reader's question | Proposed content and presentation | Research basis |
| --- | --- | --- | --- |
| Opening, `#overview` | What is this page and where does the IPO stand? | Title, central argument, three short takeaways, clear filing date, and a compact offer-status list. | Anthropic: scope, central question, missing terms. |
| Economics, `#economics` | Does rapid growth produce durable profit and cash? | Operating ledger, period switch, short revenue history, and explanations of net losses and cash. | Anthropic: financial evidence and definitions. |
| Drivers and risks, `#drivers` | What could support or undermine value? | Paired tailwind/headwind rows, each with evidence, implication, and what to watch. | Anthropic: tailwinds and headwinds. |
| Commitments and ownership, `#commitments` | What claims on future cash and shares matter? | Contract terms, cash timing, governance, financing, and dilution; detailed arrangements expandable. | Anthropic: infrastructure exposure; governance and dilution. |
| SpaceX lessons, `#spacex` | How can a strong company have a difficult IPO? | Selected dated events, three lessons, supplier/customer diagram, and a compact matched-period comparison. | SpaceX: timeline, explanations, relationship, comparison, lessons. |
| Before pricing, `#watchlist` | What information would change the assessment? | Offering-term gaps, first-results watchlist, holder-specific releases, and conditional bull/middle/bear cases. | Both documents: valuation frameworks and update lists. |
| Sources and method, `#sources` | What is fact, interpretation, or unresolved? | Indexed original sources, definitions, data dates, and a short explanation of the historical comparison. | Source maps in both documents. |

### Opening copy and status

H1: **Anthropic's IPO: growth, compute and the price you pay**

Standfirst: “A guide to the business behind Claude, the demands of frontier AI, and the lessons from SpaceX's first months on the market.”

Three takeaways:

- “Revenue is scaling quickly; future compute costs can still pressure margins.”
- “The return on the business and the return on each share can diverge.”
- “SpaceX shows why valuation, financing and share supply matter after an IPO.”

The adjacent status list reads “Preliminary filing: 26 October 2026,” “Research prepared: 30 October 2026,” “Offer price: not specified in this filing,” “Trading date: not specified in this filing,” and “Proposed symbol: ANT.” Each unresolved field describes the source's status rather than implying the information can never become available.

The main link is **“Explore the economics”**, an in-page anchor. The secondary link is **“Read the filing”**, pointing to the SEC. Include a short “Independent analysis” line, not an Anthropic logo or official-looking approval seal.

### The operating ledger

This is the page's principal visual and interaction. Two horizontal bars start from a shared zero: reported revenue and total operating expenses. The expense bar has labeled component segments; the result is stated in text beneath it. Both periods use the same 0–18bn axis so switching periods cannot exaggerate the improvement by rescaling.

| Input, US$bn | H1 2026, default | Q2 2026 |
| --- | ---: | ---: |
| Revenue | 16.286 | 11.555 |
| Compute and infrastructure | 8.945 | 5.558 |
| Personnel | 3.152 | 1.857 |
| Sales, marketing and partnerships | 3.168 | 2.135 |
| Other operating and administrative | 1.714 | 1.031 |
| Total operating expenses | 16.979 | 10.581 |
| GAAP operating income / (loss) | (0.693) | 0.974 |

Above the graphic, a native radio group switches **“First half 2026”** / **“Second quarter 2026.”** Display the selected period in the title and in the textual result. Rounded visible amounts may use two decimals, with exact figures in the table. The table and the visible numeric summaries are the factual source; chart geometry is explanatory.

Always show: **“A profitable quarter does not establish sustained profitability. Management expects margins to fluctuate as more compute comes online.”** Link that sentence to MD&A.

Provide the complete table with a native “View the figures” disclosure. Without JavaScript, display the default H1 chart and both period tables; omit the non-working switch. No number animation or hover is needed to discover a value.

Below, use a small text table to separate FY2024, FY2025, H1 2025, and H1 2026 revenue. Keep half-years in a separate group, preventing an annual-versus-half-year chart from appearing to be a comparable time series. Keep the $80.748bn H1 net loss and its $72.388bn fair-value component in an explanatory disclosure, while explicitly stating in the visible introduction that net loss differs materially from operating loss and cash use. The implied 85.4% cost-of-revenue margin stays in supporting detail with its exclusions, not in a headline statistic.

### Drivers and risks

Use six paired rows rather than an investment score or a red/green verdict:

| Theme | Tailwind to explain | Headwind to explain |
| --- | --- | --- |
| Enterprise demand | More large customers and expansion in existing accounts. | Consumption variability, concentration, and the 5%–7% policy-violating revenue estimate. |
| Model quality | Frontier research, products, and workflow integration. | Rapid competitive changes, talent retention, and costly continued development. |
| Compute | Efficiency improvements and four hardware families. | Capacity constraints, expensive temporary supply, and unused commitments. |
| Distribution | AWS, Google Cloud, Azure, and direct relationships. | Partner costs and partners acting as suppliers, investors, and competitors. |
| Trust and access | Safety and reliability may aid enterprise adoption. | Release restrictions, copyright cases, government disputes, and export controls. |
| Capital and ownership | Capital access supports research and capacity. | Financing conditions, dilution, benefit initiatives, and limited public shareholder control. |

On desktop, opposing arguments align in columns. On mobile, each theme keeps its tailwind and headwind together before moving to the next theme. Each summary adds a concrete “Watch” sentence. Facts have citations; interpretive implications are written as conditional analysis. The 900% revenue-retention figure requires a nearby definition and its Pro/Max exclusion if shown.

### Commitments and ownership

Lead with the mechanism: **“Compute is committed ahead of the revenue it may support.”** Display a sequence—commit capacity, receive capacity, incur payments and costs, serve demand—rather than adding heterogeneous contracts into one total.

Use the SpaceXAI agreement as the visible worked example: up to $120.5bn over terms extending into 2029, approximately $3.1bn per month when fully delivered, with specific cancellation rights after initial periods. Place “up to,” timing, and cancellation terms beside the amount.

The full arrangements table is supporting detail. It must state that figures overlap and mix dates, minimums, estimates, and cancellation rights. Never add the rows or compare their headline sum with a cash balance as if they were immediately due. The visible SpaceXAI amount is labeled “contract ceiling,” not “backlog,” with its cancellation terms in the same panel.

A separate ownership explanation has three parts: **control**, **economic dilution**, and **resale supply**. Show that the LTBT's majority-board role and Founder LLC's 50.1% general voting power are different rights. Describe the benefit framework as discretionary, with sustained-price conditions; distinguish fund-held shares from external distributions. Source details explain notes, compensation, and donation matching. Avoid a pie chart when the final post-IPO capitalization is incomplete.

### SpaceX lessons and the commercial connection

Section title: **“What SpaceX's first months on the market can teach us.”**

Start with three lessons: an IPO price and an opening trade differ; strong revenue can coexist with concern about capital spending; an unlock can be anticipated and does not determine a day's direction.

Use a **selected-events timeline**, not a continuous price line. Entries carry the date, the observation type, the price, and a sourced account of what was happening. The primary short sequence uses:

- 11 June: $135 offer price; 12 June: $150 exchange opening.
- 16 June: $211.39 close; $225.64 intraday high identified separately in detail.
- 5 August: $108.27 close following Q2 results.
- 6 August: $114.92 close, up approximately 6.1%, on the first major unlock day.
- 21–22 October: $159.31 then $144.75 closes, with earnings, supply, and market context.
- 29 October: $143.89 close, explicitly the research endpoint.

Do not connect these observations with interpolated daily prices or attribute a move to a single event without evidence. Keep the $104.83 intraday low in the full event detail, not mixed into a closing-price return calculation. If the user expands a stage, its explanation and sources appear below the summary; opening adds information rather than repeating the summary.

Then show a compact two-way relationship diagram: **Anthropic pays for compute; SpaceX supplies capacity.** Add a separate sentence that Grok/Cursor and Claude can compete in models and applications. The 34.5% customer share is filing data; naming that customer as Anthropic is attributed to Bloomberg. Put that attribution beside the percentage: “SpaceX disclosed one customer at 34.5% of Q3 revenue. Bloomberg identifies it as Anthropic.” The diagram must not depict the $120.5bn ceiling as revenue already earned.

The comparison displays H1 2026 revenue and GAAP operating result by default. The expanded five-row table adds operating cash flow, cash equipment purchases, and cash plus securities. Its visible introduction explains that different cloud-service and leasing models make capex alone an inadequate comparison. Include qualitative rows on competitive advantages, governance, and dilution. Do not directly rank Anthropic H1 growth against SpaceX Q3 growth as if the periods and starting bases matched.

### Before pricing

Use a short watchlist: final offer price and economic shares; primary versus secondary proceeds; updated cash and obligations; capacity deliveries and utilization; complete recent financials; and the release schedule.

Offer three text scenarios—**Growth converts to cash**, **Growth needs continued funding**, **Demand or financing disappoints**—with conditions and evidence that would support them. Do not assign probabilities or share prices. A future numerical valuation tool would require an explicit model, reliable final capitalization, and additional work; it is outside this first version.

### Sources and definitions

Every displayed figure retains its period, units, source locator, and status in the editorial data. Use ordinary inline source links with descriptive accessible names. Source entries identify the publisher, title, filing/report date, relevant section, and original URL.

Differentiate four types where ambiguity matters: filing disclosure, calculated value, management outlook, and analysis. Use explicit attribution for reported third-party claims. These are meaningful distinctions, not decorative badges on every paragraph.

Definitions cover float, lock-up, dilution, operating profit, adjusted EBITDA, run-rate revenue, and revenue retention. Important caveats remain adjacent to claims; sources and definitions provide depth rather than hiding qualifications. Include a short footer statement describing independent research and the dated snapshot.

## Layout and responsive behavior

Desktop content alternates a broad figure or comparison with focused reading text. From about 1100px, use a narrow sticky contents rail beside the main sections and a static masthead with only the title, filing link, and sources link. The opening spans the page. At smaller widths, use a compact native Contents disclosure in a sticky header and a single reading column. Only one navigation mechanism sticks at a time; there is no second mobile tab strip.

```text
Desktop
+----------------------------------------------------------------+
| Anthropic IPO                        Read the filing   Sources  |
+----------------------------------------------------------------+
| Title and central argument        | Filing status and source     |
| Three concise takeaways           | Offer terms still incomplete |
+----------------------------------------------------------------+
| Contents     | Economics: period switch                          |
|              | Revenue  [==================]                     |
|              | Expenses [segments==============]                 |
|              | Operating result, qualification, exact figures    |
|              |                                                  |
|              | Drivers and risks, paired by theme                |
|              | Commitments and ownership                        |
|              | SpaceX events, relationship, comparison           |
|              | Before pricing; sources                           |
+----------------------------------------------------------------+

Mobile, 390px
+----------------------------------+
| Anthropic IPO         Contents    |
+----------------------------------+
| Title                            |
| Argument and three takeaways     |
| Filing status                    |
| Explore economics / Read filing  |
|                                  |
| Economics                        |
| [First half] [Second quarter]     |
| Revenue / expenses visualization |
| Operating result and caveat      |
| View the figures                 |
|                                  |
| Theme                            |
| Tailwind / Headwind / Watch       |
| ...                              |
| Commitments and ownership        |
| SpaceX event summaries           |
| Relationship; matched comparison |
| Before pricing; sources          |
+----------------------------------+
```

The chart reflows its labels below the bars on small screens. Key amounts remain readable at 390px. Wide financial detail uses a named, focusable table scroll region if needed; no horizontal page scrolling. Essential compact comparisons should fit without side-scrolling. The header respects anchor offsets and uses at most approximately 64px of mobile height.

## Interaction and accessibility contract

- Navigation uses real anchors. A JavaScript current-section indicator is optional enhancement, not required for navigation.
- Period switching updates only the operating-ledger panel, its table, title, and result announcement. It does not silently change other financial periods on the page.
- Details and sources use native `<details>` / `<summary>`. Links and summaries have at least 44px touch targets; no important information is hover-only.
- The chart has a concise accessible title/description and a full data table. Avoid duplicate reading of both every SVG label and the same hidden text.
- Use logical headings, a skip link, visible focus, native radio behavior, and clear link text. Maintain text selection and browser zoom.
- Reduced motion removes transitions; source content is available without fonts, JavaScript, third-party APIs, or storage.
- Printing expands supporting details, removes sticky navigation and interactive controls, and preserves periods, qualifications, and source URLs.
- No preference storage is necessary in version one. There is no price feed or automatic quote refresh to fail.

## Design acceptance criteria

The design passes when the opening explains the thesis and filing status; both positive and adverse evidence are easy to find; the operating ledger reconciles exactly; all displayed numbers have periods and sources; SpaceX is clearly a supporting historical case; and incomplete offering terms remain explicit.

The subsequent implementation must additionally demonstrate usable 390px and desktop rendering, keyboard operation, accurate state changes, source navigation, readable tables, print output, font/JavaScript failure behavior, and no console errors. These are later browser checks, not claims about this document.

See [design-review.md](design-review.md) for the second-pass findings and [build-plan.md](build-plan.md) for the implementation sequence derived from this design.

[skill]: https://github.com/nikolaspanayotov-jpg/VibeProjects/blob/87e1fd38fccc5bae14020d99a7676fe6d4e13f21/.agents/skills/frontend-design/SKILL.md
[guidance]: https://github.com/nikolaspanayotov-jpg/VibeProjects/blob/87e1fd38fccc5bae14020d99a7676fe6d4e13f21/.agents/skills/frontend-design/references/anthropic-design.md
[repo-rules]: https://github.com/nikolaspanayotov-jpg/VibeProjects/blob/87e1fd38fccc5bae14020d99a7676fe6d4e13f21/AGENTS.md
