# BeeTrains verification

Originally checked 31 October 2026 using installed Chromium and Python Playwright. The browser acceptance checks were rerun for the audit fixes on 1 November 2026; the underlying research and station-access snapshot remain dated 31 October unless otherwise stated.

## Passed

- Static page serves successfully under `/BeeTrains/`; there are no page JavaScript errors.
- Screenshots captured at 320, 390, 768 and 1440px. No horizontal page overflow at those widths. Desktop and mobile screenshots, the mobile diagram and the selected-station layout were visually inspected.
- Embedded Barlow Condensed and Source Sans 3 load without an external font request. Fallback-font layouts were also checked for overflow.
- Glossop selects December 2026; Rose Hill Marple selects March 2027. The selected station, timeline, diagram and URL agree, and focus moves to the station result.
- Search handles punctuation-insensitive names, missing results, clearing, a maximum of six displayed matches, and markup entered as ordinary text.
- All five timeline states work. The December 2027 service state has no separate station group. The 2028 explanation distinguishes payments from integration.
- Complete station-list views contain the source's named entries for each group. IDs are unique; all internal fragment links resolve.
- Shared station URLs restore selection. Unknown station IDs show a useful message. Both successful copying and denied clipboard access were exercised.
- Keyboard checks cover the skip link, phase selection and expandable questions. Selecting a phase preserves focus on its button. Mobile Contents follows its anchors and closes.
- Reduced-motion settings disable smooth scrolling. Enlarged body text reflows at a narrow viewport.
- Print rendering exposes every milestone and station group; a PDF was generated for inspection.
- Without JavaScript, the narrative, all five milestones, all four station groups and source links remain readable.
- The same document's search and enhancements work in an offline browser-local document.
- Design-token contrast calculations: ink on paper 13.65:1, muted text on paper 5.82:1, ink on yellow 9.14:1, and muted text on white 6.41:1.

## Checks after the five design and content refinements

- Mobile milestone controls fit into two compact rows. The selected explanation precedes the diagram in both the visual and document reading order. The station search remains in the opening viewport.
- Station details use direct official facilities URLs for all 96 records: 95 National Rail pages fetched on 31 October, with Salford Central using its TfGM station page identified in indexed material. Glossop's category A access and Flowery Field's category C access were exercised in browser checks; the latter remains separate from its planned 2027–2028 work.
- A selected station shown on the diagram gets a visible halo. Stations omitted from the drawing show an explicit message and a working link to their selected full-list entry. Main Manchester hubs also support the halo. Following the audit, the December 2027 service milestone is text-only and activates no route paths.
- All three Glossop–Piccadilly–St Peter's Square payment explanations switch correctly, with prices and validity left unconfirmed. Without JavaScript, all three are readable; print exposes the panels as well.
- The local Piccadilly photograph loads at 1280px intrinsic width. Its visible caption includes archive status, author, source and CC BY-SA 3.0 licence. Mobile photography and station-result screenshots were captured for visual review.
- Shared station links bring the focused result heading into the viewport, accounting for the sticky header and the expanded station detail.

## Audit fixes checked 1 November 2026

- No shared `data-route` attribute includes `services`. The service milestone hides both the diagram and its view switch, displays a textual scope explanation, and has zero active route paths. Returning to a station milestone restores the previous diagram/list choice.
- The 2028 panel and ticket explanation explicitly attribute the all-Greater-Manchester rail-only contactless target to October reporting, distinguish it from integration through 2030, and retain unconfirmed journey and ticket conditions.
- The 43-versus-42 discrepancy is visible beside both the 2028 explanation and the generated station list, including without JavaScript. The list retains 42 named entries; no missing station was invented.
- Ticket summaries put rail contactless and the separate daily paper ticket in the shared planned December 2026 period. The first ticket-step date includes “Planned”.
- The public source context distinguishes indexed TfGM review from live verification. Accessibility dates remain explicitly planned work, with no implication of completion.
- Chromium checks passed at 320, 390, 768 and 1440px with no page JavaScript errors. The new service state and 2028 source note were captured and visually inspected.

The two requested live destinations were checked separately on 1 November:

| Destination | Retrieval result | Browser navigation result | Availability conclusion |
| --- | --- | --- | --- |
| [TfGM station directory](https://tfgm.com/ways-to-travel/train/stations) | HTTP 403 from direct retrieval and the web reader | Chromium could not complete certificate validation (`ERR_CERT_AUTHORITY_INVALID`) | Current availability unconfirmed |
| [TfGM journey planner](https://tfgm.com/plan-a-journey) | HTTP 403 from direct retrieval and the web reader | Chromium could not complete certificate validation (`ERR_CERT_AUTHORITY_INVALID`) | Current availability unconfirmed |

These checks do not establish that either link is broken or available to a normal visitor. The official URLs are retained, and the source context does not claim they were live-verified.

## Repeating the browser checks

From the repository root:

```sh
python3 BeeTrains/tests/browser_smoke.py
```

Requires Python Playwright and Chromium. `CHROMIUM_PATH` can select the browser executable. The script starts and stops a local HTTP server itself. Screenshots, print output and a JSON report are written to the ignored `tests/artifacts/` directory.

## Scope and limits

These checks cover Chromium and the interactions above, not a formal accessibility certification or a screen-reader compatibility audit. Other browser engines were not available. The environment's browser policy blocks direct `file://` navigation; local-file independence was instead checked by loading the complete HTML into an offline browser document. Serving the actual folder path passed.

The joining-date list was checked through TfGM's indexed source material. National Rail's station sitemap and 95 individual station pages were fetched successfully for the facilities enrichment on 31 October. Its Salford Central page returned 404, so the page uses the TfGM station URL identified in indexed material, with current access and live page availability unconfirmed. TfGM restricts automated fetching, so every TfGM destination's live HTTP response was not verified. The page provides source links and a research date; it does not offer live service, fare or accessibility guarantees.

TfGM's December 2028 heading says 43 stations, while the visible source list names 42. The implementation preserves the 42 named entries and avoids presenting that heading count or an overall programme total as a headline statistic. Changes remain labelled as planned until independently confirmed.
