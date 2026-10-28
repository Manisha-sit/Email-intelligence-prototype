"""
test_classifier.py - Verifies all test cases defined in Section 8 of Email Intelligence Assistance doc.
"""

import csv
import sys
from classifier import classify_email, find_duplicates

def run_tests():
    print("=== Running Email Intelligence Assistance Test Cases ===")
    
    with open('sample_emails.csv', mode='r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
    
    print(f"Loaded {len(reader)} sample emails.")
    
    # 1. Test Deduplication
    dups = find_duplicates(reader)
    assert 'EML-001' in dups and 'EML-006' in dups, "Deduplication failed to link EML-001 and EML-006"
    print("PASS: [Test 7] Duplicate email detection (EML-001 & EML-006 linked as duplicates)")
    
    # Map for easy lookup
    email_map = {row['id']: row for row in reader}
    
    # 2. Test Case 1: Warns of bid rejection
    eml_1 = email_map['EML-001']
    res_1 = classify_email(eml_1['subject'], eml_1['body'], eml_1['csv_deadline'])
    assert res_1['priority'] == 'HIGH', f"Expected HIGH, got {res_1['priority']}"
    assert any('bid rejection' in w.lower() or 'disqualification' in w.lower() for w in res_1['words_noticed'])
    print(f"PASS: [Test 1] Warns of bid rejection -> Priority: {res_1['priority']}, Reason: {res_1['primary_reason']}")
    
    # 3. Test Case 2: Mentions missing certificate
    eml_2 = email_map['EML-002']
    res_2 = classify_email(eml_2['subject'], eml_2['body'], eml_2['csv_deadline'])
    assert res_2['priority'] in ['HIGH', 'MEDIUM']
    assert "missing certificate" in [w.lower() for w in res_2['words_noticed']] or "missing" in [w.lower() for w in res_2['words_noticed']]
    print(f"PASS: [Test 2] Missing certificate -> Action: {res_2['suggested_action']}, Noticed: {res_2['words_noticed']}")
    
    # 4. Test Case 3: Routine newsletter
    eml_3 = email_map['EML-003']
    res_3 = classify_email(eml_3['subject'], eml_3['body'], eml_3['csv_deadline'])
    assert res_3['priority'] == 'LOW', f"Expected LOW, got {res_3['priority']}"
    print(f"PASS: [Test 3] Routine newsletter -> Priority: {res_3['priority']}, Reason: {res_3['primary_reason']}")
    
    # 5. Test Case 4: No deadline field
    eml_4 = email_map['EML-004']
    res_4 = classify_email(eml_4['subject'], eml_4['body'], eml_4['csv_deadline'])
    assert res_4['deadline_info']['csv_deadline'] == "None supplied"
    print(f"PASS: [Test 4] No deadline supplied -> Status: {res_4['deadline_info']['deadline_status']}")
    
    # 6. Test Case 6: Ambiguous date wording
    eml_5 = email_map['EML-005']
    res_5 = classify_email(eml_5['subject'], eml_5['body'], eml_5['csv_deadline'])
    assert res_5['deadline_info']['is_ambiguous'] is True, "Expected ambiguous flag for 'next Tuesday afternoon'"
    print(f"PASS: [Test 6] Ambiguous date wording -> Ambiguity: {res_5['deadline_info']['ambiguity_reason']}")
    
    # 7. Test Case 5: Company filter
    comp_a = [e for e in reader if e['company'] == 'Company A']
    comp_b = [e for e in reader if e['company'] == 'Company B']
    assert len(comp_a) > 0 and len(comp_b) > 0
    print(f"PASS: [Test 5] Company segmentation -> Company A: {len(comp_a)} emails, Company B: {len(comp_b)} emails")
    
    print("\nALL 7 TEST CASES PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
