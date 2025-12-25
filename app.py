import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="PRISMA & CASP Research Tool",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'prisma_data' not in st.session_state:
    st.session_state.prisma_data = {
        'identification': {'databases': 0, 'registers': 0, 'other': 0},
        'duplicates': 0,
        'screened': 0,
        'excluded': 0,
        'soughtRetrieval': 0,
        'notRetrieved': 0,
        'assessed': 0,
        'included': 0
    }

if 'studies' not in st.session_state:
    st.session_state.studies = []

# CASP Questions
CASP_QUESTIONS = {
    'RCT': [
        "Did the trial address a clearly focused issue?",
        "Was the assignment of patients to treatments randomized?",
        "Were all patients properly accounted for at its conclusion?",
        "Were patients, health workers and study personnel 'blind' to treatment?",
        "Were the groups similar at the start of the trial?",
        "Aside from the experimental intervention, were the groups treated equally?",
        "How large was the treatment effect?",
        "How precise was the estimate of the treatment effect?",
        "Can the results be applied to the local population?",
        "Were all clinically important outcomes considered?",
        "Are the benefits worth the harms and costs?"
    ],
    'Cohort': [
        "Did the study address a clearly focused issue?",
        "Was the cohort recruited in an acceptable way?",
        "Was the exposure accurately measured to minimize bias?",
        "Was the outcome accurately measured to minimize bias?",
        "Have the authors identified all important confounding factors?",
        "Was the follow up of subjects complete enough?",
        "What are the results of this study?",
        "How precise are the results?",
        "Do you believe the results?",
        "Can the results be applied to the local population?",
        "Do the results fit with other available evidence?"
    ],
    'Systematic': [
        "Did the review address a clearly focused question?",
        "Did the authors look for the right type of papers?",
        "Do you think all the important, relevant studies were included?",
        "Did the review's authors do enough to assess quality of the included studies?",
        "If the results have been combined, was it reasonable to do so?",
        "What are the overall results of the review?",
        "How precise are the results?",
        "Can the results be applied to the local population?",
        "Were all important outcomes considered?",
        "Are the benefits worth the harms and costs?"
    ]
}

def calculate_quality_score(study):
    """Calculate quality score for a study"""
    answered = sum(1 for score in study['casp_scores'] if score is not None)
    yes_count = sum(1 for score in study['casp_scores'] if score == 'Yes')
    return (yes_count / answered * 100) if answered > 0 else 0

def get_quality_rating(score):
    """Get quality rating based on score"""
    if score >= 80:
        return 'High', '🟢'
    elif score >= 60:
        return 'Moderate', '🟡'
    else:
        return 'Low', '🔴'

def export_report():
    """Generate report text"""
    pd = st.session_state.prisma_data
    total = pd['identification']['databases'] + pd['identification']['registers'] + pd['identification']['other']
    
    report = f"""PRISMA Flow Diagram Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

IDENTIFICATION
- Records from databases: {pd['identification']['databases']}
- Records from registers: {pd['identification']['registers']}
- Records from other sources: {pd['identification']['other']}
- Total records identified: {total}

SCREENING
- Records removed as duplicates: {pd['duplicates']}
- Records screened: {pd['screened']}
- Records excluded: {pd['excluded']}

ELIGIBILITY
- Reports sought for retrieval: {pd['soughtRetrieval']}
- Reports not retrieved: {pd['notRetrieved']}
- Reports assessed for eligibility: {pd['assessed']}

INCLUDED
- Studies included in review: {pd['included']}

CASP APPRAISAL SUMMARY
Total studies appraised: {len(st.session_state.studies)}

"""
    
    for i, study in enumerate(st.session_state.studies, 1):
        score = calculate_quality_score(study)
        rating, _ = get_quality_rating(score)
        report += f"""
Study {i}: {study['title']}
- Author: {study['author']} ({study['year']})
- Type: {study['study_type']}
- Quality Score: {score:.1f}%
- Rating: {rating}
"""
        if study['notes']:
            report += f"- Notes: {study['notes']}\n"
    
    return report

# Header
st.title("📊 PRISMA & CASP Research Tool")
st.markdown("**Systematic Review Management & Quality Appraisal**")
st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 PRISMA Flow", "✅ CASP Appraisal", "📈 Summary"])

# TAB 1: PRISMA FLOW
with tab1:
    st.header("PRISMA Flow Diagram")
    
    # Identification
    st.markdown("### 🔍 Identification")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.prisma_data['identification']['databases'] = st.number_input(
            "Database Records", 
            min_value=0, 
            value=st.session_state.prisma_data['identification']['databases'],
            key='db_records'
        )
    with col2:
        st.session_state.prisma_data['identification']['registers'] = st.number_input(
            "Register Records", 
            min_value=0, 
            value=st.session_state.prisma_data['identification']['registers'],
            key='reg_records'
        )
    with col3:
        st.session_state.prisma_data['identification']['other'] = st.number_input(
            "Other Sources", 
            min_value=0, 
            value=st.session_state.prisma_data['identification']['other'],
            key='other_records'
        )
    
    # Screening
    st.markdown("### 🔎 Screening")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.prisma_data['duplicates'] = st.number_input(
            "Duplicates Removed", 
            min_value=0, 
            value=st.session_state.prisma_data['duplicates'],
            key='duplicates'
        )
    with col2:
        st.session_state.prisma_data['screened'] = st.number_input(
            "Records Screened", 
            min_value=0, 
            value=st.session_state.prisma_data['screened'],
            key='screened'
        )
    with col3:
        st.session_state.prisma_data['excluded'] = st.number_input(
            "Records Excluded", 
            min_value=0, 
            value=st.session_state.prisma_data['excluded'],
            key='excluded'
        )
    
    # Eligibility
    st.markdown("### 📝 Eligibility")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.prisma_data['soughtRetrieval'] = st.number_input(
            "Sought for Retrieval", 
            min_value=0, 
            value=st.session_state.prisma_data['soughtRetrieval'],
            key='sought'
        )
    with col2:
        st.session_state.prisma_data['notRetrieved'] = st.number_input(
            "Not Retrieved", 
            min_value=0, 
            value=st.session_state.prisma_data['notRetrieved'],
            key='not_retrieved'
        )
    with col3:
        st.session_state.prisma_data['assessed'] = st.number_input(
            "Assessed for Eligibility", 
            min_value=0, 
            value=st.session_state.prisma_data['assessed'],
            key='assessed'
        )
    
    # Included
    st.markdown("### ✅ Included")
    st.session_state.prisma_data['included'] = st.number_input(
        "Studies Included", 
        min_value=0, 
        value=st.session_state.prisma_data['included'],
        key='included'
    )

# TAB 2: CASP APPRAISAL
with tab2:
    st.header("CASP Quality Appraisal")
    
    # Add new study form
    with st.expander("➕ Add New Study", expanded=len(st.session_state.studies) == 0):
        with st.form("add_study_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Study Title*")
                author = st.text_input("Author(s)*")
            with col2:
                year = st.text_input("Year")
                study_type = st.selectbox(
                    "Study Type",
                    ["RCT", "Cohort", "Systematic"],
                    format_func=lambda x: {
                        "RCT": "Randomized Controlled Trial",
                        "Cohort": "Cohort Study",
                        "Systematic": "Systematic Review"
                    }[x]
                )
            
            submitted = st.form_submit_button("Add Study")
            if submitted:
                if title and author:
                    new_study = {
                        'id': len(st.session_state.studies),
                        'title': title,
                        'author': author,
                        'year': year,
                        'study_type': study_type,
                        'casp_scores': [None] * len(CASP_QUESTIONS[study_type]),
                        'notes': ''
                    }
                    st.session_state.studies.append(new_study)
                    st.success(f"✅ Added: {title}")
                    st.rerun()
                else:
                    st.error("Please fill in Title and Author fields")
    
    # Display studies
    if st.session_state.studies:
        for idx, study in enumerate(st.session_state.studies):
            with st.expander(f"📄 {study['title']} - {study['author']} ({study['year']})", expanded=False):
                
                # Study info and quality score
                score = calculate_quality_score(study)
                rating, emoji = get_quality_rating(score)
                st.markdown(f"**Study Type:** {study['study_type']}")
                st.markdown(f"**Quality Score:** {score:.1f}% {emoji} {rating}")
                
                st.divider()
                
                # CASP questions
                questions = CASP_QUESTIONS[study['study_type']]
                for q_idx, question in enumerate(questions):
                    st.markdown(f"**{q_idx + 1}.** {question}")
                    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
                    
                    with col1:
                        if st.button("Yes", key=f"yes_{idx}_{q_idx}"):
                            st.session_state.studies[idx]['casp_scores'][q_idx] = 'Yes'
                            st.rerun()
                    with col2:
                        if st.button("No", key=f"no_{idx}_{q_idx}"):
                            st.session_state.studies[idx]['casp_scores'][q_idx] = 'No'
                            st.rerun()
                    with col3:
                        if st.button("Unclear", key=f"unclear_{idx}_{q_idx}"):
                            st.session_state.studies[idx]['casp_scores'][q_idx] = 'Unclear'
                            st.rerun()
                    with col4:
                        current = study['casp_scores'][q_idx]
                        if current:
                            color = {'Yes': '🟢', 'No': '🔴', 'Unclear': '🟡'}[current]
                            st.markdown(f"{color} **{current}**")
                
                st.divider()
                
                # Notes
                notes = st.text_area(
                    "Notes",
                    value=study['notes'],
                    key=f"notes_{idx}",
                    height=100
                )
                if notes != study['notes']:
                    st.session_state.studies[idx]['notes'] = notes
                
                # Delete button
                if st.button(f"🗑️ Delete Study", key=f"delete_{idx}", type="secondary"):
                    st.session_state.studies.pop(idx)
                    st.rerun()
    else:
        st.info("No studies added yet. Use the form above to add your first study.")

# TAB 3: SUMMARY
with tab3:
    st.header("Summary & Export")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("📥 Export Report", type="primary"):
            report = export_report()
            st.download_button(
                label="Download TXT",
                data=report,
                file_name=f"prisma-casp-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt",
                mime="text/plain"
            )
    
    # PRISMA Summary
    st.subheader("📊 PRISMA Flow Summary")
    pd = st.session_state.prisma_data
    total_identified = pd['identification']['databases'] + pd['identification']['registers'] + pd['identification']['other']
    after_duplicates = total_identified - pd['duplicates']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records Identified", total_identified)
    with col2:
        st.metric("After Duplicates Removed", after_duplicates)
    with col3:
        st.metric("Records Screened", pd['screened'])
    with col4:
        st.metric("Studies Included", pd['included'])
    
    # CASP Summary
    st.subheader("✅ CASP Quality Appraisal Summary")
    st.metric("Total Studies Appraised", len(st.session_state.studies))
    
    if st.session_state.studies:
        # Create summary table
        summary_data = []
        for study in st.session_state.studies:
            score = calculate_quality_score(study)
            rating, emoji = get_quality_rating(score)
            summary_data.append({
                'Title': study['title'],
                'Author': study['author'],
                'Year': study['year'],
                'Type': study['study_type'],
                'Score': f"{score:.1f}%",
                'Rating': f"{emoji} {rating}",
                'Notes': study['notes'][:50] + '...' if len(study['notes']) > 50 else study['notes']
            })
        
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No studies have been appraised yet.")

# Footer
st.divider()
st.markdown("*PRISMA & CASP Research Tool - Systematic Review Management*")