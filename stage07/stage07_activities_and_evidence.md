# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | [Register a patient with a valid ID like P5 and name as Alexandra Fox, under PatientSerrvice.register_patient] | [trying to register an existing ID] | [key asserting would include find patient, with negative raising a value/lookup error] |
| FR-05 Prevent practitioner conflict | [book appointment for a practitioner D2 at WHEN when D1 is already booked at WHEN] | [a double booking attemt at the same WHEN with same practitioner D1] | [practitioner D2 can have WHEN1 time for different patient, but D1 can't have an extra booking at WHEN1 when an existing appointment is scheduled, so second patient must have to wait or book another practitioner. raises a value error at AppointmentService.book_appointment] |
| FR-06 Cancel appointment | [cancelling existing appointment A1 through AppointmentService.cancel_appointment] | [cancelling an already cancelled appt A1 or completed status appt] | [assert cancelled is appt, if negative raises value error: AppointmentService.cancel_appointment] |
| FR-07 Retain cancelled history | [retrieve all appointments, incl cancelled, A1: find_apointment, list_appointments] | [retrieving unregistered appt ID RANDOM1] | [AppointmentService.find_appointment A1 in session.store.list_appointments, otherwise raises lookup error for RANDOM1 A] |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: [Weak/unclear]  Why: [execution without handled exception, return values, attribitues, status transition etc not checked]

`assert appointment is not None`
Judgement: [Weak/unclear]  Why: [can't verify wherger an object is correct or not, concerning retained data, valid/invalid fields, scheduled/cancelled]

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: [Strong for stated behaviour]  Why: [verifies cancelled]

`assert len(results) > 0`
Judgement: [Weak/unclear]  Why: [list is non-empty]

`assert data_store.find_appointment('A1') is appointment`
Judgement: [Strong for stated behaviour]  Why: [exact python object (is) and proves that shared data is well retained]

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: [
    Blank identifiers - patient_id, value error
    whitespace-only names - name = ' ', value error
    same-time practitioner bookings - one raises valueerror, other passes, allowing for prevention of conflict
    cancelled appointments - rebooking can happen
    invalid status transitions. - value error
]

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | [asserts only patient] | [verify call returns exact same object with same attributes and matching fields] |
| 2 | [asserts true means execution without a crash] | [transitions status correct] |
| 3 | [appt is not none may pass] | [find_appointment returns exact appointment record with all attributes] |
| 4 | [sms notification] | [response] |
| 5 | [notification, unneded requirement] | [status transition updated, data retrievable] |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
[measures execution. does not validate assertions executed or if they were checked, or whether other aspects like edge cases above were verified]

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01	AC-01.1	TEST-POSSRV-01	Positive Service	test_services.py:test_register_patient_stores_and_returns_patient	Valid patient data with unused ID is stored and returned	PASSED	Student-authored
FR-01	AC-01.2	TEST-NEGSRV-02	Negative Service	test_services.py:test_register_patient_duplicate_id_preserves_original	Existing patient ID raises ValueError, leaves original intact	PASSED	Student-authored
FR-01	Validation Contract	TEST-POSDOM-01	Positive Domain	test_domain.py:test_domain_patient_valid_construction	Valid construction trims whitespace, exposes read-only ID	PASSED	Student-authored
FR-01	Validation Contract	TEST-BOUDOM-02	Boundary Domain	test_domain.py:test_domain_patient_blank_id_rejected	Blank or non-string patient ID raises ValueError	PASSED	Student-authored
FR-01	Validation Contract	TEST-BOUDOM-03	Boundary Domain	test_domain.py:test_domain_patient_blank_name_rejected	Blank or non-string patient name raises ValueError	PASSED	Student-authored
FR-02	AC-02.1	TEST-POSSRV-03	Positive Service	test_services.py:test_find_patient_returns_registered_object	Known patient ID returns registered object	PASSED	Student-authored
FR-02	AC-02.2	TEST-NEGSRV-06	Negative Service	test_services.py:test_find_unknown_patient_raises_lookup_error	Unknown patient ID raises LookupError, adds nothing	PASSED	Student-authored
FR-02	Validation Contract	TEST-BOUSRV-04	Boundary Service	test_services.py:test_find_patient_trims_id	Whitespace around ID is trimmed before lookup	PASSED	Student-authored
FR-02	Validation Contract	TEST-BOUSRV-05	Boundary Service	test_services.py:test_find_patient_is_case_sensitive	Differing case IDs raise LookupError	PASSED	Student-authored
FR-02	Validation Contract	TEST-BOUSRV-07	Boundary Service	test_services.py:test_find_patient_invalid_id_raises_value_error	Blank or non-string ID raises ValueError	PASSED	Student-authored
FR-03	Registration Contract	TEST-POSNEGSRV-08	Positive/Neg Service	test_services.py:test_register_practitioner_stores_and_duplicate_preserves_original	Practitioner stored; duplicate ID raises ValueError	PASSED	Student-authored
FR-03	Supporting Lookup	TEST-POSSRV-09	Positive Service	test_services.py:test_find_practitioner_returns_registered_object	Known practitioner ID returns registered object	PASSED	Student-authored
FR-03	Supporting Lookup	TEST-NEGSRV-12	Negative Service	test_services.py:test_find_unknown_practitioner_raises_lookup_error	Unknown practitioner ID raises LookupError	PASSED	Student-authored
FR-03	Validation Contract	TEST-DOM-04	Positive Domain	test_domain.py:test_domain_practitioner_valid_construction	Practitioner trims fields, stores name/specialty	PASSED	Student-authored
FR-03	Validation Contract	TEST-BOUDOM-05	Boundary Domain	test_domain.py:test_domain_practitioner_blank_fields_rejected	Blank/non-string ID/name/specialty raises ValueError	PASSED	Student-authored
FR-04	AC-03.1	TEST-POSSRV-14	Positive Service	test_services.py:test_book_appointment_stores_and_links_participants	Registered participants + unique ID produce stored SCHEDULED appointment	PASSED	Student-authored
FR-04	AC-03.2	TEST-NEGSRV-15	Negative Service	test_services.py:test_book_appointment_unknown_participants_rejected	Unknown patient or practitioner raises LookupError	PASSED	Student-authored
FR-04	Invariant Contract	TEST-NEGSRV-16	Negative Service	test_services.py:test_book_appointment_duplicate_id_preserves_original	Duplicate appointment ID raises ValueError	PASSED	Student-authored
FR-04	Invariant Contract	TEST-POSDOM-06	Positive Domain	test_domain.py:test_domain_appointment_initial_status_is_scheduled	New appointment starts in SCHEDULED status	PASSED	Student-authored
FR-04	Invariant Contract	TEST-POSDOM-07	Positive Domain	test_domain.py:test_domain_appointment_valid_construction_and_properties	Appointment connects participant objects & naive datetime	PASSED	Student-authored
FR-04	Invariant Contract	TEST-BOUDOM-08	Boundary Domain	test_domain.py:test_domain_appointment_invalid_participants_rejected	Non-Patient or non-Practitioner raises ValueError	PASSED	Student-authored
FR-04	Invariant Contract	TEST-BOUDOM-09	Boundary Domain	test_domain.py:test_domain_appointment_invalid_status_rejected	Non-AppointmentStatus raises ValueError	PASSED	Student-authored
FR-04	Invariant Contract	TEST-BOUDOM-10	Boundary Domain	test_domain.py:test_domain_appointment_datetime_boundaries_rejected	Non-zero sec/usec, tz-aware, non-datetime raises ValueError	PASSED	Student-authored
FR-05	AC-04.1	TEST-NEGSRV-17	Negative Service	test_services.py:test_practitioner_conflict_same_time_rejected	Same practitioner/exact time/SCHEDULED raises ValueError	PASSED	Student-authored
FR-05	AC-04.2	TEST-POSSRV-18	Positive Service	test_services.py:test_practitioner_conflict_different_practitioner_allowed	Different practitioner at same time is permitted	PASSED	Student-authored
FR-05/06	Slot Re-use Contract	TEST-SRV-27	Positive Service	test_services.py:test_cancellation_frees_slot_and_keeps_history	Cancelled appointment frees timeslot for new booking	PASSED	Student-authored
FR-06	AC-05.1	TEST-POSSRV-19	Positive Service	test_services.py:test_cancel_returns_same_object_with_cancelled_status	Cancel changes status to CANCELLED, returns same object	PASSED	Student-authored
FR-06	AC-05.1	TEST-POSDOM-11	Positive Domain	test_domain.py:test_domain_appointment_cancel_changes_status	Domain cancel() changes status to CANCELLED	PASSED	Student-authored
FR-06	AC-05.3	TEST-NEGSRV-22	Negative Service	test_services.py:test_repeated_cancellation_rejected_without_change	Repeated cancellation raises ValueError; status stays CANCELLED	PASSED	Student-authored
FR-06	AC-05.3	TEST-NEGDOM-12	Negative Domain	test_domain.py:test_domain_appointment_repeated_cancellation_rejected	Domain cancel() on CANCELLED raises ValueError	PASSED	Student-authored
FR-06	State Guard Contract	TEST-NEGSRV-23	Negative Service	test_services.py:test_cancel_completed_appointment_rejected_without_change	Cancelling COMPLETED appointment raises ValueError	PASSED	Student-authored
FR-06	State Guard Contract	TEST-NEGDOM-13	Negative Domain	test_domain.py:test_domain_appointment_cancel_completed_rejected	Domain cancel() on COMPLETED raises ValueError	PASSED	Student-authored
FR-06	Lookup Contract	TEST-NEGSRV-24	Negative Service	test_services.py:test_cancel_unknown_appointment_raises_lookup_error	Unknown appointment ID raises LookupError	PASSED	Student-authored
FR-06	Validation Contract	TEST-BOUSRV-26	Boundary Service	test_services.py:test_cancel_invalid_id_raises_value_error	Blank or non-text appointment ID raises ValueError	PASSED	Student-authored
FR-07	AC-05.2	TEST-POSSRV-20	Positive Service	test_services.py:test_cancelled_appointment_is_retained_and_retrievable	Cancelled appointment remains retrievable in session	PASSED	Student-authored
FR-08	AC-06.1	TEST-POSSRV-28	Positive Service	test_services.py:test_find_appointment_success_and_unknown_raises_lookup	Known appointment ID returns appointment; unknown raises LookupError	PASSED	Supplied
|

## C Test Design
# **Section C is a redundant of section B

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [TEST-BOUDOM-02] | [Prepare invalid patient IDs ('', '   ', None, 123)] | [Patient(bad_id, 'Alex Fox')] | [with pytest.raises(ValueError):] | [Proves domain entity rejects malformed IDs before instantiation.] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| TEST-DOM-01	Patient trims whitespace and exposes fields	tests/test_domain.py::test_domain_patient_valid_construction	PASSED
TEST-DOM-02	Blank/invalid patient ID rejected	tests/test_domain.py::test_domain_patient_blank_id_rejected	PASSED
TEST-DOM-03	Blank/invalid patient name rejected	tests/test_domain.py::test_domain_patient_blank_name_rejected	PASSED
TEST-DOM-04	Practitioner trims whitespace and exposes attributes	tests/test_domain.py::test_domain_practitioner_valid_construction	PASSED
TEST-DOM-05	Blank/invalid practitioner fields rejected	tests/test_domain.py::test_domain_practitioner_blank_fields_rejected	PASSED
TEST-DOM-06	Appointment starts SCHEDULED	tests/test_domain.py::test_domain_appointment_initial_status_is_scheduled	PASSED
TEST-DOM-07	Non-Patient or non-Practitioner objects rejected	tests/test_domain.py::test_domain_appointment_invalid_participants_rejected	PASSED
TEST-DOM-08	Invalid appointment status type rejected	tests/test_domain.py::test_domain_appointment_invalid_status_rejected	PASSED
TEST-DOM-09	Datetime validation boundaries rejected	tests/test_domain.py::test_domain_appointment_datetime_boundaries_rejected	PASSED
TEST-DOM-10	Domain cancel() changes status	tests/test_domain.py::test_domain_appointment_cancel_changes_status	PASSED
TEST-DOM-11	Repeated cancellation rejected	tests/test_domain.py::test_domain_appointment_repeated_cancellation_rejected	PASSED
TEST-DOM-12	Cancellation of COMPLETED appointment rejected	tests/test_domain.py::test_domain_appointment_cancel_completed_rejected	PASSED |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

Test-SRV-01 Valid patients registration stores and returns object. FR-01 / AC-01.1 tests/test_services.py::test_register_patient_stores_and_returns_patient Passed 
Test-SRV-02 Duplicated patients records rejected FR-01 / AC-01.2 tests/test_services.py::test_register_patient_duplicate_id_preserves_original Passed 
Test-SRV-03 Patient search returns registered object. FR-02 / AC-02.1 tests/test_services.py::test_find_patient_returns_registered_object 
Test-SRV-04 Patient Look up is case sensitive. FR-02 / Validation tests/test_services.py::test_find_patient_is_case_sensitive Passed 
Test-SRV-05 Unknown patient lookup raises LookupError. FR-02 / AC-02.2 tests/test_services.py::test_find_unknown_patient_raises_lookup_error Passed 
Test-SRV-06 Invalid patient ID raises ValueError. FR-02 / Validation tests/test_services.py::test_find_patient_invalid_id_raises_value_error Passed 
Test-SRV-07 Practitioner lookup returns registered object FR-03 / Lookup tests/test_services.py::test_find_practitioner_returns_registered_object Passed 
Test-SRV-08 Unknown practitioner lookup raises LookupError. FR-03 / Lookup tests/test_services.py::test_find_unknown_practitioner_raises_lookup_error Passed 
Test-SRV-9 Invalid practitioner ID raises ValueError. FR-03 / Validation tests/test_services.py::test_find_practitioner_invalid_id_raises_value_error Passed 
Test-SRV-10 Appointment booking links objects and stores. FR-04 / AC-03.1 tests/test_services.py::test_book_appointment_stores_and_links_participants Passed 
Test-SRV-11 Booking duplicate appointment ID raises ValueError. FR-04 / Invariant tests/test_services.py::test_book_appointment_duplicate_id_preserves_original Passed 
Test-SRV-12 Same practitioner time conflict raises ValueError. FR-05 / AC-04.1 tests/test_services.py::test_practitioner_conflict_same_time_rejected Passed 
Test-SRV-13 Cancelled appointment stays in history. FR-07 / AC-05.2 tests/test_services.py::test_cancelled_appointment_is_retained_and_retrievable Passed 
Test-SRV-14 Canceling a COMPLETED appointment raises ValueError. FR-06 / Guard tests/test_services.py::test_cancel_completed_appointment_rejected_without_change Passed 
Test-SRV-15 Cancellation of appointment frees practitioner slot for booking. FR-05 / FR-06 tests/test_services.py::test_cancellation_frees_slot_and_keeps_history Passed 


## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |
Creating Patient ID check. | Empty string '', whitespace ' ', None, non-string 123 | Raises ValueError('Patient ID cannot be blank'), no object constructed TEST-DOM-02 
Creating Patient name check. | Empty string '', whitespace ' ', None, non-string 456 | Raises ValueError('Patient name cannot be blank'), no object constructed TEST-DOM-03 
Appointment Patient or Practitioner type check. | Non-Patient or non-Practitioner passed to constructor | Raises ValueError('Appointment requires a Patient/Practitioner object') TEST-DOM-08 
Unknown patient lookup. | Searching 'P404' | Raises LookupError('Patient not found'), store unmodified TEST-SRV-06 
Invalid ID lookup type. | Blank string '', ' ', None, int 7 | Raises ValueError, no store search executed TEST-SRV-15 
Exact practitioner and time conflict. | Booking second appointment for D1 at exact minute WHEN | Raises ValueError('Practitioner already has a SCHEDULED...'), store unmodified TEST-SRV-17 
Cancellation of a COMPLETED appointment. | Calling cancel on appointment in COMPLETED status | Raises ValueError('Only SCHEDULED appointments may be cancelled'), status stays COMPLETED TEST-DOM-13, TEST-SRV-23 



## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [FR-05 Prevent practitioner conflict Acceptance criterion: AC-04.1 and AC-04.2: Same practitioner/exact time/SCHEDULED conflicts]
Acceptance criterion: [Another practitioner at the same time is allowed]
Behaviour to test: [AppointmentService.book_appointment must reject booking when the target practitioner already has a SCHEDULED appointment at the exact datetime (ValueError), but allow booking at the same datetime for a different practitioner, and allow rebooking after cancellation]
Human-first test idea/categories: [Negative case: Booking practitioner D1 at time T1 when D1 already has a SCHEDULED appointment at T1 raises ValueError. Positive case: Booking practitioner D2 at time T1 when D1 is booked at T1 succeeds. Boundary case: Booking practitioner D1 at time T1 after the original booking at T1 is CANCELLED succeeds]
Prompt and purpose: [Act as a software test-design assistant. Requirement: FR-05 Prevent practitioner conflict Acceptance criterion: AC-04.1 and AC-04.2: Same practitioner at exact time and is SCHEDULED conflicts; another practitioner at the same time is allowed. Propose pytest test candidates covering a valid case, an invalid case and meaningful boundaries. For each candidate, state exactly which required behaviour it is intended to verify. Do not invent behaviour not stated in the requirement or criterion. Use observable outcomes rather than private implementation details. Use the current SmartCare public contracts and shared SmartCareDataStore. Do not introduce SQLite, repository abstractions or unrelated features. Do not claim that a proposed test has been executed.]


For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [test_book_same_practitioner_conflict checking that booking D1 at 09:00 twice raises ValueError. Candidate 1]
- What it claims to verify: [Verifies AC-04.1 conflict rejection.]
- Requirement trace: [Traces directly to FR-05 / AC-04.1.]
- Assertion quality: [Used pytest.raises(ValueError)]
- Human critique: [Setup was slightly repetitive but the check was valid. Added post-block assertion confirming store was not corrupted.]
- Decision: [Modify]
- Reason: [Needed assertion that existing scheduled appointment was preserved in data store.]
- Final test reference if accepted/modified: [tests/test_services.py::test_practitioner_conflict_same_time_rejected]
- Actual verification result: [PASSED in full suite.]  

- Copilot test idea/candidate: [test_book_different_practitioner_same_time checking that booking D2 at 09:00 succeeds when D1 is booked at 09:00. Candidate 2]
- What it claims to verify: [Verifies AC-04.2 multi-practitioner concurrency.]
- Requirement trace: [Traces directly to FR-05 / AC-04.2.]
- Assertion quality: [Strong: asserts returned appointment practitioner is D2 and both bookings are in store.]
- Human critique: [Well-structured; cleanly verifies that conflict is practitioner-specific.]
- Decision: [Accept]
- Reason: [Directly fulfills AC-04.2 without unnecessary errors or unstated rules.]
- Final test reference if accepted/modified: [tests/test_services.py::test_practitioner_conflict_different_practitioner_allowed]
- Actual verification result: [PASSED in full suite.] 

- Copilot test idea/candidate: [test_practitioner_appointment_duration_overlap checking if booking at 09:15 conflicts with a 09:00 booking assuming a 30-minute duration. Candidate 3]
- What it claims to verify: [Claims to check appointment duration overlap.]
- Requirement trace: [None; violates SmartCare specification.]
- Assertion quality: [Mistaken expectation.]
- Human critique: [SmartCare baseline explicitly defines conflict as exact-time equality: "It is an exact-time rule, not an appointment-duration overlap calculation. No duration rules apply."]
- Decision: [Reject]
- Reason: [Invents an unstated business rule that contradicts the approved revision 2 requirements baseline.]
- Final test reference if accepted/modified: [Not keep]
- Actual verification result: [N/A]  

- Copilot test idea/candidate: [test_rebook_after_cancellation_frees_slot verifying that cancelling an appointment allows the same practitioner to be booked at that time. Candidate 4]
- What it claims to verify: [Verifies that conflict logic ignores non-SCHEDULED appointments.]
- Requirement trace: [Connects FR-05 and FR-06/FR-07.]
- Assertion quality: [Strong: asserts both cancelled and new scheduled appointments coexist in store.]
- Human critique: [Essential boundary check demonstrating integration between cancellation status and conflict query.]
- Decision: [Accept]
- Reason: [Validates that cancellation frees schedule slot while retaining session history.]
- Final test reference if accepted/modified: [tests/test_services.py::test_cancellation_frees_slot_and_keeps_history]
- Actual verification result: [PASSED in full suite.]  



Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? []
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
