# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [Group 2, Monday 9:30 - 11:30]
- Members, GitHub usernames and cohorts: [Rashid, Jaspreet, Shahdeen]
- Repository URL: [https://github.com/azyx5/st1-assignment-3]
- Starting SHA: [02245b4]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: [Patient Search]
- Context: [Using this features allows users to search for patients in the system]
- Requirement: [Search bar, database, link patients to appointment history]
- Acceptance criteria: [This feature will only work if there is a patient in the system that has the same name or id that was used in the patient search, 
1. search existing registered patient ID returns existing patient record
2. return object includes all patient attributes
3. patient IDs are unique and case-sensitive
3. querying IDs that are not registered raises LookupError("Patient not found)
4. Empty strings, whitespace string raises ValueError]
- Scope: [PatientService.find_patient method implementation, unit tests in project/tests/tests_services.py]
- Definition of Done: [The feature is able to find the patients that the user is wanting to find. It should also respond with a message saying failed to find the patient if that name or id was not found in the system. Unit tests in test_services.py, all tests pass, integrated into main branch]
- Owner: [Jaspreet & Rashid]
- Actual issue link: [response]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: [Appointment Cancellation]
- Context: [When canceling a appointment the system should still keep record of that appointment]
- Requirement: [Appointment, database]
- Acceptance criteria: [This feature should only work when a user cancels an appointment, 
1. when given valid existing booking ID of scheduled appointments, it can transition its status to update AppointmentStatus
2. method returns exact object instance of appointment being cancelled
3. retained history
4. canceling cancelled appointments raises a value error, keeping the status unchanged
5. canceliling completed appointments raises a value error
6. appointment IDs are case-sensitive
7. time allocations, after a completed appointment in a specific time slot, a practitioner is no longer busy and is available for another appointment at the same time but different day etc etc]
- Scope: [cancel_appointment implementation and unit tests in test_services.py]
- Definition of Done: [The feature is done when it is able to allow users to cancel an appointment and record that appointment, status update, etc]
- Owner: [Jaspreet]
- Actual issue link: [response]

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | [Weak] | [This is a weak commit because it does not tell us what type of changes were actually made] |
| final version | [Weak] | [Although it sounds like the finished product, but what if something still needed to be worked on but the message says everything is completed] |
| Add patient search by ID | [Strong] | [This commit tells users what was worked on clearly] |
| fix stuff | [Weak] | [The response is weak, it tells us that something needs to be fixed, but not tellings us the exact issue] |
| Prevent cancellation of completed appointments | [Strong] | [This message tells us that a feature or rule that prevents completed appointments is added so important data won't go missing] |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: [PR does not follow the single responsibility principle for pull requests. Unrelated patient field renames and structural refactoring and external dependencies in regards to appointment cancelling differ the core feature, hinders review, and proves regression risks]
- Responsibility and architecture concerns: [cancellation is under AppointmentService. Modifying Patient fields can violate separation of concerns and risks  harming existing patient workflows. The architecture of the project implies a standard library only for runtime, therefore new dependency can violate the architecture]
- Testing and review concerns: [reviewers cannot always be sure whether the results validate something in specific like cancellation or prove some issues as a result of renamed fields and changes.]
- Changes to remove or separate, with reasons: [Remove external dependencies: The app's baseline requires a standard library for runtime, remove unreleated patient field renames: renames must be separate with their own specific impact and review of the renames.]

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: [did not execute tests, failed to check acceptance criteria for 6/7, like status transition and retained history, etc]
- Follow-up review question 1: [why did the test pass]
- Follow-up review question 2: [Where is the proof that the content of the test actually passed]
- Follow-up review question 3: [Was your test just a read through or also running the code so see if it actually works]
- Follow-up review question 4: [What exceptions were raised for unkown IDs/invalid IDs?]
- Follow-up review question 5: [Appointment history retainment when unit tests verify cancelation of appointment frees up a practitioner's timeslot and shows no conflict?]
- Additional questions if useful: [does cancellation return exact object]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [The names should be simple but strong meaning the name should tell users what that branch is being used for] |
| Commit message convention | [writing commits this way can be used to tells user about thats been commited in more detail] |
| PR size | [The pull request sizes should only be about on document per commit to keep things simple] |
| Another-member review requirement | [peer review by other members, approval without peer review not allowed] |
| Merge rule | [not merging, working on each stage one person at a time, so everyone can do Pull requests and push individually so to ensure everyone reviews eachother's work] |
| Significant Copilot disclosure rule | [VS-code's builtin integrated copilot chatbot on the side, with human accepts etc, used when problems arise next to output, debug, and terminal tabs] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [issue 1] | [FR-02 Patient Search] | [Rashid] | [ search existing registered patient ID returns existing patient record
2. return object includes all patient attributes
3. patient IDs are unique and case-sensitive
3. querying IDs that are not registered raises LookupError("Patient not found)
4. Empty strings, whitespace string raises ValueError] | [closed] |
| [issue 2] | [FR-06 Appointment Cancellation] | [Jasprit] | [when given valid existing booking ID of scheduled appointments, it can transition its status to update AppointmentStatus
2. method returns exact object instance of appointment being cancelled
3. retained history
4. canceling cancelled appointments raises a value error, keeping the status unchanged
5. canceliling completed appointments raises a value error
6. appointment IDs are case-sensitive
7. time allocations, after a completed appointment in a specific time slot, a practitioner is no longer busy and is available for another appointment at the same time but different day etc etc] | [closed] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.
## This section does not apply as much to us, as we are not using branching as a method of working together as a group, rather working on each stage together at different times pushing any changes and another pulls requests to receive updated version and makes their own changes further.
- PR link and title: [response]
- Linked issue and requirement: [FR-02 Patient Search]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [Jaspreet]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [Rashid, owner of the repo, Jaspreet and Shahdeen as collaborators, they both review any changes I make and I review any changes they make by PR'ing each time they make a change or I make a change (we have a groupchat, where we update eachother on updates and changes)]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [Jaspreet]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [issue/problem in test_starter.py]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [Rashid]
- Prompt/purpose and relevant issue/diff: [Act as a GitHub Copilot code-review assistant. Review the PR diff implementing PatientService.find_patient, PractitionerService.find_practitioner, and AppointmentService.cancel_appointment against FR-02, FR-06, and FR-07. Focus on boundary conditions, exception contracts, and test coverage gaps.]
- Summary of output: [The intended PR for PatientService.find_patient, PractitionerService.find_practitioner, and AppointmentService.cancel_appointment is directionally correct.
The main risk is not the happy path; it is the exact boundary behavior and exception contracts.
FR-02 expects:
valid existing IDs to return the object
unknown IDs to raise LookupError
blank/whitespace IDs to raise ValueError
no replacement object creation
FR-06 and FR-07 expect:
valid scheduled appointments to be cancelled
the same appointment object instance to be returned
the cancelled item to remain retrievable in the same session
invalid transitions to raise ValueError and leave state unchanged
]
- Human check against actual code, requirements and tests: [Rashid, Jaspreet]
- Decision — Accept / Modify / Reject: [Accept]
- Reason: [Cancellation only from scheduled or booked/pending appoiintments]
- Verification/evidence: [test_services.py]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
