import streamlit as st
import time
import random

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Pastel Task Pomodoro",
    page_icon="🍓",
    layout="centered"
)

# ----------------------------
# Pastel CSS
# ----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fde2e4, #e2ece9);
    overflow: hidden;
}

@keyframes floatUp {
    0% { transform: translateY(0); opacity: 0; }
    10% { opacity: 0.5; }
    100% { transform: translateY(-120vh); opacity: 0; }
}

.timer-box {
    background: #ffffffcc;
    border-radius: 30px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.timer-text {
    font-size: 64px;
    font-weight: 700;
    color: #6b705c;
}

.task-text {
    font-size: 26px;
    font-weight: 600;
    color: #b5838d;
    margin-bottom: 12px;
}

button {
    border-radius: 20px !important;
    height: 3em;
    background-color: #ffc8dd !important;
    color: #4a4a4a !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Floating hearts
# ----------------------------
hearts = ""
for _ in range(8):
    hearts += f"""
    <div style="
        position:fixed;
        bottom:-10px;
        left:{random.randint(0,100)}%;
        font-size:22px;
        animation: floatUp 8s linear infinite;
        opacity:0.4;
        pointer-events:none;
        z-index:1;
    ">💗</div>
    """
st.markdown(hearts, unsafe_allow_html=True)

# ----------------------------
# Session State (HARD RESET SAFETY)
# ----------------------------
if "tasks" not in st.session_state or not isinstance(st.session_state.tasks, list):
    st.session_state.tasks = []

if "active_task" not in st.session_state or not isinstance(st.session_state.active_task, (dict, type(None))):
    st.session_state.active_task = None

if "time_left" not in st.session_state or not isinstance(st.session_state.time_left, int):
    st.session_state.time_left = 0

if "running" not in st.session_state or not isinstance(st.session_state.running, bool):
    st.session_state.running = False

# ----------------------------
# Actions
# ----------------------------
def select_task(index):
    task = st.session_state.tasks.pop(index)
    st.session_state.active_task = task
    st.session_state.time_left = task["minutes"] * 60
    st.session_state.running = False

def toggle_play():
    if isinstance(st.session_state.active_task, dict):
        st.session_state.running = not st.session_state.running

def reset():
    st.session_state.running = False
    st.session_state.active_task = None
    st.session_state.time_left = 0

# ----------------------------
# Header
# ----------------------------
st.title("🍓 Task Pomodoro")

if isinstance(st.session_state.active_task, dict):
    st.markdown(
        f"<div class='task-text'>✨ {st.session_state.active_task['name']} ✨</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='task-text'>Select a task to begin 🌷</div>",
        unsafe_allow_html=True
    )

# ----------------------------
# Timer Display
# ----------------------------
minutes, seconds = divmod(st.session_state.time_left, 60)

st.markdown(f"""
<div class="timer-box">
    <div class="timer-text">{minutes:02d}:{seconds:02d}</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.button(
        "▶ play / ⏸ pause",
        on_click=toggle_play,
        disabled=not isinstance(st.session_state.active_task, dict)
    )
with col2:
    st.button("🔄 reset", on_click=reset)

# ----------------------------
# Add Task
# ----------------------------
st.subheader("📝 Add Task")

with st.form("task_form", clear_on_submit=True):
    task_name = st.text_input("Task name")
    task_minutes = st.number_input("Minutes", min_value=1, max_value=180, value=25)
    submitted = st.form_submit_button("➕ add task")

    if submitted and task_name:
        st.session_state.tasks.append({
            "name": task_name,
            "minutes": task_minutes
        })

# ----------------------------
# Task List
# ----------------------------
st.subheader("🌸 Task List")

if not st.session_state.tasks:
    st.caption("No pending tasks ✨")

for i, task in enumerate(st.session_state.tasks):
    colA, colB, colC = st.columns([4, 1, 1])
    colA.write(task["name"])
    colB.write(f"{task['minutes']} min")
    colC.button(
        "▶",
        key=f"select_{i}",
        on_click=select_task,
        args=(i,)
    )

# ----------------------------
# Timer Logic
# ----------------------------
if st.session_state.running and st.session_state.time_left > 0:
    time.sleep(1)
    st.session_state.time_left -= 1
    st.rerun()

if st.session_state.running and st.session_state.time_left == 0:
    st.session_state.running = False
    st.toast("🎉 Task complete!", icon="✨")
