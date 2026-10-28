"""
classifier.py - Rule-based Email Intelligence Classifier for Email Intelligence Assistance
Implements priority classification, trigger phrase detection, action suggestion,
date/deadline analysis, and duplicate detection.
"""

import re
from typing import Dict, List, Any, Optional

# Rule sets as specified in Email Intelligence Assistance build guide
HIGH_PRIORITY_RISK_KEYWORDS = [
    r"\bbid rejection\b",
    r"\bdisqualification\b",
    r"\bdisqualified\b",
    r"\btender risk\b",
    r"\bcure notice\b",
    r"\btermination\b",
    r"\bforfeiture\b",
    r"\bpenalty\b",
    r"\bmaterial breach\b",
    r"\bimmediate\b",
    r"\burgent\b",
    r"\bcritical\b",
]

DOCUMENT_ACTION_KEYWORDS = [
    r"\bsigned technical document\b",
    r"\bmissing certificate\b",
    r"\bmissing\b",
    r"\bemd\b",
    r"\bbank guarantee\b",
    r"\biso-\d+\b",
    r"\blaboratory batch report\b",
    r"\btechnical compliance\b",
    r"\benvironmental clearance\b",
    r"\bsign and return\b",
    r"\bfurnish\b",
    r"\bsubmit\b",
    r"\bsubmission\b",
    r"\bcompliance schedule\b",
]

ACTION_REQUEST_KEYWORDS = [
    r"\bplease submit\b",
    r"\bplease provide\b",
    r"\bkindly furnish\b",
    r"\baction required\b",
    r"\brequested to join\b",
    r"\bclarification\b",
    r"\bapproval\b",
    r"\bconfirm safe receipt\b",
    r"\bresponse\b",
    r"\bverify\b",
]

LOW_PRIORITY_INDICATORS = [
    r"\bnewsletter\b",
    r"\bdigest\b",
    r"\broutine\b",
    r"\bmaintenance window\b",
    r"\bprice trends\b",
    r"\bmarket summary\b",
    r"\bno further action\b",
    r"\bconfirm safe receipt\b",
    r"\bportal downtime\b",
]

AMBIGUOUS_DATE_PATTERNS = [
    r"\bnext (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    r"\bthis (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    r"\b(?:morning|afternoon|evening)\b",
    r"\basap\b",
    r"\bearliest convenience\b",
    r"\bsoon\b",
]

DEADLINE_EXTRACTION_PATTERNS = [
    r"\b\d{1,2}\s*(?:am|pm|AM|PM)\s*today\b",
    r"\bwithin\s*\d{1,2}\s*hours\b",
    r"\b(?:by|before|on)\s*\d{1,2}(?:st|nd|rd|th)?\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b",
    r"\b\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?\b",
    r"\b\d{1,2}:\d{2}\s*(?:am|pm|AM|PM|IST)\b",
]


def extract_matched_phrases(text: str, patterns: List[str]) -> List[str]:
    """Extracts all matched phrases based on regex patterns."""
    found = []
    lower_text = text.lower()
    for pattern in patterns:
        matches = re.finditer(pattern, lower_text)
        for m in matches:
            phrase = text[m.start():m.end()]
            if phrase.lower() not in [f.lower() for f in found]:
                found.append(phrase)
    return found


def analyze_deadline(body: str, csv_deadline: Optional[str]) -> Dict[str, Any]:
    """Analyzes deadlines from CSV and extracts dates/times or ambiguity warnings from text."""
    body_extracted_dates = extract_matched_phrases(body, DEADLINE_EXTRACTION_PATTERNS)
    ambiguous_matches = extract_matched_phrases(body, AMBIGUOUS_DATE_PATTERNS)
    
    csv_deadline_str = str(csv_deadline).strip() if csv_deadline and str(csv_deadline).lower() not in ['nan', 'none', ''] else None
    
    is_ambiguous = False
    ambiguity_reason = None
    
    if csv_deadline_str:
        for p in AMBIGUOUS_DATE_PATTERNS:
            if re.search(p, csv_deadline_str.lower()):
                is_ambiguous = True
                ambiguity_reason = f"CSV deadline '{csv_deadline_str}' contains relative/ambiguous time reference."
                break
                
    if not is_ambiguous and ambiguous_matches:
        is_ambiguous = True
        ambiguity_reason = f"Email mentions ambiguous timing: '{', '.join(ambiguous_matches)}'. Requires human verification."
        
    if not csv_deadline_str and not body_extracted_dates:
        deadline_status = "No Deadline Supplied"
    elif is_ambiguous:
        deadline_status = "Ambiguous / Needs Verification"
    elif csv_deadline_str:
        deadline_status = "Supplied via CSV"
    else:
        deadline_status = "Extracted from Text"

    return {
        "csv_deadline": csv_deadline_str if csv_deadline_str else "None supplied",
        "extracted_dates": body_extracted_dates,
        "is_ambiguous": is_ambiguous,
        "ambiguity_reason": ambiguity_reason,
        "deadline_status": deadline_status
    }


def classify_email(subject: str, body: str, csv_deadline: Optional[str] = None) -> Dict[str, Any]:
    """
    Implements Section 3 Priority Decision Flow:
    1. Check if it mentions bid rejection, disqualification or tender risk -> HIGH
    2. Check if it requests a document, response, approval or action -> MEDIUM/HIGH
    3. Check for routine/informational indicators -> LOW
    """
    full_text = f"{subject} {body}"
    
    high_risk_matches = extract_matched_phrases(full_text, HIGH_PRIORITY_RISK_KEYWORDS)
    doc_matches = extract_matched_phrases(full_text, DOCUMENT_ACTION_KEYWORDS)
    action_matches = extract_matched_phrases(full_text, ACTION_REQUEST_KEYWORDS)
    low_matches = extract_matched_phrases(full_text, LOW_PRIORITY_INDICATORS)
    
    deadline_info = analyze_deadline(body, csv_deadline)
    
    # Priority Decision Logic
    priority = "LOW"
    reasons = []
    suggested_actions = []
    
    # Step 1: Bid rejection / Disqualification / Tender risk -> HIGH
    if high_risk_matches:
        priority = "HIGH"
        reasons.append(f"Tender risk / Disqualification alert: mentions {', '.join([repr(w) for w in high_risk_matches[:3]])}")
        if doc_matches:
            suggested_actions.append(f"Immediately prepare and submit requested document ({', '.join(doc_matches[:2])})")
        else:
            suggested_actions.append("Review tender dossier urgently and contact tender officer to prevent disqualification")
            
    # Step 2: Document / Action Requests
    elif doc_matches or action_matches:
        # Check if urgent wording or impending deadline elevates to HIGH or stays MEDIUM
        has_urgent_clause = bool(re.search(r"\b(?:urgent|clarification|missing|cure notice|penalty)\b", full_text, re.IGNORECASE))
        priority = "HIGH" if has_urgent_clause and ("missing" in full_text.lower() or "notice" in full_text.lower()) else "MEDIUM"
        
        if doc_matches:
            reasons.append(f"Document request identified: {', '.join([repr(w) for w in doc_matches[:3]])}")
            suggested_actions.append(f"Verify and furnish requested compliance item ({', '.join(doc_matches[:2])})")
        if action_matches:
            reasons.append(f"Action/clarification requested: {', '.join([repr(w) for w in action_matches[:2]])}")
            if not suggested_actions:
                suggested_actions.append("Review query and provide official response before deadline")
                
    # Step 3: Low / Informational
    else:
        priority = "LOW"
        if low_matches:
            reasons.append(f"Routine or informational update: mentions {', '.join([repr(w) for w in low_matches[:2]])}")
        else:
            reasons.append("General correspondence with no urgent action items detected")
        suggested_actions.append("No immediate action required. Archive or monitor for follow-up.")

    # Deadline adjustment if deadline is today and priority is not high
    if "today" in body.lower() and priority == "MEDIUM":
        priority = "HIGH"
        reasons.append("Same-day deadline elevated priority to HIGH")

    all_noticed_words = list(dict.fromkeys(high_risk_matches + doc_matches + action_matches + deadline_info["extracted_dates"]))
    
    return {
        "priority": priority,
        "trigger_reasons": reasons,
        "primary_reason": " | ".join(reasons),
        "suggested_action": " & ".join(suggested_actions) if suggested_actions else "Human verification required",
        "words_noticed": all_noticed_words,
        "deadline_info": deadline_info
    }


def find_duplicates(emails: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Identifies duplicate emails based on subject and normalized body text.
    Returns mapping of email_id -> list of duplicate email_ids.
    """
    seen_hashes: Dict[str, List[str]] = {}
    for email in emails:
        norm_subj = re.sub(r"\s+", " ", str(email.get("subject", "")).strip().lower())
        norm_body = re.sub(r"\s+", " ", str(email.get("body", ""))[:120].strip().lower())
        sig = f"{norm_subj}||{norm_body}"
        seen_hashes.setdefault(sig, []).append(str(email.get("id")))
        
    duplicates: Dict[str, List[str]] = {}
    for sig, ids in seen_hashes.items():
        if len(ids) > 1:
            for eid in ids:
                duplicates[eid] = [other for other in ids if other != eid]
    return duplicates
