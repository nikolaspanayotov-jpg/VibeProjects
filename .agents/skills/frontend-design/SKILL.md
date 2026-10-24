---
name: frontend-design
description: Design and implement distinctive, accessible frontend interfaces. Use when building or redesigning websites, pages, dashboards, UI components, or visual styles, including typography, color, layout, and interaction. Preserve an existing product's design system unless a redesign is requested.
---

# Frontend Design

Use Anthropic's design guidance with the Codex workflow below. For a new visual
direction or substantial redesign, read the preserved
[original skill](references/anthropic-design.md). For a focused UI change, use
the workflow here and consult the original's relevant sections as needed.

## Apply the brief and repository context

- Follow the user's requested scope, applicable repository instructions, and the
  existing stack, components, design tokens, and conventions.
- Treat the original's design-studio persona and rejected proposals as creative
  framing, not facts about the user. Use only available project context and
  preferences the user has actually supplied.
- Preserve an established visual language unless the task calls for changing it.
  Treat warnings about common aesthetics as prompts for intentional choices,
  not blanket bans on appropriate fonts, colors, or layouts.
- Resolve routine choices independently. Ask a concise question when missing
  information materially changes the result; continue independent work while
  waiting. For low-impact ambiguity, state a reasonable assumption and proceed.
  A design plan does not require an extra approval step.

## Design and implement

1. Identify the audience, primary task, real content, and technical constraints.
   Inspect nearby UI and reusable components before introducing new patterns.
2. For substantial design work, choose a coherent direction and briefly define
   palette, typography, spacing, layout, and interaction. Make one element
   memorable and keep the surrounding composition disciplined. Scale planning
   to the task; avoid exhaustive alternatives or a mandatory redesign for small
   changes.
3. Build working behavior in the project's existing framework. Use consistent
   tokens and reusable components, clear CSS specificity, and responsive layouts.
   Add dependencies only when they provide a concrete benefit.
4. Write plain, specific interface copy. Make controls describe their actions and
   cover relevant loading, empty, error, and success states. Identify sample data
   as such; do not invent customer endorsements, metrics, or working integrations.

## Meet the quality floor

- Prefer semantic HTML and native controls. Provide meaningful labels, logical
  heading order, useful image alternatives, keyboard access, and visible focus.
- Maintain readable contrast and text sizing. Do not rely on color alone for
  status or meaning. Respect reduced-motion preferences and avoid unnecessary
  automatic animation.
- Check narrow and wide viewports, long content, zoom, and overflow. Keep primary
  actions usable on touch devices.
- Reuse project assets and font-loading conventions. Avoid gratuitous animation,
  oversized images, and dependencies that harm loading or interaction.

## Verify and report

Run the relevant existing lint, type, build, or test checks for the change.
When browser tools are available, exercise the main interaction and inspect
desktop and mobile rendering, keyboard focus, and console errors. Review
screenshots for hierarchy, spacing, legibility, and adherence to the brief.

Fix observed issues, then report the change and the checks actually performed.
State any verification limits clearly; do not claim browser or accessibility
checks that were not run.

## Source and preservation

The original skill and its accompanying [Apache 2.0 license](LICENSE.txt) are
preserved without content changes. This entry point is a local Codex adaptation,
not an official OpenAI or Anthropic endorsement. See [upstream.json](upstream.json)
for the pinned source revision and original-to-local file mapping.
