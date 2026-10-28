# Browser checks

From the repository root:

```bash
node --check neural/app.js
node neural/tests/browser.cjs
```

The browser check uses an existing `playwright` installation and Chromium at `/usr/bin/chromium`. Set `CHROMIUM_PATH` if the executable is elsewhere. Test dependencies belong in this tests folder, not in the application.

The test reads the real HTML, stylesheet, and JavaScript and renders them together in memory, with no network requests. This supports browser environments that block navigation to local files or preview servers. It checks actual DOM behavior, model transitions, keyboard focus, all three learning tasks, and horizontal overflow at 1440px, 390px, and 320px.

Screenshots are saved in `/tmp/neural-learning-{desktop,mobile,narrow}.png` and `/tmp/neural-round-{desktop,mobile}.png`. Review them after layout changes. This does not validate GitHub Pages hosting or externally served asset responses.
