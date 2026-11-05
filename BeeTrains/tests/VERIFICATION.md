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

## Reader-tool additions checked 1 November 2026

- The roadmap compares all five planned milestones, retains the 43-versus-42 note and unknown eligibility, reflows without horizontal overflow at 320, 390, 768 and 1440px, and opens the corresponding explorer panel from each date link. Its native disclosure is initially collapsed on a mobile visit and remains accessible without JavaScript.
- The selected-station bar appears after the whole result passes above the header. Keyboard expansion, returning focus to the result, changing stations, clearing an incompatible selection and measured header offsets passed browser checks.
- The Piccadilly transfer section links the official map, accessible station guide, Passenger Assist and TfGM advice/alerts. Its qualifications distinguish nominal facilities from live lift status. Recent updates are dated and explicitly separate guide clarifications from operational launches.
- Station-only print rendering hides the full guide, keeps the research date, planned status, official URLs and unresolved details, and restores the full page after printing. PDFs for Glossop, Flowery Field, Stockport and Salford Central were each confirmed as one A4 page using `pdfinfo`. The Stockport output was rendered and visually inspected.
- The downloaded Glossop brief was opened as a standalone document with JavaScript disabled and networking offline. Its dated facts, sources and uncertainty remain present, with no script or server dependency.
- Full-guide printing temporarily expands closed disclosures so the mobile roadmap and question answers are included, then restores their prior state.
- New roadmap, transfer and selected-station screenshots were inspected. The full browser suite passed without page JavaScript errors.

### Additional source retrieval checks

On 1 November 2026, direct retrieval returned HTTP 200 for the current Network Rail accessible guide (`/2022/08/Manchester-Piccadilly-Station-Guide-Accessible.pdf`), the official September 2025 station map and National Rail's Passenger Assist page. The PDF text was inspected for the stated lift connections and platform references. The older indexed guide URL under `/2022/11/` returned 404 and is not used in the page.

These retrievals verify the cited documents' availability at that check, not live equipment operation. TfGM advice and alert links retain the indexed-source and live-verification limitations recorded above. The general station-access data remains the 31 October research snapshot.

## Reading-clarity additions checked 2 November 2026

- The three “Start here” links reach station dates, payment plans and Piccadilly transfer planning. Station search remains above 700px on the 390px opening viewport. Four contextual definitions and the organisation-role disclosure open and close with the keyboard, retain focus and use controls at least 44px high.
- Milestone evidence expands in place without changing the page URL. Panels retain the publisher, primary/secondary attribution, publication versus review dates, supported claims, unresolved details and original external URLs. Ticket and source qualifications remain visible outside closed evidence panels.
- The Glossop example distinguishes Derbyshire geography, planned December 2026 station inclusion and unresolved ticket validity. Its three-column explanation reflows to one column on mobile. Expanded source explanations were checked for overflow at 320, 390, 768 and 1440px.
- Correction URLs were parsed without opening GitHub or submitting issues. Section drafts include the section and source prompts; station drafts update between Glossop and Rose Hill Marple and include the station ID, code, planned date and research date. They do not include the visitor's current URL. Repository metadata confirms that Issues are enabled.
- Definitions, local evidence and section correction drafts remain available with JavaScript disabled. Full-guide print expands the new disclosures. Existing offline search, the text-only December 2027 milestone, the visible 43-versus-42 discrepancy and the qualified payment targets continue to pass.
- The full Chromium suite passed with no page JavaScript errors, including four one-page station PDFs and a standalone offline station brief. Opening, boundary and payment-evidence screenshots were inspected at mobile and desktop widths. A missing arrow glyph found during visual inspection was removed; quick-start chevrons are drawn with CSS.

National Rail's saved 31 October Glossop page confirms the Derbyshire address used in the example. A fresh direct retrieval on 2 November returned HTTP 403, so this addition does not claim a newly verified live destination or change the original research date. No new rollout, fare or completion announcement is inferred from these reading tools.

## Personal reader tools checked 5 November 2026

- Comparison selectors contain all 96 station records plus an empty choice. Glossop/Stockport, Flowery Field/Salford Central, duplicate choices, clearing and opening a compared station passed. Dates, payment scope, service proposals and access use the explorer's shared fact functions. The 2028 count discrepancy and unresolved through-ticket/direct-service qualifications remain visible.
- My stations restores a saved shortlist after reload, opens the correct explorer record, removes individual/all entries and limits the list to six. Only a version and station IDs are persisted. Blocked storage reads/writes, malformed JSON and unsupported schema versions show a visit-only fallback. Invalid, duplicate and obsolete IDs are filtered. Removal retains useful keyboard focus.
- Three native journey-story disclosures work with the keyboard and their actions populate the matching station comparison. The commuting, evening and access examples retain source context, unknown ticket validity, unconfirmed last trains and the distinction between category C access and planned works.
- Four checklist topic controls filter ten source-linked checks. Two general checks remain visible; counts include only visible items. Keyboard ticks and reset work, including preserving topic choices. The checklist does not persist or describe a journey as confirmed.
- Desktop and mobile navigation each expose one current section through `aria-current="location"`. The decorative reading line reaches zero at the top and one at the bottom. Scroll updates preserve focus. Mobile Contents remains within the viewport, closes after navigation and retains the current section label.
- Four-width checks cover 320, 390, 768 and 1440px. Comparison, stories, checklist and navigation screenshots were reviewed. Component captures hide fixed navigation chrome only during capture to avoid overlapping tall-element screenshots; separate viewport captures verify the real header and current-section label.
- Existing station selection, source panels, text-only December 2027 scope, payment qualifications, reduced motion and full-guide printing remain covered. Four representative station briefs remain single-page A4 PDFs. Offline comparison and station search work; without JavaScript all three stories, ten native checklist items, source links and original station groups remain readable.
- Shared station links now restore after initial page/font loading, so the browser's initial fragment jump cannot override result focus and scrolling. The full Chromium suite passes without page JavaScript errors.

The five additions reuse the existing research snapshot. No new live source retrieval or operational confirmation is claimed: station and rollout facts remain dated 31 October 2026, and Piccadilly guidance remains dated 1 November. The 5 November update records changes to this guide.

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
