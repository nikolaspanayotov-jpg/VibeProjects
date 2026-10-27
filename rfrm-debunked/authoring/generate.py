#!/usr/bin/env python3
"""Optional authoring helper. The generated index.html has no runtime dependency."""
import hashlib
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'authoring'
BATCHES = ['energy', 'housing', 'infrastructure', 'deregulation', 'tax', 'support']
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
for a in articles:
    assert 120 <= len(a['critique'].split()) <= 200, a['id']
    assert a['sourceIds'] and all(s in source_map for s in a['sourceIds']), a['id']
    assert all(i in by_id for i in a['related']), a['id']
    assert a['number'] or a['id'].startswith('claim-')
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


def render_article(a):
    n = a['number']
    article_id = a['id']
    topic = slug(a['category'])
    number = f'{n:02d}' if n else 'Also'
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
    return f'''<article class="policy" id="{esc(article_id)}" data-number="{n or ''}" data-topic="{topic}" aria-labelledby="{esc(article_id)}-heading">
<div class="policy-head"><span class="policy-number{'' if n else ' support'}" aria-hidden="true">{number}</span><div><h3 id="{esc(article_id)}-heading" tabindex="-1"><a href="#{esc(article_id)}">{esc(a['title'])}</a></h3><p class="meta">{'Original measure '+str(n) if n else 'Supporting entry'} in {esc(a['category'])}. PDF p. {esc(a['page'])}</p></div></div>
<div class="policy-body"><p class="proposal-label">What Reform proposes</p><p class="proposal">{esc(a['proposal'])}</p><p class="counter">{esc(a['counter'])}</p><details class="analysis"><summary>Debunked<span class="sr-only">: analysis of {esc(a['title'])}</span></summary><div class="analysis-text">{analysis}</div><h4 class="sources-heading">Sources</h4><ol class="article-sources">{citations}</ol><div class="related"><strong>Related analysis</strong><br>{related}</div></details><div class="article-actions"><a href="#{esc(article_id)}">Permanent link<span class="sr-only"> to {esc(a['title'])}</span></a><button class="copy-link" type="button" hidden aria-label="Copy link to {esc(a['title'])}">Copy link</button></div><div class="copy-fallback" hidden><label for="{esc(article_id)}-copy">Copy this link</label><input id="{esc(article_id)}-copy" readonly type="text" spellcheck="false"></div></div></article>'''


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
replacements = {'SUPPORT_COUNT':len(articles)-64, 'NUMBER_INDEX':''.join(f'<a href="#measure-{i:02d}" aria-label="Measure {i}: {esc(by_id[f"measure-{i:02d}"]["title"])}">{i:02d}</a>' for i in range(1,65)), 'TOPIC_LINKS':topic_links,'TOPIC_OPTIONS':topic_options,'ARTICLES':sections,'TABLES':table_html,'BIBLIOGRAPHY':bibliography}
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

Reviewed: **27 October 2026**. Scope: **64 original numbered measures, 37 supporting entries, 10 original numbered categories, 104 source records**. All analyses are 120–200 words excluding attributed proposals and sources. This is a critical examination, not an independent fiscal certification.

## Source document and limits

The user supplied a 36-page PDF titled *Economic Rescue Plan*. Its printed pages run through page 33, followed by covers/blank material. Title, foreword, branding and metadata do not independently establish official provenance. No authenticated publisher-hosted original was established. Policy attributions refer to that supplied document; they do not imply current party policy has been independently confirmed.

The preserved summary is [economic-rescue-plan-summary.md](./economic-rescue-plan-summary.md). SHA-256: `{hashlib.sha256(summary.encode()).hexdigest()}`. It has not been edited. Numbered categories follow the preserved summary headings; detailed page breaks were checked in the extracted supplied PDF: measures 11–14 p.25, 15–20 p.26, 53–54 p.28, 55–64 p.29.

Sources were searched, opened and read through the web connector on the access dates recorded below. Live guidance may lack a displayed publication date; that is marked rather than invented. Some legislation records use the original enactment date with the accessed version identified in the URL/finding. A publication date is not itself a statement about commencement. Historical evidence is labelled in analyses. Sources primarily establish rules, data and mechanisms; proposed estimates remain attributed where replication is unavailable.

Evidence gaps: the plan's in-house tax-and-transfer model and full policy-level behavioural assumptions were not available. Counts such as 2.9 million income-tax exits, 320,000 VAT beneficiaries, £860 average reservist saving and the exact £1,300 household promise have not been independently reproduced. Tax burden comparison and trend-based £11,000 gap require complete series/method choices. No independently audited net package costing, distributional model or implementation timetable was established. These are explicit limits, not findings that every proposal is false. Sources may share underlying official data; two government pages are not independent corroboration. No uncited independent certification is implied.

## Coverage inventory against the summary

Every substantive bullet, numbered proposal, narrative proposal and financial row below maps to an article. Repeated EPL and employer-NI proposals point to measures 4 and 34–35; they are not counted as extra numbered measures. Distinct benefits, thresholds, protections, costings and timetable qualifications are retained in the articles or complete table transcriptions.

| Summary line | Source item (verbatim summary) | Analysis |
| --- | --- | --- |
'''
for line_no,ids in sorted(line_map.items()):
    assert all(i in by_id for i in ids)
    text = summary_lines[line_no-1].replace('|','\\|')
    research += f'| {line_no} | {text} | ' + ', '.join(f'[{i}](./index.html#{i})' for i in ids) + ' |\n'
research += '\n## Complete financial-table inventory\n\nBoth PDF table images were visually inspected. The complete printed page 22 savings table and page 31 fiscal table are transcribed in [authoring/tables.json](./authoring/tables.json) and rendered as accessible HTML. All financial years, numeric strings, parentheses, percentages and blank cells are preserved. Source labels retain the document’s terminology; typography is adapted. A blank is unknown/not supplied, not zero. No values were silently reconciled to force totals. Rounding can prevent exact row sums. Memo rows and included reservist costs must not be added again.\n\nThe page 31 table extends beyond the summary’s abbreviated fiscal table: it includes the 2026/27 starting aggregates, all revenue measures, interest adjustment and headroom, specific spending, primary-balance and interest effects, capital component and closing aggregates. Negative revenue/spending changes use the source’s parentheses. The borrowing reduction is a flow, net financial liabilities a stock, current deficit excludes net investment, and an accounting revaluation is not cash collected.\n\n| Table / row | Values in source order (empty = blank) | Related analysis |\n| --- | --- | --- |\n'
for key,table in tables.items():
    research += f'| {key}: financial years | '+', '.join(table['years'])+' | [Tables](./index.html#financial-tables) |\n'
    for row in table['rows']:
        target = table_target(row[0])
        vals = ', '.join(value if value else '(blank)' for value in row[1:]) or '(section heading)'
        research += f'| {key}: {row[0]} | {vals} | [{target}](./index.html#{target}) |\n'
research += '\n## Article and citation audit\n\n| ID | Original number | Category | Printed page | Critique words | Sources |\n| --- | --- | --- | --- | --- | --- |\n'
for a in articles:
    research += f'| [{a["id"]}](./index.html#{a["id"]}) | {a["number"] or "Unnumbered"} | {a["category"]} | {a["page"]} | {len(a["critique"].split())} | '+', '.join(a['sourceIds'])+' |\n'
research += '\n## Source register\n\nEach exact URL is retained. Findings state the purpose for which evidence is used; they should not be read as support for every sentence in a linked article. The articles add clearly reasoned economic inferences about incentives, distribution and implementation.\n\n'
for s in sources:
    research += f'### {s["id"]}\n\n- Publisher: {s["publisher"]}\n- Title: {s["title"]}\n- Publication/update date: {s.get("date") or "Not established; not invented"}\n- Exact URL: {s["url"]}\n- Accessed: {s["accessed"]}\n- Supported finding / qualification: {s["finding"]}\n\n'
(ROOT / 'RESEARCH.md').write_text(research)
print(f'Generated index.html ({len(page.encode()):,} bytes), RESEARCH.md, {len(articles)} articles and {len(sources)} source records.')
