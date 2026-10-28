# Email Intelligence Assistance (V1)

**Author & Lead Engineer:** Manisha  

---

## 🎯 Project Overview
This prototype is a smart inbox assistant designed to triage emails for **Company A** and **Company B**. It monitors communications for tender risks (disqualifications, bid rejections), document requests (missing certificates, EMD guarantees), and impending deadlines, while ensuring full explainability and keeping a human in control.

---

## 🏗️ Architecture & File Structure

```
email-intelligence-prototype/
├── app.py                  # Streamlit Dashboard (Triage Inbox, Filters & Human Review Center)
├── classifier.py           # Rule-based priority engine, keyword/evidence detector & deadline logic
├── sample_emails.csv       # Fictional/anonymized dataset covering all 7 Section 8 test cases
├── test_classifier.py      # Automated test runner certifying Section 8 acceptance criteria
├── extracted_discussion.md # Plaintext copy extracted from the team's project brief
└── README.md               # Documentation and execution guide
```

---

## ⚡ How to Run

1. **Activate your Python environment** and install requirements (if not already installed):
   ```bash
   pip install streamlit pandas
   ```

2. **Run the Automated Acceptance Tests**:
   ```bash
   python test_classifier.py
   ```

3. **Launch the Streamlit Dashboard**:
   ```bash
   streamlit run app.py
   ```
   Open your browser at: `http://localhost:8501`

---

## 🧠 Decision & Classification Rules

1. **HIGH Priority**:
   - Mentions bid rejection, disqualification, cure notice, penalty, termination, or material breach.
   - Mentions same-day urgent deadlines for submissions.
2. **MEDIUM Priority**:
   - Requests documents (e.g., signed technical document, missing certificate, laboratory batch report).
   - Requests clarification or action without explicit immediate disqualification threats.
3. **LOW / Informational**:
   - Routine market digests, price index newsletters, safe receipt confirmations, or maintenance notifications.
4. **Deadline Intelligence & Ambiguity Flag**:
   - Tracks both CSV-supplied deadlines and in-text references.
   - Relative/ambiguous dates (e.g., *"next Tuesday afternoon"*, *"earliest convenience"*) are explicitly flagged for human verification.
5. **Deduplication**:
   - Flags identical or duplicate emails across threads so reviewers avoid redundant actions.

---

## ✅ Acceptance Test Suite (Section 8 Verification)

| Test Case | Scenario / Target | Expected Result | Status |
| :--- | :--- | :--- | :---: |
| **1** | Email warns of bid rejection (`EML-001`) | HIGH priority and reason visible | **PASS** |
| **2** | Email mentions missing certificate (`EML-002`) | Document action suggested; source visible | **PASS** |
| **3** | Routine newsletter (`EML-003`) | LOW priority unless action words change context | **PASS** |
| **4** | No deadline field (`EML-004`) | Clearly shows "No Deadline Supplied" | **PASS** |
| **5** | Company filter selected | Isolates Company A (6) vs Company B (4) | **PASS** |
| **6** | Ambiguous date wording (`EML-005`) | Does not assume; requires human verification | **PASS** |
| **7** | Duplicate email (`EML-001` & `EML-006`) | Detects duplicate and warns reviewer | **PASS** |

---

## 🛡️ Scope & Safety Guidelines
* **Fictional Emails Only**: The prototype operates solely on sample datasets to ensure data isolation.
* **Explainability First**: Every priority tag is backed by the exact trigger phrases that caused it.
* **Human Verification Required**: The dashboard assists decision-making; final tender actions require human cross-checking and owner sign-off.
