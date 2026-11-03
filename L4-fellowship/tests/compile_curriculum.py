"""Optional authoring utility: solutions.md + design.md -> checked-in curriculum.js.

The website itself needs no build. Run with Python-Markdown installed for this
utility only: python3 -m pip install Markdown; python3 tests/compile_curriculum.py.
"""
from pathlib import Path
import hashlib
import json
import re
import markdown

ROOT = Path(__file__).resolve().parent.parent
SOURCE = (ROOT / 'solutions.md').read_text()
DESIGN = (ROOT / 'design.md').read_text()
THEMES = [
    ('Responsible data use', 'Protect people and make responsible decisions.', 'K1 K2 K4 K15 S1 S3 B1'),
    ('Planning and delivery', 'Turn a stakeholder need into a useful result.', 'K3 K9 S2 S7 B3 B7'),
    ('Structures, architecture and tools', 'Understand the systems behind your analysis.', 'K5 K6 K11 K12 S4 S9 S15'),
    ('Preparation and quality', 'Combine sources and investigate what looks wrong.', 'K8 K10 S6 S8 B4 B5'),
    ('Statistics and analytical methods', 'Choose methods, test assumptions and explain uncertainty.', 'K13 K14 S10 S11 S13 B2 B6'),
    ('User-centred communication', 'Make your findings accessible and useful.', 'K7 S5 S12 S14'),
]
TARGETS = {
 'K1':['Define UK GDPR and the Data Protection Act','Explain all seven principles','Apply the rules to access, use and retention','Connect legislation to secure working'],
 'K2':['Name actual data, security and AI policies','Explain daily compliance and role impact','Explain non-compliance and escalation'],
 'K3':['Explain all five lifecycle stages','Apply every stage to one project','Explain iteration and validation'],
 'K4':['Define open, public, administrative and research data','Classify your sources with reasons','Explain source inclusion and exclusion'],
 'K5':['Define structured and unstructured data','Explain differences and mixed structures','Justify the category of your project data'],
 'K6':['Define database, warehouse, lake, RDBMS and NoSQL','Explain normalisation and ETL','Explain implementation and maintenance','Describe SQL, APIs and other interfaces'],
 'K7':['Define UX and domain context','Explain simplicity, clarity and accessibility','Connect principles to real design decisions'],
 'K8':['Explain the five requested quality dimensions','Identify NULLs, outliers and errors','Explain decision impact','Justify mitigation, resolution or escalation'],
 'K9':['Explain stakeholder mapping and Power-Interest Matrix','Describe requirement-gathering communication','Trace requirements into scope, planning and outputs'],
 'K10':['Define primary, foreign and composite keys','Explain four joins and UNION/UNION ALL','Explain grain, cardinality and validation','Demonstrate a justified organisational benefit'],
 'K11':['Describe tools actually available in the organisation','Compare realistic tool and method options','Justify tools selected for the project'],
 'K12':['Outline actual data architecture','Explain storage, security and access implications','Connect architecture to tool choices','Discuss Big Data where relevant'],
 'K13':['Explain mean, median, mode, variance and standard deviation','Explain hypotheses, t-tests, alpha and p-values','Describe a concrete application','Interpret uncertainty and practical significance'],
 'K14':['Define descriptive, predictive and prescriptive analytics','Give a clear example of each','Demonstrate all three in your own practice'],
 'K15':['Describe source, purpose and collection method','Discuss fairness, bias, transparency, accountability and consent','Apply an appropriate ethical framework','Explain consequences and residual risk'],
 'S1':['Demonstrate compliant operation of actual systems','Embed Privacy by Design across the lifecycle','Explain minimisation, access controls and protection','Reference actual controls and verification'],
 'S2':['Execute planning','Execute data preparation','Execute analysis','Execute refining and comparison','Execute communication and handover'],
 'S3':['Apply actual sensitivity and classification rules','Justify confidentiality controls','Explain any approved flexibility','Check redaction, pseudonymisation or aggregation risks'],
 'S4':['State actual shapes, grain and structures','Discuss RDBMS advantages and trade-offs','Adapt the analysis to structural differences','Validate the transformed result'],
 'S5':['Explain layout, colour and hierarchy choices','Show accessibility consideration and evaluation','Demonstrate stakeholder need','Apply a specific domain rule'],
 'S6':['Identify and measure a real quality issue','Assess impact and investigate','Mitigate, escalate or resolve with reasons','Validate and communicate remaining risk'],
 'S7':['Translate requirements into project scope','Trace requirements to methods and planning','Demonstrate final deliverables and acceptance checks'],
 'S8':['Demonstrate a repeatable multi-source join','Justify keys, join type and grain','Explain risks and preparation','Reconcile counts, unmatched rows and totals'],
 'S9':['Name actual architecture components and tools','Explain why the interface fits the infrastructure','Demonstrate authorised interaction and constraints'],
 'S10':['Perform EDA and summary statistics','State hypotheses and significance level','Execute a justified inferential test','Check assumptions','Interpret p-values, effect and uncertainty'],
 'S11':['Apply descriptive analytics','Build and validate a predictive method','Compare a baseline and prevent leakage','Provide a justified prescriptive recommendation'],
 'S12':['Describe two distinct stakeholders','Adapt communication styles and channels','Show actual collaboration','Explain feedback and resulting changes'],
 'S13':['Define target, frequency, history window and horizon','Justify model and trend/seasonality assessment','Use time-ordered validation and a baseline','Calculate RMSE or another suitable error metric','Show a visual forecast and explain projections','Prepare a separate mining/modelling example'],
 'S14':['Collate and interpret quantitative data','Collate and interpret qualitative data','Visually represent both types','Justify charts and explain insights and limitations'],
 'S15':['Evaluate available tools against requirements','Select and apply an appropriate workflow','Justify outcome and remaining trade-offs'],
 'B1':['Describe secure, professional working habits','Apply actual controls and handling rules','Explain a specific outcome and learning'],
 'B2':['Identify a minor unexpected workplace change','Explain initiative and adaptation within your remit','Show maintained quality and productivity'],
 'B3':['Identify independent responsibilities and decisions','Describe effective collaboration','Explain your specific contribution','Describe positive impact on others'],
 'B4':['Structure an ambiguous problem independently','Explain ordered hypotheses and checks','Justify the solution from evidence','Validate the conclusion'],
 'B5':['Describe a problem with an initially unknown cause','Explain a systematic investigation','Establish the true root cause','Implement and validate the solution','Explain a recurrence-prevention control'],
 'B6':['Identify a specific challenge or setback','Explain resilient actions and support','Report an honest result','Explain learning and changed future practice'],
 'B7':['Identify a change in scope, goals or responsibilities','Explain the revised approach and plan','Manage stakeholder feedback and expectations','Describe the outcome and limitations'],
}

def html(text):
    text = re.sub(r'```mermaid\n.*?```', '<div class="forecast-example"></div>', text, flags=re.S)
    result = markdown.markdown(text.strip(), extensions=['tables','fenced_code','sane_lists'])
    result = result.replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="Study data table"><table>').replace('</table>', '</table></div>')
    return re.sub(r'<a href="(https?://[^"]+)"', r'<a target="_blank" rel="noopener noreferrer" href="\1"', result)

questions = {}
for line in DESIGN.splitlines():
    match = re.match(r'^\| \[\*\*([KSB]\d+):',line)
    if match:
        questions[match[1]] = line.split(' | ')[2].strip()

records=[]
for match in re.finditer(r'^### ([KSB]\d+) — ([^\n]+)\n(.*?)(?=^<a id="ksb-|^<a id="personal-answer|\Z)',SOURCE,re.M|re.S):
    ksb,title,body=match.groups()
    body=re.split(r'^## ',body,flags=re.M)[0].strip()
    guide,remaining=body.split('**Make it yours.**',1)
    template,remaining=remaining.split('**Evidence to reference.**',1)
    evidence,remaining=remaining.split('**Coverage check.**',1)
    coverage,followup=remaining.split('**Follow-up.**',1)
    theme=next(i for i,(_,_,ids) in enumerate(THEMES) if ksb in ids.split())
    records.append(dict(id=ksb,title=title,category=ksb[0],theme=theme,
        guide=html(guide.replace('**Answer guide.**','',1)),template=html(template),
        evidence=html(evidence),coverage=coverage.strip(),targets=TARGETS[ksb],
        followup=followup.strip(),question=questions[ksb],searchText=body,
        sourceAnchor='ksb-'+ksb.lower(),revision='2026-11-03',
        route=1 if ksb in 'K3 K4 K8 K9 K11 K12 S1 S2 S3 S4 S6 S7 S8 S12 S15 B3 B4'.split() else 2))

assert len(records)==37 and set(TARGETS)=={x['id'] for x in records}
data=dict(revision='2026-11-03',sourceSha256=hashlib.sha256(SOURCE.encode()).hexdigest(),
          items=records,themes=[dict(name=n,description=d,ids=ids.split()) for n,d,ids in THEMES],
          introduction=html(SOURCE.split('## How to use these answers',1)[1].split('## Knowledge',1)[0]),
          sources=html(SOURCE.split('## Reference register',1)[1]))
(ROOT/'curriculum.js').write_text('// Authored from solutions.md; no runtime Markdown dependency.\nwindow.L4_CURRICULUM = '+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';\n')
print('Compiled 37 complete answer records into curriculum.js')
