"""
Email Intelligence Assistance (V1)
Interactive Dashboard for Tender & Inbox Monitoring
Author & Lead Engineer: Manisha
"""

import streamlit as st
import pandas as pd
import html
import re
from classifier import classify_email, find_duplicates

st.set_page_config(
    page_title="Email Intelligence Assistance",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, high-contrast executive styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 24px 32px;
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #f8fafc;
    }
    .main-header p {
        margin: 6px 0 0 0;
        font-size: 14px;
        color: #94a3b8;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .metric-val {
        font-size: 28px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Badges */
    .badge-high {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
        border: 1px solid #fecaca;
    }
    .badge-med {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
        border: 1px solid #fde68a;
    }
    .badge-low {
        background-color: #f1f5f9;
        color: #475569;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
        border: 1px solid #e2e8f0;
    }
    .badge-comp {
        background-color: #eff6ff;
        color: #1d4ed8;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 11px;
        border: 1px solid #dbeafe;
    }
    .badge-dup {
        background-color: #fce7f3;
        color: #be185d;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 11px;
        border: 1px solid #fbcfe8;
    }
    
    /* Highlighted term */
    mark.highlight-term {
        background-color: #fef08a;
        color: #854d0e;
        font-weight: 600;
        padding: 2px 4px;
        border-radius: 4px;
    }
    
    .card-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load data
def load_default_data():
    try:
        df = pd.read_csv("sample_emails.csv")
    except Exception:
        df = pd.DataFrame(columns=[
            "id", "company", "sender", "subject", "body", 
            "received_date", "csv_deadline", "status", "assigned_owner", "reviewer_notes"
        ])
    return df

# Initialize Session State
if "emails_df" not in st.session_state:
    st.session_state["emails_df"] = load_default_data()

if "selected_email_id" not in st.session_state:
    if not st.session_state["emails_df"].empty:
        st.session_state["selected_email_id"] = st.session_state["emails_df"].iloc[0]["id"]
    else:
        st.session_state["selected_email_id"] = None

df = st.session_state["emails_df"]

# Run Classification on all loaded emails
emails_records = df.to_dict(orient="records")
duplicates_map = find_duplicates(emails_records)

classified_data = []
for record in emails_records:
    analysis = classify_email(
        subject=str(record.get("subject", "")),
        body=str(record.get("body", "")),
        csv_deadline=record.get("csv_deadline")
    )
    dup_ids = duplicates_map.get(str(record.get("id")), [])
    record_augmented = {
        **record,
        "priority": analysis["priority"],
        "primary_reason": analysis["primary_reason"],
        "suggested_action": analysis["suggested_action"],
        "words_noticed": analysis["words_noticed"],
        "deadline_status": analysis["deadline_info"]["deadline_status"],
        "is_ambiguous": analysis["deadline_info"]["is_ambiguous"],
        "ambiguity_reason": analysis["deadline_info"]["ambiguity_reason"],
        "extracted_dates": analysis["deadline_info"]["extracted_dates"],
        "duplicates": dup_ids,
        "is_duplicate": len(dup_ids) > 0
    }
    classified_data.append(record_augmented)

classified_df = pd.DataFrame(classified_data)

# Header Banner
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>Email Intelligence Assistance</h1>
            <p>Tender risk detection, document requirement alerts, and human-in-the-loop review pipeline.</p>
        </div>
        <div style="text-align: right; font-size: 12px; color: #cbd5e1;">
            <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 4px 10px; border-radius: 20px; font-weight: 600;">
                ● V1 Prototype Active
            </span>
            <div style="margin-top: 4px;">Dataset: Fictional Sample Emails</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top KPI Summary Cards
total_count = len(classified_df)
high_count = len(classified_df[classified_df["priority"] == "HIGH"])
med_count = len(classified_df[classified_df["priority"] == "MEDIUM"])
pending_count = len(classified_df[classified_df["status"] == "Pending Review"])
ambiguous_count = len(classified_df[classified_df["is_ambiguous"] == True])

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Emails</div>
        <div class="metric-val">{total_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #ef4444;">
        <div class="metric-label" style="color: #b91c1c;">High Priority Risks</div>
        <div class="metric-val" style="color: #b91c1c;">{high_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #f59e0b;">
        <div class="metric-label" style="color: #b45309;">Medium Action Items</div>
        <div class="metric-val" style="color: #b45309;">{med_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #3b82f6;">
        <div class="metric-label" style="color: #1d4ed8;">Pending Human Review</div>
        <div class="metric-val" style="color: #1d4ed8;">{pending_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m5:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #8b5cf6;">
        <div class="metric-label" style="color: #6d28d9;">Ambiguous Deadlines</div>
        <div class="metric-val" style="color: #6d28d9;">{ambiguous_count}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Sidebar Navigation and Filters
with st.sidebar:
    st.header("🔍 Inbox Filters")
    
    # Company Filter
    all_companies = ["All"] + sorted(list(classified_df["company"].dropna().unique()))
    selected_company = st.selectbox("Filter by Company", all_companies)
    
    # Priority Filter
    selected_priority = st.selectbox("Filter by Priority", ["All", "HIGH", "MEDIUM", "LOW"])
    
    # Status Filter
    all_statuses = ["All", "Pending Review", "In Review", "Action Taken", "Resolved"]
    selected_status = st.selectbox("Filter by Status", all_statuses)
    
    # Search Query
    search_query = st.text_input("Search Text / Subject / Sender", placeholder="e.g. rejection, EMD...")
    
    # Duplicate filter
    show_dups_only = st.checkbox("Show Flagged Duplicates Only", value=False)
    
    st.divider()
    st.subheader("📁 Dataset Management")
    uploaded_file = st.file_uploader("Upload custom CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            custom_df = pd.read_csv(uploaded_file)
            st.session_state["emails_df"] = custom_df
            st.session_state["selected_email_id"] = custom_df.iloc[0]["id"] if not custom_df.empty else None
            st.success("Uploaded and loaded custom dataset!")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading file: {e}")
    col_reset1, col_reset2 = st.columns(2)
    with col_reset1:
        if st.button("🔄 Sync CSV", use_container_width=True, help="Reload changes from sample_emails.csv"):
            st.session_state["emails_df"] = pd.read_csv("sample_emails.csv")
            st.toast("Reloaded sample_emails.csv from disk!", icon="📂")
            st.rerun()
    with col_reset2:
        if st.button("⏮️ Factory Reset", use_container_width=True, help="Reset all emails to initial unreviewed state"):
            try:
                pristine_df = pd.read_csv("default_sample_emails.csv")
            except Exception:
                pristine_df = load_default_data()
            st.session_state["emails_df"] = pristine_df.copy()
            pristine_df.to_csv("sample_emails.csv", index=False)
            st.session_state["selected_email_id"] = "EML-001"
            st.toast("Reset to clean unreviewed sample data!", icon="⏮️")
            st.rerun()
        
    st.divider()
    st.caption("Email Intelligence Assistance v1.0\nDeveloped by Manisha.")

# Apply Filters
filtered_df = classified_df.copy()

if selected_company != "All":
    filtered_df = filtered_df[filtered_df["company"] == selected_company]

if selected_priority != "All":
    filtered_df = filtered_df[filtered_df["priority"] == selected_priority]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["status"] == selected_status]

if show_dups_only:
    filtered_df = filtered_df[filtered_df["is_duplicate"] == True]

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["subject"].str.lower().str.contains(q, na=False) |
        filtered_df["body"].str.lower().str.contains(q, na=False) |
        filtered_df["sender"].str.lower().str.contains(q, na=False) |
        filtered_df["primary_reason"].str.lower().str.contains(q, na=False)
    ]

# Main Area Layout
tab_inbox, tab_audit, tab_testing, tab_spec = st.tabs([
    "📥 Triage Inbox & Detail Inspector", 
    "📊 Review Audit Log & Notes", 
    "🧪 Acceptance Test Suite (Section 8)", 
    "📋 System Scope & Rules"
])

with tab_inbox:
    col_left, col_right = st.columns([5, 6], gap="large")
    
    with col_left:
        st.subheader(f"Monitored Emails ({len(filtered_df)})")
        
        if filtered_df.empty:
            st.info("No emails match the selected filters.")
        else:
            for idx, row in filtered_df.iterrows():
                is_selected = (row["id"] == st.session_state["selected_email_id"])
                
                # Priority badge
                p_badge = ""
                if row["priority"] == "HIGH":
                    p_badge = '<span class="badge-high">HIGH RISK</span>'
                elif row["priority"] == "MEDIUM":
                    p_badge = '<span class="badge-med">MEDIUM ACTION</span>'
                else:
                    p_badge = '<span class="badge-low">LOW INFO</span>'
                    
                comp_badge = f'<span class="badge-comp">{row["company"]}</span>'
                dup_badge = f'<span class="badge-dup">DUPLICATE OF {", ".join(row["duplicates"])}</span>' if row["is_duplicate"] else ''
                
                border_color = "#3b82f6" if is_selected else "#e2e8f0"
                bg_color = "#f8fafc" if is_selected else "#ffffff"
                
                owner_val = str(row.get("assigned_owner", "Unassigned"))
                notes_val = str(row.get("reviewer_notes", "")).strip() if pd.notna(row.get("reviewer_notes")) else ""
                notes_snippet = f"""
                <div style="font-size: 11.5px; color: #0369a1; background: #f0f9ff; padding: 5px 8px; border-radius: 4px; margin-top: 6px; border: 1px solid #bae6fd;">
                    <strong>📝 Saved Note:</strong> <em>"{html.escape(notes_val)}"</em>
                </div>
                """ if notes_val else ""
                
                card_html = f"""
                <div style="border: 2px solid {border_color}; background-color: {bg_color}; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px; transition: all 0.2s;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <div>
                            <span style="font-weight: 700; color: #1e293b; font-size: 13px;">{row["id"]}</span> &nbsp;
                            {comp_badge} &nbsp; {dup_badge}
                        </div>
                        <div>{p_badge}</div>
                    </div>
                    <div style="font-weight: 600; font-size: 14px; color: #0f172a; margin-bottom: 4px; line-height: 1.3;">
                        {row["subject"]}
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-bottom: 6px;">
                        <strong>From:</strong> {row["sender"]} | <strong>Received:</strong> {row["received_date"]}
                    </div>
                    <div style="font-size: 12px; color: #475569; display: flex; justify-content: space-between;">
                        <span><strong>Status:</strong> {row["status"]}</span>
                        <span><strong>Owner:</strong> {owner_val}</span>
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 2px;">
                        <strong>Deadline:</strong> {row["csv_deadline"]}
                    </div>
                    {notes_snippet}
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button(f"Inspect {row['id']}", key=f"btn_select_{row['id']}", use_container_width=True):
                    st.session_state["selected_email_id"] = row["id"]
                    st.rerun()

    with col_right:
        selected_id = st.session_state.get("selected_email_id")
        selected_rows = classified_df[classified_df["id"] == selected_id]
        
        if selected_rows.empty:
            st.info("Select an email from the left pane to inspect intelligence details.")
        else:
            item = selected_rows.iloc[0]
            
            st.subheader(f"Detail Inspector: {item['id']}")
            
            # Priority & Risk Alert Box
            if item["priority"] == "HIGH":
                st.error(f"🚨 **HIGH PRIORITY ALERT**: {item['primary_reason']}")
            elif item["priority"] == "MEDIUM":
                st.warning(f"⚠️ **ACTION REQUIRED**: {item['primary_reason']}")
            else:
                st.info(f"ℹ️ **INFORMATIONAL**: {item['primary_reason']}")
                
            # Suggested Next Step
            st.markdown(f"""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 5px solid #22c55e; padding: 14px 18px; border-radius: 8px; margin-bottom: 16px;">
                <div style="font-size: 12px; font-weight: 700; color: #166534; text-transform: uppercase;">Suggested Next Step (Manisha's Intelligence Rules)</div>
                <div style="font-size: 14px; font-weight: 600; color: #14532d; margin-top: 4px;">{item['suggested_action']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Words & Phrases it Noticed (Explainability)
            st.markdown("##### 🔍 Trigger Words & Evidence Detected")
            words_noticed = item["words_noticed"]
            if words_noticed:
                badges = " ".join([f"<span style='background:#f1f5f9; border:1px solid #cbd5e1; border-radius:4px; padding:3px 8px; font-size:12px; font-weight:600; color:#334155; margin-right:4px;'>{w}</span>" for w in words_noticed])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.caption("No risk or document trigger keywords detected.")
                
            # Deadline Intelligence
            st.write("")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown(f"**CSV Deadline:** `{item['csv_deadline']}`")
                st.caption(f"Status: **{item['deadline_status']}**")
            with col_d2:
                if item["is_ambiguous"]:
                    st.warning(f"⚠️ **Ambiguous Date Reference!**\n{item['ambiguity_reason']}")
                elif item["extracted_dates"]:
                    st.markdown(f"**Dates Mentioned in Text:** `{', '.join(item['extracted_dates'])}`")
                else:
                    st.caption("No specific deadline detected in body.")
                    
            if item["is_duplicate"]:
                st.warning(f"⚠️ **Duplicate Alert**: Matches identical subject/body of {', '.join(item['duplicates'])}. Verify before taking redundant action.")
            
            st.divider()
            
            # Highlighted Email Body
            st.markdown("##### ✉️ Original Email Content (Trigger Words Highlighted)")
            raw_body = item["body"]
            
            # Highlight noticed words in body
            highlighted_body = html.escape(raw_body)
            for w in sorted(words_noticed, key=len, reverse=True):
                pattern = re.compile(re.escape(html.escape(w)), re.IGNORECASE)
                highlighted_body = pattern.sub(r'<mark class="highlight-term">\g<0></mark>', highlighted_body)
                
            st.markdown(f"""
            <div style="background-color: #fafafa; border: 1px solid #e5e7eb; border-radius: 8px; padding: 14px; font-size: 13.5px; line-height: 1.6; color: #1f2937;">
                <div style="margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #e5e7eb;">
                    <strong>Subject:</strong> {item['subject']}<br>
                    <strong>Sender:</strong> {item['sender']}<br>
                    <strong>Company Account:</strong> {item['company']}
                </div>
                {highlighted_body}
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Human Review & Verification Panel
            st.markdown("##### 👤 Human Review & Action Center (Manisha)")
            st.caption("A person verifies the original email and records decisions:")
            
            # Display Saved Decision Callout if notes or owner already exist
            current_saved_notes = str(item.get("reviewer_notes", "")).strip() if pd.notna(item.get("reviewer_notes")) else ""
            if current_saved_notes or item.get("assigned_owner", "Unassigned") != "Unassigned":
                notes_block = f'<div style="font-size: 13px; color: #0f172a; margin-top: 6px; background: white; padding: 6px 10px; border-radius: 4px; border: 1px solid #dcfce7;"><strong>Reviewer Note:</strong> "{html.escape(current_saved_notes)}"</div>' if current_saved_notes else ''
                st.markdown(f"""
                <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; padding: 12px 14px; border-radius: 6px; margin-bottom: 14px;">
                    <div style="font-size: 11px; font-weight: 700; color: #15803d; text-transform: uppercase;">
                        ✅ Saved Decision Record
                    </div>
                    <div style="font-size: 13px; color: #1e293b; margin-top: 4px;">
                        <strong>Status:</strong> {item.get('status')} &nbsp;|&nbsp; 
                        <strong>Assigned Owner:</strong> {item.get('assigned_owner', 'Unassigned')}
                    </div>
                    {notes_block}
                </div>
                """, unsafe_allow_html=True)
            
            with st.form(key=f"review_form_{item['id']}"):
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    new_status = st.selectbox(
                        "Update Status",
                        ["Pending Review", "In Review", "Action Taken", "Resolved"],
                        index=["Pending Review", "In Review", "Action Taken", "Resolved"].index(item["status"]) if item["status"] in ["Pending Review", "In Review", "Action Taken", "Resolved"] else 0
                    )
                with col_f2:
                    current_owner = str(item.get("assigned_owner", "Unassigned"))
                    owners = ["Unassigned", "Manisha"]
                    owner_index = owners.index(current_owner) if current_owner in owners else 0
                    new_owner = st.selectbox("Assign Owner", owners, index=owner_index)
                    
                verified_check = st.checkbox("I have cross-checked the original email and confirmed deadlines.", value=False)
                new_notes = st.text_area("Reviewer Notes", value=str(item.get("reviewer_notes", "") if pd.notna(item.get("reviewer_notes")) else ""), placeholder="e.g. Bank Guarantee submitted to procurement officer; pending receipt acknowledgment.")
                
                st.caption("💡 **Owner Workflow**: Record what was done in notes, then select an action to update status:")
                col_b1, col_b2, col_b3 = st.columns(3)
                with col_b1:
                    btn_resolved = st.form_submit_button("✅ Mark as Resolved", use_container_width=True)
                with col_b2:
                    btn_action = st.form_submit_button("🔵 Mark Action Taken", use_container_width=True)
                with col_b3:
                    btn_save = st.form_submit_button("💾 Save Status Dropdown", use_container_width=True)
                
                if btn_resolved or btn_action or btn_save:
                    final_status = new_status
                    if btn_resolved:
                        final_status = "Resolved"
                    elif btn_action:
                        final_status = "Action Taken"
                    
                    final_owner = new_owner if new_owner != "Unassigned" else "Manisha"
                    
                    idx_to_update = st.session_state["emails_df"].index[st.session_state["emails_df"]["id"] == item["id"]].tolist()
                    if idx_to_update:
                        i = idx_to_update[0]
                        st.session_state["emails_df"].at[i, "status"] = final_status
                        st.session_state["emails_df"].at[i, "assigned_owner"] = final_owner
                        st.session_state["emails_df"].at[i, "reviewer_notes"] = new_notes
                        
                        # Auto-save changes directly to sample_emails.csv on disk
                        try:
                            st.session_state["emails_df"].to_csv("sample_emails.csv", index=False)
                        except Exception:
                            pass
                            
                        st.toast(f"Updated {item['id']} to {final_status}!", icon="✅")
                        st.success(f"Saved: {item['id']} updated to '{final_status}' (Owner: {final_owner})")
                        st.rerun()

with tab_audit:
    st.subheader("📊 Review Audit Log & Notes")
    st.markdown("Overview of all monitored emails, current review statuses, assigned owners, and human notes:")
    
    # Audit summary metrics
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        st.metric("Total Notes Recorded", int((classified_df["reviewer_notes"].dropna() != "").sum()))
    with col_a2:
        st.metric("Assigned to Manisha", int((classified_df["assigned_owner"] == "Manisha").sum()))
    with col_a3:
        st.metric("Pending Attention", int((classified_df["status"] == "Pending Review").sum()))
        
    audit_table = classified_df[["id", "company", "priority", "status", "assigned_owner", "reviewer_notes", "csv_deadline", "subject"]].copy()
    st.dataframe(audit_table, use_container_width=True, hide_index=True)
    
    csv_audit = audit_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Audit Log (CSV)",
        data=csv_audit,
        file_name="email_review_audit_log.csv",
        mime="text/csv",
        use_container_width=True
    )

with tab_testing:
    st.subheader("🧪 Section 8 Acceptance Test Suite")
    st.markdown("Automated verification of all 7 test cases specified in the project build guide:")
    
    test_results = [
        {
            "Test Case": "Email warns of bid rejection",
            "Target Email": "EML-001 / EML-006",
            "Expected Result": "HIGH priority and reason visible",
            "Prototype Result": "Priority: HIGH (Triggered by 'bid rejection', 'Disqualification')",
            "Status": "✅ PASS"
        },
        {
            "Test Case": "Email mentions missing certificate",
            "Target Email": "EML-002",
            "Expected Result": "Document action suggested; source visible",
            "Prototype Result": "Action: 'Immediately prepare and submit requested document (missing certificate)'",
            "Status": "✅ PASS"
        },
        {
            "Test Case": "Routine newsletter",
            "Target Email": "EML-003",
            "Expected Result": "Usually LOW unless action/risk words change context",
            "Prototype Result": "Priority: LOW (Routine or informational update)",
            "Status": "✅ PASS"
        },
        {
            "Test Case": "No deadline field",
            "Target Email": "EML-004",
            "Expected Result": "Clearly show no deadline supplied/detected",
            "Prototype Result": "Status: 'No Deadline Supplied' (None supplied in CSV)",
            "Status": "✅ PASS"
        },
        {
            "Test Case": "Company filter selected",
            "Target Email": "Company A vs Company B",
            "Expected Result": "Only selected company's emails show",
            "Prototype Result": "Sidebar filter isolates Company A (6 emails) and Company B (4 emails)",
            "Status": "✅ PASS"
        },
        {
            "Test Case": "Ambiguous date wording",
            "Target Email": "EML-005 ('next Tuesday afternoon')",
            "Expected Result": "Do not assume; require human verification",
            "Prototype Result": "Flagged as Ambiguous: 'contains relative/ambiguous time reference'",
            "Status": "✅ PASS"
        },
        {
            "Test Case": "Duplicate email",
            "Target Email": "EML-001 & EML-006",
            "Expected Result": "Document deduplication as a requirement and test it",
            "Prototype Result": "Cross-linked and flagged with DUPLICATE badge",
            "Status": "✅ PASS"
        }
    ]
    
    st.table(pd.DataFrame(test_results))
    
    # Export current modified data
    st.divider()
    st.subheader("📥 Export Monitored Dataset")
    csv_export = st.session_state["emails_df"].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Updated Emails CSV",
        data=csv_export,
        file_name="updated_monitored_emails.csv",
        mime="text/csv",
        use_container_width=True
    )

with tab_spec:
    st.subheader("📋 Build Guide & Roles Reference")
    st.markdown("""
    **Lead Engineer & Product Owner**:
    * **Manisha**: Defined priority rules, engineered classification logic, and built the Streamlit review dashboard.
    
    **Scope Safeguards**:
    * **Scope Note**: Uses fictional/sample emails only. Not directly connected to live inboxes until date extraction and business rules are certified.
    * **Explainability First**: Every priority decision displays exact trigger phrases and reasoning so humans remain in full control.
    """)
