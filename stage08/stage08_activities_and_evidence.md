# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [9:30-11:30, Monday]
Members and UG/PG cohorts: [Shahdeen, Rashid, Jaspreet]
Record owner / contribution links for each member: [Shahdeen, Rashid, Jaspreet]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation. 
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [- its an observable failure from user perspective, there is no concrete data.
- hypothesis: smartcare data store exposes that there is no public delete or removal method
- evidene: concrete observable fact found from test excecution
- opinion: subjective evalaution with no measurable data
- evidence: identifies where python detected and unhandled condition]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [selected behaviour: canceleldd appoointment history retention
expected behaviour: when an appointment is cancelled, the status shows AppointmentStatus.CANCELLED and the data is retrievable. 
observed behaviour: after calling cancelled appointment returns none and appointment.find_appoinment raises lookup error]
minimal reproduction: in a seperate test, create a patient, practitioner, appointment and then assert. 
initial hypothesis: filters out appointments
evidence to inspect: method body of SmartCareDataStore.find_appointment

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [
1. change the test expecting deletion
2. conflicting test]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [the method has several code smells like excessive length, duplication, collection manipulation.]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: 

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [a test failure is not always the root cause, so changing the code immediately might result into something more vulnerable and the change the expected outcome. it might cause a different issue rather then solving the actual problem.]


Classification responses (1–5, each with reason): [
1. debugging requires first reproducing failure with a minimal test
2. consulting the requirements
3. forming testable hypothesis
4. inspecting the concrete evidence.
5. making every small fix
]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [all throughout project]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [all throughout propject]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
- Baseline test command / working directory / observed result / evidence: [all tests are passing]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [one branch, all 3 members working together but one commit/push at a time each like one person modifies/changes/makes new files and works on it, pushes, then another does next activities.]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [some]
- Initial prepared full-suite command / result / key failures: [python3 -m pytest tests/test_regressions.py -q]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [same exact practitioner at same time raises a value error. So there is no double booking issues/conflicts]
- Expected behaviour and requirement: [raises value error, keeping existing booking intact, however same time and different practitioner is allowed.]
- Minimal synthetic reproduction steps: [mix and match]
- Meaningful failing test path/name and exact relevant failure: [in tests_regressions.py]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [everything runs]
- Smallest justified fix / diff / why other behaviour is preserved: [versions pushed to github]
- Repair SHA / focused verification result: [tests passed]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [cancelled appointment wouldve been returning none, fixed.]
- Expected behaviour and requirement: [cancellation is status as cancelled while data is stored and retrievable through ID, find_appointment, list-appointment()]
- Minimal synthetic reproduction steps: [check/refer to files.]
- Meaningful failing test path/name and exact relevant failure: [refer to versions pushed on github]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [filter in find_appointment]
- Smallest justified fix / diff / why other behaviour is preserved: [fixed, refer to versions pushed to github]
- Repair SHA / focused verification result: [Tests passed]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [conflicting times/attributes]
Evidence intended to inspect / competing explanation / discriminating check: [fixing conflict issues, datetime/WHEN to differentiate, practitioner/patient IDs. and appointment IDs to differentiate]
Member and saved sequence/time or commit showing this preceded consultation: [Jaspreet consulted]

### F8-02 human entry
Likely cause and why plausible: [find_appointment returning non at appointment.status cancelled. Shows cancelled appt, but returns none]
Evidence intended to inspect / competing explanation / discriminating check: [inspected find_appointment, edited data_store.py]
Member and saved sequence/time or commit showing this preceded consultation: [Shahdeen consultd]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
