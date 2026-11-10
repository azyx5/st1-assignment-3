# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <9:30-11:30, MONDAY>
Members and responsibilities: <Shahdeen, Rashid, Jaspreet>
Stage 8 integrated SHA, command, working directory and actual result: <passed>

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity |Required session/domain state |Patient information must remain available throughout the session so the system can identify patients, retrieve their data and link them to appointments (FR-01/FR-02). |
| Appointment history | Required session/domain state| All appointments data must remain in memory during the session. This will allow the system to run properly (FR-06/FR-07, QRY-01–04).|
| Temporary menu choice | Transient state|A menu selection is needed only to determine what the user wants to do next. Once the selected action has been processed, the input is no longer needed (UI-01/UI-02). |
| Practitioner specialty | Transient state| Every practitioner's specialty is stored as part of their domain information so the system can use this data. (FR-03/FR-04).|
| Debug print output |Required session/domain state | Debug messages are only used during development to help identify problems.|
| Appointment status | Required session/domain state|The status of each appointment must remain available throughout the session so the system can identify the appointment status (FR-06/FR-07, QRY-02). |

What is intentionally lost on exit? <SmartCare is designed to operate using in-memory data only. As a result when the user closes the application, information held during that session is lost. The system does not save this information to a database. This is intentional because persistent storage (FR-10) has been retired from the current requirements. As a result, every time the application is started again, it begins with a new session and an empty data store.>

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | Appointment|tuple[datetime, str] Sorting appointments as per date and time, using appointment ID  | | |
| select_appointments | appointments | list[Appointment]| Filters and sorts matching appointments without changing the original data| |
| Service listing |practitioner_id: str, `status: AppointmentStatus |optional status | list | validates practitoner existing data  |
| Console | terminal user input | list[Appointment] | Checks if practitioner and status are valid, retrieves appointments data from the data store and returns the filtered results.| Public service interfaces|

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: <Patient, practitioner and appointment details follow the previous domain rules from Stages 6–8. All IDs should be non-blank strings with surrounding whitespace removed. Appointments must reference actual registered Patient and Practitioner objects, rather than storing detached IDs. Each appointment should use valid, minute-precision data. Its status must be an AppointmentStatus value, initially set to SCHEDULED. When booking an appointment, AppointmentService checks that both participants are registered, the appointment ID is unique and the practitioner has no conflicting scheduled appointment. These checks help maintain consistent and reliable appointment records.
>

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input |appointment should not interect directly with terminal| console.py prompts and collects input ; cancel() transitions status or raises value error |
| Service prints/reads the menu | application service layer presentation console | presentation layer run_menu() handling UI loop; services cater to logic and return to domain object |
| Query sorts its source in place | pure query mutating data structure | pure read only projections |
| Store prints Appointment saved | data store only | confirmation of data storing |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: <appointments.sort(key=appointment_sort_key): Rearranges items
result = sorted(appointments, key=appointment_sort_key): Leaves appointments untouched in its original order.>

Score-example prediction and explanation of passing the named key: <Passing key=appointment_sort_key passes the function object as a first-class callable to sorted(). For each element, Python calls appointment_sort_key(element) to extract its comparison key tuple (date_time, appointment_id)>

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: <Cancellation vs Deletion: Cancellation is a guarded status transition,Deletion would remove the record entirely
Same-session lookup:retrieves the exact same object from the store
All-status listing: returns all appointments for practitioner across any status
SCHEDULED-only exclusion: list_practitioner_appointments('D1', status=AppointmentStatus.SCHEDULED) filters out A1 because its status is CANCELLED.
>

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <actual object identity, unchanged state etc>

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
|QRY-01|appointments, practitioner_id='D1'	|select_appointments in queries.py	Returns only appointments where practitioner.practitioner_id == 'D1'. Other practitioners excluded.|
QRY-02	appointments, practitioner_id='D1', status (None / enum)	select_appointments in queries.py	If status=None, returns all statuses. If status=AppointmentStatus.X, returns only appointments with matching status.
QRY-03	appointments, practitioner_id	select_appointments via appointment_sort_key	Returns list ordered chronologically ascending by date_time; equal date_time broken by appointment_id ascending.
QRY-04	practitioner_id: str, `status: AppointmentStatus	None`	AppointmentService.list_practitioner_appointments
FP-01	appointments iterable	select_appointments in queries.py	Pure function: does not alter source iterable, source elements, or global state; produces no I/O.
FP-02	appointments iterable	select_appointments in queries.py	Returns a new list instance (res is not appointments) containing identical entity references (res[i] is appointments[j]).
FP-03	appointment: Appointment	appointment_sort_key in queries.py	Returns (appointment.date_time, appointment.appointment_id) tuple directly usable as
UI-01	Synthetic demo sequence: P1, D1, D2, A1, A2, A3	End-to-end service coordination	Registers P1, D1, D2; books A1; rejects same-time conflict for D1; books A2 for D2; cancels A1; verifies A1 retained; lists scheduled (empty) and all (A1); books A3 in freed slot; lists all (A1, A3).
UI-02	Interactive menu options 0–8, invalid inputs	run_menu in console.py	Executes all menu options, formats multi-line details, catches and displays ValueError and LookupError as Error: <msg> without crashing, recovers, exits cleanly on 0 or EOF.
FR-01–09	Full system state and operations	Domain entities, data store, and services	Preserves registration invariants, participant existence, double-booking prevention, cancellation guards, and session retention.

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <actual object identity, unchanged state >

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| | | | | |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
