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
if "profile_pic" not in st.session_state:
    st.session_state["profile_pic"] = None
if "user_name" not in st.session_state:
    st.session_state["user_name"] = "Your Name"
if "personal_notes" not in st.session_state:
    st.session_state["personal_notes"] = []
if "homework" not in st.session_state:
    st.session_state["homework"] = []

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

# Custom CSS for Styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f7fc;
        font-family: Arial, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #343a40;
        color: white;
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #0056b3;
        transition: background-color 0.3s ease;
    }
    .custom-header {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    .tab-content {
        animation: fadeIn 1s;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Tabs
with st.sidebar:
    st.title("📚 Degree Progress Tracker")
    tab = st.radio("Navigate", ["Dashboard", "Profile", "Homework Tracker", "Calendar"], index=0)

# Dashboard Tab
if tab == "Dashboard":
    st.markdown('<div class="custom-header"><h1>Dashboard</h1></div>', unsafe_allow_html=True)
    st.subheader("📊 Progress Overview")
    # Dashboard code remains the same...

# Profile Tab
elif tab == "Profile":
    st.markdown('<div class="custom-header"><h1>Profile</h1></div>', unsafe_allow_html=True)
    st.subheader("👤 User Profile")

    # Profile Picture
    uploaded_pic = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
    if uploaded_pic:
        st.session_state["profile_pic"] = uploaded_pic
        st.success("Profile picture updated!")

    if st.session_state["profile_pic"]:
        st.image(st.session_state["profile_pic"], caption="Your Profile Picture", use_column_width=True)

    # Editable User Name
    user_name = st.text_input("Name", st.session_state["user_name"])
    if st.button("Update Name"):
        st.session_state["user_name"] = user_name
        st.success("Name updated!")

    st.write(f"**Name:** {st.session_state['user_name']}")

    # Personal Notes Section
    st.subheader("📝 Personal Notes")
    new_note = st.text_area("Write a note:")
    if st.button("Add Note"):
        if new_note.strip():
            st.session_state["personal_notes"].append({"note": new_note, "timestamp": datetime.now()})
            st.success("Note added!")
        else:
            st.warning("Note cannot be empty.")

    for note in st.session_state["personal_notes"]:
        st.write(f"- {note['note']} (Added on {note['timestamp'].strftime('%Y-%m-%d %H:%M:%S')})")

# Homework Tracker Tab
elif tab == "Homework Tracker":
    st.markdown('<div class="custom-header"><h1>Homework Tracker</h1></div>', unsafe_allow_html=True)
    st.subheader("📝 Manage Your Homework Assignments")

    with st.form("Homework Form"):
        hw_course = st.selectbox("Select Course", [course["Course Code"] for course in courses])
        hw_details = st.text_input("Homework Details")
        hw_due_date = st.date_input("Due Date", datetime.now() + timedelta(days=7))
        submitted = st.form_submit_button("Add Homework")
        if submitted:
            st.session_state["homework"].append({"course": hw_course, "details": hw_details, "due_date": hw_due_date})
            st.success("Homework added!")

    st.subheader("📖 Homework List")
    for hw in st.session_state["homework"]:
        st.write(f"📘 **{hw['course']}**: {hw['details']} (Due: {hw['due_date']})")

# Calendar Tab
elif tab == "Calendar":
    st.markdown('<div class="custom-header"><h1>Calendar</h1></div>', unsafe_allow_html=True)
    st.subheader("🗓️ Your Schedule")

    if st.session_state["homework"]:
        for hw in st.session_state["homework"]:
            st.write(f"📅 **{hw['due_date']}** - **{hw['course']}**: {hw['details']}")
    else:
        st.info("No events or deadlines on your calendar.")
