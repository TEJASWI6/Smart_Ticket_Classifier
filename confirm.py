import os
import urllib.parse

import pandas as pd
import streamlit as st


def main():
    st.markdown(
        "<h2 style='text-align:center;'>📬 Confirm Complaint Resolution</h2>",
        unsafe_allow_html=True
    )

    query_params = st.query_params

    # Extract parameters safely
    email_raw = query_params.get("email")
    timestamp_raw = query_params.get("timestamp")
    response_raw = query_params.get("response")

    email = urllib.parse.unquote(email_raw or "").strip().lower()
    timestamp = urllib.parse.unquote(timestamp_raw or "").strip()
    response = (response_raw or "").strip().lower()

    if not email or not timestamp or not response:
        st.warning("😕 Oops! That link doesn't look right. Please try again.")
        return

    log_path = "logs/predictions.csv"
    if not os.path.exists(log_path):
        st.error("📂 Complaint records not found. Something’s missing behind the scenes!")
        return

    try:
        df = pd.read_csv(log_path)
        df["email"] = df["email"].astype(str).str.strip().str.lower()
        df["timestamp"] = df["timestamp"].astype(str).str.strip()
    except Exception as e:
        st.error("😓 Unable to open complaints file. Technical gremlins at work!")
        return

    match = (df["email"] == email) & (df["timestamp"] == timestamp)

    if not match.any():
        st.error("❌ Hmm... We couldn’t find your complaint. Maybe a typo snuck in?")
        return

    # Update based on response
    if response == "yes":
        df.loc[match, "status"] = "Resolved"
        df.loc[match, "user_confirmation"] = "Confirmed"
        df.to_csv(log_path, index=False)
        st.success("🎉 Yay! We're glad your issue is resolved. Thanks for confirming! 😊")

        # Rating feedback
        st.markdown("#### Please rate your experience (1 = Poor, 5 = Excellent):")
        rating = st.radio("Your Rating", [1, 2, 3, 4, 5], horizontal=True, key="rating")
        if st.button("Submit Rating"):
            df.loc[match, "user_feedback"] = rating
            df.to_csv(log_path, index=False)
            st.success("🙏 Thank you for your feedback! We appreciate your input.")
            
    elif response == "no":
        df.loc[match, "status"] = "Reopened"
        df.loc[match, "user_confirmation"] = "Rejected"
        st.info("🔁 No worries! We've reopened your complaint and our team will jump on it. 🛠️")
        
        feedback = st.text_area("We'd love to know more. Please share any additional feedback (optional):", key="feedback")
        if st.button("Submit Feedback"):
            df.loc[match, "user_feedback"] = feedback
            df.to_csv(log_path, index=False)
            st.success("🙏 Thank you for your feedback! Our team will review it carefully.")
        else:
            df.to_csv(log_path, index=False)
    else:
        st.warning("⚠️ Uh-oh! That response doesn’t seem right. Please try the link again.")
        return

    st.markdown("---")
    if st.button("⬅️ Back to App"):
        st.switch_page("app.py")  # Make sure your app structure supports this

if __name__ == "__main__":
    main()
