# Anthropic IPO update and implementation plan — 14 November 2026

## Verified source changes

The SEC submissions register was reviewed on 14 November. It lists five additional FWPs with filingDate 12 November: website/factsheet/founders’ letter (`072949`), UK materials (`072952`), Australian/Canadian wrappers (`072953`), EEA/Swiss prospectus (`073040`) and Japanese amendment translation (`073045`). Accession prefix is `0001628280-26-`. Website/UK/Australian-Canadian communications are issuer-dated 10 November; EEA/Swiss and Japanese communications are issuer-dated 11 November. Some acceptance timestamps precede the SEC register’s filingDate; use labelled dates, without relabelling these as a new S-1 amendment. The 10 November S-1/A remains the latest registration amendment at review.

The official IPO website’s FAQ expects pricing on **18 November EST** and trading on **19 November EST**, subject to clearance/demand/market conditions. The Australian timetable expresses pricing/trading as **19/20 November AEDT**; do not frame the civil-date difference as a second listing date. The reviewed official legal notice still says the registration statement is not effective. No final price, completed IPO, allocation or first-day return is confirmed.

## Implementation plan

1. Update the review date, status card, returning-reader changes, filing history and roadmap. Show the expected company timetable separately from the final price and the dated preliminary terms. Preserve the original $70–$78 proposal and financial models.
2. Add a compact demand/evidence section. Attribute the approximately six-times order-book report to Reuters/Bloomberg on 12 November, with the later Reuters 13 November account and its competition/forecast uncertainty. Explain that reported orders do not determine final allocations, durable demand or aftermarket returns; make no probability or price target from the subscription ratio. Retain the older 5 November sentiment report as historical context.
3. Extend retail access with source-linked regional details: UK intermediary deadline on 18 November (each firm sets its cutoff); covered EEA/Swiss expected closing 18 November at 16:00 CET / 10:00 ET, subject to change; the $120 maximum is a regional legal ceiling, not a replacement U.S. range or fair-value target. Identify the nine covered EEA countries and Swiss status; Australian/Canadian/Japanese materials have their own eligibility and application terms. Country documents do not create universal eligibility or guarantee shares. Keep the six U.S.-named platform groups visible.
4. Contextualise issuer roadshow evidence: selected enterprise deployment examples, and the greater-than-four-times compute-efficiency ratio since Q1 2025. The latter is a revenue/compute-expense ratio, not a direct hardware-speed measure; it coexists with the existing Q2-to-Q3 cost-intensity deterioration. Company case studies do not establish incremental revenue or causal productivity gains. Treat the 10 November enterprise event as a past event page; no unreviewed outcomes are asserted.
5. Synchronise the two-page brief, source index/previews and maintenance notes; test calculations, date/status distinctions, regional scope, source dialogs, keyboard/no-JavaScript behavior, mobile/desktop reflow and both brief PDF paths. Inspect actual screenshots/PDFs. Commit only `Anthropic-ipo/` to main and verify deployment/served bytes.

## Evidence links and limits

- [SEC submissions register](https://data.sec.gov/submissions/CIK0002130357.json).
- [Official IPO website/FAQ](https://ipo.anthropic.com/us/), reviewed 14 November; FAQ timeline and legal notice.
- [Website FWP](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072949/anthropicpbc-fwpipowebsi.htm): issuer-dated 10 November, SEC register filing date 12 November. Exhibits include the timeline, company highlights and selected customer stories. The website and FWP are company offering materials, not independent evidence.
- [UK FWP](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072952/anthropicpbc-fwpukmaterials.htm): participation is through RetailBook’s participating intermediaries for UK-resident/physically present investors; deadline and firm cutoffs are qualified. Applications/currency and account eligibility require current intermediary confirmation.
- [EEA/Swiss FWP](https://www.sec.gov/Archives/edgar/data/2130357/000162828026073040/anthropicpbc-fwpxeeaprospea.htm): covered countries, offer maximum/indicative range, expected closing and order/eligibility conditions. Regional shares are a tranche of the global offer, not additional shares to add to it. Regulatory prospectus approval does not establish U.S. effectiveness.
- [Australian/Canadian FWP](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072953/anthropicpbc-fwpauswrapcap.htm): local wraps, Australian timetable in AEDT, indicative and subject to change.
- [Japan FWP](https://www.sec.gov/Archives/edgar/data/2130357/000162828026073045/anthropicpbc-fwpjapanamend.htm): 11 November local amended registration/prospectus and its preliminary status. No broad eligibility inference.
- [Reuters via Investing.com, 12 November](https://www.investing.com/news/stock-market-news/anthropics-ipo-is-about-six-times-oversubscribed-bloomberg-news-reports-5023345): attributes the six-times figure and allocation-priority claim to Bloomberg/people familiar. Details may change; company did not confirm the report.
- [Reuters via MarketScreener, 13 November](https://www.marketscreener.com/news/investors-flock-to-anthropic-ipo-but-question-durability-of-ai-lead-ce785eded889f123): attributed institutional interest and valuation/competition questions. Bank/buy-side forecasts are not company guidance; they are not adopted as model inputs. The article’s selected SpaceX subscription comparison is not a controlled predictor of returns. Historical SpaceX prices retain their existing 29 October cutoff.

Official newsroom/model pages and the old event page were also checked for relevant updates. No new GAAP quarter or revised U.S. indicative range was identified in the reviewed sources. This is a dated review of accessible official material and relevant reporting, not a claim to have read every paywalled article, watched the full roadshow video or verified every broker’s live availability.

## Status

The planned changes are implemented. Actual checks, visual review, publication and verification limits are recorded in `tests/VERIFICATION.md`.
