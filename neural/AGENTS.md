# Neural

An interactive field guide for complete beginners learning how a neural network practices with examples. The stable folder is `neural`; do not rename it. The default lamp rule is AND (both switches on), with XOR (exactly one on) offered as a harder follow-up. OR is also available.

## Run and files

Open `index.html` directly, or serve this folder with `python3 -m http.server 8000`. No build, backend, external resources, runtime dependencies, or persistence.

- `index.html`: semantic page structure, experiment, lesson rail, reference material.
- `style.css`: design tokens, dark experiment stage, reading surfaces, responsive and sticky layouts.
- `app.js`: numerical model, training, model snapshots, slow rounds, rendering, guided lesson, and challenges.
- `tests/browser.cjs`: Playwright smoke and regression checks, using an existing Playwright/Chromium installation. See `tests/README.md`.

The source was split once it grew beyond a small single-file demo. Keep all assets self-contained with relative paths.

## Model and invariants

Fixed 2–4–1 network, sigmoid hidden/output activations, mean squared error. `forward` computes a prediction. `trainEpoch(rate)` accumulates gradients across all four binary examples, then applies exactly one batch update. An epoch is described as a practice round. Do not change one model parameter while still calculating another gradient in the same batch.

`weights`, `biases`, `outWeights`, and `outBias` hold live parameters. `copyModel` and `restoreModel` deep-copy arrays. `baseline` retains the initial model, four initial scores, and initial error until Reset or a task change. `replayStart` restores that exact model and clears round history; it does not randomize or replace the comparison baseline. This lets users compare adjustment sizes from identical starting settings.

`liveInput` is a query, independent of the four training examples. Sliders, presets, hero switches, table buttons, and map dragging must never train the model. `selected` is a binary-example index, or -1 for intermediate inputs. Intermediate inputs have no supplied correct answer. `inspected` identifies a circle (`i0`, `h0`, `o0`, etc.).

The requestAnimationFrame loop uses a fixed 30 Hz practice clock with bounded catch-up. Speed changes rounds per tick; learning rate changes adjustment size. Practice automatically pauses when every score is within 0.08 of its supplied target. This only checks training examples, not generalization.

## Slow round

`roundDemo` is null, or a four-stage state machine: guess (0), compare (1), adjust (2), try again (3). `startRound` pauses normal learning and captures the current model, scores, error, adjustment size, and epoch. Stages 0 and 1 do not change parameters. Entering stage 2 calls `trainEpoch` exactly once; stage 3 and Finish do not train again. Exit before adjusting changes nothing; exit after adjusting keeps the committed update. Do not roll it back silently.

Competing input/training/task/reset/replay controls are locked during a slow round. Circle inspection remains available. The optional table shows all four before/after scores at higher precision. `biggestWeightChange` identifies the real connection with the greatest absolute weight adjustment; `drawNetwork` highlights it in yellow. Biases are adjusted too. An individual example may worsen temporarily because the update reflects all four examples.

## Guided learning and accessibility

`guide` has five steps, each with a nearby target and explicit action. The lesson rail stays beside the experiment and results on desktop. On mobile it becomes compact and sticky; expanding lesson details makes it flow normally so it cannot cover the entire experiment. Keep scroll margins consistent with the compact rail height.

`guideAction` advances an active slow round instead of restarting it. Navigation never starts a practice round. `challengeForStep` supplies a short conceptual question with explanatory feedback. The first question adapts to the selected rule. `challengeAnswers` stays in memory; changing rules resets it. No locked progression or persistence. Preserve keyboard focus after choosing an answer.

`taskInfo` and `syncTaskCopy` keep story and rule descriptions consistent. `renderExamples` updates stable table rows with native buttons so training does not remove keyboard focus. The starting and current scores remain separate. Improvement text distinguishes category correctness from distance to the target.

Charts have drawn axis titles, values, and a starting-error reference. `mapBounds` defines the plotted rectangle for both rendering and pointer conversion. The selected-point readout includes input values, predicted answer/score, and the supplied answer if there is one. Corner dots represent targets, background represents predictions, and the white ring marks the current query. Keep slider alternatives for canvas interactions.

Use plain explanations before technical terms. Keep equations and extra controls optional. A score is not a calibrated confidence probability. Scores are rounded for display; Yes/No uses the full value with a 0.5 threshold. Brightness is activation, not knowledge or certainty.

## Design

Follow `../.agents/skills/frontend-design/SKILL.md` and its reference. Interactive field-guide direction: pale sage reading surfaces surrounding a forest-green experiment stage. The live switch/lamp circuit is the main visual element.

Core tokens: background #f2f5ef, white paper, panel #e4ecdf, ink #213d32, muted #52655b, accent #245a3c. Stage #142b23, light ink #f0f3e9, lime positive connections #c6f681, coral negative connections #df9a87, blue low-score map #75c6db. Canvas constants mirror stage colors; keep them synchronized. Yellow highlights the largest weight adjustment in a slow round.

Local serif stack for large headings/values (Iowan Old Style / Palatino / Georgia), humanist sans for reading (Trebuchet MS / Segoe UI / sans-serif). No remote fonts. Visible focus, sentence case, restrained borders, readable contrast, reduced motion. Breakpoints at 1100px, 760px, 520px, with a 360px adjustment. Reduced motion suppresses moving signal particles; user-paced slow rounds still work.

## Verification and deployment

Run `node --check neural/app.js` and `node neural/tests/browser.cjs` from the repository root with Playwright and Chromium available. Tests cover exact single-update slow rounds, unchanged exploration, exact replay, immutable baselines, challenge feedback/focus, all three learning tasks, training controls, keyboard table actions, mobile/desktop/narrow overflow, and console errors. Inspect screenshots, including the active slow round at phone width.

Browser checks and screenshot inspection passed for the guided-learning update. The browser environment blocks local-file and local-server navigation, so the test assembles the actual HTML/CSS/JS into an in-memory browser page without network requests. Relative asset references and HTML IDs/nesting are also checked separately.

Publish all application files together; index now references both style.css and app.js. Hosting depends on repository GitHub Pages settings; do not claim a live URL without verifying it.
