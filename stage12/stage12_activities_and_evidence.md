# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: [Monday 9.30-11.30]
Members and UG/PG applicability: [Rashid, Jaspreet, Shahdeem]


## A Release scope and starting SHA

Release label/version and requirements baseline: [SmartCare Assessment 3, all business rules, query rules,fp rules, ui rules implemented]
Common starting SHA / branch / applicable members: [Rashid, Jaspreet, Shahdeen]
PG starting SHA / branch / applicable members or not applicable: [N/A]
Working-state review and approved integration: [response]
Protected common candidate and PG differences: [response]
Feature freeze / owner / verifier: [Rashid, Jaspreet, Shahdeen]


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: [all tests passed]

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | [store.find_appointment and appointments.find_appointment return the cancelled instance with status == CANCELLED; scheduled slot freed; all-status query lists record.] | [in code] | [Jaspreet] | [yes] | [none] |
| Architecture responsibilities are appropriate | [Entities (domain.py) own invariants; repository (data_store.py) manages session collections; services (services.py) orchestrate workflows; queries (queries.py) are pure projections; console (console.py) owns UI.] | [incode] | [Shahdeen] | [yes] | [none] |
| Rescheduling is safe — PG only | [response] | [response] | [response] | [response] | [response] |
| AI use is responsible — common recheck / PG assurance | [Copilot suggestions audited; speculative persistence proposals (SQLite/files) rejected; pure query refactor verified against contracts.] | [responsibly used, like copilot sections insome md files] | [Shahdeen, Jaspreet, Rashid] | [yes] | [none] |
| System is maintainable | [all throughout, and tests pass] | [project] | [Everonereviewed] | [yes] | [none] |
| FR-01–03 register/find and validation | [non-blank IDs] | [tests/test_domain.py and test_regressions.py] | [Rashid, Jaspreet] | [yes] | [yes, but fixed] |
| FR-04–05 booking/conflict rules | [conflicts rejected] | [test_services.py, test_regressions.py] | [Jaspreet, Shahdeen] | [yes] | [none] |
| FR-06–08 cancellation/history/find | [secure cancellation transition] | [test_services.py, test_domain.py] | [Shahdeen and Jaspreet] | [yes] | [none] |
| FR-09 and QRY/FP listing/filter/order/purity | [status filtering, tie breaking, non mutating pure queries] | [test_queries.py, test_workflows.py] | [Jaspreet] | [yes] | [none] |
| UI full console sequence and error recovery | [menu options] | [test_workflows.py] | [Shahdeen] | [yes] | [none] |
| Session-only scope / FR-10 retired | [in session memrory] | [project] | [Whole team] | [yes] | [none] |
| PG RES and assurance integration | [response] | [response] | [response] | [response] | [response] |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | [Python 3.14.3 / macOS / pytest-8.3.5] | [/project: python -m pytest -v] | [response] | [170 passed in 0.17s] | [project/tests/] |
| Complete PG if applicable | [N/A] | [response] | [response] | [response] | [response] |
| Affected focused checks after correction | [Python 3.14.3 / macOS / pytest-8.3.5] | [project] | [passed] | [test_regressions.py] | [tests/test_workflows.py, tests/test_queries.py] |
| Full integrated recheck | [Python 3.14.3 / macOS / pytest-8.3.5] | [/project: python -m pytest -q] | [response] | [170 tests passed in 0.12 seconds] | [python -m pytest -v] |
Prior assertions preserved / reviewed test diff: [all test passed]
Remaining failure / limitation: [0 test failures]


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | [Outpatient healthcare clinic coordinator needs a simple system] | [Clinic coordinator requires easy handling and editition of the data] | [all requirements mentioned properly] | [all throughout] |
| Register and find Patient and two Practitioners | [multiple options] | [valid enttities registered and retrievable] | [same as expectation] | [test_workflows.py ] |
| Valid booking | [available] | [status Scheduled, linked to actual Patient and Practitioner] | [Appointment booked successfully.] | [console.py#run_menu] |
| Same practitioner exact-time conflict rejected | [available] | [double booking rejection] | [Error: Practitioner already has a SCHEDULED appointment at this time. No partial record stored.] | [test_workflows.py] |
| Different practitioner same time allowed | [available] | [same patient booked 2 practitioners] | [Appointment booked successfully] | [test_workflows.py] |
| Cancel SCHEDULED and retain/find CANCELLED object | [available] | [status cancellation successful] | [Appointment cancelled successfully] | [console.py] |
| Invalid/repeated cancellation rejected | [Programmatic & service verification: cancel A1 again] | [cancelled appointment cannot be cancelled] | [ValueError('Appointment already cancelled') raised] | [test_services.py::test_repeated_cancellation_rejected_without_change] |
| Default all-status listing | [option available] | [returns all appointments] | [Displays A1 with status Cancelled] | [test_workflows.py] |
| Explicit filtering / empty vs unknown / deterministic order | [multiple options available] | [filters out when there is no appointment] | [empty list handled cleanly] | [test_workflows.py] |
| Invalid date/status/menu/lookup recovery and continued operation | [option available] | [catches errors when there is an error] | [Error: Use date/time format YYYY-MM-DD HH:MM] | [test_workflows.py] |
| Session-only limitation and normal exit | [exit] | [clean terminal] | [Goodbye. Session data discarded.] | [console.py] |
| One meaningful requirement-linked pytest test explained | [n/a] | [response] | [response] | [response] |
| Architecture and one actual AI decision / known limitation | [Explain decoupling of pure queries from stateful repository; explain rejection of SQLite caching; state session-only scope] | [Separation of concerns: queries are pure functions; services coordinate store snapshots; presentation is headless; persistence rejected.] | [Architecture diagrams and Copilot audit log presented clearly to marker.] | [stage09/stage09_activities_and_evidence.md Section E] |
| PG reschedule identity/participants/time and no-op | [response] | [response] | [response] | [response] |
| PG conflict/invalid status/failure non-mutation | [response] | [response] | [response] | [response] |
| PG old slot / current lookup/list ordering / assurance risks | [response] | [response] | [response] | [response] |
Stable demo owner / fresh process / command: [Rashid]
PG demonstrations through service/tests or not applicable: [response]


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | [domain.py, data_store.py, services.py, queries.py, console.py] | [No finding] | [No change needed.] |
| PascalCase and snake_case naming | [All files in project/smartcare/ and project/tests/] | [No finding.] | [no change needed] |
| Useful type hints and meaningful docstrings | [All module headers, classes, and public methods] | [no finding] | [none] |
| Four-space indentation and imports/layout | [All Python source and test files] | [no finding ] | [no change needed] |
| Focused methods / duplication / dead or commented code | [console.py, test_queries.py, test_workflows.py] | [no finding] | [refactored] |
| Globals / leakage / unnecessary inheritance or frameworks | [project smartcare] | [no finding] | [no change needed] |
| No SQLite/persistence/repository ABCs/speculative features | [Entire project/ directory] | [no finding] | [erified by codebase] |
| Synthetic data / secrets / dependencies / provenance | [entire repository] | [no finding] | [verified by audit] |
| Significant common Copilot contributions and human verification | [project/smartcare/queries.py, services.py, console.py] | [Finding] | [REJECTED and MODIFIED by human.] |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | [response] | [response] | [response] |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] |
Access route or approved equivalent / limitations: [response]
Available AI evidence and missing evidence honestly disclosed: [response]


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | [README.md, project/README.md] | [Shahdeen] | [Verified] |
| Out-of-scope capabilities and known limitations | [project/README.md] | [Rashid] | [Verified] |
| Confirmed teaching Python version and dependency installation | [project/README.md] | [jaspreet] | [Verified] |
| Working directory / demo / interactive / test commands | [project/README.md] | [Shahdeen] | [Verified] |
| Repository structure and architecture responsibilities | [project/README.md] | [Jaspreet] | [Verified] |
| Responsible AI summary / synthetic-data rule | [README.md, project/README.md] | [Rashid] | [Verified] |
| Release label/version and SHA links | [README.md] | [Shahdeen] | [Verified] |
Root README index and project/README verified: [Both README files inspected and confirmed]
Fresh clone or extracted ZIP / candidate identity: [Source archive generated via git archive]
Verifier and clean environment / actual version: [ndependent verifier using macOS with clean Python 3.14.3 virtual environment]
Setup/run/test commands and observed results: [all passed]
Missing local file or setup gap / remedy and recheck: [N/A]


## G Known limitations debt and release notes

Delivered features: [All features present in codebase.]
Important fixes: [Correct practitioner schedule conflict, return cancelled appointments, etc.]
Architecture/quality improvements: [Pure query projections, clear boundary.]
Known limitations: [Session only storage.]
AI-assisted development note: [For some test errors and inline code readability suggestions.]

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| [in memory storage] | [Data lost in termination] | [High] | [Implement database] | [Accepted] |
Session-only synthetic data and minute-precision local time: [Fully tested and meets all acceptance criteria.]
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: [Out of scope.]
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: [Architectural debt]
Difference between accepted scope limit and unresolved required behaviour: [Accepted scope]
PG assurance residual risks / owner / status or not applicable: [response]


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| [Code based quality] | [full audit] | [Low] | [Rashid, Jaspreet, Shahdeen] | [No defect found] | [python3 -m pytest -q/-v] | [None] |
Justified no-change conclusion if no defect found: [All functions requirements operate well.]
Release blockers still open / status: [0]


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: [response]
Independent reviewer / feedback / response: [Jaspreet]
Integration commit / full recheck: [Rashid, Jaspreet, Shahdeen]
Tracked and untracked file inspection / cleanliness: [Verified]
Secrets/staff material/caches/tool-metadata exclusion check: [Verified]
Candidate recovery plan / known-good SHA: [response]
Named substantive contributions: [Rashid, Jaspreet, Shahdeen]


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [Ready for release]
Approver / date / rationale and evidence: [Rashid, 10/11/2026, All requirments satisfied]
What risks remain / conditions / owners: [Storage across restarts, Rashid]
Can the team explain the system: [Yes]
Can a change be recovered: [Yes]
Common decision / PG decision where different: [N/A]


## K Final tested release SHA

Exact common tested SHA: [response]
Exact PG tested SHA or not applicable: [response]
Final submitted SHA / repository URL: [https://github.com/azyx5/st1-assignment-3]
Evidence-only later commit and difference explanation: [response]
Executable changes after testing and re-verification: [response]
Source ZIP name / SHA correspondence / extracted comparison: [Extracted]


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [Canvas]
Deadline/timezone: [10/11/2026 (We got an extension)]
Repository access arrangement: [Shared github repository]
Mixed-candidate upload arrangement: [N/A]
Oral/video recording/accessibility arrangements: [Canvas, Cadmus]
Remaining administration or release dependency: [None]


## M Formative questions

1. What is a release candidate? [response]

2. What is feature freeze and why is it used? [response]

3. What is regression testing in a release context? [response]

4. What is a known limitation? [response]

5. What is technical debt? [response]

6. What are release notes? [response]

7. What is software maintenance? [response]

8. What is the purpose of the individual demonstration/viva? [response]

9. What should the final responsible-AI check establish before release? [response]

10. What is the main course conclusion about AI and the role of the software engineer? [response]


## N Reflection viva and handover

Strongest evidence SmartCare is ready: [response]
Weakest area: [response]
How AI use changed from Stage 1 to Stage 12: [response]
Start doing — engineering and AI use: [response]
Stop doing — engineering and AI use: [response]
Continue doing — engineering and AI use: [response]
What worked / caused rework / future delivery improvement: [response]
One paragraph — If AI can write code why do we still need software engineers: [response]

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | [response] |
| Two requirements and acceptance criteria | [response] |
| Domain model and architecture | [response] |
| Design trade-off | [response] |
| Meaningful test and its limits / 100 percent coverage | [response] |
| Diagnosed defect and verification | [response] |
| Shared store and session-state/query responsibilities | [response] |
| What would break if session-state lookup/query responsibilities changed? | [response] |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | [response] |
| FR-07 retained history test | [response] |
| Actual AI change rejected/modified or honestly accepted with verification | [response] |
| Unresolved limitation / future production work | [response] |
| Personal implementation contribution | [response] |
| Personal test/review/design/integration contribution | [response] |
| PG agentic change and rescheduling verification | [response] |
| PG responsible-AI risk/remediation or supported no finding | [response] |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: [response]
No further coding stage. Later corrections use the published assessment process.
