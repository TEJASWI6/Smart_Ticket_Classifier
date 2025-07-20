def main():
    import pandas as pd
    import streamlit as st

    st.markdown("<h2 style='text-align:center;'>📋 AI Ticket Logs</h2>", unsafe_allow_html=True)

    try:
        df = pd.read_csv("logs/predictions.csv")

        expected_columns = ['ticket_num','email', 'text', 'category', 'confidence', 'timestamp', 'user_role','status','notes','priority','user_confirmation','user_feedback']
        if list(df.columns) != expected_columns:
            st.warning("⚠️ Column mismatch in logs. Please check CSV headers.")
            return

        if df.empty:
            st.warning("⚠️ No logs found yet. Try submitting a complaint.")
        else:
            st.dataframe(df[::-1])  # Newest logs first

    except FileNotFoundError:
        st.warning("⚠️ Log file not found. Try submitting a complaint.")
    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
