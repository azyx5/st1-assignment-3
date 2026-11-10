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
QRY-01 / FP-01	project/smartcare/queries.py#select_appointments	Filter to D1: 3 of 4 sample appointments match D1, 1 matches D2; asserts all returned have practitioner_id == 'D1'.	PASSED	test_queries.py::test_select_appointments_filters_to_requested_practitioner
QRY-01	project/smartcare/queries.py#select_appointments	Query for unregistered practitioner 'D999' against fixture list; asserts returns empty list [].	PASSED	test_queries.py::test_select_appointments_unmatched_practitioner_returns_empty_list
QRY-02	project/smartcare/queries.py#select_appointments	Status filter default None: returns 3 appointments for D1 across SCHEDULED, CANCELLED, and COMPLETED.	PASSED	test_queries.py::test_select_appointments_default_status_none_includes_all
QRY-02	project/smartcare/queries.py#select_appointments	Explicit status filter: verifies filtering by SCHEDULED, CANCELLED, and COMPLETED returns exactly the matching subset.	PASSED	test_queries.py::test_select_appointments_explicit_status_filtering
QRY-03 / FP-03	project/smartcare/queries.py#appointment_sort_key	Asserts sorting orders ascending by date_time, and equal date_time (T1) orders by appointment_id ('A1' before 'A2').	PASSED	test_queries.py::test_select_appointments_orders_by_datetime_and_id_tiebreak
FP-01	project/smartcare/queries.py#select_appointments	Purity and non-mutation: verifies source list ordering and contained objects are identical before and after query execution.	PASSED	test_queries.py::test_select_appointments_pure_and_non_mutating
FP-02	project/smartcare/queries.py#select_appointments	Container allocation and identity: result is not appointments while result[0] is appointments[0].	PASSED	test_queries.py::test_select_appointments_returns_new_container_preserving_object_identity
QRY-04	project/smartcare/services.py#AppointmentService.list_practitioner_appointments	Unknown practitioner 'D999' raises LookupError('Practitioner not found').	PASSED	test_workflows.py::test_list_practitioner_appointments_unknown_practitioner_raises_lookup
QRY-04	project/smartcare/services.py#AppointmentService.list_practitioner_appointments	Blank practitioner ID '' or ' ' raises ValueError('Practitioner ID cannot be blank').	PASSED	test_workflows.py::test_list_practitioner_appointments_blank_practitioner_raises_value_error
QRY-04	project/smartcare/services.py#AppointmentService.list_practitioner_appointments	Invalid status argument (e.g. string 'scheduled' or int) raises ValueError('Invalid appointment status').	PASSED	test_workflows.py::test_list_practitioner_appointments_invalid_status_raises_value_error
QRY-04	project/smartcare/services.py#AppointmentService.list_practitioner_appointments	Service returns new list defensively: mutating caller's result list does not affect subsequent queries.	PASSED	test_workflows.py::test_list_practitioner_appointments_returns_new_list_defensively

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- project/smartcare/queries.py:appointment_sort_key(appointment) reads strictly the public fields ; select_appointments(appointments, practitioner_id, status=None) operates exclusively on arguments passed to it -->
What the tests do and do not establish: <!-- tests show that sorting and filtering is done correctly. And the tests cannot guarantee that other code will never change appointment data after retrieving it. -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow |Register P1, D1, D2; Book A1 (D1 at T1); Conflict A-CONFLICT (D1 at T1); Book A2 (D2 at T1); Cancel A1; Find A1; List D1 all; List D1 scheduled; Book A3 (D1 at T1); List D1 all; Exit 0 |follows transcript,cancelled record and detained, clean exit |output matches expected demonstration output | test_workflows.py::test_ui01_end_to_end_booking_cancellation_and_history_workflow, test_workflows.py::test_ui02_console_interactive_full_demonstration|
| UI-02 invalid-input recovery | Duplicate patient P1; Invalid booking date format; Find unknown appointment UNKNOWN; List with invalid status filter pending; Unknown menu choice 99; Exit 0.| prints Error: Patient ID already exists, Error: Use date/time format YYYY-MM-DD HH:MM, Error: Appointment not found, Error: Status must be scheduled, cancelled or completed, Unknown choice. Choose a number from 0 to 8.; menu re-prompts after every error.| expected Error: <msg> lines; menu loop remained fully operational| test_workflows.py::test_ui02_console_handles_input_exceptions_gracefully|
| Automated service workflow | PatientService, PractitionerService, AppointmentService.|can run properly without terminal  |Services return objects, handle errors, and manage session data. | test_workflows.py::test_ui01_end_to_end_booking_cancellation_and_history_workflow |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.
Before booking conflict: Practitioner D1 has 1 appointment A1 at 2026-10-01 09:00 (SCHEDULED).
Conflict attempt: Booking A-CONFLICT for D1 at the same time raises ValueError('Practitioner already has a SCHEDULED appointment at this time').
State check: len(store.list_appointments()) == 1; A-CONFLICT is discarded and never entered into the store.
Different practitioner: Booking A2 for Jordan Example (D2) at the exact same timestamp 2026-10-01 09:00 succeeds; len(store.list_appointments()) == 2.
Cancellation: Cancelling A1 transitions its status to AppointmentStatus.CANCELLED.
History retention check: store.find_appointment('A1') returns the same object; appointments.find_appointment('A1') displays multi-line status Cancelled.
Filter check: Option 8 for D1 with status scheduled displays No appointments found.; option 8 with all statuses displays A1 with status Cancelled.
Slot re-booking: Booking A3 for D1 at 2026-10-01 09:00 succeeds because the slot is now free of scheduled appointments.
Subsequent query: Listing D1 for all statuses returns both A1 and A3 ordered deterministically by (date_time, appointment_id) -> [A1, A3].


## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- section A and B -->
Actual prompt/context supplied: <!--  reviewqueries.py and services.py , verify whether selected appointments is pure, whether sorting key handles tiebreking and what improvements can be made -->
Actual response: <!-- confirmed select_appointments is pure and uses sorted() and suggested SQ lite -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| Add database for queries|Proposed file storage or SQLite schema in queries.py |Critical | REJECT| no change| Code inspection of queries.py and services.py confirms zero database/file imports. |
| Validate isinstance(status, AppointmentStatus) inside select_appointments| queries.py#select_appointments | Minor| REJECT / MODIFY | Kept validation | test_list_practitioner_appointments_invalid_status_raises_value_error |
| Confirm sorted() returns a new list| queries.py#select_appointments | Informational | ACCEPT |retained | test_select_appointments_returns_new_container_preserving_object_identity |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- Domain invariants: Patient, Practitioner, and Appointment
Shared-store collections: SmartCareDataStore encapsulates internal dictionaries (_patients, _practitioners, _appointments),
Service coordination: AppointmentService, PatientService, and PractitionerService
Pure queries: select_appointments and appointment_sort_key in queries.py
Console effects: console.py and main.py handle all terminal interaction (input(), print()) -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- The main architectural concern was to keep every part of the system responsible for its own job. `AppointmentService` checks whether the practitioner exists and validates the input, while `queries.py` only filters and sorts appointments. This keeps the query function simple, reusable and independent of the data store. -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- 
Copilot suggested adding file storage or an SQLite database to save query results. it was ejected because SmartCare is designed to use temporary in-memory data only. -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- it was verified through automated tests and console testing -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- select_appointments is pure because it has referential transparency and modifying the source collection within the function would break purity. -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- select_appointments requires appointments (an iterable of Appointment objects), practitioner_id are needed explcitly. A global store is avoided because global state couples query logic to a specific instance which prevents independent queries. -->
3. How can a new list reuse Appointment objects safely? <!-- A new list can safely contain references to existing Appointment objects because changing the list (adding or removing items) does not change the original data store. -->
4. Why use a named key, and what breaks equal-time ties? <!-- A named key function makes sorting easier to understand, reuse and test. -->
5. How do default and explicit status filters differ? <!-- The default filter (status=None) shows all appointments, including scheduled, cancelled and completed ones. An explicit filter, such as SCHEDULED, only shows appointments with that status. -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- Empty: The practitioner is registered and valid
Unknown practitioner: The practitioner ID is syntactically valid but does not exist in the store
Invalid filter: The status argument passed is neither None nor an AppointmentStatus instance -->
7. Which console errors recover, and how is unchanged state checked? <!-- run_menu() handles errors relating to appointment. Unchanged state is checked by asserting that the data store's collection counts (len(store.list_patients()) -->
8. What is data integrity for registered participants, conflicts and history? <!-- Registered participants: Appointments cannot be booked for non-existent patients or practitioners
Conflicts: A practitioner cannot have more than one SCHEDULED appointment at the exact same time  -->
9. What is Copilot's review role, and who verifies findings? <!-- copilot acts as an automated advisory reviewer. human verifies the findings -->
10. How do pure functions and OOP responsibilities work together? <!-- Pure functions are used where transformations, projections, and calculations are needed without state. OOP is used where state encapsulation, data identity, and invariant protection are needed.  -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- N/A, we are bot doing branches -->
PR/diff and another-member human reviewer: <!-- Rashid, Shahdeen, Jaspreet -->
Review responses and Copilot comparison: <!-- human verified -->
Integrated common Stage 9 SHA: <!--  -->
Full regression command, working directory, actual count/result and evidence: <!-- working directory smartcare/project -->
README run instructions and scope/limitations: <!-- we will update readme -->
Unresolved issues and support/action: <!-- None as such -->
UG common candidate / PG future branch plan: <!-- complete -->

#all completed

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
