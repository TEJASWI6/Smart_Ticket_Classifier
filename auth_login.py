def main():
    import pyrebase
    import streamlit as st

    from firebase_config import firebase_config

    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()

    st.markdown("<h2 style='text-align:center;'>🔐 Login to Your Account</h2>", unsafe_allow_html=True)

    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("⚠️ Please enter both email and password.")
        else:
            try:
                # ✅ Sign in user
                user = auth.sign_in_with_email_and_password(email, password)

                # ✅ Get latest account info
                user_info = auth.get_account_info(user['idToken'])
                is_verified = user_info['users'][0].get('emailVerified', False)

                if is_verified:
                    # ✅ Set session
                    st.session_state.user = email
                    st.session_state.user_email_verified = True
                    st.session_state.user_role = "admin" if email == "eddalatejaswi@gmail.com" else "user"
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.warning("📩 Please verify your email first. Check your inbox (or spam).")

            except Exception as e:
                error_str = str(e)
                if "EMAIL_NOT_FOUND" in error_str or "INVALID_PASSWORD" in error_str:
                    st.error("❌ Invalid credentials. Please check your email and password.")
                else:
                    st.error(f"❌ Login failed: {error_str}")
