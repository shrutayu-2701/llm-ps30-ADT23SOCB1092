"""Streamlit interface for AI Lesson Plan Generator."""

import os

import streamlit as st

from llm_service import (
    DEFAULT_MODEL,
    LessonPlanError,
    get_ollama_models,
    stream_lesson_plan,
    validate_inputs,
)

st.set_page_config(page_title="AI Lesson Plan Generator", layout="centered")
st.markdown(
    """
    <style>
      :root { color-scheme: light; }
      html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #f3f7fc !important;
        color: #1b2b41 !important;
      }
      [data-testid="stHeader"] {
        background: rgba(243, 247, 252, 0.98) !important;
        color: #1b2b41 !important;
      }
      [data-testid="stToolbar"] { color: #1b2b41 !important; }
      .block-container { max-width: 920px; padding-top: 2.2rem; }
      .stApp h1, .stApp h2, .stApp h3,
      [data-testid="stMarkdownContainer"],
      [data-testid="stMarkdownContainer"] p,
      [data-testid="stMarkdownContainer"] li,
      [data-testid="stMarkdownContainer"] th,
      [data-testid="stMarkdownContainer"] td,
      [data-testid="stMarkdownContainer"] blockquote,
      [data-testid="stCaptionContainer"],
      [data-testid="stWidgetLabel"],
      [data-testid="stWidgetLabel"] p,
      label, .stApp p {
        color: #203650 !important;
      }
      [data-testid="stMarkdownContainer"] pre,
      [data-testid="stMarkdownContainer"] code {
        background-color: #eaf0f7 !important;
        color: #183b5b !important;
      }
      [data-testid="stForm"] {
        background: #ffffff !important;
        border: 1px solid #d2deeb !important;
        border-radius: 12px;
        padding: 1.25rem;
      }
      input, textarea,
      [data-baseweb="select"] > div,
      [data-testid="stNumberInput"] input {
        background-color: #ffffff !important;
        color: #172b45 !important;
        border: 1px solid #b8c8da !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        -webkit-text-fill-color: #172b45 !important;
      }
      input:focus, textarea:focus, [data-baseweb="select"] > div:focus-within {
        border-color: #3278b8 !important;
        box-shadow: 0 0 0 2px rgba(50, 120, 184, 0.18) !important;
      }
      input::placeholder, textarea::placeholder {
        color: #65778d !important;
        -webkit-text-fill-color: #65778d !important;
        opacity: 1 !important;
      }
      [data-baseweb="select"] *,
      [data-baseweb="popover"],
      [role="listbox"], [role="option"] {
        color: #172b45 !important;
      }
      [data-baseweb="select"] * { background-color: transparent !important; }
      [data-baseweb="select"] svg { color: #52677d !important; fill: currentColor !important; }
      [data-baseweb="popover"], [role="listbox"], [role="option"] {
        background-color: #ffffff !important;
      }
      .stButton > button, [data-testid="stDownloadButton"] button {
        background: #ffffff !important;
        color: #245b91 !important;
        border: 1px solid #8daecc !important;
        border-radius: 8px;
      }
      .stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
        background: #edf5ff !important;
        border-color: #245b91 !important;
        color: #173f68 !important;
      }
      .stButton > button[kind="primary"],
      [data-testid="stFormSubmitButton"] button {
        background: #245b91 !important;
        color: #ffffff !important;
        border-color: #245b91 !important;
      }
      .stButton > button[kind="primary"] *,
      [data-testid="stFormSubmitButton"] button * {
        color: #ffffff !important;
      }
      [data-testid="stAlert"] { color: #203650 !important; }
    </style>
    """, unsafe_allow_html=True,
)

st.title("AI Lesson Plan Generator")
st.caption("Create a practical, structured lesson plan with a local Ollama model.")


@st.cache_data(ttl=10)
def load_local_models():
    return get_ollama_models()


try:
    installed_models = load_local_models()
    if installed_models:
        st.caption(f"Ollama is connected · {len(installed_models)} local model(s) available")
    else:
        st.warning("Ollama is connected, but no models are installed. Run `ollama pull llama3.2:3b` in PowerShell.")
except LessonPlanError as exc:
    installed_models = []
    st.warning(f"{exc} Start Ollama, then refresh this page. If needed, install it from ollama.com/download.")


def clear_inputs():
    """Reset the form and any previously generated output."""
    st.session_state.topic = ""
    st.session_state.subject = "Science"
    st.session_state.grade = "7"
    st.session_state.duration_choice = 45
    st.session_state.custom_duration = 50
    st.session_state.learning_level = ""
    st.session_state.teaching_instructions = ""
    st.session_state.pop("lesson_plan", None)
    st.session_state.pop("lesson_details", None)


st.button("Clear / Reset Inputs", on_click=clear_inputs)

with st.form("lesson_form"):
    if installed_models:
        configured_model = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
        model = st.selectbox(
            "Local Ollama model",
            installed_models,
            index=installed_models.index(configured_model) if configured_model in installed_models else 0,
        )
    else:
        model = st.text_input(
            "Local Ollama model",
            value=os.getenv("OLLAMA_MODEL", DEFAULT_MODEL),
            help="Install this model with `ollama pull llama3.2:3b`, or enter another installed model.",
        )
    topic = st.text_input("Lesson/topic name *", placeholder="e.g., Introduction to Artificial Intelligence", key="topic")
    subject = st.text_input("Subject *", value="Science", placeholder="e.g., Computer Science", key="subject")
    grade = st.selectbox("Grade/Class *", [str(n) for n in range(1, 13)], index=6, key="grade")
    duration_choice = st.selectbox("Lesson duration", [30, 40, 45, 60, "Custom"], index=2, key="duration_choice")
    duration = (st.number_input("Custom duration (minutes)", min_value=1, max_value=180,
                                value=50, step=5, key="custom_duration")
                if duration_choice == "Custom" else duration_choice)
    learning_level = st.text_input("Student learning level (optional)",
                                   placeholder="e.g., mixed ability, beginner", key="learning_level")
    teaching_instructions = st.text_area("Teaching style or additional instructions (optional)",
                                         placeholder="e.g., use a short group activity and simple examples",
                                         height=90, key="teaching_instructions")
    submitted = st.form_submit_button("Generate Lesson Plan", type="primary", use_container_width=True)

if submitted:
    error = validate_inputs(topic, subject, grade, int(duration))
    if error:
        st.error(error)
    else:
        st.session_state.pop("lesson_plan", None)
        st.session_state.pop("lesson_details", None)
        stream_placeholder = st.empty()
        try:
            with st.spinner("Ollama is generating. Your lesson plan will appear progressively below..."):
                generated_plan = stream_placeholder.write_stream(stream_lesson_plan(
                    topic, subject, grade, int(duration), model=model,
                    teaching_instructions=teaching_instructions, learning_level=learning_level,
                ))
            stream_placeholder.empty()
            if not generated_plan or not generated_plan.strip():
                raise LessonPlanError("Ollama returned an empty response. Try again.")
            st.session_state.lesson_plan = generated_plan.strip()
            st.session_state.lesson_details = {
                "topic": topic.strip(), "subject": subject.strip(),
                "grade": grade, "duration": int(duration), "model": model,
            }
            st.rerun()
        except LessonPlanError as exc:
            stream_placeholder.empty()
            st.error(str(exc))

if st.session_state.get("lesson_plan"):
    details = st.session_state.lesson_details
    st.divider()
    st.subheader("Generated lesson plan")
    st.caption(f"{details['topic']}  |  {details['subject']}  |  Grade {details['grade']}  |  {details['duration']} minutes  |  {details['model']}")
    plan = st.session_state.lesson_plan
    st.markdown(plan)
    st.download_button("Download as Markdown (.md)", plan, file_name="lesson_plan.md",
                       mime="text/markdown", use_container_width=True)
    st.download_button("Download as text (.txt)", plan, file_name="lesson_plan.txt",
                       mime="text/plain", use_container_width=True)
