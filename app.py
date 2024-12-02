import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# Initialize session state
if "user_courses" not in st.session_state:
    st.session_state["user_courses"] = []
if "notifications" not in st.session_state:
    st.session_state["notifications"] = []
if "achievements" not in st.session_state:
    st.session_state["achievements"] = []

# Hardcoded course data
# Hardcoded course data
courses = [
    {"Course Code": "CIS 5040", "Course Name": "Information Systems", "Credits": 3, "Prerequisites": "None", "Description": "Overview of computer, communication and software systems.", "Type": "Core", "Status": "In progress"},
    {"Course Code": "CIS 5850", "Course Name": "Communication and Information Services", "Credits": 3, "Prerequisites": "CIS 5040", "Description": "Computer communication technologies and trends.", "Type": "Core", "Status": "Not Started"},
    {"Course Code": "CIS 5900", "Course Name": "MSIS CAPSTONE: INFORMATION SYSTEMS", "Credits": 3, "Prerequisites": "CIS 5040 AND CIS 5850", "Description": "Strategic perspective for aligning organizational strategy and information systems.", "Type": "Core", "Status": "Not Started"},
    {"Course Code": "BUS 5960", "Course Name": "COMPREHENSIVE EXAMINATION", "Credits": 0, "Prerequisites": "Advancement to Candidacy", "Description": "See the Comprehensive Examination under the University Requirements for Master’s Degree.", "Type": "Comprehensive exam", "Status": "Not Started"},
    {"Course Code": "CIS 5100", "Course Name": "IS/IT Architectures", "Credits": 3, "Prerequisites": "None", "Description": "Deep understanding and analysis of contemporary IT architectures.", "Type": "Required Course", "Status": "In progress"},
    {"Course Code": "CIS 5200", "Course Name": "System Analysis and Design", "Credits": 3, "Prerequisites": "None", "Description": "Life cycle of systems development; UML modeling techniques; hands-on experience.", "Type": "Required Course", "Status": "In progress"},
    {"Course Code": "CIS 5610", "Course Name": "Design of an E-Commerce Site", "Credits": 3, "Prerequisites": "Basic Knowledge of HTML OR XML", "Description": "Design of a web-based e-commerce site model for an actual business.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5620", "Course Name": "Authoring Websites", "Credits": 3, "Prerequisites": "Knowledge of Programming Language", "Description": "Designing and developing websites using HTML, CSS, JavaScript.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5630", "Course Name": "Mobile Applications", "Credits": 3, "Prerequisites": "Knowledge of Programming Language", "Description": "Designing and developing applications suitable for mobile devices.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5210", "Course Name": "Healthcare Data Analytics", "Credits": 3, "Prerequisites": "None", "Description": "Analytic challenges on dealing with healthcare data; hands-on experience.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5250", "Course Name": "Visual Analytics", "Credits": 3, "Prerequisites": "None", "Description": "Data visualization, dashboard creation techniques, storytelling.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5270", "Course Name": "Business Intelligence", "Credits": 3, "Prerequisites": "None", "Description": "Data wrangling, data mining, dashboards, business intelligence technologies.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5320", "Course Name": "Data Integration and Analysis in ERP Systems", "Credits": 3, "Prerequisites": "None", "Description": "Data modeling, integration, visualization using ERP systems.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5430", "Course Name": "Databases and Data Warehousing", "Credits": 3, "Prerequisites": "None", "Description": "Database and data warehouse administration and development tools.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5560", "Course Name": "Introduction to Big Data Science", "Credits": 3, "Prerequisites": "None", "Description": "Learn practical knowledge of Big Data, processing, and analysis.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5910", "Course Name": "Introduction to Big Data Analysis and Development", "Credits": 3, "Prerequisites": "None", "Description": "Learn basics of Big Data and Hadoop data intensive computing.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5300", "Course Name": "Enterprise Processes Integrations", "Credits": 3, "Prerequisites": "None", "Description": "Integrate technology and business processes using SAP tools.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5310", "Course Name": "Advanced Topics in Enterprise Systems", "Credits": 3, "Prerequisites": "None", "Description": "Orientation to Design Thinking methodology and state-of-the-art technologies.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5830", "Course Name": "Information Systems Consulting", "Credits": 3, "Prerequisites": "None", "Description": "Approaches and tools for consulting in information-age organizations.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5860", "Course Name": "Information Systems Project and Change Management", "Credits": 3, "Prerequisites": "None", "Description": "Project planning, staffing, control, and implementation of technology-based systems.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5600", "Course Name": "Computer Networks", "Credits": 3, "Prerequisites": "CIS 5850 or Consent", "Description": "Network theory, advanced network technology, and trends.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5710", "Course Name": "Multimedia Communication Applications", "Credits": 3, "Prerequisites": "CIS 5040 or Equivalent", "Description": "Techniques involved in multimedia communication applications.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5720", "Course Name": "Wireless Networks for Information Systems", "Credits": 3, "Prerequisites": "CIS 5040 or Equivalent", "Description": "Concepts in wireless communication networks for information systems.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5730", "Course Name": "Computer and Network Security", "Credits": 3, "Prerequisites": "CIS 5040 or Equivalent", "Description": "Concepts and techniques in computer and network security.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5840", "Course Name": "Controlling and Auditing Computer Systems", "Credits": 3, "Prerequisites": "None", "Description": "Controlling interactive computer/data communication systems.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5880", "Course Name": "Seminar Information Security", "Credits": 3, "Prerequisites": "CIS 5040 or Equivalent", "Description": "Broad coverage of CISSP Common Body of Knowledge.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "ACCT 5240A", "Course Name": "Accounting Information Systems", "Credits": 3, "Prerequisites": "Graduate Standing", "Description": "Focus on the study of accounting systems and internal controls.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5810", "Course Name": "Healthcare Information Systems", "Credits": 3, "Prerequisites": "None", "Description": "Overview of health care information technology applications.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5280", "Course Name": "Current Problems in Computer Information Systems", "Credits": 3, "Prerequisites": "None", "Description": "Latest research projects in computer information systems.", "Type": "Elective", "Status": "Not Started"},
    {"Course Code": "CIS 5980", "Course Name": "Graduate Directed Study", "Credits": 3, "Prerequisites": "None", "Description": "Investigation of an approved project leading to written report.", "Type": "Elective", "Status": "Not Started"},
]


core_courses = [course["Course Code"] for course in courses if course["Type"] == "Core"]
total_credits_required = 30

# Helper function to add notification
def add_notification(message):
    st.session_state["notifications"].append({"message": message, "timestamp": datetime.now()})

# Application Layout
st.set_page_config(
    page_title="Degree Progress Tracker",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Tabs
with st.sidebar:
    st.title("Degree Progress Tracker")
    tab = st.radio("Navigate", ["Dashboard", "Profile", "Homework Tracker", "Calendar"], index=0)

# Dashboard Tab
if tab == "Dashboard":
    st.header("Dashboard")
    
    # Notifications Bar
    if st.session_state["notifications"]:
        st.info("Notifications:")
        for note in st.session_state["notifications"][-5:]:
            st.write(f"🛎️ {note['message']} at {note['timestamp'].strftime('%H:%M:%S')}")

    # Course Selection
    st.subheader("Add Courses")
    selected_course = st.selectbox(
        "Select a course to add:",
        [f"{course['Course Code']} - {course['Course Name']}" for course in courses]
    )
    if st.button("Add Course"):
        course_code = selected_course.split(" - ")[0]
        if course_code not in st.session_state["user_courses"]:
            st.session_state["user_courses"].append(course_code)
            add_notification(f"Added course: {selected_course}")
            st.success(f"Course {selected_course} added!")
        else:
            st.warning(f"Course {selected_course} already added.")

    # Graduation Status Check
    st.subheader("Graduation Status")
    completed_credits = len(st.session_state["user_courses"]) * 3
    remaining_credits = total_credits_required - completed_credits
    missing_core_courses = [core for core in core_courses if core not in st.session_state["user_courses"]]

    if st.button("Check Graduation Status"):
        if completed_credits >= total_credits_required and not missing_core_courses:
            st.success("🎓 Congratulations! You're ready to graduate!")
            if "Degree Completed!" not in st.session_state["achievements"]:
                st.session_state["achievements"].append("Degree Completed!")
        else:
            st.warning(
                f"Credits Completed: {completed_credits}/{total_credits_required}. Missing Core Courses: {', '.join(missing_core_courses) or 'None'}."
            )

    # Badges / Achievements
    st.subheader("Achievements")
    if completed_credits >= 15 and "Halfway There!" not in st.session_state["achievements"]:
        st.session_state["achievements"].append("Halfway There!")
    for achievement in st.session_state["achievements"]:
        st.write(f"🏅 {achievement}")

    # Charts
    st.subheader("Progress Visualizations")
    pie_chart = px.pie(
        names=["Completed", "Remaining"],
        values=[completed_credits, remaining_credits],
        title="Progress Overview",
    )
    st.plotly_chart(pie_chart, use_container_width=True)

    bar_chart = px.bar(
        x=["Completed", "Remaining"],
        y=[completed_credits, remaining_credits],
        labels={"x": "Status", "y": "Credits"},
        title="Credit Distribution",
    )
    st.plotly_chart(bar_chart, use_container_width=True)

    column_chart = px.bar(
        x=st.session_state["user_courses"],
        y=[3] * len(st.session_state["user_courses"]),
        labels={"x": "Courses", "y": "Credits"},
        title="Courses Completed",
    )
    st.plotly_chart(column_chart, use_container_width=True)

# Profile Tab
elif tab == "Profile":
    st.header("Profile")
    st.write("Student Name: [Your Name]")
    st.write(f"Courses Completed: {len(st.session_state['user_courses'])}")
    st.write("Achievements:")
    for achievement in st.session_state["achievements"]:
        st.write(f"🏅 {achievement}")

# Homework Tracker Tab
elif tab == "Homework Tracker":
    st.header("Homework Tracker")
    if "homework" not in st.session_state:
        st.session_state["homework"] = []

    with st.form("Add Homework"):
        hw_course = st.selectbox("Select Course", [course["Course Code"] for course in courses])
        hw_details = st.text_input("Homework Details")
        hw_due_date = st.date_input("Due Date", datetime.now() + timedelta(days=7))
        submitted = st.form_submit_button("Add Homework")
        if submitted:
            st.session_state["homework"].append({"course": hw_course, "details": hw_details, "due_date": hw_due_date})
            st.success("Homework added!")

    st.subheader("Homework List")
    for hw in st.session_state["homework"]:
        st.write(f"📘 **{hw['course']}**: {hw['details']} (Due: {hw['due_date']})")

# Calendar Tab
elif tab == "Calendar":
    st.header("Calendar")
    st.write("🗓️ View and manage your academic schedule!")
    for hw in st.session_state.get("homework", []):
        st.write(f"📅 **{hw['due_date']}**: {hw['course']} - {hw['details']}")
