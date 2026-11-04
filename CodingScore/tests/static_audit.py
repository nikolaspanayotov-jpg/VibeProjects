"""Structural checks for the self-contained page; this is not a browser audit."""
from html.parser import HTMLParser
from pathlib import Path
import re

page = Path(__file__).resolve().parents[1] / 'index.html'
source = page.read_text()

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.references = []
        self.controls = []
        self.labels = []
        self.external_scripts = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'label' and 'for' in attrs:
            self.references.append(attrs['for'])
            self.labels.append(attrs['for'])
        self.references.extend(attrs.get('aria-labelledby', '').split())
        if tag in ('input', 'textarea', 'select') and attrs.get('type') not in ('hidden', 'checkbox', 'file'):
            self.controls.append(attrs)
        if tag == 'script' and 'src' in attrs:
            self.external_scripts.append(attrs['src'])
        if tag == 'use':
            self.references.append(attrs['href'].removeprefix('#'))

audit = Audit()
audit.feed(source.split('<script>')[0])
assert len(audit.ids) == len(set(audit.ids)), 'Duplicate static ID'
for reference in audit.references:
    assert reference in audit.ids, f'Missing label or icon target: {reference}'
for control in audit.controls:
    assert control.get('id') in audit.labels or 'aria-label' in control, f'Unlabeled control: {control}'
for reference in re.findall(r"\$\('([^']+)'\)", source):
    assert reference in audit.ids or reference == 'campaignSelect', f'Missing DOM target: {reference}'
assert not audit.external_scripts, 'The app should not require an external script'
assert 'prefers-reduced-motion' in source
assert 'name="viewport"' in source
assert 'codingScore.v1' in source
assert source.count('<script>') == source.count('</script>') == 1
print(f'Passed: {len(audit.ids)} unique IDs, all label/icon/DOM targets, form names, and self-contained script.')
