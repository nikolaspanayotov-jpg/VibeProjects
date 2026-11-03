# Worked project: a fictional service-capacity briefing

This is a fully fictional teaching portfolio, built from the study desk's synthetic CSV fixtures. The service, team, approvals, review conversations and decision log are illustrative. The numerical results are reproducible from the fixtures or the explicitly separate small statistical examples. Nothing here is the learner's own workplace evidence or proof of competence.

The question is: **What can a small public-service team responsibly infer about demand, completed-case waiting time and possible capacity pressure?** A service manager needs a short decision briefing; a data engineer needs enough technical detail to check definitions and reproducibility. The work moves through the analysis lifecycle and ends with an honest account of uncertainty.

## Planning

Agree the decision, definitions and boundaries before choosing charts or models. The fictional team narrows an earlier annual-review request into a capacity briefing. It retains essential quality and handling checks rather than treating urgency as permission to bypass them.

### P01 — Requirements and scope

**Purpose.** Turn a broad request into testable analytical deliverables.

**Artefact.**

| Requirement | Decision or method | Acceptance check |
| --- | --- | --- |
| Describe the request extract | Count requests at one row per request; separate open and completed cases | Source and final distinct request counts reconcile to 300 |
| Explain completed-case waiting time | Use calendar days for this fixture; exclude open cases from completed-case duration, but report them separately | 270 completed cases and 30 open cases; check date order and unusual values |
| Describe service patterns | Join to a checked reference list without multiplying requests | Final request-level result has 300 rows; unmatched/missing keys remain visible |
| Investigate a possible difference in completion times | Use a separately constructed independent two-group example, not the 300-request extract | State the sample, test, hypotheses, effect, interval and limitations |
| Provide a short demand outlook | Use the separate 12-month teaching series; train on January–September and evaluate October–December | Report time windows, model, naive baseline, holdout error and projections |
| Add qualitative context | Code the 36 synthetic comments; allow several themes per comment | Document coding rules and the denominator; do not claim representative satisfaction |
| Support a decision | Compare feasible responses to demand against an explicitly assumed capacity of 150 per month | Recommendation is conditional, with an owner role and a review plan |

**Scope exclusions:** no citizen-level prediction, no causal claim about staffing, no claim that feedback is representative, and no conversion of synthetic study work into personal evidence.

**Example engagement plan:** the service manager has high interest in the decision and the data engineer in reliable extraction and definitions. Affected service users must still be considered even if they have little organisational power. The fictional analyst owns preparation and explanation, while source authority and operational decisions remain with the relevant roles.

**KSB mapping.**

| KSB | Why this artefact is useful for study |
| --- | --- |
| K3 | Connects planning to preparation, analysis, validation and communication |
| K9 | Turns stakeholder needs into definitions, scope and acceptance checks |
| S2 | Shows a lifecycle chain with traceable outputs; actual personal execution is still needed |
| S7 | Maps each requirement to a method and a deliverable check |
| B3 | Distinguishes independent analytical ownership from collaboration and decisions owned by others |
| B7 | Records a broader shift from annual review to capacity briefing |

## Preparation

Understand source structures, decide handling and investigate joins before interpreting any pattern. The CSVs are completely synthetic, so the handling record below illustrates questions and controls rather than asserting a real organisation's rules.

### P02 — Source, handling and architecture note

**Purpose.** Explain what the sources mean and how an authorised workflow would be selected.

**Artefact.**

| Source | Shape | Grain and caveat |
| --- | --- | --- |
| service_requests.csv | 300 rows × 5 columns | One request per row; identifiers, dates and channel; some missing keys and open cases |
| service_lookup.csv | 6 rows × 2 columns | Intended as one service per row, but S2 appears twice with conflicting labels |
| monthly_requests.csv | 12 rows × 2 columns | A separately constructed monthly series for 2025, not an aggregation of the request extract |
| feedback.csv | 36 rows × 3 columns | One comment per row; free-text meaning requires interpretation |
| Approved lookup for this example | 5 rows × 2 columns | A fictional source-owner decision chooses the canonical labels Service 1 through Service 5 |

**Architecture sketch:** operational source → controlled preparation → checked reference data → analytical outputs → authorised recipients. A real employer's architecture, permissions, storage, retention, lawful basis and policies must be confirmed separately.

**Example handling decisions:** collect only necessary fields; use approved access and workspace; restrict working copies and recipients; record source and transformation lineage; check disclosure before sharing; document retention and deletion arrangements. Pseudonymisation and aggregation would require residual-risk assessment with real data. The fictional analyst queries data, and does not claim to administer database security or backups.

**Tool decision:** compare a repeated manual lookup with a reproducible SQL join, and compare manual calculations with a recorded analysis workflow. This example uses SQL and documented calculations for repeatability; an actual choice must fit the available infrastructure, skills, support, security, accessibility and cost. A warehouse, a lake and a relational database are different architectural choices; none is assumed to exist at the learner's employer.

**Ethical check:** operational origin does not imply public reuse rights. Synthetic comments make no claim about a real population. A future analysis of real feedback would need to examine missing groups, collection bias, consent where relevant, accountability and an appropriate ethics framework.

**KSB mapping.**

| KSB | Why this artefact is useful for study |
| --- | --- |
| K1 | Connects legal questions to purpose, access, minimisation, disclosure and retention |
| K2 | Shows where actual organisational data, security and AI rules must shape the workflow |
| K4 | Separates administrative origin, public availability, research purpose and open reuse rights |
| K5 | Distinguishes structured fields from unstructured feedback meaning |
| K6 | Explains grain, keys, reference design, pipelines and system responsibilities |
| K11 | Compares realistic tools and methods against requirements |
| K12 | Explains a source-to-consumer architecture and its constraints |
| K15 | Identifies fairness, collection bias, transparency and accountability questions |
| S1 | Illustrates a lifecycle of handling controls; genuine performed compliance must be evidenced separately |
| S3 | Applies sensitivity and confidentiality reasoning without inventing universal security labels |
| S4 | Adapts the approach to request, lookup, monthly and free-text structures |
| S9 | Links tools and interfaces to architecture and permissions |
| S15 | Justifies the repeatable workflow that is applied in P03–P05 |
| B1 | Connects everyday access, sharing and working habits to protection |

### P03 — Quality log and reproducible join

**Purpose.** Establish the request grain, explain an inflated count and preserve unresolved issues.

**Artefact.**

| Check | Reproducible result | Interpretation and treatment |
| --- | --- | --- |
| Requests before combination | 300 | Baseline request count |
| Lookup uniqueness | S2 has two rows | A left join can multiply records; investigate source authority |
| Rows after joining flawed lookup | 357 | 57 S2 requests each match twice, creating 57 extra rows |
| Missing request service ID | 4 | Different from a known non-null key with no reference match |
| Non-null service ID without match | 8 records with S99 | Retain and report as unmatched; do not hide them with an inner join |
| Missing completion date | 30 | Open cases in this fixture; not zero-day completed cases |
| Unusual completed duration | Six cases of 80 days | Investigate in real work; retain the deliberately planted observations in this teaching result |
| Rows after approved lookup | 300 | Restores the intended request grain without concealing missing/unmatched service keys |

The following SQL uses table names matching the downloaded CSVs after import. CSV blanks should be checked alongside NULL; the example explicitly handles both where needed. Adapt import and date syntax to the approved database.

```sql
-- Diagnose the reference-key problem.
SELECT service_id, COUNT(*) AS rows_per_key
FROM service_lookup
GROUP BY service_id
HAVING COUNT(*) > 1;

-- Reproduce the flawed-join count: 357.
SELECT COUNT(*) AS joined_rows
FROM service_requests AS r
LEFT JOIN service_lookup AS s ON r.service_id = s.service_id;

-- Apply the explicitly approved five-row lookup for this fictional case.
-- approved_service_lookup contains S1...S5 with canonical labels.
SELECT r.request_id, r.service_id, s.service_name,
       r.received_date, r.completed_date, r.channel
FROM service_requests AS r
LEFT JOIN approved_service_lookup AS s ON r.service_id = s.service_id;

-- Preserve and quantify missing and unmatched keys separately.
SELECT
  SUM(CASE WHEN NULLIF(r.service_id, '') IS NULL THEN 1 ELSE 0 END)
    AS missing_service_keys,
  SUM(CASE WHEN NULLIF(r.service_id, '') IS NOT NULL
            AND s.service_id IS NULL THEN 1 ELSE 0 END)
    AS unmatched_nonnull_keys
FROM service_requests AS r
LEFT JOIN approved_service_lookup AS s ON r.service_id = s.service_id;
```

**Decision log:** the duplicate label is not resolved by silently taking the first row or using DISTINCT. In this fictional case the source-owner role confirms the five canonical labels. A real analyst must obtain an authoritative rule. Retain the 12 unresolved service keys and their limits on service-level interpretation.

**KSB mapping.**

| KSB | Why this artefact is useful for study |
| --- | --- |
| K8 | Names quality dimensions, measures issue scale and explains decision impact |
| K10 | Explains keys, grain, left-join cardinality and the benefit of a checked lookup |
| S6 | Demonstrates detection, investigation, treatment and validation in a synthetic task |
| S8 | Shows a repeatable multi-source join with missing/unmatched-key checks |
| B4 | Traces ordered checks from source count to cardinality and reference uniqueness |
| B5 | Distinguishes inflated totals, duplicate-key mechanism and a missing uniqueness control |

## Analysis

Keep descriptive summaries, statistical inference, predictive evaluation and recommendations distinct. The dashboard uses the 300-request fixture. The independent t-test sample and monthly series are separate constructed datasets and must not be represented as estimates derived from that extract.

### P04 — Descriptive and inferential analysis note

**Purpose.** Explain centre, spread and uncertainty without overstating a small example.

**Artefact.**

The request fixture has **300 requests**, **270 completed cases** and **30 open cases**. Completed-case median duration is **8 calendar days** and mean duration is **9.1444 calendar days**. Six completed cases have a deliberately planted 80-day duration. Open cases are reported separately, and the mean should not conceal the distribution.

For an independent calculation exercise, use process A values `[8, 9, 10, 11, 12]` and process B values `[6, 7, 8, 9, 10]`, in days. The hypotheses are equal population means versus a two-sided difference, with alpha 0.05. Welch's test gives **t = 2**, **p ≈ 0.08052**, a mean difference of **2 days** and a 95% interval of approximately **−0.306 to 4.306 days**.

The example does not reject the null at 0.05, and does not establish equality. Independence, distribution, collection design and practical importance still need assessment. Five neat values per group are not sufficient evidence of representativeness. The p-value is not the probability that the null is true.

**KSB mapping.**

| KSB | Why this artefact is useful for study |
| --- | --- |
| K13 | Explains descriptive measures, hypotheses, significance, p-values and uncertainty |
| S10 | Provides EDA checks and an independently reproducible inferential calculation with limitations |

### P05 — Forecast, pattern mining and conditional recommendation

**Purpose.** Evaluate a forecast, identify a separate pattern and explain what action the evidence could support.

**Artefact.**

Monthly requests are `[116, 120, 121, 125, 128, 131, 133, 138, 140, 144, 149, 151]` for January–December 2025. Train a time-trend regression on January–September, setting January to `t = 1`. The fitted candidate is **113 + 3t**.

| Holdout month | Actual | Fixed trend forecast | Naive baseline |
| --- | --- | --- | --- |
| October | 144 | 143 | 140 |
| November | 149 | 146 | 140 |
| December | 151 | 149 | 140 |

Holdout RMSE is **2.160** requests for the trend candidate and **8.524** for the naive baseline. The same frozen model projects **152, 155 and 158** for January–March 2026. These are example projections from that training cutoff, not a current operational forecast. The short series does not establish annual seasonality or calibrated uncertainty intervals. A real deployment needs more evaluation, any refit documented, appropriate uncertainty estimates and monitoring for structural change.

**Separate pattern-mining example:** code the 36 comments into themes. Waiting is mentioned in 12 comments, helpful response in 12, and both in six. Co-occurrence support is **6/36 = 16.7%**; among waiting comments, **6/12 = 50%** also mention helpfulness. These planted patterns illustrate mining and interpretation, not a representative relationship or a causal effect. Explain coding and validation rather than reporting a pattern alone.

**Conditional recommendation:** if the fictional service can process 150 requests per month, compare flexible capacity or scheduling responses with the projected pressure, costs and uncertainty. The manager owns the operational choice. This example does not claim a staffing benefit has been implemented or proved.

**KSB mapping.**

| KSB | Why this artefact is useful for study |
| --- | --- |
| K14 | Connects descriptive, predictive and prescriptive questions without merging their claims |
| S11 | Defines a target, compares a baseline and links evaluation to a constrained recommendation |
| S13 | Shows time windows, visual/table values, metric, trend/seasonality limits, projections and a separate mining example |

## Validation

Test the whole argument, including the connection between outputs and the original requirements. A clean-looking output is not sufficient if its grain, sample or conclusions are wrong.

### P06 — Validation and root-cause review

**Purpose.** Show how the fictional analyst checked results and planned to prevent recurrence.

**Artefact.**

| Validation | Expected check and limitation |
| --- | --- |
| Request grain | 300 source requests and 300 final rows after approved lookup; no duplicated request identifiers |
| Missing/unmatched services | Four missing and eight non-null unmatched keys remain separately documented |
| Duration population | 270 completed cases and 30 open; no zero replacement for open-case duration |
| Forecast evaluation | October–December observations are not used to fit the reported candidate; both metrics use the same holdout |
| Claim boundaries | No causal staffing claim, representative-satisfaction claim or personal-competence claim |
| Acceptance criteria | Each P01 requirement links to an output and a recorded caveat |

**Root-cause chain:** inflated total → several matches for S2 → conflicting lookup records → missing reference-uniqueness validation in the fictional loading process. The corrective plan is an authoritative reference list plus a uniqueness gate, exception report and owner role. Later loads must be checked before claiming the prevention control works.

**KSB mapping.**

| KSB | Why this artefact is useful for study |
| --- | --- |
| K8 | Evaluates remaining quality risk against intended use |
| S6 | Rechecks the effect of the correction and retains limitations |
| B4 | Tests alternative explanations and reconciles outcomes |
| B5 | Connects a proven immediate mechanism to a prevention plan, without claiming future success |

## Communication

Use the same evidence with different levels of detail for the two fictional audiences. The page's illustrative dashboard provides numerical and qualitative views, exact values and explanatory alternatives.

### P07 — Annotated dashboard and two stakeholder briefings

**Purpose.** Explain a decision clearly while preserving technical and ethical limits.

**Artefact.**

The quantitative view reports 300 requests, 270 completed and 30 open, with median completed duration of eight calendar days. Service counts after the approved lookup are **59, 57, 57, 58 and 57** for Services 1–5, with **12 missing/unmatched**. These sum to 300. The artificial fixture is not representative of a real service; apparent service differences must not be interpreted as causal performance rankings.

The qualitative view codes **36** comments into **42 theme assignments**: clear instructions **6**, long wait **12**, progress update needed **6**, helpful response **12**, unclear instructions **6**. Six comments carry both waiting and helpfulness themes. Counts can exceed the number of comments, and the convenience sample does not measure population satisfaction.

**Briefing for the fictional service manager:** the verified extract count is 300; quality correction prevents 57 duplicate joined rows. The short demand example suggests a possible capacity question under a 150-request assumption, but it is not a reliable operational forecast without further evaluation. Choose whether to commission better data and a bounded capacity review.

**Walkthrough for the fictional data engineer:** inspect source grain, lookup authority, four missing keys, eight S99 matches, SQL, timing of transformations and the proposed uniqueness gate. Check refresh behaviour and exception ownership before using the workflow operationally.

**Illustrative feedback and revision:** the manager asks for clearer open-case labelling; the engineer asks that missing keys and unmatched non-null keys remain separate. The fictional analyst adds those distinctions. These are invented review events to demonstrate the structure of a good account, not feedback about the learner.

**Design rationale:** give the key decision and caveats prominence; label units and population; distinguish actuals and forecasts by labels/line style; provide exact tables; avoid colour-only meaning. Domain definitions determine calculations, not just wording.

**KSB mapping.**

| KSB | Why this artefact is useful for study |
| --- | --- |
| K7 | Links domain definitions and user tasks to design |
| S5 | Explains hierarchy, labels, accessibility and illustrative evaluation |
| S12 | Contrasts two stakeholders, adapted channels/detail and specific fictional revisions |
| S14 | Collates, interprets and displays quantitative measures and qualitative themes |

## Reflection

Separate small unexpected operational issues, wider changes in direction and lessons from an inconclusive result. A real Behaviour account needs the learner's actual actions and outcomes, not adoption of this fictional history.

### P08 — Decisions, changes and lessons

**Purpose.** Show how an account can connect context, judgement, collaboration and learning.

**Artefact.**

| Fictional event | Decision and rationale | Result or limit to report |
| --- | --- | --- |
| Earlier annual review becomes a capacity briefing | Agree a narrower scope and retain quality/handling checks; tell stakeholders what is excluded | Revised brief in P01; no unsupported annual-performance claim |
| A nonessential feedback field is unavailable | Continue a limited thematic account and state the omission; do not invent values or expand access | A minor adjustment within the analyst's remit; review if the missing field becomes essential |
| Joined count rises from 300 to 357 | Investigate keys and grain before interpreting demand | Approved lookup returns 300; exceptions are retained |
| Statistical exercise is inconclusive | Report the interval and sample limitations instead of forcing a positive finding | No population-difference claim; plan better evidence |
| Manager and engineer need different detail | Prepare separate briefing and technical walkthrough; respond to each review question | Clearer population labels and more explicit key-quality checks |
| Future refresh may recreate the problem | Propose a uniqueness gate and exception owner | Prevention is a plan until checked on later loads |

**Example lesson:** an inconclusive test is not an analytical failure to hide. It can expose a need for better sampling, clearer decisions or a more suitable method. A real reflection should identify a subsequent change in practice and evidence it where available.

**KSB mapping.**

| KSB | Why this artefact is useful for study |
| --- | --- |
| B2 | Separates a minor unavailable-field adjustment, initiative and remit |
| B3 | Identifies independent work, collaboration and effects on other roles |
| B6 | Shows a constructive response and specific learning from an inconclusive result |
| B7 | Explains the broader scope shift and management of expectations |

## Applying this example to your own work

Use the artefacts to understand the reasoning and the shape of an account. Then open the relevant KSB and write a genuine example: situation, task, your actions, justification, validation, result and learning. Keep evidence in its approved location and explain why it supports that particular KSB. Visiting this project or downloading its portfolio never marks a personal example or evidence complete.
