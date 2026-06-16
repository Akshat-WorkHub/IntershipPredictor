import streamlit as st
import requests

st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Interview Preparation Assistant")
st.caption("Resume Analysis & Candidate Readiness Predictor")

st.divider()

# Resume Upload

st.subheader("📄 Upload Resume")

resume_file = st.file_uploader(
    "Upload PDF Resume",
    type=["pdf"]
)

if resume_file:
    st.success("Resume uploaded successfully")

    st.divider()

    st.subheader("📊 Additional Information")

    col1, col2 = st.columns(2)

    with col1:

        communication_score = st.slider(
            "Communication Skill",
            1, 10, 5
        )

        coding_score = st.slider(
            "Coding Skill",
            1, 10, 5
        )

        aptitude_score = st.slider(
            "Aptitude Skill",
            1, 10, 5
        )

    with col2:

        soft_skills_score = st.slider(
            "Soft Skills",
            1, 10, 5
        )

        backlogs = st.number_input(
            "Backlogs",
            min_value=0,
            value=0
        )

        college_tier = st.selectbox(
            "College Tier",
            ["Tier 1", "Tier 2", "Tier 3"]
        )

        placement_training = st.selectbox(
            "Placement Training",
            ["Yes", "No"]
        )

    st.divider()

    if st.button(
        "🚀 Generate Candidate Profile",
        use_container_width=True
    ):

        response = requests.post(
            url="http://127.0.0.1:8000/profile/generate",

            files={
                "resume": (
                    resume_file.name,
                    resume_file.getvalue(),
                    "application/pdf"
                )
            },

            data={
                "communication_score": communication_score,
                "coding_score": coding_score,
                "aptitude_score": aptitude_score,
                "soft_skills_score": soft_skills_score,
                "backlogs": backlogs,
                "college_tier": college_tier,
                "placement_training": placement_training
            }
        )

        if response.status_code == 200:
            st.json(response.json())
            st.success("Candidate Profile Generated Successfully")
        else:
            st.error(response.text)