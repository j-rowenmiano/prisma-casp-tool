import streamlit as st
import pandas as pd

st.set_page_config(page_title="Research Pipeline", layout="wide")

# --- APP STATE MANAGEMENT ---
if 'papers_df' not in st.session_state:
    # Creating a dummy template for users to start with
    st.session_state.papers_df = pd.DataFrame(columns=["Title", "Author", "Year", "CASP_Score", "Notes"])

def main():
    st.title("🔬 PRISMA & CASP Research Pipeline")
    
    tabs = st.tabs(["📊 1. PRISMA Filter", "📋 2. CASP Appraisal", "📥 3. Export Results"])

    # --- TAB 1: PRISMA ---
    with tabs[0]:
        st.header("Step 1: Study Selection")
        # (Same PRISMA code as before for the flowchart)
        db_results = st.number_input("Records identified", value=100)
        excluded = st.number_input("Records excluded", value=80)
        final_count = db_results - excluded
        st.success(f"Target number of papers for CASP: {final_count}")

    # --- TAB 2: CASP ---
    with tabs[1]:
        st.header("Step 2: Critical Appraisal")
        
        # Allow user to upload their list of papers
        uploaded_file = st.file_uploader("Upload your list of papers (CSV)", type=["csv"])
        if uploaded_file:
            st.session_state.papers_df = pd.read_csv(uploaded_file)
        
        if not st.session_state.papers_df.empty:
            st.write("### Papers to Appraise")
            # Create a selection box to choose which paper to grade
            selected_paper = st.selectbox("Select a paper to appraise:", st.session_state.papers_df["Title"].tolist())
            
            # Simple CASP Checklist
            col1, col2 = st.columns(2)
            with col1:
                q1 = st.radio("Is the study valid?", ["Yes", "No", "Can't Tell"])
                q2 = st.radio("Are the results important?", ["Yes", "No", "Can't Tell"])
            with col2:
                score = st.slider("Overall Quality Score (1-10)", 1, 10, 5)
                notes = st.text_area("Reviewer Notes")

            if st.button("Save Appraisal for this Paper"):
                # Update the dataframe with the score
                idx = st.session_state.papers_df.index[st.session_state.papers_df['Title'] == selected_paper][0]
                st.session_state.papers_df.at[idx, 'CASP_Score'] = score
                st.session_state.papers_df.at[idx, 'Notes'] = notes
                st.toast(f"Saved {selected_paper}!")

    # --- TAB 3: EXPORT ---
    with tabs[2]:
        st.header("Step 3: Final Dataset")
        st.dataframe(st.session_state.papers_df)
        
        # Convert dataframe to CSV for download
        csv = st.session_state.papers_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Final Appraisal Report (CSV)",
            data=csv,
            file_name="final_research_set.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
    