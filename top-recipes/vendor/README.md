# Local browser libraries

These browser distributions are checked in so the page works without a CDN or an application build step.

| Library | Version | Source | License |
| --- | --- | --- | --- |
| Marked | 15.0.12 | `marked/lib/marked.umd.js` from its npm package | `marked.LICENSE.md` |
| js-yaml | 4.1.0 | `js-yaml/dist/js-yaml.min.js` from its npm package | `js-yaml.LICENSE` |

They parse Markdown tokens and YAML metadata only. Authored recipe content is rendered through text nodes, not as HTML. Test dependencies in `tests/package.json` pin the same versions. When updating a library, replace its browser file and license and rerun the checks.
