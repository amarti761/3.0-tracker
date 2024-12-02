import streamlit as st
import plotly.express as px
import sqlite3
import bcrypt
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta

# Initialize database connection
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# Create tables for user authentication and data storage
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS user_data (
    user_id INTEGER,
    data TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

conn.commit()

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

# Helper functions
def add_notification(message):
    if "notifications" not in st.session_state:
        st.session_state["notifications"] = []
    st.session_state["notifications"].append({"message": message, "timestamp": datetime.now()})

def register_user(username, email, password):
    try:
        validate_email(email)
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                  (username, email, hashed_password))
        conn.commit()
        st.success("Account created successfully!")
    except EmailNotValidError as e:
        st.error(f"Invalid email: {e}")
    except sqlite3.IntegrityError:
        st.error("Username or email already exists.")

def login_user(username, password):
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        return user[0]
    return None

def reset_password(email, new_password):
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
    conn.commit()

def save_user_data(user_id, data):
    c.execute("INSERT INTO user_data (user_id, data) VALUES (?, ?)", (user_id, data))
    conn.commit()

def get_user_data(user_id):
    c.execute("SELECT data FROM user_data WHERE user_id = ?", (user_id,))
    return c.fetchall()

# Streamlit page configuration
st.set_page_config(
    page_title="Degree Progress Tracker",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for user authentication
with st.sidebar:
    st.title("Degree Progress Tracker")
    if "user_id" not in st.session_state:
        auth_tab = st.radio("Authentication", ["Login", "Register", "Forgot Password"])

        if auth_tab == "Register":
            st.subheader("Create an Account")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            if st.button("Register"):
                if password == confirm_password:
                    register_user(username, email, password)
                else:
                    st.error("Passwords do not match.")

        elif auth_tab == "Login":
            st.subheader("Login")
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            if st.button("Login"):
                user_id = login_user(login_username, login_password)
                if user_id:
                    st.session_state["user_id"] = user_id
                    st.success(f"Welcome, {login_username}!")
                else:
                    st.error("Invalid username or password.")

        elif auth_tab == "Forgot Password":
            st.subheader("Forgot Password")
            reset_email = st.text_input("Enter your email")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            if st.button("Reset Password"):
                if new_password == confirm_new_password:
                    reset_password(reset_email, new_password)
                    st.success("Password reset successfully!")
                else:
                    st.error("Passwords do not match.")
    else:
        if st.sidebar.button("Logout"):
            del st.session_state["user_id"]
            st.success("Logged out successfully!")

# Main app layout
if "user_id" in st.session_state:
    tab = st.sidebar.radio("Navigate", ["Dashboard", "Profile", "Homework Tracker", "Calendar"])

    # Dashboard
    if tab == "Dashboard":
        st.header("Dashboard")
        completed_credits = len(st.session_state.get("user_courses", [])) * 3
        remaining_credits = total_credits_required - completed_credits
        missing_core_courses = [core for core in core_courses if core not in st.session_state.get("user_courses", [])]

        st.subheader("Graduation Status")
        if st.button("Check Graduation Status"):
            if completed_credits >= total_credits_required and not missing_core_courses:
                st.success("🎓 Congratulations! You're ready to graduate!")
                if "Degree Completed!" not in st.session_state.get("achievements", []):
                    st.session_state["achievements"].append("Degree Completed!")
            else:
                st.warning(
                    f"Credits Completed: {completed_credits}/{total_credits_required}. "
                    f"Missing Core Courses: {', '.join(missing_core_courses) or 'None'}."
                )

        st.subheader("Progress Visualizations")
        pie_chart = px.pie(
            names=["Completed", "Remaining"],
            values=[completed_credits, remaining_credits],
            title="Progress Overview",
        )
        st.plotly_chart(pie_chart, use_container_width=True)

    # Profile
    elif tab == "Profile":
        st.header("Profile")
        user_data = get_user_data(st.session_state["user_id"])
        st.write(f"Courses Completed: {len(st.session_state.get('user_courses', []))}")
        st.write("Achievements:")
        for achievement in st.session_state.get("achievements", []):
            st.write(f"🏅 {achievement}")
        st.subheader("Personal Data")
        for data in user_data:
            st.write(data[0])

    # Homework Tracker
    elif tab == "Homework Tracker":
        st.header("Homework Tracker")
        # Homework tracker logic...

    # Calendar
    elif tab == "Calendar":
        st.header("Calendar")
        # Calendar logic...
