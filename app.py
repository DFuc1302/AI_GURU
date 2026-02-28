import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent AI", layout="wide")

# ========== SIDEBAR ==========
st.sidebar.title("⚙ Settings")

theme = st.sidebar.selectbox(
    "Choose Theme",
    ["Light", "Dark"]
)

model_name = st.sidebar.text_input(
    "Model name (LM Studio)",
    value="local-model"
)

if theme == "Dark":
    st.markdown(
        """
        <style>
        body {background-color: #0E1117; color: white;}
        </style>
        """,
        unsafe_allow_html=True
    )

# ========== SESSION HISTORY ==========
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🤖 Multi-Agent AI Coding System")

problem = st.text_area("Enter your programming problem", height=150)

if st.button("🚀 Solve"):

    if problem.strip() == "":
        st.warning("Please enter a problem")
    else:
        with st.spinner("Agents thinking... 🤖"):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/solve",
                    json={"prompt": problem}
                )

                data = response.json()

                st.session_state.history.append({
                    "problem": problem,
                    "result": data
                })

            except Exception as e:
                st.error(f"Error: {e}")

# ========== DISPLAY HISTORY ==========
for item in reversed(st.session_state.history):

    st.markdown("---")
    st.subheader("📝 Problem")
    st.write(item["problem"])

    result = item["result"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Plan")
        st.write(result.get("plan"))

        st.subheader("🔍 Review")
        st.write(result.get("review"))

    with col2:
        st.subheader("💻 Code")
        st.code(result.get("code"), language="python")

        st.subheader("🧪 Sandbox Output")

        sandbox = result.get("sandbox", {})

        if "error" in sandbox:
            st.error(sandbox["error"])
        else:
            st.text("STDOUT:")
            st.code(sandbox.get("stdout", ""))

            st.text("STDERR:")
            st.code(sandbox.get("stderr", ""))
