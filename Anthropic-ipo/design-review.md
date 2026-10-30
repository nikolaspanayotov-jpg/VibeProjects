# Anthropic IPO page: second-pass design review

Reviewed on 30 October 2026 against [the design and content plan](design-and-content-plan.md), [the Anthropic research](key-points-summary.md), [the SpaceX research](../SpaceX-ipo/key-points-and-anthropic-comparison.md), and the repository's [Frontend Design skill][skill]. This is the assistant's second-pass specification review. There is no implemented page yet, so it does not establish browser behavior or visual quality in a rendered interface.

## Outcome

The revised design is ready to guide implementation. It provides a clear argument, real content, concrete visual tokens, mobile and desktop structures, and a bounded set of interactions. Anthropic remains the main subject; the SpaceX case supplies historical evidence and a commercial connection.

The content plan was written first, reviewed next, and revised before the [build plan](build-plan.md) was prepared. No additional design approval step is introduced.

## Findings and resolutions

| Review area | Finding | Resolution in the revised design |
| --- | --- | --- |
| Navigation | The initial desktop sketch included several header destinations alongside the contents rail, creating duplicate section navigation. | Desktop masthead now keeps only the title, filing link, and sources; the rail supplies section navigation. Smaller screens use one sticky header with native Contents. |
| Financial narrative | Growth alone would not express the research's central tension. A large loss headline alone would also misrepresent cash use. | Keep the operating ledger as the main visual. Show revenue, all four operating-cost categories, and the GAAP result. Explain net-loss fair-value adjustments separately and keep a visible qualification. |
| Period comparison | A shared scale is necessary to prevent a switch between a half-year and a quarter from visually overstating improvement. | Both ledger views use a fixed 0–18bn axis, with dates in the title and controls. Annual and half-year revenue remain separate groups. |
| Sparse SpaceX prices | The source contains selected observations, including offer, opening, closing, and intraday values. Connecting them would suggest a daily history the inputs do not contain. | Use dated event entries, explicitly label observation types, and keep intraday extrema separate from close-to-close calculations. No interpolated price series. |
| Contract amounts | A $120.5bn headline could be mistaken for earned revenue or a non-cancelable backlog. | Label it a contract ceiling and place delivery timing and cancellation rights in the same visible panel. The detailed commitments table has no summed total. |
| Customer attribution | A source link alone could obscure the distinction between a filed percentage and a reported customer identity. | Put the exact distinction beside the 34.5% figure: SpaceX disclosed the unnamed concentration; Bloomberg supplied the Anthropic identification. |
| Mobile comparison | A large two-company table would crowd a 390px screen and encourage readers to overlook period and capital-model caveats. | Default to two matched-period metrics, with the five-row table in supporting detail and the capex qualification in the visible introduction. Theme arguments stack in pairs. |
| Governance | Shareholder control, economic dilution, and available-for-sale shares are easily conflated. | Give them separate explanations. Distinguish LTBT and Founder LLC rights, fund-held shares and external distributions, and new issuance versus existing-share sales. |
| Long-form content | Both source documents together exceed what a first-time reader should encounter on one reading path. | Set a main-copy budget, compress the drivers into six themes, and use detail disclosures for additional evidence. Do not hide a critical caveat behind a disclosure. |
| Distinctiveness | The existing Budget page offers useful interaction conventions, but copying its layout would produce another policy-list page. | The new page uses Archivo/Source Sans 3, white/blue tokens, and the operating ledger as its defining feature. Open reading sections support the central argument. |
| Scope and repository fit | A planning task does not need a new app stack or hosting workflow. Renaming the existing folder would break shared paths. | Plan one standalone vanilla `index.html`, preserve `Anthropic-ipo`, and keep all future runtime data local to that file. The original research documents remain intact. |

## Checks actually performed

The proposed ledger values were checked with decimal arithmetic:

- H1 2026 expenses: 8.945 + 3.152 + 3.168 + 1.714 = **16.979bn**. Revenue 16.286 − expenses 16.979 = **−0.693bn**.
- Q2 2026 expenses: 5.558 + 1.857 + 2.135 + 1.031 = **10.581bn**. Revenue 11.555 − expenses 10.581 = **+0.974bn**.

Both source documents were located and their relevant sections were used to check the planned claims and dates. The key distinctions—preliminary offer terms, period labels, up-to versus guaranteed payments, named versus unnamed customer evidence, and unlock eligibility versus actual selling—were reviewed against those documents. This was not a new comprehensive verification of every underlying external source.

Calculated WCAG contrast ratios for proposed text on white:

| Foreground | Ratio |
| --- | ---: |
| Ink `#17324D` | 13.13:1 |
| Muted `#51657B` | 6.00:1 |
| Accent `#2348A5` | 8.26:1 |
| Tailwind `#14675C` | 6.72:1 |
| Headwind `#A53240` | 6.71:1 |

These pairs exceed 4.5:1 for ordinary text. They do not establish contrast for every future tinted surface, chart element, component state, or disabled control. Decorative dividers are not suitable input boundaries without stronger treatment.

## Implementation verification completed — 30 October 2026

The reviewed design has been implemented in [index.html](index.html) and published privately. Actual browser checks, inspected screenshots, corrections, print output, and remaining limitations are recorded in [tests/VERIFICATION.md](tests/VERIFICATION.md). The checks specified below are retained as the review requirements; they are not a claim that unavailable checks passed.

## Original implementation check requirements

The browser review must test 390px and desktop layouts, 320px fallback, zoom, long URLs, sticky offsets, radio-group operation, source disclosures, tables, reduced motion, missing fonts, JavaScript disabled, print, and console output. Screenshots must be inspected, not merely generated. Correct anything observed and record evidence in a later `tests/VERIFICATION.md`.

Before publication, refresh the filing status, unresolved offering terms, source links, and market-data endpoint. Do not quietly present this October research snapshot as current. These checks are implementation and publication work, rather than blockers to completing the design documents now.

[skill]: https://github.com/nikolaspanayotov-jpg/VibeProjects/blob/87e1fd38fccc5bae14020d99a7676fe6d4e13f21/.agents/skills/frontend-design/SKILL.md
