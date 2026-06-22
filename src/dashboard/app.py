import sys
from pathlib import Path

# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import streamlit as st

from pipeline.ranking_pipeline import RankingPipeline
from config.settings import TOP_CANDIDATES_FILE


st.set_page_config(
    page_title="AI Candidate Discovery Platform",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Candidate Discovery Platform")
st.write("AI-powered Candidate Discovery & Ranking System")

uploaded_file = st.file_uploader(
    "Upload Job Description (.docx)",
    type=["docx"],
)

if st.button("Run Candidate Ranking"):

    if uploaded_file is None:
        st.warning("Please upload a Job Description first.")
        st.stop()

    upload_dir = SRC_DIR.parent / "uploads"
    upload_dir.mkdir(exist_ok=True)

    upload_path = upload_dir / uploaded_file.name

    with open(upload_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Ranking candidates..."):
        pipeline = RankingPipeline()
        ranked_candidates = pipeline.run(upload_path)

    st.success("✅ Ranking Completed!")

    rows = []

    for rank, candidate in enumerate(ranked_candidates, start=1):

        rows.append(
            {
                "Rank": rank,
                "Candidate ID": candidate.candidate.candidate_id,
                "Role": candidate.candidate.current_role,
                "Final Score": round(candidate.match.final_score, 2),
                "Skill Score": round(candidate.match.skill_score, 2),
                "Experience Score": round(candidate.match.experience_score, 2),
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(df, use_container_width=True)

    selected_candidate = st.selectbox(
        "Select Candidate",
        df["Candidate ID"],
    )

    candidate = next(
        c for c in ranked_candidates
        if c.candidate.candidate_id == selected_candidate
    )

    st.subheader("📋 Candidate Details")

    st.write("**Role:**", candidate.candidate.current_role)
    st.write("**Experience:**", candidate.candidate.years_of_experience)
    st.write("**Final Score:**", f"{candidate.match.final_score:.2f}%")

    st.write("### ✅ Matched Skills")
    st.write(candidate.match.matched_skills)

    st.write("### ❌ Missing Skills")
    st.write(candidate.match.missing_skills)

    with open(TOP_CANDIDATES_FILE, "rb") as file:

        st.download_button(
            label="📥 Download Top Candidates CSV",
            data=file,
            file_name="top_candidates.csv",
            mime="text/csv",
        )