# tracker_app.py
# 6-Month Personal Transformation Tracker
# One-file Streamlit app
# Beginner friendly + portfolio ready

import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os

# -----------------------------
# Page setup (dark mode ready)
# -----------------------------
st.set_page_config(
    page_title="Personal Transformation Tracker",
    page_icon="🧭",
    layout="centered"
)

st.title("🧭 6-Month Personal Transformation Tracker")

# -----------------------------
# Dark mode toggle
# -----------------------------
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown(
        """
        <style>
        body { background-color: #0e1117; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Data file
# -----------------------------
DATA_FILE = "tracker_data.csv"

# Create file if it does not exist
if not os.path.exists(DATA_FILE):
    columns = ["Date"] + [f"Task_{i}" for i in range(1, 21)] + ["Score"]
    pd.DataFrame(columns=columns).to_csv(DATA_FILE, index=False)

# Load data safely (handles empty file)
try:
    df = pd.read_csv(DATA_FILE)
except pd.errors.EmptyDataError:
    columns = ["Date"] + [f"Task_{i}" for i in range(1, 21)] + ["Score"]
    df = pd.DataFrame(columns=columns)
    df.to_csv(DATA_FILE, index=False)


today = date.today().isoformat()
st.subheader(f"📅 Today: {today}")

# -----------------------------
# CHECKLISTS
# -----------------------------
tasks = []

st.markdown("### 🕌 Spirituality")
tasks += [
    st.checkbox("Fajr"),
    st.checkbox("Dhuhr"),
    st.checkbox("Asr"),
    st.checkbox("Maghrib"),
    st.checkbox("Isha"),
    st.checkbox("Quran / Islamic reminder"),
]

st.markdown("### 🧠 Mind & Discipline")
tasks += [
    st.checkbox("Woke up on time"),
    st.checkbox("No phone first 30 mins"),
    st.checkbox("Planned my day"),
    st.checkbox("Night reflection"),
]

st.markdown("### 💻 Career / Learning")
tasks += [
    st.checkbox("Internship task done well"),
    st.checkbox("Skill learning"),
    st.checkbox("Notes / practice done"),
]

st.markdown("### 💰 Money")
tasks += [
    st.checkbox("Sent outreach DMs"),
    st.checkbox("Worked on a task"),
    st.checkbox("Tracked expenses"),
]

st.markdown("### 💪 Physique")
tasks += [
    st.checkbox("Workout / walk"),
    st.checkbox("Drank enough water"),
    st.checkbox("Ate proper meals"),
]

# -----------------------------
# Score
# -----------------------------
score = sum(tasks)
st.info(f"✅ Daily Score: {score} / 20")

# -----------------------------
# Save button
# -----------------------------
if st.button("💾 Save Today"):
    df = df[df["Date"] != today]

    row = {"Date": today}
    for i, value in enumerate(tasks, start=1):
        row[f"Task_{i}"] = value
    row["Score"] = score

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    st.success("Saved. Consistency beats perfection 🤍")

# -----------------------------
# STREAK CALCULATION
# -----------------------------
df_sorted = df.sort_values("Date")
streak = 0
expected_day = date.today()

for d in reversed(df_sorted["Date"].tolist()):
    if d == expected_day.isoformat():
        streak += 1
        expected_day -= timedelta(days=1)
    else:
        break

st.metric("🔥 Current Streak", f"{streak} days")

# -
