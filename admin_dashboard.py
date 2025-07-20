import os
import smtplib
import urllib.parse
from email.mime.text import MIMEText

import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def send_resolution_email(user_email, timestamp):
    ADMIN_EMAIL = "eddalatejaswi@gmail.com"
    APP_PASSWORD = "vtdl tqhb vxyp rozr"

    encoded_email = urllib.parse.quote_plus(user_email)
    encoded_time = urllib.parse.quote_plus(timestamp)

    subject = "🛠 Is Your Complaint Resolved?"
    body = f"""
    Hi {user_email},

    Our team has marked your complaint as resolved.

    Please confirm if your issue is resolved:
    ✅ Yes: http://localhost:8501/confirm?email={encoded_email}&timestamp={encoded_time}&response=yes
    ❌ No: http://localhost:8501/confirm?email={encoded_email}&timestamp={encoded_time}&response=no

    Thank you,
    Support Team
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = ADMIN_EMAIL
    msg["To"] = user_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(ADMIN_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
        return False

def show_insights(df):
    st.markdown("---")
    st.subheader("📊 Complaint Insights & Analytics")

    # Basic summary stats
    total_complaints = len(df)
    resolved_count = (df["status"].str.lower() == "resolved").sum()
    awaiting_count = (df["status"].str.lower() == "awaiting user confirmation").sum()
    reopened_count = (df["status"].str.lower() == "reopened").sum()
    unresolved_count = (df["status"].str.lower() == "unresolved").sum()
    high_priority_count = (df["priority"].str.lower() == "high").sum()

    st.markdown(
        f"""
        <div style="display:flex;gap:2rem;flex-wrap:wrap;">
            <div><b>Total Complaints:</b> {total_complaints}</div>
            <div><b>Resolved:</b> {resolved_count}</div>
            <div><b>Awaiting User:</b> {awaiting_count}</div>
            <div><b>Reopened:</b> {reopened_count}</div>
            <div><b>Unresolved:</b> {unresolved_count}</div>
            <div><b>High Priority:</b> {high_priority_count}</div>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("")
    col1, col2 = st.columns(2)

    # Complaints by category (bar chart)
    with col1:
        if "category" in df.columns:
            cat_counts = df["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            chart = alt.Chart(cat_counts).mark_bar().encode(
                x=alt.X("Category", sort='-y'),
                y="Count",
                tooltip=["Category", "Count"]
            ).properties(title="Complaints by Category", width=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No 'category' column found in data.")

    # Status distribution (pie chart)
    with col2:
        status_counts = df["status"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        plt.title("Status Distribution")
        st.pyplot(fig1)

    st.markdown("")
    col3, col4 = st.columns(2)

    # Priority distribution (bar or pie)
    with col3:
        priority_counts = df["priority"].value_counts().reset_index()
        priority_counts.columns = ["Priority", "Count"]
        chart2 = alt.Chart(priority_counts).mark_bar().encode(
            x=alt.X("Priority", sort=["High", "Medium", "Low"]),
            y="Count",
            color="Priority",
            tooltip=["Priority", "Count"]
        ).properties(title="Priority Level Distribution", width=300)
        st.altair_chart(chart2, use_container_width=True)

    with col4:
        fig2, ax2 = plt.subplots()
        ax2.pie(priority_counts["Count"], labels=priority_counts["Priority"], autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        plt.title("Priority Distribution")
        st.pyplot(fig2)

def show_insights_plotly(df):
    st.markdown("---")
    st.subheader("📊 Complaint Insights & Analytics (Plotly)")

    # Summary statistics
    try:
        total_complaints = len(df)
        resolved_count = (df["status"].str.lower() == "resolved").sum()
        awaiting_count = (df["status"].str.lower() == "awaiting user confirmation").sum()
        reopened_count = (df["status"].str.lower() == "reopened").sum()
        unresolved_count = (df["status"].str.lower() == "unresolved").sum()
        high_priority_count = (df["priority"].str.lower() == "high").sum()
    except Exception:
        st.warning("Some required columns for summary statistics are missing.")
        return

    st.markdown(
        f"""
        <div style="display:flex;gap:2rem;flex-wrap:wrap;">
            <div><b>Total Complaints:</b> {total_complaints}</div>
            <div><b>Resolved:</b> {resolved_count}</div>
            <div><b>Awaiting User:</b> {awaiting_count}</div>
            <div><b>Reopened:</b> {reopened_count}</div>
            <div><b>Unresolved:</b> {unresolved_count}</div>
            <div><b>High Priority:</b> {high_priority_count}</div>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("")
    col1, col2 = st.columns(2)

    # Pie Chart: Status Distribution
    with col1:
        if "status" in df.columns and not df["status"].isnull().all():
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig = px.pie(status_counts, names="Status", values="Count", title="Status Distribution", hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No 'status' column found in data.")

    # Pie Chart: Priority Distribution
    with col2:
        if "priority" in df.columns and not df["priority"].isnull().all():
            priority_counts = df["priority"].value_counts().reset_index()
            priority_counts.columns = ["Priority", "Count"]
            fig2 = px.pie(priority_counts, names="Priority", values="Count", title="Priority Distribution", hole=0.3)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No 'priority' column found in data.")

    st.markdown("")
    col3, col4 = st.columns(2)

    # Bar Chart: Complaints by Category
    with col3:
        if "category" in df.columns and not df["category"].isnull().all():
            cat_counts = df["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig3 = px.bar(cat_counts, x="Category", y="Count", title="Complaints by Category", color="Category")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("No 'category' column found in data.")

    # Bar or Pie Chart: Rating Distribution
    with col4:
        if "user_feedback" in df.columns and not df["user_feedback"].isnull().all():
            rating_counts = df["user_feedback"].value_counts().reset_index()
            rating_counts.columns = ["Rating", "Count"]
            fig4 = px.bar(rating_counts, x="Rating", y="Count", title="Rating Distribution", color="Rating")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("No 'user_feedback' column found in data.")

def main():
    st.markdown("<h2 style='text-align:center;'>🛠 Smart Admin Panel</h2>", unsafe_allow_html=True)

    log_path = "logs/predictions.csv"
    if not os.path.exists(log_path):
        st.warning("⚠️ No complaint logs found.")
        return

    try:
        df = pd.read_csv(log_path)
        df['email'] = df['email'].astype(str).str.strip().str.lower()
        df['timestamp'] = df['timestamp'].astype(str).str.strip()
    except Exception as e:
        st.error(f"❌ Failed to read CSV: {e}")
        return

    # Prepare necessary columns
    for col, default in [("status", "Unresolved"), ("notes", ""), ("priority", "Medium"), ("user_confirmation", "Pending")]:
        if col not in df.columns:
            df[col] = default

    df["priority"] = pd.Categorical(df["priority"], categories=["High", "Medium", "Low"], ordered=True)
    df = df.sort_values(by=["status", "priority"], ascending=[True, True])

    st.subheader("📋 All Complaints")

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True)
    gb.configure_column("status", editable=False)
    gb.configure_column("priority", editable=True, cellEditor='agSelectCellEditor',
                         cellEditorParams={"values": ["High", "Medium", "Low"]})
    gb.configure_column("notes", editable=True)
    gb.configure_column("user_confirmation", editable=False)
    gb.configure_selection("single")

    grid = AgGrid(df, gridOptions=gb.build(), update_mode=GridUpdateMode.MODEL_CHANGED,
                  fit_columns_on_grid_load=True)

    # ✅ Save updates
    if st.button("💾 Save All Changes"):
        updated_df = grid["data"]
        updated_df.to_csv(log_path, index=False)
        st.success("✅ Changes saved to log file.")

    selected = grid.get("selected_rows", [])
    if isinstance(selected, pd.DataFrame):
        selected = selected.to_dict(orient='records')

    if selected and len(selected) > 0:
        selected_row = selected[0]
        raw_email = selected_row.get("email", "").strip().lower()
        timestamp = str(selected_row.get("timestamp", "")).strip()

        if not raw_email or not timestamp:
            st.warning("⚠️ Email or timestamp missing in selected complaint.")
            return

        st.info(f"Selected: {raw_email} | Time: {timestamp}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📩 Send Resolution Confirmation Email"):
                df.loc[(df["email"] == raw_email) & (df["timestamp"] == timestamp), "status"] = "Awaiting User Confirmation"
                df.to_csv(log_path, index=False)
                if send_resolution_email(raw_email, timestamp):
                    st.success("📬 Email sent to user.")

        with col2:
            if st.button("🔄 Reopen Complaint"):
                df.loc[(df["email"] == raw_email) & (df["timestamp"] == timestamp), "status"] = "Reopened"
                df.to_csv(log_path, index=False)
                st.success("🔁 Complaint status updated.")

    # Add single insights selector
    st.markdown("---")
    insight_mode = st.radio("How would you like to view insights?", ["Classic (Altair/Matplotlib)", "Plotly"], index=0)
    if st.button("📊 Show Insights"):
        if insight_mode == "Classic (Altair/Matplotlib)":
            show_insights(df)
        else:
            show_insights_plotly(df)

if __name__ == "__main__":
    main()
