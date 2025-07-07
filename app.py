import streamlit as st
import requests
import json
from datetime import date, datetime

API_URL = "http://127.0.0.1:5000"

def load_data():
    st.session_state.task_history = []
    st.session_state.todos = []
    try:
        with open("task_history.json", "r") as f:
            st.session_state.task_history = json.load(f)
        with open("todos.json", "r") as f:
            st.session_state.todos = json.load(f)
    except:
        pass

def save_data():
    with open("task_history.json", "w") as f:
        json.dump(st.session_state.task_history, f)
    with open("todos.json", "w") as f:
        json.dump(st.session_state.todos, f)

if "task_history" not in st.session_state or "todos" not in st.session_state:
    load_data()

st.markdown("""
<div style='background-color:#6A5ACD;padding:16px;border-radius:12px;text-align:center;color:white;font-size:32px;font-weight:bold;margin-bottom:20px;'>
 Smart Task Analyzer
</div>
""", unsafe_allow_html=True)

task_text = st.text_input("📝 Enter your task:")

if st.button("🔍 Analyze Task"):
    if not task_text.strip():
        st.warning("Please enter a task.")
    else:
        with st.spinner("Analyzing..."):
            try:
                resp1 = requests.post(f"{API_URL}/classify_task", json={"task": task_text})
                task_type = resp1.json().get("task_type", "Unknown")

                words = task_text.lower().split()
                word_count = len(words)
                has_urgent = int(any(w in words for w in ["urgent", "asap", "immediately"]))
                has_deadline = int(any(w in words for w in ["by", "before", "due"]))
                features = [word_count, has_urgent, has_deadline]

                resp2 = requests.post(f"{API_URL}/predict_priority", json={"features": features})
                priority = resp2.json().get("priority", "Unknown")

                st.success("✅ Task analyzed!")
                st.markdown(f"**🗂️ Type:** `{task_type}`")
                st.markdown(f"**🚦 Priority:** `{priority}`")

                st.session_state.task_history.append({
                    "task": task_text,
                    "type": task_type,
                    "priority": priority
                })
                save_data()

            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.session_state.task_history:
    if st.button("🧹 Clear History"):
        st.session_state.task_history = []
        save_data()
        st.rerun()

    st.markdown("### 📜 Task History")
    for i, record in enumerate(reversed(st.session_state.task_history), 1):
        st.markdown(f"""
        <div style='padding:10px;margin-bottom:10px;border-radius:8px;background-color:#f8f9fa;border-left:5px solid #6c757d;color:#212529;'>
        <b>{i}.</b> {record['task']}<br>🏷️ <b>Type:</b> {record['type']}<br>🚨 <b>Priority:</b> {record['priority']}
        </div>
        """, unsafe_allow_html=True)

    st.download_button("⬇️ Download History", data=json.dumps(st.session_state.task_history, indent=2),
                       file_name="task_history.json", mime="application/json")

st.divider()
st.markdown("## ✅ To-Do List")

with st.form("todo_form"):
    todo_text = st.text_input("➕ Add task:")
    due_date = st.date_input("📅 Optional due date:", value=date.today())
    submit = st.form_submit_button("Add")
    if submit and todo_text.strip():
        st.session_state.todos.append({
            "todo": todo_text.strip(),
            "due": due_date.strftime("%Y-%m-%d"),
            "done": False
        })
        save_data()
        st.rerun()

if st.session_state.todos:
    st.markdown("### 📌 To-Dos")
    for i, item in enumerate(st.session_state.todos):
        cols = st.columns([0.05, 0.75, 0.2])
        checked = cols[0].checkbox("", value=item["done"], key=f"todo_{i}")
        st.session_state.todos[i]["done"] = checked

        due = datetime.strptime(item["due"], "%Y-%m-%d").date()
        today = date.today()
        color = "#2ecc71" if due > today else "#e74c3c" if due < today else "#f39c12"
        style = "text-decoration: line-through;" if item["done"] else ""
        cols[1].markdown(f"<span style='{style}'>{item['todo']}</span>", unsafe_allow_html=True)
        cols[2].markdown(f"<span style='color:{color}'><b>{item['due']}</b></span>", unsafe_allow_html=True)

    if any(t["done"] for t in st.session_state.todos):
        if st.button("❌ Remove Completed"):
            st.session_state.todos = [t for t in st.session_state.todos if not t["done"]]
            save_data()
            st.rerun()

    st.download_button("⬇️ Download To-Dos", data=json.dumps(st.session_state.todos, indent=2),
                       file_name="todos.json", mime="application/json")