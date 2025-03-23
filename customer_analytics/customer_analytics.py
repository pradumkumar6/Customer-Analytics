import streamlit as st
import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Customer Behavior Analysis",
    layout="wide"
)

# MongoDB Connection
@st.cache_resource
def init_connection():
    uri = "Your MongoDb Uri"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client

# Get data from MongoDB

def get_data():
    client = init_connection()
    
    # ✅ Use the correct database name
    db = client.customer_click_behaviour  # Fixed typo in DB name
    data = list(db.click_data.find({}, {'_id': 0}))

    if not data:
        st.error("No data retrieved from MongoDB.")
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # ✅ Ensure timestamp conversion
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
        st.warning("No 'timestamp' field found. Using current timestamp as fallback.")
        df['timestamp'] = datetime.now()

    return df


# Load data
df = get_data()

# Layout
st.title("📊 Customer Behavior Analysis Dashboard")

# First row - Key Metrics
st.subheader("Key Metrics")
col_metrics = st.columns(4)

with col_metrics[0]:
    total_users = df['user_id'].nunique()
    st.metric("Total Users", total_users)

with col_metrics[1]:
    total_activities = len(df)
    st.metric("Total Activities", total_activities)

with col_metrics[2]:
    unique_products = df['product'].nunique()
    st.metric("Unique Products", unique_products)

with col_metrics[3]:
    activities_per_user = total_activities / total_users
    st.metric("Activities per User", f"{activities_per_user:.1f}")

# Second row - Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Activity Timeline")
    # Group by date and count activities
    daily_activity = df.groupby(df['timestamp'].dt.date).size().reset_index()
    daily_activity.columns = ['date', 'count']
    
    timeline = px.line(
        daily_activity,
        x='date',
        y='count',
        title='Daily Activity Count'
    )
    timeline.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Activities"
    )
    st.plotly_chart(timeline, use_container_width=True)

with col2:
    st.subheader("Product Distribution")
    product_dist = df['product'].value_counts()
    product_pie = px.pie(
        values=product_dist.values,
        names=product_dist.index,
        title='Distribution by Product'
    )
    st.plotly_chart(product_pie, use_container_width=True)

# Third row - Charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("Activity Types")
    activity_counts = df['activity'].value_counts()
    activity_bar = px.bar(
        x=activity_counts.index,
        y=activity_counts.values,
        title='Activity Distribution'
    )
    activity_bar.update_layout(
        xaxis_title="Activity Type",
        yaxis_title="Count"
    )
    st.plotly_chart(activity_bar, use_container_width=True)

with col4:
    st.subheader("User Activity Patterns")
    user_activity = df.groupby('user_id').size().sort_values(ascending=False)
    user_activity_df = pd.DataFrame(user_activity).reset_index()
    user_activity_df.columns = ['user_id', 'activity_count']
    
    user_patterns = px.bar(
        user_activity_df.head(10),
        x='user_id',
        y='activity_count',
        title='Top 10 Most Active Users'
    )
    user_patterns.update_layout(
        xaxis_title="User ID",
        yaxis_title="Number of Activities"
    )
    st.plotly_chart(user_patterns, use_container_width=True)

# Recent Activity Table
st.subheader("Recent Activities")
recent_activities = df.sort_values('timestamp', ascending=False).head(10)
st.dataframe(
    recent_activities[['timestamp', 'user_id', 'activity', 'product']],
    use_container_width=True
)

# Sidebar filters
st.sidebar.title("Filters")
# Date range filter
min_date = df['timestamp'].min().date()
max_date = df['timestamp'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Activity type filter
activities = sorted(df['activity'].unique())
selected_activities = st.sidebar.multiselect(
    "Select Activities",
    activities,
    default=activities
)

# Product filter
products = sorted(df['product'].unique())
selected_products = st.sidebar.multiselect(
    "Select Products",
    products,
    default=products
)