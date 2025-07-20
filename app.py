import io  # For image handling, if you ever use images from bytes
import os
import random

import streamlit as st

# --- GLOBAL PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Ticket Classifier",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize ALL Global Session State Variables HERE (ONLY ONCE) ---
st.session_state.setdefault("dark_mode", False)
st.session_state.setdefault("user", None)
st.session_state.setdefault("user_role", None)
st.session_state.setdefault("user_email_verified", False)
st.session_state.setdefault("profile_pic", None)
st.session_state.setdefault("user_name", "")
st.session_state.setdefault("time_zone", "UTC")

current_mode = st.session_state.get("dark_mode", False)

# --- GLOBAL CUSTOM CSS FOR PROFESSIONAL LOOK AND THEME MANAGEMENT ---
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }}
        .stApp {{
            background-color: {'#1C1E2B' if current_mode else '#FFFFFF'} !important;
            color: {'#E0E0E0' if current_mode else '#212529'} !important;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, {'0.2' if current_mode else '0.05'}) !important;
            transition: background-color 0.3s, color 0.3s;
            min-height: 100vh;
        }}
        .main-title {{
            font-size: 4.5em;
            color: {'#00C9A7' if current_mode else '#007BFF'} !important;
            text-align: center;
            margin-bottom: 50px;
            text-shadow: 3px 3px 8px rgba({{'0, 201, 167, 0.3' if current_mode else '0,0,0,0.1'}}) !important;
            font-weight: 800;
            letter-spacing: -1.5px;
        }}
        .stSubheader {{
            color: {'#A084E1' if current_mode else '#0056b3'} !important;
            font-size: 2.5em;
            margin-top: 55px;
            margin-bottom: 25px;
            border-bottom: 3px solid {'#3A3D4E' if current_mode else '#E9ECEF'} !important;
            padding-bottom: 12px;
            font-weight: 700;
            letter-spacing: -0.7px;
        }}
        .stBlock {{ margin-bottom: 30px; }}

        /* Enhanced input styling for dark mode */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div>div>input,
        .stSelectbox>div>div>div[data-baseweb="select"] {{
            background-color: {'#2A2E3E' if current_mode else '#F8F9FA'} !important;
            color: {'#FFFFFF' if current_mode else '#343A40'} !important;
            border: 1px solid {'#4A4E69' if current_mode else '#CED4DA'} !important;
            border-radius: 10px;
            padding: 12px;
            font-size: 1.1em;
            transition: all 0.2s ease-in-out;
        }}
        .stTextInput>div>div>input:focus,
        .stSelectbox>div>div>div>div>input:focus,
        .stSelectbox>div>div>div[data-baseweb="select"]:focus-within {{
            border-color: {'#A084E1' if current_mode else '#007BFF'} !important;
            box-shadow: 0 0 0 0.25rem rgba({{'160, 132, 225, .25' if current_mode else '0,123,255,.25'}}) !important;
            outline: none;
        }}
        .stTextInput>div>div>input[type='password'] {{
            color: {'#FFFFFF' if current_mode else '#343A40'} !important;
        }}

        /* Professional gradient button styling */
        .stButton>button {{
            background: linear-gradient(135deg, {'#0F4C75, #3282B8' if current_mode else '#3B4EF9, #8DF5F7'}) !important;
            color: #FFFFFF !important;
            border-radius: 10px;
            padding: 12px 30px;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 0 4px 12px {'rgba(15, 76, 117, 0.8)' if current_mode else 'rgba(59, 78, 249, 0.7)'} !important;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background: linear-gradient(135deg, {'#1B6CA8, #4A90E2' if current_mode else '#2A3BC0, #6EDFE0'}) !important;
            box-shadow: 0 6px 16px {'rgba(26, 108, 168, 1)' if current_mode else 'rgba(59, 78, 249, 0.9)'} !important;
            transform: translateY(-3px) !important;
        }}
        .stButton>button:active {{
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 6px {'rgba(15, 76, 117, 0.6)' if current_mode else 'rgba(59, 78, 249, 0.3)'} !important;
        }}
        .stFileUploader label {{
            font-size: 1.25em;
            font-weight: 600;
            color: {'#B0B0B0' if current_mode else '#343A40'} !important;
            margin-bottom: 10px;
            display: block;
        }}
        .stFileUploader>div>div>button {{
            background-color: {'#6C757D' if current_mode else '#6C757D'} !important;
            color: #E0E0E0 !important;
            border-radius: 10px;
            padding: 12px 20px;
            font-size: 1.1em;
            border: none;
        }}
        .stFileUploader>div>div>button:hover {{
            background-color: {'#7A828B' if current_mode else '#5A6268'} !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .stImage img {{
            border-radius: 18px;
            border: 5px solid {'#4A4E69' if current_mode else '#E0E0E0'} !important;
            box-shadow: 0 8px 20px rgba(0,0,0,{'0.25' if current_mode else '0.1'}) !important;
            object-fit: cover;
        }}
        .stToggle label {{
            font-size: 1.3em;
            font-weight: 600;
            color: {'#B0B0B0' if current_mode else '#343A40'} !important;
            margin-left: 10px;
        }}
        .stToggle [data-testid="stSwitchV1"] input[type="checkbox"] + div {{
            background-color: {'#5A607D' if current_mode else '#CED4DA'} !important;
            border-color: {'#6A708F' if current_mode else '#ADB5BD'} !important;
        }}
        .stToggle [data-testid="stSwitchV1"] input[type="checkbox"]:checked + div {{
            background-color: {'#00C9A7' if current_mode else '#28A745'} !important;
            border-color: {'#00C9A7' if current_mode else '#28A745'} !important;
        }}
        .stSuccess {{
            background-color: {'#2F4F4F' if current_mode else '#D4EDDA'} !important;
            color: {'#B0E0E6' if current_mode else '#155724'} !important;
            border-left: 8px solid {'#3CB371' if current_mode else '#28A745'} !important;
            padding: 20px;
            border-radius: 12px;
            margin-top: 25px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,{'0.15' if current_mode else '0.07'}) !important;
        }}
        .stInfo {{
            background-color: {'#2F3C57' if current_mode else '#D1ECF1'} !important;
            color: {'#ADD8E6' if current_mode else '#0C5460'} !important;
            border-left: 8px solid {'#6495ED' if current_mode else '#17A2B8'} !important;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,{'0.15' if current_mode else '0.07'}) !important;
        }}
        .stExpander div[data-baseweb="panel"] {{
            border: 1px solid {'#4A4E69' if current_mode else '#E0E0E0'} !important;
            border-radius: 15px;
            padding: 25px;
            background-color: {'#2A2E3E' if current_mode else '#FDFDFD'} !important;
            box-shadow: 0 4px 18px rgba(0,0,0,{'0.2' if current_mode else '0.06'}) !important;
            transition: background-color 0.3s, border-color 0.3s;
        }}
        .st-emotion-cache-1pxx795.e1f1d6gn0,
        .st-emotion-cache-nahz7x.e1f1d6gn0 {{
            padding-right: 20px;
            padding-left: 20px;
        }}
        hr {{
            margin-top: 60px;
            margin-bottom: 60px;
            border: 0;
            height: 3px;
            background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(255, 255, 255, {'0.15' if current_mode else '0.1'}), rgba(0, 0, 0, 0)) !important;
        }}
        .stCheckbox span {{
            font-size: 1.15em;
            font-weight: 500;
            color: {'#B0B0B0' if current_mode else '#343A40'} !important;
        }}
        /* === Robust dark mode label override for all input labels === */
        { '''
        [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] > p, label {
            color: #fff !important;
        }
        ''' if current_mode else '' }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTENT ---
with st.sidebar:
    st.markdown("### Theme Settings")
    dark_mode_toggle_value = st.toggle(
        "🌙 Enable Dark Mode",
        value=current_mode,
        key="global_dark_mode_toggle"
    )

    if dark_mode_toggle_value != current_mode:
        st.session_state.dark_mode = dark_mode_toggle_value
        st.rerun()

    st.markdown("---")

    if st.session_state.user is None:
        st.title("🔐 Authentication")
        page = st.radio("Choose Page", ["🔑 Login", "✍️ Register"])
    else:
        st.title("📚 Navigation")
        profile_pic_source = st.session_state.profile_pic if st.session_state.profile_pic else "https://via.placeholder.com/100?text=No+Photo"
        profile_pic_caption = st.session_state.user_name if st.session_state.user_name else "👤 User"
        st.image(profile_pic_source, width=100, caption=profile_pic_caption)
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        if st.session_state.user_role == "admin":
            page = st.radio("Admin Panel", ["📊 Dashboard", "📋 Logs", "⚙️ Settings"])
        else:
            page = st.radio("User Panel", ["📩 Submit Complaint", "⚙️ Settings"])

    st.markdown("---")
    st.title("🎫 Smart Ticket Classifier")
    st.write("Welcome to your personal AI-powered support system! 🤖")

    st.subheader("💡 What This App Does:")
    st.markdown("""
    - Submit your complaint using the form
    - Our model auto-classifies your issue
    - You get an email update instantly!
    """)

    st.markdown("Built with ❤️ using Python, Streamlit & Transformers.")
    st.markdown("---")
    st.caption("📦 `app.py`")

# ---------------------- MAIN ROUTING ----------------------
if st.session_state.user is None:
    if page == "🔑 Login":
        import pages.auth_login as auth
        auth.main()
    else:
        import pages.register as reg
        reg.main()
else:
    if st.session_state.user_role == "admin":
        if page == "📊 Dashboard":
            import pages.admin_dashboard as admin
            admin.main()
        elif page == "📋 Logs":
            import pages.Logs as logs  # <-- FIX: lowercase, not 'Logs'
            logs.main()
        else:
            import pages.settings as settings
            settings.main()
    else:
        if page == "📩 Submit Complaint":
            import pages.user_complaint as user
            user.main()
        else:
            import pages.settings as settings
            settings.main()

        # --- UNIQUE FEATURE: Quick Ticket Status Checker ---
        with st.expander("🔎 Quick Ticket Status Checker", expanded=False):
            st.markdown("Enter your ticket ID below to instantly check the status of your complaint.")
            ticket_id = st.text_input("Ticket ID", placeholder="e.g., TCKT-123456")
            if st.button("Check Status"):
                # Dummy logic for demonstration; replace with real DB/API lookup
                if ticket_id.strip() == "":
                    st.warning("Please enter a valid Ticket ID.")
                else:
                    statuses = [
                        ("🟢 Resolved", "Your ticket has been resolved. Please check your email for details."),
                        ("🟡 In Progress", "Your ticket is currently being reviewed by our support team."),
                        ("🔴 Pending", "Your ticket is pending. We will update you soon."),
                        ("⚪ Not Found", "No ticket found with this ID. Please check and try again.")
                    ]
                    cleaned_id = ticket_id.strip().upper()
                    # For demo, pick a status based on hash of ticket_id
                    idx = (sum(ord(c) for c in cleaned_id) % (len(statuses)-1)) if cleaned_id.startswith("TCKT") else 3
                    status, msg = statuses[idx]
                    st.info(f"**Status:** {status}\n\n{msg}")
# --- END OF MAIN ROUTING ---