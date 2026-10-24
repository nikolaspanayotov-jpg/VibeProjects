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

Deep green background, lime signals for positive weights, coral for negative weights, blue-to-lime decision field. CSS custom properties define the palette. Canvas colors are mirrored as constants. Keep both in sync when changing themes. Respect reduced-motion preferences; suppress moving signal particles while retaining useful training updates. Mobile breakpoint is 620px. Keep all controls usable by keyboard; canvas actions have slider/button alternatives.

The `neural` folder is the stable URL path. Do not rename it. Deployment depends on repository GitHub Pages settings; do not claim a live URL without verifying hosting.

## Verification

Check XOR, AND, and OR learning, live-input feedback, inspected calculations, guide navigation, dragging the field, play/pause, reset, speed changes, and mobile overflow. Network initialization is random, so allow occasional slow XOR convergence. JavaScript syntax, numerical convergence for all three tasks, and interaction-handler checks passed for the beginner rewrite. Checks cover asking without training, presets, sliders, task-specific stories, all five guide actions, pause/reset, inspection, and map input. HTML IDs, anchor links, labels, and ARIA references were checked. Browser launch remains blocked by sandbox socket restrictions, so phone/desktop screenshots and actual browser interaction checks remain outstanding.
