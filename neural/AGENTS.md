# Neural

Interactive educational neural-network simulation. `index.html` contains the interface, CSS, canvas rendering, and real batch gradient-descent training. No dependencies, build step, external assets, persistence, or backend. Open the file directly or serve this folder with `python3 -m http.server 8000`.

## Architecture

- Fixed 2–4–1 network, sigmoid hidden/output activations, mean squared error. `forward` computes predictions; `trainEpoch` accumulates gradients across all four binary examples before applying updates. Keep numerical changes separate from rendering.
- `weights`, `biases`, `outWeights`, and `outBias` contain model parameters. `epoch` and `history` track learning. History is periodically downsampled to bound memory.
- `liveInput` is independent of training data: sliders and decision-field dragging explore continuous values; only the four binary corners train the model. Intermediate inputs have no ground-truth target.
- `selected` is a corner-row index, or -1 for intermediate inputs. `inspected` identifies a neuron (`i0`, `h0`, `o0`, etc.). Accessible neuron buttons mirror diagram selection.
- `render` updates metrics, table, explanations, and canvases. `updateExplore` explains the current prediction and neuron calculation. `showGuide` advances a five-step beginner walkthrough. Each step has an explicit action in `guideAction`; navigation alone must not start learning or reset model settings. `taskInfo` and `syncTaskCopy` keep the lamp story and worked example consistent with XOR, AND, and OR.
- The animation loop uses a fixed 30 Hz training clock with bounded catch-up. The speed selector changes epochs per tick. Training pauses when every binary example has absolute prediction error below 0.08; the user can continue. Reset and task changes stop training and randomize parameters.

## Beginner explanations

Use the two-switch/lamp story: 0 = off/no, 1 = on/yes. Describe XOR as exactly one switch on, AND as both on, and OR as at least one on (including both). Explain concepts before jargon. Asking with sliders, presets, table rows, or the map must not train the model; only training controls change parameters.

Display epochs as practice rounds and accuracy as correct examples out of four. Keep the distinction between correct Yes/No categories and score error. Scores use a 0.5 threshold and are not calibrated confidence probabilities. Scores are rounded for display; classification uses the full value. Completion only means the four practice scores are close to their targets, not that generalization has been tested.

Middle circles are small calculators, weights are signed influences, biases are learned starting nudges, and activation is the outgoing signal. Keep equations and extra controls optional in collapsed `details`. The answer-map background shows predictions, corner dots show correct teaching answers, and the white ring shows the current query. Intermediate inputs have no supplied target. Glossary and FAQ content should remain accurate if the algorithm changes.

## UI conventions

The frontend design follows the repository's `.agents/skills/frontend-design/SKILL.md` and its design reference. The direction is an interactive field guide: pale sage reading surfaces around a forest-green experiment panel. The live switch-and-lamp circuit is the main visual element; surrounding headings, navigation, and lesson sections stay simple.

CSS tokens: `--bg` #f2f5ef, `--paper` #ffffff, `--panel` #e4ecdf, `--ink` #213d32, `--muted` #52655b, `--accent` #245a3c. The experiment panel scopes a dark palette using `--stage` #142b23, light ink, lime positive signals, and coral negative signals. Keep canvas constants synchronized with stage tokens. Blue-to-lime answer-map semantics remain unchanged.

Large headings and values use a local serif stack (Iowan Old Style / Palatino / Georgia); reading text uses a humanist sans stack (Trebuchet MS / Segoe UI / sans-serif). No remote fonts or assets are required. Use sentence case, visible focus, restrained borders, and meaningful section anchors. Main responsive breakpoints are 1100px, 760px, and 520px, with a narrow 360px adjustment. Respect reduced motion; suppress moving signal particles while retaining training updates.

The opening circuit uses `heroSwitch0/1`, `heroBulb`, `heroScore`, and `heroTarget`. `updateExplore` synchronizes them with `liveInput` and the current model. The switches only query the network; they must not train it. The lamp shows the network's Yes/No guess, while the separate correct-answer text uses the selected task. Intermediate inputs have no supplied target. Canvas interactions have keyboard-accessible controls as alternatives.

The `neural` folder is the stable URL path. Do not rename it. Deployment depends on repository GitHub Pages settings; do not claim a live URL without verifying hosting.

## Verification

Check XOR, AND, and OR learning, live-input feedback, inspected calculations, guide navigation, dragging the field, play/pause, reset, speed changes, and mobile overflow. Network initialization is random, so allow occasional slow XOR convergence. JavaScript syntax, numerical convergence for all three tasks, and interaction-handler checks passed for the beginner rewrite. Checks cover asking without training, presets, sliders, task-specific stories, all five guide actions, pause/reset, inspection, and map input. HTML IDs, anchor links, labels, and ARIA references were checked. For the design update, DOM binding and interaction-handler checks passed for the opening switches, score/target synchronization across all rules, guide actions, training controls, inspector, and map input. Core text/background color pairs were calculated above 4.5:1 contrast. HTML section nesting and references passed. Browser launch remains blocked by sandbox socket restrictions, so phone/desktop screenshots, actual browser interactions, and rendered overflow/focus checks remain outstanding.
