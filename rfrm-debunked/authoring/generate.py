#!/usr/bin/env python3
"""Optional authoring helper. The generated index.html has no runtime dependency."""
import hashlib
import html
import json
import re
from collections import OrderedDict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'authoring'
BATCHES = ['energy', 'housing', 'infrastructure', 'deregulation', 'tax', 'support', 'updates']
articles, sources = [], []
for name in BATCHES:
    batch = json.loads((DATA / f'{name}.json').read_text())
    articles.extend(batch['articles'])
    sources.extend(batch['sources'])
by_id = {a['id']: a for a in articles}
source_map = {s['id']: s for s in sources}
assert len(by_id) == len(articles)
assert len(source_map) == len(sources)
assert [a['number'] for a in articles if a['number']] == list(range(1, 65))
EVIDENCE_LABELS = {'Internal contradiction', 'Legal obstacle', 'Costing uncertainty', 'Strong evidence', 'Distributional trade-off', 'Reasonable policy with caveats'}
for a in articles:
    assert a['evidenceLabel'] in EVIDENCE_LABELS, a['id']
    assert 120 <= len(a['critique'].split()) <= 200, a['id']
    assert a['sourceIds'] and all(s in source_map for s in a['sourceIds']), a['id']
    assert all(i in by_id for i in a['related']), a['id']
    assert a['number'] or a['id'].startswith('claim-')
    for panel in a.get('evidencePanels', []):
        assert all(i in source_map for i in panel['sourceIds'])
    assert all(link['id'] in by_id for link in a.get('dependencies', []))
for s in sources:
    assert s['url'].startswith('https://'), s['id']


def esc(value):
    return html.escape(str(value), quote=True)


def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def article_link(article_id, label=None):
    return f'<a href="#{esc(article_id)}">{esc(label or by_id[article_id]["title"])}</a>'


groups = OrderedDict()
for a in articles:
    groups.setdefault(a['category'], []).append(a)


# Curated entry points collect existing categories without renumbering articles.
SHORTCUTS = {
    'pay': {'label': 'Pay and taxes', 'topics': ['Tax cuts and household bills', 'Reducing the cost of hiring British workers', 'Welfare claims'], 'ids': []},
    'energy': {'label': 'Energy bills', 'topics': ['Unlocking the North Sea', 'Reindustrialising Britain'], 'ids': ['claim-energy-bills', 'claim-net-zero-spending']},
    'housing': {'label': 'Housing', 'topics': ['Getting homes built in cities', 'Building critical national infrastructure'], 'ids': []},
    'services': {'label': 'Public services', 'topics': ['Spending and services', 'Welfare claims'], 'ids': []},
}
assert all(category in groups for shortcut in SHORTCUTS.values() for category in shortcut['topics'])
assert all(article_id in by_id for shortcut in SHORTCUTS.values() for article_id in shortcut['ids'])


TERM_LABELS = {"headroom":"Fiscal headroom","marginal-pricing":"Marginal pricing","ets":"Emissions Trading Scheme (ETS)","cbam":"Carbon Border Adjustment Mechanism (CBAM)","ni":"National Insurance (NI)","uc":"Universal Credit (UC)"}
ARTICLE_TERMS = {"measure-04":["marginal-pricing"],"measure-06":["ets","cbam"],"measure-07":["cbam","ets"],"measure-34":["ni"],"measure-35":["ni"],"claim-energy-bills":["marginal-pricing","ets"],"claim-personal-allowance":["uc","ni"],"claim-fiscal-headroom":["headroom"],"claim-fiscal-timing":["headroom"]}
FUNDING_ROUTE = ['measure-35', 'measure-34', 'claim-fiscal-timing']
ROUTE_LABELS = ['the levy', 'the NI cut', 'funding assumptions']


def contextual_terms(article_id):
    terms = ARTICLE_TERMS.get(article_id, [])
    return ('<p class="term-links">Terms: ' + ' '.join(f'<a href="#term-{key}">{esc(TERM_LABELS[key])}</a>' for key in terms) + '</p>') if terms else ''


def route_navigation(article_id):
    if article_id not in FUNDING_ROUTE:
        return ''
    i = FUNDING_ROUTE.index(article_id)
    previous = (f'<a href="#{FUNDING_ROUTE[i-1]}">Previous: {ROUTE_LABELS[i-1]}</a>' if i else '<a href="#funding-route">Route introduction</a>')
    following = (f'<a href="#{FUNDING_ROUTE[i+1]}">Next: {ROUTE_LABELS[i+1]}</a>' if i < 2 else '<a href="#funding-route">Finish: return to the route</a>')
    return f'<nav class="route-steps" aria-label="Funding reading route"><p>Funding route: step {i+1} of 3</p>{previous}{following}</nav>'


def correction_url(article_id):
    reference = 'https://github.com/nikolaspanayotov-jpg/VibeProjects/blob/main/rfrm-debunked/index.html' + ('#' + article_id if article_id else '')
    body = 'Article: ' + reference + '\n\nWhat seems wrong:\n\nEvidence / source URL (and relevant quotation or figures):\n\nSuggested correction:\n'
    title = 'rfrm debunked: correction' + (' — ' + article_id if article_id else '')
    return 'https://github.com/nikolaspanayotov-jpg/VibeProjects/issues/new?title=' + quote(title, safe="~()*!.'-") + '&body=' + quote(body, safe="~()*!.'-")


def render_article(a):
    n = a['number']
    article_id = a['id']
    topic = slug(a['category'])
    number = f'{n:02d}' if n else 'Also'
    shortcuts = ' '.join(key for key, entry in SHORTCUTS.items() if a['category'] in entry['topics'] or article_id in entry['ids'])
    source_refs = ' '.join(f'<a href="#{esc(article_id)}-source-{i}" aria-label="Source {i} for {esc(a["title"])}">[{i}]</a>' for i, _ in enumerate(a['sourceIds'], 1))
    paragraphs = a['critique'].split('\n\n')
    if len(paragraphs) == 1:
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z£])', paragraphs[0])
        target, total, split_at = len(a['critique'].split()) / 2, 0, 0
        for i, sentence in enumerate(sentences[:-1], 1):
            total += len(sentence.split())
            if total >= target:
                split_at = i
                break
        if split_at:
            paragraphs = [' '.join(sentences[:split_at]), ' '.join(sentences[split_at:])]
    analysis = ''.join(f'<p>{esc(p)}' + (f' <span class="citations">{source_refs}</span>' if i == len(paragraphs) - 1 else '') + '</p>' for i, p in enumerate(paragraphs))
    citations = ''
    for i, source_id in enumerate(a['sourceIds'], 1):
        s = source_map[source_id]
        date = s.get('date') or 'Publication date not established; accessed 27 October 2026'
        citations += f'<li id="{esc(article_id)}-source-{i}"><a href="{esc(s["url"])}">{esc(s["publisher"])}: {esc(s["title"])}</a> <span>({esc(date)})</span></li>'
    related = ' '.join(article_link(i) for i in a['related'])
    evidence_panels = ''
    for i, panel in enumerate(a.get('evidencePanels', []), 1):
        panel_sources = ' '.join(f'<a href="{esc(source_map[source_id]["url"])}">{esc(source_map[source_id]["publisher"])}</a>' for source_id in panel['sourceIds'])
        evidence_panels += f'<aside class="evidence-panel" id="{esc(article_id)}-evidence-{i}" aria-labelledby="{esc(article_id)}-evidence-heading-{i}"><h4 id="{esc(article_id)}-evidence-heading-{i}">{esc(panel["title"])}</h4>' + ''.join(f'<p>{esc(paragraph)}</p>' for paragraph in panel['paragraphs']) + f'<p class="panel-sources">Evidence: {panel_sources}</p></aside>'
    dependencies = ''
    if a.get('dependencies'):
        dependencies = '<div class="dependencies"><strong>What this depends on</strong><ul>' + ''.join(f'<li>{article_link(link["id"])}: {esc(link["reason"])}</li>' for link in a['dependencies']) + '</ul></div>'

    return f'''<article class="policy" id="{esc(article_id)}" data-number="{n or ''}" data-topic="{topic}" data-shortcuts="{shortcuts}" aria-labelledby="{esc(article_id)}-heading">
<div class="policy-head"><span class="policy-number{'' if n else ' support'}" aria-hidden="true">{number}</span><div><h3 id="{esc(article_id)}-heading" tabindex="-1"><a href="#{esc(article_id)}">{esc(a['title'])}</a></h3><p class="meta">{'Original measure '+str(n) if n else 'Supporting entry'} in {esc(a['category'])}. PDF p. {esc(a['page'])}</p></div></div>
<div class="policy-body"><p class="evidence-label">{esc(a["evidenceLabel"])}</p><p class="proposal-label">What Reform proposes</p><p class="proposal">{esc(a['proposal'])}</p><p class="proposal-label question-label">Main question</p><p class="counter">{esc(a['counter'])}</p><details class="analysis"><summary>Analysis and sources<span class="sr-only">: analysis of {esc(a['title'])}</span></summary>{contextual_terms(article_id)}<div class="analysis-text">{analysis}</div>{evidence_panels}{dependencies}<h4 class="sources-heading">Sources</h4><ol class="article-sources">{citations}</ol><div class="related"><strong>Related analysis</strong><br>{related}</div>{route_navigation(article_id)}<a class="back-results" href="#explorer-heading">Back to results</a></details><div class="article-actions"><a href="#{esc(article_id)}">Permanent link<span class="sr-only"> to {esc(a['title'])}</span></a><button class="copy-link" type="button" hidden aria-label="Copy link to {esc(a['title'])}">Copy link</button><a class="report-error" data-article="{esc(article_id)}" href="{esc(correction_url(article_id))}">Report an error<span class="sr-only"> in this entry</span></a></div><div class="copy-fallback" hidden><label for="{esc(article_id)}-copy">Copy this link</label><input id="{esc(article_id)}-copy" readonly type="text" spellcheck="false"></div></div></article>'''


sections = ''
topic_links, topic_options = '', ''
for category, group in groups.items():
    key = slug(category)
    numbers = [a['number'] for a in group if a['number']]
    range_label = f'Original measures {min(numbers)}–{max(numbers)}' if numbers else f'{len(group)} supporting entries'
    topic_links += f'<li><a href="#topic-{key}" data-topic="{key}">{esc(category)}</a></li>'
    topic_options += f'<option value="{key}">{esc(category)}</option>'
    sections += f'<section class="topic-section" id="topic-{key}" aria-labelledby="heading-{key}"><h2 class="section-heading" id="heading-{key}"><span class="range">{range_label}</span>{esc(category)}</h2>' + ''.join(render_article(a) for a in group) + '</section>'


def table_target(label):
    text = label.lower()
    mappings = [('personal allowance','claim-personal-allowance'),('energy bills','claim-energy-bills'),('fuel duty','claim-fuel-duty'),('vat threshold','claim-vat-threshold'),('north sea','measure-04'),('family farms','claim-inheritance-reliefs'),('employer ni','measure-34'),('migrant workers levy','measure-35'),('reservists','claim-reservist-pay'),('overtime','claim-overtime'),('pubs','claim-pubs'),('immigration fees','claim-fiscal-revenue'),('welfare','claim-welfare-disability-redesign'),('zero subsidies','claim-net-zero-spending'),('foreign aid','claim-spending-aid-cap'),('hotel','claim-spending-migrant-hotels'),('quangos','claim-spending-civil-service'),('student loans','claim-spending-overseas-loans'),('doctors and nurses','claim-spending-nhs-training'),('defence','claim-defence'),('spending','claim-fiscal-spending'),('headroom','claim-fiscal-headroom'),('against','claim-fiscal-headroom'),('borrowing costs','claim-fiscal-timing'),('savings','claim-fiscal-savings'),('small measures','claim-fiscal-savings')]
    for term, target in mappings:
        if term in text:
            return target
    return 'claim-fiscal-borrowing'


tables = json.loads((DATA / 'tables.json').read_text())
table_html = ''
for key, table in tables.items():
    rows = ''
    for row in table['rows']:
        if len(row) == 1:
            rows += f'<tr class="table-section"><th colspan="{len(table["years"])+1}" scope="colgroup">{esc(row[0])}</th></tr>'
        else:
            assert len(row) == len(table['years']) + 1
            total = row[0].isupper() or row[0].startswith('ADDITIONAL SPENDING')
            rows += f'<tr class="{"table-total" if total else ""}"><th scope="row">{article_link(table_target(row[0]), row[0])}</th>' + ''.join(f'<td>{esc(value)}</td>' for value in row[1:]) + '</tr>'
    table_html += f'<div class="table-scroll" role="region" aria-label="{esc(table["caption"])}; scroll horizontally for all years" tabindex="0"><table id="table-{key}"><caption>{esc(table["caption"])}</caption><thead><tr><th scope="col">Source table item</th>' + ''.join(f'<th scope="col">{year}</th>' for year in table['years']) + f'</tr></thead><tbody>{rows}</tbody></table></div>'

bibliography = ''
for s in sources:
    date = s.get('date') or 'Publication date not established'
    bibliography += f'<li id="source-{esc(s["id"])}"><a href="{esc(s["url"])}">{esc(s["title"])}</a><small>{esc(s["publisher"])}. {esc(date)}. Accessed {esc(s["accessed"])}.</small><p class="source-finding">{esc(s["finding"])}</p></li>'
highlights = json.loads((DATA / 'highlights.json').read_text())
highlight_cards = []
for i, card in enumerate(highlights):
    assert card['label'] in EVIDENCE_LABELS
    assert all(source_id in source_map for source_id in card['sourceIds'])
    links = ' '.join(f'<a href="#{esc(link["id"])}">{esc(link["label"])}</a>' for link in card['links'])
    evidence = ' '.join(f'<a href="{esc(source_map[source_id]["url"])}" title="{esc(source_map[source_id]["title"])}">{esc(source_map[source_id]["publisher"])}</a>' for source_id in card['sourceIds'])
    highlight_cards.append(f'<div class="headline-card" id="{esc(card["id"])}"><span class="evidence-label">{esc(card["label"])}</span><h3>{esc(card["title"])}</h3><p>{esc(card["text"])}</p><div class="headline-links">{links}</div><p class="headline-evidence">Evidence: {evidence}</p></div>')

highlight_html = '<div class="headline-grid">' + ''.join(highlight_cards[:3]) + '</div><details class="overview-more" id="more-findings"><summary>Explore five more findings</summary><div class="headline-grid">' + ''.join(highlight_cards[3:]) + '</div></details>'
shortcut_controls = '<div class="shortcut-controls enhanced" hidden role="group" aria-label="Everyday topics"><p class="search-label">What matters to you?</p><div class="shortcut-buttons">' + ''.join(f'<button type="button" data-shortcut="{key}" aria-pressed="false">{entry["label"]}</button>' for key, entry in SHORTCUTS.items()) + '</div><p class="hint">These shortcuts collect related parts of the plan. Search and the original topic filter narrow the selection further.</p><p id="shortcut-status" class="hint" role="status"></p></div>'

# Visualise existing source-backed arithmetic; preserve the original worked notes.
uc_panel = by_id['claim-personal-allowance']['evidencePanels'][0]
uc_sources = ' · '.join(f'<a href="{esc(source_map[key]["url"])}">{esc(source_map[key]["publisher"])}</a>' for key in uc_panel['sourceIds'])
uc_notes = ''.join(f'<p>{esc(note)}</p>' for note in uc_panel['paragraphs'])
uc_visual = f'''<figure class="calculation" id="uc-calculation" aria-labelledby="uc-caption"><figcaption id="uc-caption">How £486 tax relief can leave £218.70</figcaption><p class="hint">Illustrative annual change with the full 55% Universal Credit taper.</p><dl class="calculation-values"><div><dt>Income-tax saving</dt><dd>£486.00</dd></div><div><dt>Less Universal Credit</dt><dd>−£267.30</dd></div><div><dt>Retained by the household</dt><dd>£218.70</dd></div></dl><div class="uc-bar" aria-hidden="true"><span class="uc-lost">55% less UC</span><span class="uc-kept">45% retained</span></div><div class="calculation-notes">{uc_notes}</div><p class="figure-source">Sources: {uc_sources}. <a href="#claim-personal-allowance">Read the full analysis</a>.</p></figure>'''
fiscal_rows = {row[0]: row for row in tables['fiscal']['rows']}
ni_row = fiscal_rows['Reverse Rachel Reeves’ employer NI increase']
levy_row = fiscal_rows['Introduce Migrant Workers Levy']
paired_bars = ''
for year, ni, levy in zip(tables['fiscal']['years'][2:], ni_row[3:], levy_row[3:]):
    assert ni == '(' + levy + ')'
    width = float(levy) / 7.14 * 100
    paired_bars += f'<div class="funding-year"><h4>{esc(year)}</h4><div class="funding-row"><span>NI cut cost <strong>£{esc(levy)}bn</strong></span><span class="funding-track" aria-hidden="true"><span class="ni-bar" style="width:{width:.2f}%"></span></span></div><div class="funding-row"><span>Levy receipts <strong>£{esc(levy)}bn</strong></span><span class="funding-track" aria-hidden="true"><span class="levy-bar" style="width:{width:.2f}%"></span></span></div></div>'
levy_source = source_map['official-plan-download']
levy_visual = f'''<figure class="calculation" id="funding-calculation" aria-labelledby="funding-caption"><figcaption id="funding-caption">One funding assumption, two matching rows</figcaption><p class="hint">Published annual nominal £bn, on a shared scale from zero to £7.14bn. Costs and receipts are shown as magnitudes.</p>{paired_bars}<p>The levy receipts exactly match the employer NI cut in all four years. These are two sides of one funding assumption, not two independent gains.</p><p>The intended substitution into British labour and automation can change the levy’s tax base. The eventual receipts depend on those behavioural assumptions; these bars show the plan’s figures, not predicted effects.</p><p class="figure-source">Source: <a href="{esc(levy_source['url'])}">Reform’s official plan, printed p.31</a>. <a href="#measure-34">NI analysis</a> · <a href="#measure-35">Levy analysis</a>.</p></figure>'''
calculation_html = '<section class="calculations" aria-labelledby="calculation-heading"><h3 id="calculation-heading">Two calculations to check</h3><div class="calculation-grid">' + uc_visual + levy_visual + '</div></section>'

audit = json.loads((DATA / 'audit.json').read_text())
assert len(audit['rows']) == 20
AUDIT_STATUSES = {'Published', 'Partial', 'Not provided in the plan', 'Not applicable'}
# Common notes remain verbatim, once, with explicit links from every relevant check.
from collections import Counter
note_counts = Counter(cell['note'] for row in audit['rows'] for cell in row['checks'].values())
common_notes = {note: f'audit-note-{i}' for i, (note, count) in enumerate(note_counts.items(), 1) if count > 1}
note_labels = {}
for row in audit['rows']:
    for dim in audit['dimensions']:
        note_labels.setdefault(row['checks'][dim['id']]['note'], dim['title'])
glossary = '<div class="audit-common"><h3>Common disclosure limitations</h3><p>A named OBR baseline is not OBR certification of this package. Repeated limitations are recorded here once; each relevant check links to its full note.</p><dl>' + ''.join(f'<div id="{anchor}"><dt>{esc(note_labels[note])}</dt><dd>{esc(note)}</dd></div>' for note, anchor in common_notes.items()) + '</dl></div>'
audit_rows = ''
for row in audit['rows']:
    assert row['target'] in by_id
    assert set(row['checks']) == {d['id'] for d in audit['dimensions']}
    checks = ''
    for dim in audit['dimensions']:
        cell = row['checks'][dim['id']]
        assert cell['status'] in AUDIT_STATUSES
        note = (f'<a href="#{common_notes[cell["note"]]}">See common {esc(dim["title"].lower())} note</a>' if cell['note'] in common_notes else esc(cell['note']))
        checks += f'<div class="audit-check" data-dimension="{dim["id"]}"><dt>{esc(dim["title"])}</dt><dd><span class="audit-status">{esc(cell["status"])}</span><span class="audit-note">{note}</span></dd></div>'
    audit_rows += f'<details class="audit-item" id="audit-{esc(row["target"])}"><summary><span class="audit-title">{esc(row["title"])}</span><span class="audit-profile">Published nominal profile: {esc(row["profile"])}</span><span class="audit-prompt">View disclosure details</span></summary><div class="audit-detail"><p>{article_link(row["target"], "Read the policy analysis")} · Printed PDF p.{esc(row["page"])}</p><dl class="audit-checks">{checks}</dl></div></details>'
audit_html = '''<section class="reference-section costing-audit" id="costing-audit" aria-labelledby="costing-heading"><h2 id="costing-heading">Can the major costings be reproduced?</h2><p><strong>The arithmetic is published; the model needed to reproduce it is not.</strong> This disclosure audit covers the official plan and its linked policy page reviewed on 27 October 2026. It does not establish that no related material exists elsewhere, or that an unreplicated number is false.</p><p>Scope: every policy line with an absolute effect of at least £1bn in any financial year from 2027/28 to 2031/32: 20 lines. Aggregates, memo items and opening/closing stocks are excluded. Amounts below show first and final populated years, not necessarily the maximum. Read the complete financial tables for the annual profile.</p><p class="audit-key"><strong>Published</strong>: the relevant assumption or calculation is explicitly disclosed. <strong>Partial</strong>: some relevant information is disclosed, but it does not complete the calculation. <strong>Not provided in the plan</strong>: the reviewed plan does not disclose the reproducible detail required by this test. <strong>Not applicable</strong>: the question does not fit that line; the reason is stated. These are disclosure findings, not confidence scores.</p><p>Six questions: what is the baseline; who or what is covered and at what take-up; how do people and firms respond; what does administration cost; how do policies interact; and how sensitive is the answer? An official OBR baseline is not OBR certification of the policy package.</p>''' + glossary + '<div class="audit-list" aria-label="Twenty major policy lines, six disclosure checks each">' + audit_rows + '</div>' + '''<p>The two NI/levy rows are a linked funding pair, not two independent gains. Overtime includes reservist pay. Student-loan revaluation is distinguished from recurring cash. Source: <a href="https://reformparty.uk/policies/economic-rescue-plan/download">Reform’s official plan</a>, especially printed pp.13–22 and 30–31; relevant article links explain each line.</p></section>'''

replacements = {'SUPPORT_COUNT':len(articles)-64, 'NUMBER_INDEX':''.join(f'<a href="#measure-{i:02d}" aria-label="Measure {i}: {esc(by_id[f"measure-{i:02d}"]["title"])}">{i:02d}</a>' for i in range(1,65)), 'TOPIC_LINKS':topic_links,'TOPIC_OPTIONS':topic_options,'ARTICLES':sections,'TABLES':table_html,'BIBLIOGRAPHY':bibliography,'HIGHLIGHTS':highlight_html,'SHORTCUTS':shortcut_controls,'CALCULATIONS':calculation_html,'COSTING_AUDIT':audit_html}
page = (DATA / 'template.html').read_text()
for key,value in replacements.items():
    page = page.replace('{{'+key+'}}', str(value))
assert '{{' not in page
(ROOT / 'index.html').write_text(page)

# Every substantive source-summary item is mapped, including repeated table rows.
line_map = {
11:['claim-spend-tax-borrow-less','claim-growth-inflation-causality'],12:['claim-household-relief'],13:['claim-debt-three-trillion'],14:['claim-tax-burden-comparison'],15:['claim-living-standards-counterfactual'],16:['claim-growth-inflation-causality'],22:['claim-personal-allowance'],23:['claim-energy-bills','measure-06'],24:['measure-04'],25:['claim-vat-threshold'],26:['claim-fuel-duty'],27:['measure-34','measure-35'],28:['claim-overtime'],29:['claim-reservist-pay'],30:['claim-pubs'],31:['claim-inheritance-reliefs'],39:['claim-welfare-community-work'],40:['claim-welfare-citizenship'],41:['claim-welfare-disability-redesign'],42:['claim-welfare-disability-redesign'],43:['claim-welfare-fraud-error','claim-welfare-indexation-child-cap'],44:['claim-welfare-seven-thousand','claim-welfare-citizenship'],45:['claim-welfare-employer-disability'],49:['claim-net-zero-spending'],53:['claim-spending-aid-cap'],57:['claim-spending-civil-service'],58:['claim-spending-alb-budgets','measure-63'],59:['claim-spending-civil-service'],63:['claim-spending-degree-funding','claim-spending-overseas-loans'],67:['claim-spending-nhs-training'],68:['claim-defence','claim-fiscal-spending'],69:['claim-spending-triple-lock'],70:['claim-spending-migrant-hotels'],178:['claim-welfare-disability-redesign','claim-fiscal-savings'],179:['claim-welfare-indexation-child-cap','claim-fiscal-savings'],180:['claim-net-zero-spending'],181:['claim-spending-aid-cap'],182:['claim-spending-migrant-hotels'],183:['claim-spending-civil-service','claim-spending-alb-budgets'],184:['claim-spending-degree-funding','claim-spending-overseas-loans'],185:['claim-fiscal-savings'],186:['claim-fiscal-savings'],190:['claim-fiscal-timing'],194:['claim-fiscal-revenue'],195:['claim-defence','claim-spending-nhs-training','claim-fiscal-spending'],196:['claim-fiscal-spending'],197:['claim-fiscal-borrowing'],199:['claim-fiscal-revenue'],200:['claim-fiscal-borrowing'],201:['claim-fiscal-headroom'],202:['claim-fiscal-borrowing'],203:['claim-fiscal-headroom'],204:['claim-fiscal-timing']}
summary = (ROOT / 'economic-rescue-plan-summary.md').read_text()
summary_lines = summary.splitlines()
for line_no,line in enumerate(summary_lines,1):
    numbered = re.match(r'^(\d+)\. ',line)
    if numbered:
        line_map[line_no] = [f'measure-{int(numbered[1]):02d}']
research = f'''# Research and coverage record

Reviewed: **27 October 2026**. Scope: **64 original numbered measures, 37 supporting entries, 10 original numbered categories, {len(sources)} source records**. All analyses are 120–200 words excluding attributed proposals and sources. This is a critical examination, not an independent fiscal certification.

## Source document and limits

Reform UK published its official *Economic Rescue Plan* on **26 October 2026**. The [official policy page](https://reformparty.uk/policies/economic-rescue-plan) links a [36-page PDF download](https://reformparty.uk/policies/economic-rescue-plan/download), and the [official launch](https://reformparty.uk/news/reform-economic-rescue-plan-jenrick-tax-free-overtime-growth) supplies the publication date. The official text was checked against the supplied document, including the foreword, 64 measures and p.30 model/phasing passages. This establishes the publisher-hosted version’s provenance; no byte-for-byte identity is claimed. The original supplied summary remains preserved as historical source notes.

The preserved summary is [economic-rescue-plan-summary.md](./economic-rescue-plan-summary.md). SHA-256: `{hashlib.sha256(summary.encode()).hexdigest()}`. It has not been edited. Numbered categories follow the preserved summary headings; detailed page breaks were checked in the extracted supplied PDF: measures 11–14 p.25, 15–20 p.26, 53–54 p.28, 55–64 p.29.

Sources were searched, opened and read through the web connector on the access dates recorded below. Live guidance may lack a displayed publication date; that is marked rather than invented. Some legislation records use the original enactment date with the accessed version identified in the URL/finding. A publication date is not itself a statement about commencement. Historical evidence is labelled in analyses. Sources primarily establish rules, data and mechanisms; proposed estimates remain attributed where replication is unavailable.

Evidence gaps: the official plan and linked policy page do not provide the in-house model needed to reproduce the published arithmetic. This is a scoped disclosure finding, not a claim about every document that may exist elsewhere. Counts such as 2.9 million income-tax exits, 320,000 VAT beneficiaries, £860 average reservist saving and the exact £1,300 household promise have not been independently reproduced. Tax burden comparison and trend-based £11,000 gap require complete series/method choices. No independently audited net package costing, distributional model or implementation timetable was established. These are explicit limits, not findings that every proposal is false. Sources may share underlying official data; two government pages are not independent corroboration. No uncited independent certification is implied.

## Coverage inventory against the summary

Every substantive bullet, numbered proposal, narrative proposal and financial row below maps to an article. Repeated EPL and employer-NI proposals point to measures 4 and 34–35; they are not counted as extra numbered measures. Distinct benefits, thresholds, protections, costings and timetable qualifications are retained in the articles or complete table transcriptions.

| Summary line | Source item (verbatim summary) | Analysis |
| --- | --- | --- |
'''
for line_no,ids in sorted(line_map.items()):
    assert all(i in by_id for i in ids)
    text = summary_lines[line_no-1].replace('|','\\|')
    research += f'| {line_no} | {text} | ' + ', '.join(f'[{i}](./index.html#{i})' for i in ids) + ' |\n'
research += '\n## Editorial update and evidence types\n\nThe page now leads with eight static headline panels: five principal funding/legal/trade questions and three panels on UC, energy and credible concessions. Every one of the 101 policy articles has an explicit evidence label describing the argument, not an automatic truth verdict. Legal obstacles are potential compatibility issues, not findings of adjudicated unlawfulness. Worked examples and dependency panels remain outside the 120–200 word core critique and are included in DOM search.\n\nUpdated analysis covers the exact NI/levy funding pair, non-like-for-like May TPA versus October overtime estimates, current EUSS rights and legal cohorts, paid-carbon credits under the EU CBAM regime and contingent ETS linkage, real electricity policy costs alongside gas exposure, the UC net-earnings example and baseline-sensitive fiscal headroom.\n\n## Major costing disclosure audit\n\nScope: all 20 policy lines whose absolute effect reaches £1bn in any 2027/28–2031/32 year, excluding aggregates, memos and starting/closing stocks. The arithmetic is published; the model needed to reproduce it is not in the reviewed plan or its linked policy page. This is not evidence that every number is wrong or that no related material exists elsewhere. Published, Partial, Not provided in the plan, and Not applicable are disclosure statuses, not truth scores. Each question is recorded below; policy narrative notes identify where partial disclosure occurs. The NI/levy lines form one funding pair; overtime includes reservist pay; loan revaluation is not recurring cash.\n\n| Policy / printed p.31 table label / profile | Baseline | Take-up or coverage | Behaviour | Administration | Interactions | Sensitivity |\n| --- | --- | --- | --- | --- | --- | --- |\n'
for row in audit['rows']:
    research += f'| [{row["title"]}](./index.html#{row["target"]}) — {row["tableLabel"]} — {row["profile"]} | ' + ' | '.join(row['checks'][dim['id']]['status']+': '+row['checks'][dim['id']]['note'] for dim in audit['dimensions']) + ' |\n'
research += '\n## Complete financial-table inventory\n\nBoth PDF table images were visually inspected. The complete printed page 22 savings table and page 31 fiscal table are transcribed in [authoring/tables.json](./authoring/tables.json) and rendered as accessible HTML. All financial years, numeric strings, parentheses, percentages and blank cells are preserved. Source labels retain the document’s terminology; typography is adapted. A blank is unknown/not supplied, not zero. No values were silently reconciled to force totals. Rounding can prevent exact row sums. Memo rows and included reservist costs must not be added again.\n\nThe page 31 table extends beyond the summary’s abbreviated fiscal table: it includes the 2026/27 starting aggregates, all revenue measures, interest adjustment and headroom, specific spending, primary-balance and interest effects, capital component and closing aggregates. Negative revenue/spending changes use the source’s parentheses. The borrowing reduction is a flow, net financial liabilities a stock, current deficit excludes net investment, and an accounting revaluation is not cash collected.\n\n| Table / row | Values in source order (empty = blank) | Related analysis |\n| --- | --- | --- |\n'
for key,table in tables.items():
    research += f'| {key}: financial years | '+', '.join(table['years'])+' | [Tables](./index.html#financial-tables) |\n'
    for row in table['rows']:
        target = table_target(row[0])
        vals = ', '.join(value if value else '(blank)' for value in row[1:]) or '(section heading)'
        research += f'| {key}: {row[0]} | {vals} | [{target}](./index.html#{target}) |\n'
research += '\n## Article and citation audit\n\n| ID | Original number | Category | Printed page | Critique words | Evidence type | Sources |\n| --- | --- | --- | --- | --- | --- | --- |\n'
for a in articles:
    research += f'| [{a["id"]}](./index.html#{a["id"]}) | {a["number"] or "Unnumbered"} | {a["category"]} | {a["page"]} | {len(a["critique"].split())} | {a["evidenceLabel"]} | '+', '.join(a['sourceIds'])+' |\n'
research += '\n## Source register\n\nEach exact URL is retained. Findings state the purpose for which evidence is used; they should not be read as support for every sentence in a linked article. The articles add clearly reasoned economic inferences about incentives, distribution and implementation.\n\n'
for s in sources:
    research += f'### {s["id"]}\n\n- Publisher: {s["publisher"]}\n- Title: {s["title"]}\n- Publication/update date: {s.get("date") or "Not established; not invented"}\n- Exact URL: {s["url"]}\n- Accessed: {s["accessed"]}\n- Supported finding / qualification: {s["finding"]}\n\n'
(ROOT / 'RESEARCH.md').write_text(research)
print(f'Generated index.html ({len(page.encode()):,} bytes), RESEARCH.md, {len(articles)} articles and {len(sources)} source records.')
