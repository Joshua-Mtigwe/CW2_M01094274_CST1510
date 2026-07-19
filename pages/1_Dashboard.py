import streamlit as st, pandas as pd, time, plotly.express as px

from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.db import get_connection

#I am configuring the page layout to wide mode so our charts and dataframes have plenty of horizontal space.
st.set_page_config(page_title="Home", page_icon="🏡", layout="wide")

#I need to enforce a security checkpoint to keep unauthenticated users out of the dashboard.
if "logged_in" not in st.session_state:
    st.warning("Please sign in to access the dashboard.")
    with st.spinner("Teleporting you to Home page...🚀"):
        time.sleep(1.5)
        st.switch_page("Home.py")
    st.stop()
else:
    st.success("Successfully Signed In!")

st.title("Welcome to the Cyber Incidents Dashboard🛡️")

#Fetching our core dataset directly from the active database connection.
conn = get_connection()
data = get_all_cyber_incidents(conn)

#Setting up a localized filtering panel in the sidebar to keep the main view clean.
with st.sidebar:
    st.header("Navigation")
    severity_ = st.selectbox("Severity Level", data["severity"].unique())

#Standardizing timestamps to datetime objects so our grouping calculations don't break.
data["timestamp"] = pd.to_datetime(data["timestamp"])
filtered_data = data[data["severity"] == severity_]

st.subheader(f"Cyber Incident Categories by Month for {severity_} Severity")

#I am loading the raw CSV here to ensure we have a fallback or comparison dataset if needed.
df = pd.read_csv("DATA/cyber_incidents.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

#I chose 'MS' frequency to bucket incidents into the first day of each respective month for clean timeline intervals.
trend = (
    filtered_data.groupby(
        [pd.Grouper(key="timestamp", 
                    freq="MS"), 
                    "category"]
    )
    .size()
    .reset_index(name="Count")
)

trend = trend.sort_values(["timestamp", "category"])

fig = px.bar(
    trend,
    x="timestamp",
    y="Count",
    color="category",
)

#Chose 'x unified' hover mode here because I want the user to see a  breakdown of all categories at that exact point in time.
fig.update_layout(
    barmode="stack",
    xaxis_title="Month",
    yaxis_title="Number of Incidents",
    hovermode="x unified",
    legend_title="Category",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader(f"Cyber Incidents with {severity_} Severity")
pie_data = filtered_data["category"].value_counts().reset_index()
pie_data.columns = ["category", "count"]

fig = px.pie(
    pie_data,
    names="category",
    values="count",
    title="Category Distribution",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)

#I put labels inside the pie slices to reduce reliance on the legend.
fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered Data")

#Isolating specific columns to keep the display relevant and avoid overloading the user with info.
filtered_df = filtered_data[
    [
        "timestamp",
        "category",
        "severity",
        "status",
        "description",
        "incident_id",
    ]
]

#I am reformatting the date strings for standard user readability inside the UI table component.
filtered_df["timestamp"] = pd.to_datetime(filtered_df["timestamp"]).dt.strftime(
    "%d %b %Y %H:%M"
)

#Hiding the default dataframe index because it doesn't add contextual value to the security logs.
st.dataframe(filtered_df, 
    hide_index=True, 
    use_container_width=True
)