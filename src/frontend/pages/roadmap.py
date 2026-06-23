import streamlit as st

st.title(
    "📚 Personalized Learning Roadmap"
)

if "roadmap" not in st.session_state:
    st.warning("Please generate a roadmap first.")
    st.stop()

roadmap_data = st.session_state["roadmap"]

st.markdown("## 🎯 Missing Skills")

skills_html = ""

for skill in roadmap_data["missing_skills"]:
    skills_html += f"""
    <span style="
        background-color:#1E293B;
        color:white;
        padding:8px 15px;
        margin:5px;
        border-radius:20px;
        display:inline-block;
        font-size:16px;
    ">
        {skill.title()}
    </span>
    """

st.markdown(skills_html, unsafe_allow_html=True)

st.subheader("🗓️ Learning Plan")

for week in roadmap_data["roadmap"]:

    with st.expander(
        f"Week {week['week']} - {week['focus']}",
        expanded=True
    ):

        st.markdown("### Topics")

        for topic in week["topics"]:
            st.write(f"• {topic}")

        st.markdown("### Resources")

        for resource in week["resources"]:
            st.write(f"• {resource}")

        st.markdown("### Project")

        st.success(
            week["project"]
        )