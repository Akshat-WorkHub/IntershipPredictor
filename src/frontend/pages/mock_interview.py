import streamlit as st
import requests
import bootstrap
from src.utils.session_storage import load_profile, save_evaluation


st.title("🎤 AI Mock Interview")

if st.session_state.get(
    "interview_completed",
    False
):

    st.success(
        "Interview Submitted Successfully 🎉"
    )

    if st.button(
        "📖 View Interview Analysis",
        use_container_width=True
    ):
        st.switch_page(
            "pages/interview_analysis.py"
        )

    st.stop()

if "profile_result" not in st.session_state:

    profile = load_profile()
    if profile:
        st.session_state["profile_result"] = profile


if "profile_result" not in st.session_state:
    st.warning(
        "Please generate a candidate profile first."
    )
    st.stop()

# ==========================
# Interview Setup Section
# ==========================

if not st.session_state.get(
    "interview_started",
    False
):

    st.divider()

    interview_mode = st.selectbox(
        "Interview Mode",
        [
            "Technical Round",
            "HR Round",
            "Project Discussion",
            "Full Mock Interview"
        ]
    )

    question_count = st.selectbox(
        "Number of Questions",
        [1, 3, 5, 10]
    )

    if st.button(
        "🚀 Start Interview",
        width='stretch'
    ):

        profile_data = (
            st.session_state["profile_result"]
        )

        response = requests.post(
            url="http://127.0.0.1:8000/interview/generate",
            json={
                "interview_mode": interview_mode,
                "number_of_questions": question_count,
                "resume_data": profile_data["resume_data"],
                "jd_data": profile_data["jd_data"],
                "missing_skills": profile_data["missing_skills"]
            }
        )

        if response.status_code == 200:

            response_data = response.json()

            st.session_state["interview_questions"] = response_data["questions"]
            st.session_state["answers"] = {}
            st.session_state["scores"] = []


            st.session_state["current_question"] = 0
            st.session_state["interview_started"] = True
            st.session_state["interview_completed"] = False

            st.rerun()

        else:
            st.error(response.text)

# ==========================
# Interview Section
# ==========================

if st.session_state.get(
    "interview_started",
    False
):

    questions = st.session_state["interview_questions"]
    total_questions = len(questions)

    current_idx = st.session_state["current_question"]
    question = questions[current_idx]

    progress = (
        (current_idx + 1) / total_questions
    )

    st.divider()

    st.subheader(
        f"Question {current_idx + 1} of {total_questions}"
    )

    st.progress(progress)

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"Category: {question['category']}"
        )

    with col2:
        st.info(
            f"Difficulty: {question['difficulty']}"
        )

    st.markdown(
        f"""
    ### ❓ Interview Question

    {question['question']}
    """
    )

    saved_answer = (
        st.session_state["answers"]
        .get(current_idx, {})
    )

    default_answer = (
        saved_answer.get(
            "answer",
            ""
        )
    )

    default_dont_know = saved_answer.get("dont_know",False)

    dont_know = st.checkbox(
        "I don't know the answer",
        value=default_dont_know,
        key=f"dont_know_{current_idx}"
    )

    answer = st.text_area(
        "Your Answer",
        value=default_answer,
        height=250,
        disabled=dont_know,
        key=f"answer_box_{current_idx}"
    )



    

    col1, col2 = st.columns(2)
    # ==========================
    # Previous Question
    # ==========================

    with col1:

        if current_idx > 0:

            if st.button(
                "⬅ Previous Question",
                width='stretch'
            ):

                st.session_state["answers"][current_idx] = {
                    "question":
                        question["question"],

                    "answer":
                        answer,
                    
                    "category": 
                        question["category"],

                    "dont_know":
                        dont_know
                }

                st.session_state["current_question"] -= 1

                st.rerun()

    # ==========================
    # Next / Submit
    # ==========================

    with col2:

        # Not Last Question

        if current_idx < total_questions - 1:

            if st.button(
                "Next Question ➡️",
                width='stretch'
            ):

                if (
                    not answer.strip()
                    and not dont_know
                ):

                    st.warning(
                        "Please provide an answer or select 'I don't know the answer'."
                    )

                else:

                    st.session_state["answers"][current_idx] = {
                        "question":
                            question["question"],

                        "answer":
                            answer,

                        "category": 
                            question["category"],

                        "dont_know":
                            dont_know
                    }

                    st.session_state["current_question"] += 1
                    st.rerun()

        # ==========================
        # Last Question
        # ==========================

        else:

            if st.button(
                "🚀 Submit Interview",
                width='stretch'
            ):

                if (
                    not answer.strip()
                    and not dont_know
                ):

                    st.warning(
                        "Please provide an answer or select 'I don't know the answer'."
                    )

                else:
                    st.session_state["answers"][current_idx] = {
                        "question":
                            question["question"],
                        "answer":
                            answer,

                        "category": 
                            question["category"],

                        "dont_know":
                            dont_know
                    }

                    response = requests.post(
                        url="http://127.0.0.1:8000/interview/evaluate",
                        json={
                            "answers": st.session_state["answers"],
                        }
                    )

                    if response.status_code == 200:
                        st.session_state["evaluation_report"] = (
                            response.json()
                        )
                        save_evaluation(
                            st.session_state["evaluation_report"]
                        )

                        st.session_state["interview_completed"] = True
                        st.success(
                            "Interview Submitted Successfully 🎉"
                        )
                        st.rerun()

                    else:

                        st.error(
                            "Failed to evaluate interview."
                        )

