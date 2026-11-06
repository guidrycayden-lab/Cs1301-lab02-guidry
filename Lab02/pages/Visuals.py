# This creates the page for displaying data visualizations.

import json
import streamlit as st
import pandas as pd
import plotly.express as px
import os


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---

# Load the JSON data
infile = open("data.json")
myData = json.load(infile)

st.header(myData["chart_title"])

# STATIC: bar chart of personal bests (advanced chart, Plotly)
st.subheader("Personal Bests")
pbs = pd.DataFrame(myData["personal_bests"])
fig = px.bar(
    pbs,
    x="label",
    y="value",
    title="Personal Bests by Event",
    labels={"label": "Event", "value": "Time (seconds)"},
)
st.plotly_chart(fig)

# DYNAMIC: line chart that changes with the radio button (uses session state)
st.subheader("Race Progression")

if "event" not in st.session_state:
    st.session_state.event = "400m"

st.radio("Pick an event", ["400m", "800m"], key="event")

races = pd.DataFrame(myData["race_progression"])
st.line_chart(races, x="race", y=st.session_state.event)


# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.header("Survey Results")

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    survey = pd.read_csv("data.csv")
    survey["value"] = pd.to_numeric(survey["value"], errors="coerce")
else:
    survey = pd.DataFrame(columns=["category", "value"])

if survey.empty:
    st.info("No survey responses yet. Fill out the Survey page first!")
else:
    st.subheader("Favorite Events")
    counts = survey["category"].value_counts().reset_index()
    counts.columns = ["Event", "Responses"]
    fig3 = px.pie(
        counts,
        names="Event",
        values="Responses",
        title="Favorite Track Events",
    )
    st.plotly_chart(fig3)

    st.subheader("Who Gets Enough Sleep?")

    if "min_sleep" not in st.session_state:
        st.session_state.min_sleep = 0.0

    st.slider(
        "Only count people who sleep at least this many hours",
        min_value=0.0,
        max_value=12.0,
        step=0.5,
        key="min_sleep",
    )

    filtered = survey[survey["value"] >= st.session_state.min_sleep]

    if filtered.empty:
        st.info("Nobody in the survey sleeps that much!")
    else:
        st.bar_chart(filtered["category"].value_counts())
