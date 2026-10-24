# PHP explained

An interactive plain-language guide to the October 2026 PHP2Shell disclosures. Current draft saved at the user's request; full browser verification remains incomplete.

## Running
Open index.html in a browser, or serve this folder with `python3 -m http.server 8000`. No build or runtime dependencies. A file preview may disable JavaScript; open in a full browser to use the controls.

## Architecture
All page HTML, CSS and JavaScript are inline in index.html. The `notes` data and `render()` drive two four-step stories; `mode`, `step` and `patched` hold their state. Separate handlers power audience guidance, version guidance, the quiz, copy and print. No persistence, network scanning or application backend.

## Design and constraints
Paper, green and warm warning colors, serif headings and system body text. Responsive layout and reduced-motion support. The desk is a teaching analogy, not a working exploit. Keep source citations and distinguish the October 23 follow-up from the October 21 pair. Security facts are dated October 24, 2026 and need review before future updates.

## Verification status
JavaScript syntax and logic checks using a DOM test double passed. A real Chromium launch was blocked by sandbox restrictions; the subsequent permission request was interrupted. Do not claim all browser controls or mobile rendering have passed.

qa/buttons.cjs contains the prepared Playwright check, not a completed result. It currently uses the original workspace file and screenshot paths and the system Chromium executable; adjust those paths for another checkout. Playwright is a test-only dependency supplied by the original environment. Print invocation is intercepted in that test; the native print dialog is not tested. Clipboard permissions and file-preview JavaScript support remain environment-dependent.
