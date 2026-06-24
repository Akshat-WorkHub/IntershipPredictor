import streamlit as st
import requests
import bootstrap
from src.utils.session_storage import save_profile, load_profile

if "profile_result" not in st.session_state:

    profile = load_profile()
    if profile:
        st.session_state["profile_result"] = profile

st.set_page_config(
    page_title="CareerPrep",
    page_icon="🎯",
    layout="wide"
)

col1, col2 = st.columns([1, 3])

with col1:
    st.image(
        "src/frontend/logo/logo.png",
        width='stretch'
    )

with col2:
    st.markdown(
        """
        <div style="padding-top:10px">
            <h1 style="margin-bottom:0;">CareerPrep</h1>
            <p style="margin-top:0;">
                AI Interview Preparation Assistant :
                Analyze, Improve, and Succeed in Your Career Journey.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

resume_col, job_description_col = st.columns(2)

with resume_col:
    st.subheader("📄 Upload Resume")

    resume_file = st.file_uploader(
        "Upload PDF Resume",
        type=["pdf"]
    )

with job_description_col:
    st.subheader("💼 Job Description")

    jd_file = st.file_uploader(
        "Upload Job Description",
        type=["pdf"]
    )

if (resume_file and jd_file) or ("profile_result" in st.session_state):
    st.success("Both Resume and Job Description uploaded successfully")

    st.divider()

    st.subheader("📊 Additional Information")

    col1, col2 = st.columns(2)

    with col1:
        github_url = st.text_input(
            "GitHub Profile URL (Optional)"
        )

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
        width='stretch'
    ):

        response = requests.post(
            url="http://127.0.0.1:8000/profile/generate",

            files={
                "resume": (
                    resume_file.name,
                    resume_file.getvalue(),
                    "application/pdf"
                ),

                "job_description": (
                    jd_file.name,
                    jd_file.getvalue(),
                    "application/pdf"
                )
            },

            data={
                "github_url": github_url,
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
            st.session_state["profile_result"] = response.json()
            save_profile(st.session_state["profile_result"])

        else:
            st.error(response.text)

    if "profile_result" in st.session_state:
        response_data = st.session_state["profile_result"]

        result, pred_prob ,skill_gap = (
            response_data["Result"], 
            response_data["prediction_probability"], 
            response_data["skill_gap"]
        )

        confidence_titles = [
            "🎉 Strong Match Detected",
            "⚡ Moderate Match", 
            "⚠️ Improvement Needed"
        ]

        confidence_messages = [
            "Your profile shows a high likelihood of passing the initial screening stage.",
            "Your profile aligns reasonably well, but improving missing skills could increase your chances.",
            "There are noticeable gaps between your profile and the target role."
        ]

        if pred_prob >= 80:
            confidence_title = confidence_titles[0]
            confidence_message = confidence_messages[0]
            bg, color = "#83f274", "#082b11"

        elif pred_prob >= 60:
            confidence_title = confidence_titles[1]
            confidence_message = confidence_messages[1]
            bg, color =  "#ecf14c", "#131603",

        else:
            confidence_title = confidence_titles[2]
            confidence_message = confidence_messages[2]
            bg, color = "#83f274", "#082b11"

        st.subheader("🎯 Screening Confidence")

        st.progress(pred_prob / 100)
        st.metric("Selection Probability",f"{pred_prob}%")
        st.markdown(
            f"""
            <div style="
                background-color:{bg};
                color:{color};
                padding:10px;
                border-radius:20px;
                border-left:10px solid #ffffff;
            ">
                <h5>{confidence_title}</h5>
                <p style="font-size:14px; font-weight:650;">
                    {confidence_message}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        match_percent = skill_gap['match_percentage']
        
        if match_percent >= 80:
            compatibility_level, background_palette, color_palette  = "Excellent Match 🟢", "#064E3B", "#34D399" 

        elif match_percent >= 60:
            compatibility_level, background_palette, color_palette   = "Good Match 🟡", "#78350F", "#FBBF24"

        elif match_percent >= 40:
            compatibility_level, background_palette, color_palette   = "Average Match 🟠", "#7C2D12", "#FB923C"

        else:
            compatibility_level, background_palette, color_palette   = "Weak Match 🔴", "#7F1D1D", "#F7D4D4"

        st.subheader("📄 Resume-JD Compatibility")
        
        st.progress(match_percent / 100)
        st.metric("Compatibility Score",f"{match_percent:.2f}%")
        st.markdown(
            f"""
            <div style="
                background-color:{background_palette};
                color:{color_palette};
                padding:10px;
                border-radius:10px;
                border-left:10px solid #ffffff;
                margin-bottom: 10px;
            ">
                <h5>{compatibility_level}</h5>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🚀 Create Personalized Roadmap"):

            roadmap_response = requests.post(
                "http://127.0.0.1:8000/roadmap/generate",
                json={
                    "missing_skills": skill_gap["missing_skills"]
                }
            )

            if roadmap_response.status_code == 200:
                st.session_state["roadmap"] = (
                    roadmap_response.json()
                )

                st.session_state["generate_roadmap"] = True

        if st.session_state.get("generate_roadmap",False):
            st.success("Roadmap Generated Successfully")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "📖 View Roadmap",
                    width='stretch'
                ):
                    st.switch_page(
                        "pages/roadmap.py"
                    )

            with col2:
                if st.button(
                    "🎤 Start Mock Interview",
                    width='stretch'
                ):
                    st.switch_page(
                        "pages/mock_interview.py"
                    )