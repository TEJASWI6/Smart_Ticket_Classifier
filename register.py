def main():
    import pyrebase
    import streamlit as st

    from firebase_config import firebase_config

    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()

    st.markdown("<h2 style='text-align:center;'>✍️ Register</h2>", unsafe_allow_html=True)

    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Register"):
        if not email or not password:
            st.warning("⚠️ Please enter email and password.")
        else:
            try:
                auth.create_user_with_email_and_password(email, password)
                auth.send_email_verification(auth.sign_in_with_email_and_password(email, password)['idToken'])
                st.success("✅ Registered! Check your email to verify.")
            except Exception as e:
                st.error(f"❌ Registration failed: {e}")
