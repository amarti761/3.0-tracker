import streamlit as st
import pandas as pd
import plotly.express as px

# Hard-coded course catalog
course_data = [
    {"Course Code": "CIS 5040", "Course Name": "Information Systems", "Credits": 3, "Prerequisites": "None", "Description": "Overview of computer, communication and software systems.", "Type": "Core", "Status": "In progress"},
    {"Course Code": "CIS 5850", "Course Name": "Communication and Information Services", "Credits": 3, "Prerequisites": "CIS 5040", "Description": "Computer communication technologies and trends.", "Type": "Core", "Status": "Not Started"},
    {"Course Code": "CIS 5900", "Course Name": "MSIS CAPSTONE:INFORMATION SYSTEMS", "Credits": 3, "Prerequisites": "CIS 5040 AND CIS 5850", "Description": "Examines the strategic perspective for aligning organizational strategy.", "Type": "Core", "Status": "Not Started"},
    # Add more courses as required
]

# Convert the hard-coded data into a DataFrame
df_courses = pd.DataFrame(course_data)

# Streamlit app
st.title("Degree Progress Tracker")

# Dropdown to select a course
course_selection = st.selectbox("Select a course:", options=df_courses["Course Code"] + " - " + df_courses["Course Name"])

if course_selection:
    selected_course = df_courses[df_courses["Course Code"] == course_selection.split(" - ")[0]].iloc[0]
    st.subheader(f"Course Details for {selected_course['Course Name']}")
    st.write(f"**Course Code:** {selected_course['Course Code']}")
    st.write(f"**Credits:** {selected_course['Credits']}")
    st.write(f"**Prerequisites:** {selected_course['Prerequisites']}")
    st.write(f"**Description:** {selected_course['Description']}")
    st.write(f"**Type:** {selected_course['Type']}")
    st.write(f"**Status:** {selected_course['Status']}")

# Global variables for user data
if "user_courses" not in st.session_state:
    st.session_state["user_courses"] = []
if "achievements" not in st.session_state:
    st.session_state["achievements"] = []

# Add course button
if st.button("Add Course"):
    if selected_course["Course Code"] not in st.session_state["user_courses"]:
        st.session_state["user_courses"].append(selected_course["Course Code"])
        st.success(f"Course '{selected_course['Course Name']}' added!")
    else:
        st.warning(f"Course '{selected_course['Course Name']}' is already added!")

# Check graduation status
if st.button("Check Graduation Status"):
    total_credits = sum(df_courses[df_courses["Course Code"].isin(st.session_state["user_courses"])]["Credits"])
    remaining_credits = 30 - total_credits  # Assume total credits required is 30

    st.subheader("Graduation Status")
    if total_credits >= 30:
        st.success("🎓 Congratulations! You have completed your degree!")
    else:
        st.info(f"Credits Completed: {total_credits}/30")
        st.info(f"Remaining Credits: {remaining_credits}")

# Visualize progress
st.subheader("Progress Overview")

# Pie chart for credits
pie_chart = px.pie(
    values=[sum(df_courses[df_courses["Course Code"].isin(st.session_state["user_courses"])]["Credits"]), 30 - sum(df_courses[df_courses["Course Code"].isin(st.session_state["user_courses"])]["Credits"])],
    names=["Completed", "Remaining"],
    title="Credit Progress",
)
st.plotly_chart(pie_chart)

# Bar chart for course completion
bar_chart = px.bar(
    x=st.session_state["user_courses"],
    y=[3] * len(st.session_state["user_courses"]),
    labels={"x": "Courses", "y": "Credits"},
    title="Courses Completed",
)
st.plotly_chart(bar_chart)

# Display achievements
st.subheader("Achievements")
if len(st.session_state["user_courses"]) >= 5 and "Halfway There!" not in st.session_state["achievements"]:
    st.session_state["achievements"].append("Halfway There!")
if sum(df_courses[df_courses["Course Code"].isin(st.session_state["user_courses"])]["Credits"]) >= 30 and "Degree Completed!" not in st.session_state["achievements"]:
    st.session_state["achievements"].append("Degree Completed!")

for achievement in st.session_state["achievements"]:
    st.write(f"🏆 {achievement}")
