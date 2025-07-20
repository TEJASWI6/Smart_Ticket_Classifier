def apply_theme():
    import streamlit as st

    if st.session_state.get("dark_mode"):
        st.markdown("""
            <style>
                body {
                    background-color: #111 !important;
                    color: #eee !important;
                }
                .main-title {
                    color: #ff4b4b !important;
                    text-shadow: 0 0 20px #ff4b4b !important;
                }
                textarea, input {
                    background: #1f1f1f !important;
                    color: #eee !important;
                    border-color: #444 !important;
                }
                .result-card {
                    background: #1f1f1f !important;
                    border: 1px solid #444 !important;
                }
            </style>
        """, unsafe_allow_html=True)
