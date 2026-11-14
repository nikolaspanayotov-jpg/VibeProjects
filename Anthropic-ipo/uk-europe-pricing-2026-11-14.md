# UK and European IPO pricing: source review and implementation plan

Reviewed 14 November 2026. This is an independent explanation of the published offer terms, not an application or broker quote. The worked example uses a maximum of 20 shares through Interactive Brokers (IBKR).

## Finding

There is no disclosed UK-residency premium in the issuer's IPO price. UK terms use the global Offer Price. EEA/Swiss terms expressly make their final price equal to the final U.S. IPO price. Currency conversion, intermediary charges and different execution times can change the amount a buyer actually pays.

The $120 maximum belongs to the current EEA/Swiss prospectus. It is neither a separate European purchase price nor an immutable worldwide cap. Section 8.1.7 allows amendments to that maximum. The UK terms permit the global price to move outside the indicative $70–$78 range; this review did not establish a separate $120 UK ceiling. Do not subtract $78 from $120 and describe the result as a UK/European surcharge.

## Primary evidence and precise locations

- [UK offer materials, issuer-dated 10 November, filed 12 November](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072952/anthropicpbc-fwpukmaterials.htm): Disclosure Summary, Part E §3, printed pp. 45–46, uses the global Offer Price for the UK buyer. Part E §5, pp. 46–48, describes the GBP conversion, benchmark-based rate to be announced by RetailBook, possible intermediary-specific conversion and CDIs issued one for one against underlying shares. Part C, pp. 26–27, warns about conversion timing and CDI liquidity; Part E §5 includes possible CREST charges and indirect rights. These are not a UK exchange listing.
- [EEA/Swiss prospectus, issuer-dated 11 November, filed 12 November](https://www.sec.gov/Archives/edgar/data/2130357/000162828026073040/anthropicpbc-fwpxeeaprospea.htm): cover and §8.1.3, printed pp. 203–204, distinguish $120 maximum from the $70–$78 indicative U.S. range and explicitly equate final European/Swiss and U.S. prices, before intermediary costs/taxes. Orders without a limit can be valid up to the maximum. §8.1.7 permits changes to the maximum; a limit below the final price may get no allocation.
- [Anthropic's international broker list](https://support.claude.com/en/articles/17889756-anthropic-ipo-international-retail-brokers-and-selling-agents): official company page, checked 14 November, names Interactive Brokers among UK participants, coordinated by RetailBook. Account eligibility and allocation still require confirmation.
- [IBUK's 12 November announcement, distributed by Business Wire and reproduced by StreetInsider](https://www.streetinsider.com/Business%2BWire/Interactive%2BBrokers%2B%28U.K.%29%2BLimited%2BParticipating%2Bin%2Bthe%2BUK%2BRetail%2BOffer%2Bfor%2BAnthropic%2C%2BPBC/27328732.html): eligible clients resident and physically located in the UK can apply, with sufficient U.S.-dollar-equivalent funds. No guaranteed allocation. This announcement did not establish the account's IPO application commission or FX route.
- [IBUK spot-currency tariff](https://www.interactivebrokers.co.uk/en/pricing/commissions-spot-currencies.php): checked 14 November. First manual-conversion tier is 0.20 basis point = 0.002%, minimum $2 per order. Auto conversion typically adjusts the rate by 0.03%, without a separate conversion commission. Account/program restrictions and rate changes apply. These general rates do not prove automatic conversion is available for this IPO application.
- [IBUK ordinary U.S. stock tariff](https://www.interactivebrokers.co.uk/en/pricing/commissions-stocks.php?re=amer): checked 14 November. At 20 shares, general base minimums are $0.35 tiered, plus applicable external costs, or $1 fixed. These are ordinary secondary-market tariffs, not verified IPO subscription fees.

The broker's advertised UK IPO URL redirected to its homepage during this review. No authenticated Client Portal or account-specific order preview was accessed. Do not claim its exact subscription fee, accepted instrument, funding workflow, cutoff or allocation rules were verified. The Irish/EEA IBKR application deadline is not evidence of the UK account's cutoff.

## Twenty-share comparison

Assume an IPO allocation of all 20 shares at the $74 indicative-range midpoint and an invented exchange rate of $1.25 per £1. Final price, actual rate and allocation remain unknown. Share consideration is $1,480, equivalent to £1,184 before costs. The matched U.S. comparator already holds USD; neither side's unverified IPO application commission is included.

| Funding route, if available | Additional FX cost | Additional GBP per share | Currency-cost uplift |
| --- | ---: | ---: | ---: |
| Already held USD, no new conversion | $0 / £0 | £0 | 0% |
| Automatic conversion, approximate 0.03% | $0.444 / about £0.36 | about £0.018 | about 0.03% |
| One manual conversion, $2 minimum | $2 / £1.60 | £0.08 | about 0.135% |

Manual formula: max($2, share consideration × 0.00002). Auto formula is an approximation to a rate adjustment, share consideration × 0.0003. Market bid/ask spread, rate timing, extra conversion orders, different account tariffs and IPO-specific charges can change actual totals. The $2 minimum dominates throughout a 20-share order at the current indicative range. At $70–$78, share consideration is $1,400–$1,560; auto FX is approximately $0.42–$0.468, whereas one manual conversion still costs $2. These figures are not a total-cost upper bound.

Existing USD may have incurred earlier acquisition costs. A zero new FX fee does not mean no currency exposure. GBP value can fall if USD weakens even at an unchanged USD stock price. Future sale/withdrawal fees, holding costs and personal taxes are outside this entry-only comparison; no blanket stamp-duty charge has been invented.

## Design and implementation plan

1. Add a visible `uk-ipo-costs` section beside the existing regional-access material. Lead with equal issuer pricing; distinguish the amendable EEA/Swiss maximum from the UK/global terms. Link directly from the update summary and regional note.
2. Use three concise funding comparisons and an editable calculator for assumed USD price, 1–20 allocated whole shares and USD per £1. Default to 20 × $74 at 1.25. Show currency-only additions, subtotals and per-share differences; keep IPO fees explicitly unresolved. Retain a complete static/no-JavaScript illustration, native disclosures and print output.
3. Explain the UK GBP/CDI versus USD/share routes, intermediary-specific exceptions, allocation and the distinction between IPO price and subsequent market price. Add an IBKR account-preview checklist, including a hard 20-share limit where the order form permits one. A cash subscription alone cannot guarantee precisely 20 shares before pricing/FX are known.
4. Add four dated source previews, update the concise brief and project instructions. Preserve financial, commitment and historical SpaceX datasets.
5. Test calculation/rounding, alternative price and allocation, invalid/empty inputs, reset, keyboard/source focus, search/deep links, mobile reflow, no-JavaScript and print. Inspect actual screenshots and two-page brief PDFs, then commit project-only changes to main and verify the public deployment.

## Review before publication

Do not describe conditional auto FX as confirmed IPO eligibility, ordinary stock commissions as subscription fees, the $120 maximum as a universal cap, or estimated currency-only totals as all-in prices. Do not promise a 20-share allocation or use an order-book multiple as an allocation probability. The final account preview and final issuer pricing remain necessary to establish an exact personal cost.
