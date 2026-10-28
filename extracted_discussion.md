AgriNexus AI

Author Argha

Email Intelligence Prototype

Plain-language build guide for Argha, Amarnath and Aman

Purpose: align on what we are building, how information moves, who codes each part, and how we test the first version.

SCOPE NOTE  The first prototype uses fictional/sample emails only. It is not connected to Sayan's inbox and must not be used as the only control for live tender deadlines.

1. The idea in one minute

Think of this as a smart assistant for the inbox. It looks for emails that ask for action, spots possible missing documents or deadlines, explains why a message was flagged, and shows it on a dashboard. A person checks the original email and decides what to do.

Company A + Company B emails

↓

Read email subject, sender and message text

↓

Look for risk words, requested actions, documents and dates

↓

Show priority + reason + suggested next step

↓

A person verifies the original email and updates status

2. End-to-end system flow

The prototype starts with a sample CSV file. Connecting real email accounts is a later phase.

1. SOURCESample CSVLater: Gmail / Outlook

2. CLEANStandardize text,sender and fields

3. ANALYZERules first;AI after testing

4. DISPLAYDashboard, filters,priority and action

5. REVIEWHuman verifies,acts and updates

Important: in the current sample app, a deadline is displayed from a CSV field. Automatic date extraction from email text still needs to be built and tested.

3. Simple priority decision flow

START: An email is loaded

↓

Does it mention bid rejection, disqualification or tender risk?

YES → HIGH priority; show the phrase that triggered the alert

NO → Does it request a document, response, approval or other action?

YES → Flag for action; apply agreed HIGH/MEDIUM rules and show the reason

NO → LOW / informational

Always show the source text so a person can verify the result

4. Example in everyday language

Sample email: “Please submit the signed technical document by 3 PM today. Failure to submit may result in bid rejection.”

ITEM

WHAT THE TOOL SHOULD SHOW

Words it notices

“signed technical document”, “3 PM today”, “bid rejection”

Priority

HIGH — because the email mentions possible bid rejection

Suggested action

Submit the signed technical document

Deadline

3 PM today only if verified or correctly extracted; check the original email

Human check

Open the original message, confirm deadline and assign an owner

5. First version: what is in scope?

BUILD NOW

NOT IN FIRST VERSION

WHY

Load fictional emails from CSV

Live inbox connection

Simple, safe starting point

Keyword-based priority and reason

Fully automated AI decisions

Rules are easier to explain and debug

Show subject, sender, body and CSV deadline

Guaranteed date extraction

Date parsing needs separate testing

Company, priority and status filters

Automatic replies or document submission

Keep a human in control

Basic Streamlit dashboard

Production-grade access controls and audit logging

Required before real business use

6. Suggested technical flow

sample_emails.csv  →  sample input data

app.py  →  Streamlit dashboard and current processing

classifier.py (later)  →  priority rules and action suggestions

date_extractor.py (later)  →  detect dates/times and retain source evidence

Database (later)  →  email reference, owner, priority and status

Gmail API / Microsoft Graph (later)  →  authorized inbox access

Notification service (later)  →  reminders after deadline logic is validated

Keep the first version in one app if that is easier. Split code into modules when the logic becomes difficult to test or maintain.

7. Suggested team responsibilities

OWNER

RESPONSIBILITY

DELIVERABLE

Argha — product / business logic

Define HIGH/MEDIUM/LOW; confirm dashboard fields and examples with Sayan.

Priority rules and acceptance checklist

Amarnath — Python / data

Review CSV, handle missing values, help write and test classification logic.

Validated input and classification function

Aman — dashboard / QA

Build or refine Streamlit screen and filters; test examples and record defects.

Usable dashboard and test results

This is a suggested split; adjust it to each person's coding comfort. One team member should review the combined code before a demo.

8. Test cases and expected results

TEST CASE

EXPECTED RESULT

PASS

Email warns of bid rejection

HIGH priority and reason visible

☐

Email mentions missing certificate

Document action suggested; source visible

☐

Routine newsletter

Usually LOW unless action/risk words change context

☐

No deadline field

Clearly show no deadline supplied/detected

☐

Company filter selected

Only selected company's emails show

☐

Ambiguous date wording

Do not assume; require human verification

☐

Duplicate email

Document deduplication as a requirement and test it

☐

9. Risks and safeguards

False negatives: urgent emails may use words the rules do not recognize. Test varied examples.

False positives: a harmless message may mention “deadline”. Show the reason for every flag.

Deadline errors: “next Tuesday” depends on received date and time zone. Validate before sending reminders.

Privacy: use fictional or anonymized samples for demos. Obtain account-owner approval before inbox access; never share passwords or tokens.

Human responsibility: this dashboard supports decisions; it does not prove a tender was submitted.

10. Team meeting agenda

Agree the first version's scope and what is explicitly out of scope.

Review the sample CSV columns and decide whether any are missing.

Agree priority rules using 10–20 fictional or anonymized email examples.

Run the app locally and record confusing labels, bugs and missing cases.

Assign one owner per task and define what counts as a successful demo.

Only after the sample version works, plan secure inbox integration and date extraction.

Decisions to record

☐  Who owns each coding task and reviews changes?

☐  What exactly counts as HIGH priority for Sayan?

☐  Which fields must always appear on the dashboard?

☐  Where will the pilot app run, and who can access it?

☐  What test results are required before live inbox access?

Internal draft for planning and coding discussion. This is not a production specification or a promise of timeline/cost. Confirm business rules and security requirements with the business owners before implementation.