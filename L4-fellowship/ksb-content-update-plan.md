# KSB content update plan

Status: implemented; final release verification is recorded in tests/VERIFICATION.md.

## Recommendation

Extend the existing answer bank with a source-referenced assessment layer, targeted evidence prompts and distinction practice. Retain the current 37 lessons, visual cues, worked project and preparation tools. Most foundational explanations and the AM1/AM2 mapping already match the supplied reference; the substantial gaps are exact grouped criteria, explicit grading-versus-provider labels, provider evidence-pack mappings and a larger, traceable discussion-question bank.

The phases and acceptance checks below describe the implemented assessment layer. The new public source is assessment-criteria.json; shared views are provided by assessment.js and assessment.css.

## 1. Sources and baseline

Reviewed against repository commit `5cb03aa8a261f5eb9bf17f3aa2036e86e4f75a48` in `nikolaspanayotov-jpg/VibeProjects`.

New input: the supplied `KSB-Codex-Content-Reference.md` attachment, whose underlying workbook is **KSB list information 2.xlsx**, worksheet **Sheet1**, conversion dated **7 November 2026**. The attachment says it supersedes the earlier PDF transcription. That precedence applies to the supplied provider material; it does not establish precedence over an applicable official assessment plan or legislation.

- Supplied Markdown SHA-256: `faa4541f0cb859bf9329c36123ef5f6a350b4de8039fece0d5c392e5041be9c6`.
- Workbook SHA-256 reported by the attachment: `e77a67fc8f7fa2de73be89fe72d642c31192e8967cfb2d3384f80fdf01b9b035`. The workbook itself was not supplied for this review, so that checksum and transcription accuracy are reported provenance, not independently verified facts.
- The attachment retains 1,654 nonempty source cells, including 27 labelled export-summary cells. Some text is truncated or technically imprecise; some table columns are flattened. Export summaries and sample scenarios are contextual material, not additional criteria.
- This is training-provider guidance, including Multiverse marking guidance. Confirm the learner's applicable standard, assessment-plan version and EPA organisation before presenting a requirement as officially applicable.
- No personal portfolio links, employer policies, completed evidence, marks or learner progress were supplied. Add empty editable fields where needed; create no fictional learner records.

Existing files reviewed: [solutions.md](./solutions.md), [curriculum.js](./curriculum.js), [index.html](./index.html), [design.md](./design.md), [tests/compile_curriculum.py](./tests/compile_curriculum.py), the authored activity sources, [preparation-data.js](./preparation-data.js) and [preparation.js](./preparation.js).

### Baseline findings

| Area | Existing page | Proposed change |
| --- | --- | --- |
| Coverage and methods | All 37 KSBs exist. The current route assignments match the new source: 17 individual KSBs in AM1 and 20 in AM2. AP03 filtering already requires learner confirmation. | Preserve these assignments. Add the source's 30 grouped rows and their exact criteria, with explicit provenance. |
| Explanations | Definitions, fictional examples, common mistakes, personal-answer templates and 111 initial/follow-up/probing prompts already exist. | Add the missing detail in section 4; keep correct explanations and avoid duplicating entire lessons. |
| Grading | The bank centres on pass preparation and self-review targets. It does not store the supplied grouped pass/distinction criteria or provider marking rows as separate records. | Add exact source criteria, provider checklists and derived revision material as three visibly distinct layers. |
| Evidence | Safe references, per-KSB rationales, draft/linked/reviewed states, two S12 stakeholder slots and an S13 forecast/mining worksheet already exist. | Add provider pack mappings, clearer evidence prompts, optional authenticity/review metadata and genuinely separate coverage reviews. |
| Practice | Discussion, quiz, workshops, methods, labs, changed cases, evidence rehearsal, mock EPA, SQL, comparisons and recordings already exist. | Feed the new question bank and evaluation prompts into these tools. Retain their saved drafts and histories. |
| Visual learning | All 37 KSBs already have distinct, stable visual cues; a visual map and comparison cards exist. | Reuse these cues when displaying grouped criteria, evidence packs and evaluation exercises. |
| Technical caveats | The current guide already distinguishes joins/unions, pseudonymisation/anonymisation, dataset type/security classification, and association/causation. | Preserve those corrections when incorporating imperfect source wording. |

## 2. Content rules and source model

Create a curated public source file, proposed name **`assessment-criteria.json`**, and extend the authoring compiler to embed it in the existing curriculum. Use one shared dataset for lessons, filtering, practice and summaries. Do not fetch or interpret the large attachment dynamically in the browser.

The public assessment layer should contain:

1. **30 grading-group records:** stable group ID, member KSB IDs, source method AM1/AM2, exact overview pass text, exact overview distinction text or `null`, overview cell reference and detailed-section reference.
2. **Provider guidance records:** source-referenced evidence expectations, separately labelled “Meets expectations” and “Exceeds expectations” items where boundaries are clear. Keep uncertain items in an explicit review category rather than guessing their column.
3. **Question records:** stable ID, group, member KSBs, method, source cell, verbatim/derived label, question purpose and rubric. Distinguish source sample questions from newly authored practice.
4. **Evidence-pack records:** provider pack number, confirmed required KSBs, optional KSBs and source cells. These are course guidance, separate from the EPA assessment-method mapping.
5. **Editorial review records:** source claim, cell, issue, proposed treatment, verification status and the source used to resolve it.

Example shape, showing the separation rather than a complete implementation schema:

```json
{
  "groupId": "K14+S11",
  "members": ["K14", "S11"],
  "sourceAssessmentMethod": "AM2",
  "gradingPass": "Explains the principles of descriptive, predictive and prescriptive analytics and demonstrates how they have been applied within their own data analysis practice",
  "gradingDistinction": "Critically evaluates the risks and benefits of predictive analytics",
  "overviewCell": "Sheet1!A124",
  "detailCell": "Sheet1!A2050",
  "providerMeets": [],
  "providerExceeds": [],
  "providerUnresolved": [],
  "derivedLearning": [],
  "questions": []
}
```

Each nonempty child record must carry its own cell reference and content-kind label. Preserve exact overview wording, including punctuation, in quoted criteria. Use the detailed sections for explanation and examples. Learning copy may correct an imprecise statement, but must be labelled derived and linked to an editorial note; do not silently alter a quotation.

### Grouping and grading

- Preserve all **37 individual KSB IDs** and their learning/evidence records. Display the **30 assessment groups** as a different view, with its own denominator.
- AM1 has **13 groups / 17 KSBs**; AM2 has **17 groups / 20 KSBs**. Seven groups combine a Knowledge item with a Skill or Behaviour.
- **Eight groups** have an explicit distinction criterion: AM1 **K8+S6, K9+S7, K11+S15, S4, B4**; AM2 **K10, K14+S11, S14**.
- For the remaining **22 groups**, store distinction as `null` and display “No separate distinction criterion listed in this source.” This is not an overall grade determination.
- Provider “Exceeds expectations” guidance exists for several groups whose grading distinction is N/A. Display it as provider extension guidance, never as a newly invented EPA distinction requirement.
- One evidence item may support both members of a group, but the learner must identify what demonstrates each member. Revising K13 cannot automatically demonstrate practical S10.

## 3. Changes to the page and study flows

### Lessons and answer bank

Add one clearly labelled **Assessment and evidence** disclosure to each lesson. Show its group and source method, exact pass wording, distinction wording where supplied, and worksheet references. Keep the existing concise explanation, full guide, fictional example, visual cue and personal answer easy to reach.

Within the disclosure, use separate headings for **Source grading criteria**, **Provider evidence guidance**, and **My evidence review**. An optional provider extension should not appear as a required pass checklist. Keep personal reflections editable and quoted criteria read-only.

Update `solutions.md` first, preserving every `ksb-*` anchor and the compiler's current lesson blocks. Add the source-status note, short targeted additions from section 4 and explicit links to the grouped criteria. Update the source register to identify the new reference and its verification limits; retain the existing external reference notes and legal caveats.

### Readiness, filtering and revision

Retain the current independent recall, personal-example and evidence dimensions. Add optional filters for source method, assessment group, “has a source distinction criterion” and unresolved source issues. Keep the existing distinction between the source's mapping and the learner's confirmed assessment configuration.

Provide three separate preparation questions, drawn from `Sheet1!A663` and `A674`: **Can I explain it? Can I reference genuine evidence? Can I answer questions about it?** These are learner self-reviews, not assessor outcomes. Use a group summary to expose gaps without double-counting either shared evidence or individual KSBs.

### Questions and existing practice tools

Import the provider's sample discussion and write-up questions into one traceable bank. Route AM1 prompts to project/presentation questioning preparation and AM2 prompts to portfolio-supported professional discussion. Preserve the source's terminology alongside the applicable assessment-plan terminology; do not rename both methods “professional discussion” indiscriminately.

Use source prompts in discussion, mock EPA, answer workshops, briefings, evidence rehearsal and optional spoken-answer practice. Keep model guidance hidden until the learner requests it or finishes the mock. Open-ended source questions have no supplied machine-markable answer key: provide a self-review rubric instead of automatic correctness, pass or distinction claims.

Add derived evaluation exercises for the eight distinction groups. Reuse existing methods, changed cases and comparison cards where they fit. Label authored flashcards, quiz answers, diagrams, mind-map labels and any future slide summaries **Derived learning content**; keep them tied to the same IDs and filters. Retain the existing visual map and connections rather than adding several new global navigation destinations.

### Evidence planning and resource shelf

Add the four provider evidence-pack templates in section 6. Link them to the existing evidence notebook, course-material shelf and organisation-context notes. Display approved reference aliases and per-KSB rationales, not raw employer/patient documents.

Allow optional learner-entered review/authenticity information: responsible role, date, safe reference and feedback. Attribute employer sign-off to the provider guidance and confirm the applicable process; a study-page checkbox must not impersonate employer or assessor approval.

Resource titles without URLs stay as titles with an empty editable URL. Do not invent Multiverse/community links, submit evidence, message coaches or upload workplace material automatically.

## 4. Content changes for every grading group

These are targeted refinements to existing material. “Add” can mean an explicit prompt, example or rubric where the current explanation already covers the underlying principle. All references below are to **Sheet1**. Overview cells bind the grading row; detailed ranges support the proposed changes.

### AM1 — project preparation

| Group | Overview / detailed references | Content change | Distinction treatment |
| --- | --- | --- | --- |
| K3 + S2 | A7; A914; A942–A972 | Map each of the five lifecycle stages to an actual action, output and validation point. Explain the provider's clarification that modelling is not compulsory in this AM1 project, while substantial analysis and interpretation still are. Keep AM2 predictive evidence requirements separate. | None listed. |
| K4 | A9; A979; A1013–A1043 | Make the source-inventory prompt explicitly define all four types, classify the sources used, and explain unused types. Retain the distinction between origin/access/licensing and security classification; link to S3 without merging them. | None listed. |
| K8 + S6 | A11; A1430; A1492–A1522 | Add a quality-check log: issue/check, impact, action, escalation route, recheck and residual risk. Include the source's “no major issue found” branch: record checks actually performed and label any hypothetical escalation separately. Do not invent a resolved defect. | Evaluate the analysis outcome and alternative tools/methods for stakeholders; a list of cleaning actions alone does not cover this. |
| K9 + S7 | A13; A1529; A1557–A1585 | Extend requirements traceability to include alternatives, constraints and why the chosen plan best addresses customer needs. Connect each requirement to scope, method, output and acceptance evidence. | Explain how analysis of requirements led to an optimum solution, with realistic rejected alternatives and trade-offs. |
| K11 + S15 | A15; A1715; A1745–A1769 | Keep licensed-tool/code comparisons; add an outcome-led evaluation, available organisational options, maintenance implications and stakeholder benefits. | Evaluate outcomes and recommend beneficial alternatives, with reasons; reuse a common evaluation structure with K8+S6 and B4. |
| K12 | A17; A1774; A1882–A1906 | Add an annotated, sanitised source-to-storage-to-consumer sketch prompt. Tie real architecture to central storage/access rules, refresh, lineage and tool choices. Explain Big Data only where relevant. | None listed; architecture-improvement ideas may still be useful learning. |
| S1 | A19; A2599; A2629–A2657 | Strengthen the lifecycle control narrative: applicable policy/legislation, necessary fields, authorised environment, access, transfer, disclosure and retention checks. Define and demonstrate Privacy by Design using genuine actions. | None listed. |
| S3 | A21; A2662; A2718–A2742 | Add a classification decision record: source/type, sensitivity, organisational label, controls and approved changes. If no classification change occurred, explain when a change would be appropriate without claiming it happened. | None listed; avoid importing the source's pseudonymisation or universal low/medium/high simplifications. |
| S4 | A23; A2747; A2789–A2819 | Add a dataset/design inventory: rows, columns, grain, types, schema/relationships, structural differences and analytical adaptation. Include an optional ERD reference and outcome comparison. Do not equate different filenames with different database designs. | Demonstrate use of different structures/designs to solve a problem or improve accuracy/efficiency. Merely describing alternatives is insufficient. |
| S8 | A25; A2925; A3001–A3027 | Make the provider's concrete expectation explicit: join at least two sources using SQL/Power Query/Python/BI or a comparable robust method; document keys, join type, preparation, risks and reconciliations. A UNION-only example or basic lookup does not satisfy that provider checklist. | None listed; present the join/tool expectations as provider guidance alongside the broader grading wording. |
| S12 | A27; A3105; A3139–A3175 | Reuse the two stakeholder slots; add presentation/channel changes, feedback, constructive conflict handling, stakeholder priority and optional RACI/Power-Interest support. Explain impact on understanding or decisions. | None listed; two stakeholders is an explicit provider write-up prompt at A3161, not a new quotation of the overview criterion. |
| B3 | A29; A257; A291–A323 | Add explicit prompts for switching between independent and collaborative work, seeking guidance and the impact of one's contribution on other people. Keep attribution specific. | None listed. |
| B4 | A31; A336; A354–A388 | Make the independent reasoning chain reviewable: alternatives considered, evidence, choice, checks and conclusion. Link to the outcome/alternative-method evaluation used elsewhere. | Evaluate outcomes and alternatives benefiting stakeholders; do not award it simply for independent working. |

### AM2 — portfolio and discussion preparation

| Group | Overview / detailed references | Content change | Distinction treatment |
| --- | --- | --- | --- |
| K1 + B1 | A110; A679; A745–A821 | Keep the current UK GDPR/DPA explanation and seven principles. Separate K1's explanation of legislation from B1's actual safe, professional and productive working practices. Add provider extension prompts about improving practice and educating others. | None listed, even though the provider includes exceeds-expectations items. Verify legal currency before updating legal claims. |
| K2 | A112; A826; A862–A908 | Extend the organisation notebook with actual policy/standard names, versions, access route, daily application, role contribution and consequences/escalation. Include relevant AI policy. Flag the flattened marking boundary around A880–A886 for review. | None listed; recommendations beyond policy are provider extension guidance. |
| K5 | A114; A1049; A1143–A1191 | Add a comparison of actual dataset characteristics, examples of both structures, and an explanation of why the learner's data falls into its category. Extend optional practice with unstructured-data challenges and mitigations; retain semi-structured and mixed-field nuance. | None listed; working with unstructured data is provider extension guidance here, not a universal extra pass project. |
| K6 | A116; A1195; A1245–A1309 | Strengthen the ERD/data-flow explanation and access/maintenance narrative. Distinguish understanding implementation and maintenance from claiming database-administrator work personally performed. | None listed; improvements and richer ERDs are provider extensions. |
| K7 | A118; A1316; A1368–A1424 | Make internal data consumers visible alongside external customers. Add a principle → design choice → domain rule → user consequence explanation, linked to S5. | None listed; provider examples of best practice remain labelled extensions. |
| K10 | A120; A1592; A1656–A1710 | Add a worked benefit/risk evaluation using before/after measures, unmatched records, duplicate multiplication, security, licensing and residual risk. Explain why the selected join fits the agreed population. | Explicitly evaluate benefits and risks of combining sources, not just define keys/joins. |
| K13 + S10 | A122; A1911; A1969–A2045 | Keep descriptive/inferential teaching and EDA. Add business-context justification of statistics, alternatives, alpha and Type I/II consequences. Separate knowledge explanation from the provider's practical S10 expectations. Do not present a t-test as the only permitted inferential method. | None listed. The provider includes stronger justification prompts; these do not create an official distinction row. |
| K14 + S11 | A124; A2050; A2118–A2194 | Add an explicit chain from descriptive finding to validated prediction to feasible recommendation, with genuine examples of all three. Extend regression explanation, metric selection, coefficient interpretation and leakage/overfit/underfit review. | Critically evaluate predictive risks and benefits, including mitigation and impact. The provider additionally evaluates descriptive/prescriptive methods; label that broader extension correctly. |
| K15 | A126; A2199; A2251–A2329 | Add a framework-to-decision reflection, affected populations, bias, transparency/accountability and prioritisation of competing considerations. Include ethical consequences of statistical decision errors where relevant. Separate legal permission from ethical suitability. | None listed; framework comparison/prioritisation is provider extension guidance. |
| S5 | A128; A2824; A2868–A2920 | Add a design-decision/feedback log: audience, domain rule, layout, colour, accessibility checks, user feedback and improvements. Support claims with safe visual references where available. | None listed; feedback and usability improvements are provider extensions. |
| S9 | A130; A3032; A3060–A3100 | Connect actual tools/interfaces to architecture and authorised access. Add an optional comparison of strengths/weaknesses of at least two relevant tools or techniques. | None listed; the two-tool comparison is provider exceeds-expectations guidance. |
| S13 | A132; A3180; A3250–A3308 | Extend the existing forecast/mining worksheet with a traceable second predictive/mining example, forecasting model choice, time windows, baseline/error comparison and business recommendation. Add technically correct trend/seasonality/stationarity teaching and optional model diagnostics. | None listed. Two forecasts and error comparison are provider extension items; forecasting plus another modelling example is provider guidance. ARIMA, ADF and deployment must not become universal pass conditions. |
| S14 | A134; A3313; A3357–A3409 | Add a side-by-side comparison of two suitable visual approaches for the same question/data, including qualitative categories and numerical measures. Explain construction, insight, accessibility and stakeholder interpretation. | Compare and contrast visual approaches and how they aid understanding; require a reasoned choice, not merely two screenshots. |
| B2 | A136; A159; A199–A241 | Add a minor-change reflection with adjustment, initiative, retained productivity and quality checks. Keep the current B2/B7 visual comparison; discuss overlap without erasing the grading distinction. | None listed; proactive preparation for larger changes is provider extension guidance. |
| B5 | A138; A404; A442–A494 | Add an investigation trail from unknown cause to tested root cause, solution and prevention control. Include optional team buy-in prompts. Explain how recurrence risk was reduced and monitored rather than promise that recurrence is impossible. | None listed. |
| B6 | A140; A501; A521–A569 | Make clear that a valid challenge may be non-data-related and need not have an optimal outcome. Add resilient actions, support, lessons and changes to later practice. | None listed; future prevention is provider extension guidance. |
| B7 | A142; A574; A608–A656 | Add a before/after scope or responsibility record, revised approach, stakeholder feedback, outcome and reflection. Include organisational/role shifts as well as project changes. | None listed; improvements and reflection are provider extension guidance. |

## 5. Distinction practice priorities

Build six reusable evaluation patterns covering all eight distinction groups. Their rubrics are derived learning aids, not an automated marking scheme.

| Pattern | Groups | Candidate exercise and expected reasoning |
| --- | --- | --- |
| Evaluate an outcome and an alternative | K8+S6, K11+S15, B4 | Given an analysis outcome and stakeholder constraints, compare the current method with one feasible alternative. Explain outcome evidence, quality, cost, accessibility, maintenance and who benefits or bears risk. |
| Defend an optimum plan | K9+S7 | Compare two analysis plans against explicit customer requirements, constraints and acceptance checks; explain the compromise selected. |
| Demonstrate structural adaptation | S4 | Analyse a synthetic relational extract and nested/long-form source, explaining the structural transformations and measured accuracy/efficiency effect. Clearly label this practice, not workplace evidence. |
| Balance integration benefits and risks | K10 | Compare join choices and source inclusion; calculate exclusions or row multiplication, explain benefit, mitigation and remaining risk. |
| Critically evaluate prediction | K14+S11 | Compare a baseline and a predictive model, including unseen-data performance, leakage, uncertainty, bias, error consequences and decision constraints. Distinguish prediction from an intervention's causal effect. |
| Compare visual representations | S14 | Use the same synthetic dataset and stakeholder question to compare two defensible charts. Explain what each highlights/hides and justify the clearer choice. |

Initial derived misconceptions to add to the quiz bank: N/A does not determine an overall grade; provider “Exceeds” is not automatically distinction; reading a grouped lesson does not demonstrate its Skill; a union differs from a join; pseudonymisation retains personal-data obligations; lack of a visible trend does not prove stationarity. Each needs an authored explanation, source/review linkage and a new stable question ID.

## 6. Provider evidence packs

Use the explicit required/optional lists at **A2458–A2528**. These four on-programme evidence packs prepare the AM2 portfolio; they are not four AM1 EPA projects and not a universal official portfolio-count rule. The required lists cover the source's 20 AM2 KSBs once; optional mappings are repeated opportunities, not additional unique coverage.

| Provider pack | Focus for the page | Required KSBs | Optional KSBs | Source cells |
| --- | --- | --- | --- | --- |
| Project Evidence #1 | Data used in the role; legal, ethical and secure analysis | K1, K2, K5, K15, B1, B5 | None listed | A2462–A2476 |
| Project Evidence #2 | Visual analysis serving stakeholder needs | K7, S5, S14, B2 | K6, K10 | A2478–A2494 |
| Project Evidence #3 | Statistical analysis and combining sources | K6, K10, K13, S9, S10, B6 | None listed | A2496–A2510 |
| Project Evidence #4 | Predictive analytics and forecasting | K14, S11, S13, B7 | K13, S10 | A2512–A2528 |

Each template should guide **situation → task → personal actions → checks → result/impact → reflection → safe reference → KSB rationale → feedback/review**. Preserve existing evidence records and let a learner link one record to multiple packs/KSBs without duplicating it.

The provider describes kickoff, task, feedback, write-up, marking and reflection stages at A2334–A2414. Add that explanatory workflow. Keep the module/hackathon timing at A2416–A2456 as attributed relative guidance requiring confirmation; do not invent calendar deadlines or replace the learner's saved EPA plan. Clarify the flattened category descriptions at A2562–A2588 before introducing provider feedback statuses, and keep any coach-entered result separate from a learner self-review.

## 7. Editorial and verification queue

Resolve these issues before publishing affected derived answers. Retain the source reference and distinguish a corrected learning explanation from its original wording.

| Source cells / issue | Planned treatment |
| --- | --- |
| Overview tables versus detailed/provider text | Treat A5–A31 and A110–A142 as the supplied grading index. Preserve differences in detailed text as notes. Verify applicability separately against the current official standard and assessment plan; do not infer an overall grade algorithm. |
| A880–A886: flattened K2 marking columns | Keep uncertain column assignments unresolved. In particular, practical compliance guidance does not become optional simply because it appears after an exceeds-expectations boundary in the flattened export. Confirm with provider/source layout before assigning that category. |
| A1668 and A2961: union described alongside joins / oversimplified compatibility | Retain current correct joins-versus-row-appending explanation, compatible UNION columns/types and UNION ALL distinction. Attribute the provider's separate S8 join requirement at A3021–A3023. |
| A2692: pseudonymisation presented as a path to non-PII | Preserve the existing correction: pseudonymised data can remain personal data; aggregation or redaction also needs identification-risk review. Do not imply that making categorical counts automatically changes legal classification. |
| A2696–A2702: universal high/medium/low sensitivity | Explain these as source examples. Use the learner's actual organisational classification policy. Do not assume they are government security classification labels. |
| A1824–A1826: relational systems supposedly cannot store unstructured content and NoSQL is necessary | Explain actual capabilities, including text/JSON/binary fields and object/file storage. Choose architecture by requirements; NoSQL is not universally necessary. |
| A1125: qualitative/quantitative terms appear reversed | Flag the wording; teach categorical/textual versus numerical measurements correctly, including numeric category codes. Preserve the current distinction between data structure and measurement type. |
| A2088–A2090: prescriptive heading begins with predictive explanation | Separate prediction from action recommendation and constraints. Preserve the exact source as a reviewed issue rather than importing the misplaced paragraph as a definition. |
| A2098: binary outcome, probability and logit wording | Distinguish observed binary labels from estimated event probabilities and explain log-odds accurately. Check metric explanations against suitable statistical references. |
| A3294: stationarity equated with no trend | Explain the relevant stability assumptions; absence of an obvious trend alone is insufficient. ADF is an optional unit-root diagnostic with assumptions and limitations, not universal proof of stationarity. |
| A3220: automatic exclusion of outliers | Teach investigation and justified treatment; an extreme but valid observation may be important. Preserve the existing data-quality caveat. |
| A3232: decision trees called universally most powerful and requiring no domain knowledge/parameter setting | Remove universal superiority from derived content. Explain tuning, validation, overfitting and domain-dependent choices. |
| A2281–A2291: anonymity, unbiased survey collection and password protection | Treat as illustrative suggestions, not proof of unbiased collection, anonymisation or adequate security. Add population/access/disclosure checks and actual approved controls. |
| A2235–A2237: keys/storytelling within K15 background material | Classify as misplaced context, not new ethics requirements. Keep relevant topics under their appropriate lessons. |
| GDPR, legal obligations and framework currency | Use the existing source register as a starting point, recheck GOV.UK/ICO and applicable commencement dates, and record verification dates. Do not present EU GDPR wording alone as the complete UK position or make consent mandatory for all government work. |
| Truncated summaries, flattened deadlines/marking categories and resource titles without links | Preserve an “incomplete/needs confirmation” status; do not reconstruct missing wording, hardcode dates, invent hyperlinks or convert summaries into criteria. |

## 8. State, architecture and compatibility

Implementation must preserve `l4-fellowship.v1`, numeric schema version 1, all 37 KSB IDs, existing anchors, visual associations and established question/activity IDs.

A specific migration risk exists: the current `coverage` dictionary uses numeric target indexes from `tests/compile_curriculum.py`. Reordering or replacing targets could silently attach a saved “covered” flag to a different requirement. Prefer a new keyed assessment-review section and keep existing target meanings/indexes stable. If any old target genuinely needs semantic replacement, specify a migration that preserves the old response/review context and requests a new self-review; do not silently transfer its completion.

- Add public group/provider/question/pack metadata to the curriculum without putting personal notes in those sources. Preserve the six current source hashes and add a checksum for the curated assessment source.
- Keep legacy confidence, recall, next-review dates, personal-example confirmation, evidence links, practice/quiz drafts, recordings/review metadata and game history intact. New assessment reviews should default to empty values and remain separate from earned practice rewards.
- Implement any new personal-review or provider-feedback state through guarded reads/writes, strict validation, conflict-safe backup merge, deletion handling where applicable, and both JSON/Markdown exports.
- Record content revisions and use the existing changed-guide notice. A content update is a reason to recheck coverage, not a reason to erase saved evidence or assume new criteria are satisfied.
- An older quiz or mock must retain the question/revision it answered. New or materially changed questions need stable new/versioned IDs; do not reinterpret historical answers or replay celebrations on import/reload.
- Reuse the current grouped Practice navigation and Preparation Studio. Keep accessible disclosures, source labels, mobile controls and the existing KSB icon associations.

## 9. Implementation sequence and acceptance checks

### Phase 1 — curate and reconcile the source

Deliver the curated assessment dataset, a source-review ledger, the updated source register and validated group/pack mappings. Extract exact overview criteria first, then classify detailed evidence guidance, questions, examples and export summaries.

Acceptance: 30 groups map to exactly 37 unique KSB IDs; AM1/AM2 totals are 13/17 groups and 17/20 KSBs; eight groups have distinction text and 22 have `null`; every criterion resolves to a source cell; all four evidence packs match the required/optional lists. Uncertain source claims remain attributed and visibly unresolved until verified.

### Phase 2 — revise the answers and evidence prompts

Apply the section 4 changes to `solutions.md`; add the assessment disclosure and provider pack templates to the existing lesson/evidence flows. Keep concise explanations readable and source quotations distinguishable. Update `design.md`, project instructions and README for the final behaviour. Regenerate `curriculum.js` through the compiler.

Acceptance: all 37 lessons retain anchors, cues and answer blocks; each shows the correct group and method; source distinction appears only on the eight applicable groups; provider extensions remain separate; no learner evidence, employer facts or approval states are fabricated.

### Phase 3 — update practice and preparation views

Add the traceable question bank, source/method filters and the six evaluation patterns to existing tools. Extend source-linked terminology/comparisons where needed, including stationarity, Type I/II error consequences and legitimate classification changes. Add the independent understanding/evidence/discussion self-review prompts and group summaries.

Acceptance: all practice views resolve the same records and filters; source questions and derived questions are distinguishable; open-ended rubrics do not assign grades; mock guidance gating, saved drafts and recordings still work; practice completion leaves evidence and assessment coverage independent.

### Phase 4 — verify, release and inspect

Run authoring/structural checks, both Node suites and all eleven existing browser suites. Add focused checks for exact source text, group mapping/counts, distinction/provider separation, required/optional packs, source links, changed-review handling and legacy backup preservation. Verify an old v1 backup containing covered target indexes, personal responses, evidence, unfinished sessions and reward history; exercise merge conflicts and failed-storage recovery.

Inspect 320/390px, tablet and desktop views, keyboard/focus behaviour, print and direct-file operation. Independently reconcile any new calculations/charts and keep sample data synthetic. Record the actual browser build and any testing limitations in `tests/VERIFICATION.md`.

After cached content is final, regenerate `sw.js` with the new curated public source and paired versioned scripts. Check real offline reloads, rejection of mismatched releases, explicit updates and retained progress. Publish using the proven bounded-blob/checkpoint process, create one coherent tested release, update `main` with an expected-head lease and verify deployed hashes. Keep `.release-local/`, private attachments, personal notes and test recordings out of the public tree.

### Original planning-commit scope

Commit only this new Markdown plan. It does not change lesson text, the application, saved progress or the offline manifest. Document checks are appropriate for this commit; the runtime/compiler/browser acceptance work above applies when the plan is implemented.
