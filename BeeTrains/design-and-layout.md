# BeeTrains: page design and layout

Design brief for the future BeeTrains web page. Prepared 31 October 2026.

Content foundation: [Bee Network plans](bee-network-plans.md). Design guidance: the repository's [Frontend Design skill](../.agents/skills/frontend-design/SKILL.md) and its [original reference](../.agents/skills/frontend-design/references/anthropic-design.md).

## The direction

**A contemporary rail atlas: precise, welcoming and quietly distinctive.** Draw on station signs, route diagrams and the pleasure of understanding a connected network. A fine yellow railway line connects the page's main ideas. Typography, space and useful interaction give the page its character.

The audience is Greater Manchester residents, commuters and occasional travellers. Their first questions are: “When does my station join?” and “What will change for me?” Answer those before explaining the wider programme.

The memorable element is a route diagram connected to a selectable rollout timeline. Everything around it is calm: generous space, readable prose, clear sources and a small number of deliberate controls. Keep the existing `BeeTrains` folder name and page identity.

## Visual system

### Palette

Use these six base colours as CSS custom properties. Additional treatments should use opacity or these existing values rather than introduce competing accents.

| Token | Value | Purpose |
| --- | --- | --- |
| `--paper` | `#F5F4EE` | Main background, like a clean printed network guide |
| `--surface` | `#FFFFFF` | Station search, selected detail and occasional inset panels |
| `--ink` | `#222823` | Text, buttons and the main diagram structure |
| `--muted` | `#58615B` | Supporting text and secondary route lines |
| `--bee` | `#F2C500` | Selected phase, route emphasis and focus highlight |
| `--rule` | `#D5D9CF` | Quiet separators and nonessential diagram structure |

Use charcoal text on yellow. Yellow can fill a selected control or run inside a dark route outline; it should not carry small text or essential boundaries against white. Status always has a written label and, where useful, a distinct symbol. Check the final foreground/background combinations for contrast.

### Typography

- **Barlow Condensed, weight 600:** headlines and milestone dates. Its narrow proportions recall rail signage without copying official branding.
- **Source Sans 3, weights 400 and 600:** prose, navigation, controls and station names. Its open shapes support sustained reading.
- Use sensible fallbacks: `"Arial Narrow", sans-serif` for display; `"Segoe UI", Arial, sans-serif` for body. The layout must survive a failed font request.
- Body: 18px, line height 1.6, maximum reading width 65ch. Small source notes stay at least 14px. Inputs use at least 16px.
- Headline: about 52px on mobile, growing to 88px on desktop; line height 1.02. Section headings: 32–44px. Use sentence case and left alignment throughout.
- Keep the whole headline in one treatment. Give emphasis through size, wording and placement.

### Space and detail

Use a spacing scale of 4, 8, 12, 16, 24, 32, 48, 64 and 96px. Desktop sections have 80–96px of vertical separation; mobile sections use 48–64px.

Keep most content on the page background. Give the station result one distinct white surface with an 8px radius. Inputs and buttons use a 6px radius. Milestone markers are circles because they represent stops. Borders communicate grouping or selection; avoid decorative frames around every paragraph.

Use small, consistent outline icons for rail, bus, tram, accessibility and external links. Pair meaningful icons with text. The wordmark is simply **BeeTrains**, with a small station-ring symbol. The site is described as an independent guide near the introduction; the design should have its own identity.

## Page structure

### Desktop wireframe

Maximum page width: 1152px. Use a 12-column grid with 24px gaps and at least 32px outer gutters. Reading passages occupy around seven columns; navigation and supporting notes use the rest.

```text
BeeTrains                     Explore stations   What changes   Sources
─────────────────────────────────────────────────────────────────────
Trains,                         Original route diagram
joining the                     with selected rollout group
Bee Network.                    and readable station labels

Short explanation               Selected milestone and its meaning
Find your station [          ]
Independent guide · research date shown as ordinary text
─────────────────────────────────────────────────────────────────────
Explore the rollout
[Dec 2026] [Mar 2027] [Dec 2027] [By Dec 2028] [By 2030]
 Selected milestone explanation       Station list / station detail
 Supporting source                     and link to its official page
─────────────────────────────────────────────────────────────────────
What changes for your journey?
Tickets and payments     At the station     Services and connections
─────────────────────────────────────────────────────────────────────
Tickets, explained             Step-by-step ticketing illustration
─────────────────────────────────────────────────────────────────────
Stations and accessibility     Specific schemes, status and sources
─────────────────────────────────────────────────────────────────────
Services and responsibility    Clear explanation of who does what
─────────────────────────────────────────────────────────────────────
Common questions              Expandable answers
Sources and latest review     Source list and update note
```

This is one scrolling page with stable section anchors. The hero diagram and rollout controls form one explorer: the diagram may sit beside the introduction on desktop, while its selected detail sits directly below. Do not create a second, independently controlled map further down the page.

### Mobile wireframe

Design at 390px first, with 20px gutters; also support 320px without horizontal page scroll.

```text
BeeTrains              Contents

Trains, joining
the Bee Network.
Short introduction and review date

Find your station
[Station name                 ]
[Matching station buttons     ]

Explore the rollout
[Dec 2026] [Mar 2027]
[Dec 2027] [By Dec 2028] [By 2030]
Selected phase explanation
[Diagram] [Station list]
Readable diagram or full list
Selected station detail

What changes for your journey?
Three short, stacked summaries

Tickets, explained
Vertical ticketing steps

Stations and accessibility
Services and responsibility
Common questions
Sources
```

Below 760px, stack the hero and explorer. At 760–1023px, allow a wider diagram with stacked text. From 1024px, use the desktop composition. Date controls wrap onto rows; they never require dragging. Keep station labels at least 14px and recompose the diagram for a narrow screen instead of shrinking a desktop SVG to fit.

## The opening

Use this initial copy, subject to the content review:

> **Trains, joining the Bee Network.**
>
> Explore when your station is planned to join, and what it could mean for tickets, stations and connections.

Place the labelled **Find your station** input immediately below this introduction. Under it, show “Independent guide. Plans checked 31 October 2026.” as readable supporting text, with the date linked to Sources.

The first viewport should show the subject and station search at 390px. The explorer follows in normal document flow. Avoid a fixed-height or full-screen hero that pushes the useful controls out of reach.

Desktop navigation contains three anchors: **Explore stations**, **What changes**, **Sources**. Mobile uses a native **Contents** disclosure containing those links. A slim header may stick after scrolling, provided it never obscures focus or anchor targets.

## Interaction 1: station finder

Search is global across the verified station dataset; changing the timeline does not narrow the search results.

| Reader action or state | Behaviour and visible response |
| --- | --- |
| Start typing | Match station names without case or punctuation sensitivity. Show up to six matches as ordinary, labelled buttons beneath the input, plus a match count. |
| Select a station | Select its integration milestone, highlight it in the diagram and reveal its detail beneath the controls. Move focus to the result heading after this explicit selection. |
| View station detail | Show station name, “Planned to join: …”, the scope of that milestone, source, review date and an official station-information link. Show accessibility information only where separately verified. |
| No matches | “No stations match ‘…’. Try another spelling, or browse the station list.” Provide the list link beside the message. |
| Station found, date unresolved | “Joining date not yet confirmed in this guide.” Keep the official source link available. Never infer a phase from proximity to another station. |
| Clear search | Restore the unfiltered search state. Keep the selected milestone until the reader chooses another. |

Use a labelled search input and a normal list of result buttons, avoiding the keyboard complexity of a custom autocomplete widget. Results stay in normal document flow. A short polite announcement reports the number of matches; do not announce the entire result panel on every keystroke.

Include **Copy station link** in the selected detail. A shared URL stores a stable station ID and scrolls to its result. Show “Link copied” after success; if clipboard access fails, reveal a selectable URL. Unknown IDs return to the explorer with a useful message.

## Interaction 2: connected timeline and route diagram

Five date controls organise the milestones already described in the content brief:

| Control | Content revealed |
| --- | --- |
| December 2026 | First 14 stations on the Piccadilly–Glossop/Hadfield corridor; explain the separate daily paper ticket proposal. |
| March 2027 | Next 15 stations, including Victoria, Stalybridge, Marple and Rose Hill Marple. |
| December 2027 | Proposed service enhancements. State that this stop concerns services; do not imply that it adds another station group. |
| By December 2028 | Further station integration and planned payment milestones. Distinguish rail contactless coverage from full integration. |
| By 2030 | Remaining local integration, with a link to the relevant official station group. |

Default to December 2026 with the label **Planned milestone**. Selecting a date changes the explanatory passage, diagram emphasis and relevant station list without scrolling the page or moving keyboard focus. Use buttons with `aria-pressed` inside a labelled group; the selected state has a dark outline, yellow fill and a written indication.

A station selection can set its matching phase. If a later manual phase change excludes that station, clear its highlight and detail, and announce the new phase. Search text may remain so the reader can return to the result.

Draw an original SVG schematic from verified route relationships. Use generous station spacing, visible branch points and consistently placed names. Label it **Rollout diagram** with “Simplified; use official journey planning for travel.” It illustrates planned groups, with no claim of showing live services or travel times.

Emphasise the chosen group in yellow within a dark outline. Other routes use muted lines. Station markers and text distinguish the selected group even in greyscale. Date selection shows the scope of that milestone, not a simulated future network assumed to be in operation.

**Diagram / Station list** is an explicit view switch. The list provides every participating station for the chosen group, including stations omitted from the compact diagram. Search is the primary way to select any station; labelled diagram buttons may offer the same action for featured stops. Never make a tiny marker the only route to information. All diagram interaction works by tap, click and keyboard; hover can add emphasis but carries no unique content.

## The reading sections

### What changes for your journey?

Use three concise summaries in one shared band, separated by space or rules rather than three floating cards:

- **Tickets and payments:** contactless rail payments first, followed by broader integration.
- **At the station:** information, wayfinding and accessibility work with individual delivery dates.
- **Services and connections:** planned timetable improvements and onward travel.

Each summary links to its full section. On mobile they stack in that order.

### Tickets, explained

Show three static stages with small rail, bus and tram diagrams: **Rail contactless**, **A daily ticket across modes**, **Integrated daily and weekly caps**. Place the relevant planned date and a source beside each. This is a conceptual explanation, so readers can understand the difference without opening a control.

An optional **Show an example** disclosure can illustrate a transfer between train and tram. Label it “Illustrative journey”; include no prices, claimed savings or ticket-validity promises until those details are verified. Keep the paper ticket distinct from contactless capping.

### Stations and accessibility

Use a generous text section with a compact table of verified schemes and planned dates. On mobile, render each table row as a labelled block while preserving the relationships. Keep “Planned work” and “Current facilities” separate. Link current access information to the official station page.

### Services and responsibility

Give the service changes a short dated explanation. Follow with a simple role list for TfGM, train operators, Network Rail and government. Use plain sentences about responsibilities. Readers should understand who runs trains and why joining the network does not itself guarantee a new timetable or step-free access.

### Common questions and sources

Use native `details` / `summary` for questions such as “Will my train operator change?” and “Does joining mean my station will be step-free?” Allow multiple answers to remain open. Essential dates and fare distinctions stay visible in the main narrative.

Keep Sources visible as a normal section, with publisher, document title, publication date where known and review date. Place a nearby source link on each factual panel; distinguish primary material from secondary reporting. Include the revised 14/15-station launch grouping and explain the older 17-station announcement only where it helps resolve a discrepancy.

## Motion and accessibility

- Use motion only to explain a reader's action: a 160–220ms route-emphasis change or a short detail-panel crossfade. Keep container changes stable so the page does not jump. No looping train, moving background, automatic phase playback or scroll-controlled narrative.
- Under `prefers-reduced-motion`, remove transitions and smooth scrolling. Every state remains immediately understandable.
- Provide a skip link, semantic landmarks, one `h1`, ordered section headings, visible focus and native keyboard behaviour. Keep meaningful text selectable.
- Aim for WCAG 2.2 AA: 4.5:1 for normal text, 3:1 for large text and essential interface graphics. Give controls at least 44×44px touch areas. Use a dark outer focus ring with a yellow inner ring so focus survives both light and dark surfaces.
- The SVG has a short accessible description; the adjacent HTML list supplies full station information. Avoid hundreds of duplicate screen-reader stops.
- Support 200% text zoom and reflow at a 320px viewport. Sticky navigation must not cover focused content; use suitable anchor offsets.
- With JavaScript unavailable, show the complete narrative, chronological milestones, verified station groups and sources. Enhanced controls appear only after they are ready.
- Printing expands answers and shows all milestone content and sources, with controls removed.

## Implementation boundaries for the later build

Follow the repository's default: one self-contained `index.html` with inline CSS and JavaScript, no framework, backend or build requirement. It must work when opened locally and when hosted under `/BeeTrains/`. The current deliverable is this design document; the web page is the next implementation step.

Use one verified set of station records to drive searching, phase membership, details and share URLs. Store stable IDs, display names, planned integration group, source URL and review date. Model payment and service events separately from station integration, so the interface cannot accidentally turn one into the other. Keep official links in the records; do not construct them from guessed station names.

Render useful content in the base HTML and enhance it. Validate IDs, phase references and links before release. No account, location permission or live-data connection is needed for these interactions. No persistent browser state is necessary for the first version; shared station links provide continuity.

## Design review and acceptance

The initial atlas idea could easily become a decorative network map. The final direction makes the diagram respond to real station and milestone questions, gives it an equally capable list view, and keeps the narrative prominent. Condensed transport typography, useful route geometry and restrained yellow distinguish the page without adding a dashboard of repeated cards.

Before calling the eventual implementation finished:

- Inspect screenshots at 390px and 1440px; also check 320px and 768px for wrapping and overflow.
- Find Glossop and Rose Hill Marple, switch between their milestones, clear the search and test a missing station. Confirm details against the content sources.
- Check the service-only December 2027 state and the distinction between payment coverage and integration in 2028.
- Navigate the full page by keyboard, including contents, phase selection, station results, disclosures and shared links.
- Check reduced motion, text zoom, contrast, failed font loading, JavaScript disabled and print output.
- Test source links and direct station URLs. Refresh evidence and review dates before displaying a milestone as available.
- Inspect console errors and verify the page works both from a local file and under its folder URL.

These are acceptance criteria for the later page build. This document does not imply that browser or accessibility testing has already been performed.
