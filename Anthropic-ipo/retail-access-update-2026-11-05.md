# Retail IPO access — 5 November 2026

The user approved all five integration proposals: add a compact access section under Before pricing, show unresolved terms, connect to the SpaceX entry-price example, explain possible market effects as analysis, and refresh the change summary and dated source previews.

## Source evidence and boundaries

- [SEC submissions register](https://data.sec.gov/submissions/CIK0002130357.json), checked 5 November: latest public IPO filing remains the 2 November S-1/A, accession 0001628280-26-068676. The check is not a new filing event.
- [Amended prospectus](https://www.sec.gov/Archives/edgar/data/2130357/000162828026068676/anthropicpbc-sx1ax1.htm), Underwriting, Sales to Retail Investors, printed page 331: Anthropic anticipates retail distribution through named platforms. Offering purchases through them use the IPO price and remain subject to platform terms and requirements. Final pricing and retail allocation size are not supplied here.
- [Barron's coverage](https://www.barrons.com/advisor/articles/anthropic-ant-ipo-brokerage-firms-afe39034), dated 4 November: reports the retail distribution plans disclosed in that 2 November filing. Attribute the report separately from the primary disclosure; it is not a new prospectus amendment or price announcement.

The official register, primary passage and report were read through the web connector. A direct executor download of the SEC document returned a proxy 403; it was not retried through a substitute proxy or host. No raw filing archive was obtained through that failed request. The accessible primary passage establishes the facts used here.

## Platform names

| Platform group | Name used in the retail-distribution passage |
| --- | --- |
| Schwab | Charles Schwab & Co., Inc. |
| Fidelity | Fidelity Brokerage Services LLC; Fidelity Capital Markets, a division of National Financial Services LLC |
| Robinhood | Robinhood Financial, LLC |
| Trade-PMR | Trade-PMR, Inc. |
| SoFi | SoFi Securities LLC |
| E*TRADE | E*TRADE from Morgan Stanley |

These are six platform groups; the Fidelity row retains both names. Being listed does not establish individual eligibility, currently open applications or a guaranteed allocation. Current broker requirements, location restrictions and request deadlines must be confirmed separately. Do not introduce unverified account minimums, an allocation percentage or a pricing date.

## Implementation

`retail-access` sits below the Before pricing introduction. It groups the filed plan, unresolved terms, the visible six-platform list, an expandable table of names from the filing, two entry routes and conditional market implications. Ordinary links connect it to `entry-comparison` in both directions. The existing dated SpaceX arithmetic is unchanged.

The change summary now highlights 4 November coverage of the 2 November disclosure, checked 5 November. The register/status date advances to 5 November. Existing company research and the product-event schedule retain their separate review dates. `source-a-retail` is a Filing dated 2 November; `source-retail-barrons` is a Third-party report dated 4 November. All 28 sources use the existing local preview behavior. No new original quotation is introduced.

The market-effect text is analysis: wider access could broaden initial demand, while sentiment and subsequent selling could increase volatility. Neither statement predicts a price direction. Monitor allocations, valuation, tradable supply and actual selling together.

## Acceptance

Verify the six rows and exact filed names, prospective participation, broker-dependent requirements, unresolved allocation/price/deadline fields, distinct filing/report/check dates, both ordinary anchor links, mobile header clearance, source previews, responsive expanded-table reflow and complete no-JavaScript content. Inspect phone, desktop and printed output. Reuse the existing financial/reading checks; introduce no runtime fetch, package, account connection, trading link or backend. Preserve original research, all existing financial data and historical SpaceX dates. Record actual checks and publication in `tests/VERIFICATION.md`.
