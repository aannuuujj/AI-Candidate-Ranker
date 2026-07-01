import sys
from pathlib import Path

# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st

from pipeline.ranking_pipeline import RankingPipeline
from config.settings import TOP_CANDIDATES_FILE
from explainability.recommendation_engine import RecommendationEngine
st.set_page_config(
    page_title="AI Candidate Discovery Platform",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Candidate Discovery Platform")
st.write("AI-powered Candidate Discovery & Ranking System")

uploaded_file = st.file_uploader(
    "Upload Job Description",
    type=[
        "docx",
        "pdf",
        "jpg",
        "jpeg",
        "png",
    ],
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
                "Experience": candidate.candidate.years_of_experience,
            }
        )

    df = pd.DataFrame(rows)

    # ===========================
    # KPI CARDS
    # ===========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Candidates", len(df))
    col2.metric("Top Score", f"{df['Final Score'].max():.2f}%")
    col3.metric("Average Score", f"{df['Final Score'].mean():.2f}%")
    col4.metric("Average Experience", f"{df['Experience'].mean():.1f} yrs")

    st.divider()

    # ===========================
    # FILTERS
    # ===========================

    minimum_score = st.slider("Minimum Score", 0, 100, 0)
    search = st.text_input("🔍 Search Candidate ID")

    filtered_df = df[df["Final Score"] >= minimum_score]

    if filtered_df.empty:
     st.warning("No candidates match the selected filters.")
     st.stop()

    if search:
        filtered_df = filtered_df[
            filtered_df["Candidate ID"].str.contains(search, case=False)
        ]

    st.dataframe(filtered_df, use_container_width=True)

    # ===========================
    # CHART - SCORE DISTRIBUTION
    # ===========================

    st.subheader("📊 Candidate Score Distribution")

    fig = px.histogram(
        filtered_df,
        x="Final Score",
        nbins=10,
        title="Final Score Distribution",
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===========================
    # CHART - TOP CANDIDATES
    # ===========================

    st.subheader("🏆 Top Candidates")

    fig2 = px.bar(
       filtered_df.sort_values(
    by="Final Score",
    ascending=False,
).head(10),
        x="Candidate ID",
        y="Final Score",
        color="Final Score",
        text="Final Score",
        title="Top Ranked Candidates",
    )

    fig2.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    fig2.update_layout(
        xaxis_title="Candidate ID",
        yaxis_title="Final Score",
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ===========================
    # SELECT CANDIDATE
    # ===========================

    if len(filtered_df) > 0:

        selected_candidate = st.selectbox(
            "Select Candidate",
            filtered_df["Candidate ID"].tolist(),
        )

        candidate = next(
            c for c in ranked_candidates
            if c.candidate.candidate_id == selected_candidate
        )

        st.subheader("📋 Candidate Details")

        col1, col2 = st.columns(2)

        
        

    with col1:
           
     st.metric("Final Score", f"{candidate.match.final_score:.2f}%")
    st.metric("Skill Score", f"{candidate.match.skill_score:.2f}%")
    st.metric("Experience Score", f"{candidate.match.experience_score:.2f}%")

    engine = RecommendationEngine()

    recommendation, reasons = engine.recommend(
        candidate.match
    )

    st.success(recommendation)

    st.subheader("🤖 AI Explanation")

    for reason in reasons:
        st.write("✅", reason)

    st.subheader("🧠 AI Summary")

    summary = f"""
This candidate matched {len(candidate.match.matched_skills)} required skills
and missed {len(candidate.match.missing_skills)} skills.

Overall Score: {candidate.match.final_score:.2f}%

Recommendation:
{recommendation}
"""

    st.info(summary)