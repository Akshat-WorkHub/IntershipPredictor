import streamlit as st
import bootstrap
from src.utils.session_storage import (
    load_evaluation
)


if "evaluation_report" not in st.session_state:
    report = load_evaluation()
    if report:
        st.session_state["evaluation_report"] = report

st.set_page_config(
    page_title="Interview Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Interview Analysis")
st.caption("Review your interview performance and identify areas for improvement.")

if "evaluation_report" not in st.session_state:
    st.warning("No interview analysis available.")
    st.stop()

report = st.session_state["evaluation_report"]

st.subheader("🎯 Overall Performance")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Overall Score",
        f"{report['overall_score']}/10"
    )

with col2:
    st.metric(
        "Attempted",
        report["attempted_questions"]
    )

with col3:
    st.metric(
        "Not Attempted",
        report["unattempted_questions"]
    )

st.divider()
col1, col2 = st.columns(2)

with col1:

    st.subheader("💪 Strengths")

    for item in report["strengths"]:
        st.success(item)

with col2:

    st.subheader("🚀 Areas for Improvement")

    for item in report["improvements"]:
        st.warning(item)

st.divider()
st.subheader("📚 Questions To Revise")

for item in report["questions_to_revise"]:
    st.info(item)


st.divider()
st.subheader("📝 Question Wise Analysis")

for idx, question in enumerate(
    report["question_analysis"],
    start=1
):

    with st.expander(
        f"Question {idx} • {question['status']} • Score {question['score']}/10"
    ):

        st.markdown(
            f"**Question:** {question['question']}"
        )

        st.markdown(
            f"**Category:** {question['category']}"
        )

        st.markdown(
            f"**Your Answer:**"
        )

        st.write(
            question["candidate_answer"]
        )

        st.markdown(
            f"**Feedback:**"
        )

        st.info(
            question["feedback"]
        )

        st.markdown(
            "**Strengths:**"
        )

        for item in question["strengths"]:
            st.success(item)

        st.markdown(
            "**Improvements:**"
        )

        for item in question["improvements"]:
            st.warning(item)

        st.markdown(
            "**Ideal Answer:**"
        )

        st.code(
            question["ideal_answer"]
        )

st.divider()

if st.button(
    "🔄 Retake Interview",
    width='stretch'
):
    keys_to_clear = [
        "interview_started",
        "interview_completed",
        "current_question",
        "interview_questions",
        "answers",
        "evaluation_report"
    ]

    for key in keys_to_clear:

        if key in st.session_state:
            del st.session_state[key]

    st.switch_page(
        "pages/mock_interview.py"
    )