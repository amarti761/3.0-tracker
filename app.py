import os
import json
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# File paths
COURSE_CATALOG_FILE = r"C:\Users\alici\Desktop\Degree Tracker\MSIS CATALOG SPREADSHEET - Sheet1 (2).csv"

# Load course catalog
if not os.path.exists(COURSE_CATALOG_FILE):
    raise FileNotFoundError(f"Course catalog file '{COURSE_CATALOG_FILE}' not found.")

course_data = pd.read_csv(COURSE_CATALOG_FILE)
course_catalog = [
    {"label": f"{row['Course Code']} - {row['Course Name']}", "value": row['Course Code']}
    for _, row in course_data.iterrows()
]

# Global data
user_courses = []
notifications = []
achievements = []
core_courses = ["CIS 5040", "CIS 5850", "CIS 5900"]  # Example core courses

# Layout
app.layout = dbc.Container(
    [
        html.H1("Degree Progress Tracker", className="text-center my-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="course-dropdown",
                            options=course_catalog,
                            placeholder="Select a course",
                            className="mb-3"
                        ),
                        dbc.Button("Add Course", id="add-course-button", color="primary", className="mb-3"),
                        html.Div(id="notifications-bar", className="alert alert-info mt-3"),
                        dbc.Button("Check Graduation Status", id="graduation-check-button", color="success", className="mb-3"),
                        html.Div(id="achievements", className="mt-3"),
                    ],
                    md=4
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="pie-chart", className="mb-3"),
                        dcc.Graph(id="bar-chart", className="mb-3"),
                        dcc.Graph(id="column-chart", className="mb-3"),
                    ],
                    md=8
                ),
            ]
        ),
        html.Div(
            dbc.Switch(
                id="dark-mode-toggle",
                label="Enable Dark Mode",
                className="mt-4"
            ),
            className="d-flex justify-content-end"
        ),
    ],
    fluid=True,
)

# Callbacks
@app.callback(
    [
        Output("notifications-bar", "children"),
        Output("pie-chart", "figure"),
        Output("bar-chart", "figure"),
        Output("column-chart", "figure"),
        Output("achievements", "children"),
    ],
    [
        Input("add-course-button", "n_clicks"),
        Input("graduation-check-button", "n_clicks"),
    ],
    State("course-dropdown", "value"),
)
def update_charts_and_status(add_clicks, grad_clicks, course_code):
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    notifications_content = "No notifications yet."
    achievements_html = html.Ul(
        [html.Li("No achievements yet. Add courses to earn badges!")]
    )

    # Default placeholder charts
    pie_chart = px.pie(
        values=[1],
        names=["No Data"],
        title="Progress Overview",
    )
    bar_chart = px.bar(
        x=["No Data"],
        y=[0],
        title="Credit Distribution",
    )
    column_chart = px.bar(
        x=["No Data"],
        y=[0],
        title="Courses Completed",
    )

    if triggered_id == "add-course-button":
        if not course_code or add_clicks is None:
            return (
                "No course selected.",
                pie_chart,
                bar_chart,
                column_chart,
                achievements_html,
            )

        # Add course to user data
        if course_code not in user_courses:
            user_courses.append(course_code)
            notifications.append(f"Course '{course_code}' added.")
        notifications_content = html.Div([html.P(note) for note in notifications])

        # Update progress
        total_credits = 30
        completed_credits = len(user_courses) * 3
        remaining_credits = total_credits - completed_credits

        pie_chart = px.pie(
            values=[completed_credits, remaining_credits],
            names=["Completed", "Remaining"],
            title="Progress Overview",
        )
        bar_chart = px.bar(
            x=["Completed", "Remaining"],
            y=[completed_credits, remaining_credits],
            labels={"x": "Status", "y": "Credits"},
            title="Credit Distribution",
        )
        column_chart = px.bar(
            x=user_courses,
            y=[3] * len(user_courses),
            labels={"x": "Courses", "y": "Credits"},
            title="Courses Completed",
        )

        # Achievements
        if completed_credits >= 15 and "Halfway There!" not in achievements:
            achievements.append("Halfway There!")
        if completed_credits >= 30 and "Degree Completed!" not in achievements:
            achievements.append("Degree Completed!")

        achievement_icons = {"Halfway There!": "🏅", "Degree Completed!": "🎓"}
        achievements_html = html.Ul(
            [
                html.Li(f"{achievement_icons.get(achievement, '')} {achievement}")
                for achievement in achievements
            ]
        )

    elif triggered_id == "graduation-check-button":
        completed_core = [course for course in core_courses if course in user_courses]
        missing_core = [course for course in core_courses if course not in user_courses]
        completed_credits = len(user_courses) * 3

        if completed_credits >= 30 and len(missing_core) == 0:
            achievements_html = html.Div(
                "🎓 Congratulations! You're ready to graduate!",
                className="text-success"
            )
        else:
            achievements_html = html.Div(
                [
                    html.P(f"Credits Completed: {completed_credits}/30"),
                    html.P(f"Missing Core Courses: {', '.join(missing_core) or 'None'}"),
                    html.P("Keep going! You're almost there!"),
                ]
            )

    return notifications_content, pie_chart, bar_chart, column_chart, achievements_html

@app.callback(
    Output("page-content", "className"),
    Input("dark-mode-toggle", "value"),
)
def toggle_dark_mode(is_dark_mode):
    return "dark-mode" if is_dark_mode else "light-mode"

# Run the server
import os

# At the end of your app.py
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Use the PORT variable provided by Render
    app.run_server(debug=True, host="0.0.0.0", port=port)  # Bind to all IPs and use the port

