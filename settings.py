# pages/settings.py

import io

import streamlit as st
from PIL import Image


def main():
    # --- IMPORTANT: st.set_page_config() and global CSS are now handled in app.py.
    # This file focuses purely on the UI components and their logic.

    # --- Initialize Session State Variables (for this page's components) ---
    # These variables persist across reruns of the app.
    # Ensure these are initialized here as they are specific to this page's components.
    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "notifications" not in st.session_state:
        st.session_state.notifications = True
    if "profile_pic" not in st.session_state:
        st.session_state.profile_pic = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "time_zone" not in st.session_state:
        st.session_state.time_zone = "UTC"


    # ---------- UI Layout and Components ----------
    # Removed the main title as it's now in app.py for better consistency.
    # st.markdown("<h1 class='main-title'>⚙️ User Settings</h1>", unsafe_allow_html=True)

    # --- Section 1: Profile and Account ---
    st.subheader("👤 Profile & Account")
    st.write("Manage your personal information and profile picture.")
    st.markdown("<br>", unsafe_allow_html=True) # Add some vertical space

    # User Name Input
    user_name = st.text_input(
        "Your Name",
        value=st.session_state.user_name,
        placeholder="Enter your full name",
        key="user_name_input"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Profile Picture Upload and Display
    col1, col2 = st.columns([1, 2]) # Adjusted column ratio for better visual balance

    with col1:
        # Determine the image source and caption based on whether a profile pic is set
        image_source = st.session_state.profile_pic if st.session_state.profile_pic else "https://via.placeholder.com/180?text=No+Photo"
        caption_text = "Your Current Photo" if st.session_state.profile_pic else "No Photo Yet"
        st.image(image_source, width=180, caption=caption_text)
        st.markdown("<br>", unsafe_allow_html=True) # Add space below image

    with col2:
        uploaded_image = st.file_uploader("Choose a JPG or PNG file", type=["jpg", "jpeg", "png"], key="profile_uploader")
        if uploaded_image:
            image_bytes = uploaded_image.read()
            st.session_state.profile_pic = image_bytes
            st.success("✅ Profile picture uploaded successfully!")
        st.markdown("<br>", unsafe_allow_html=True) # Space below uploader

        # Clear Profile Picture Button
        if st.session_state.profile_pic is not None:
            if st.button("🗑️ Clear Profile Picture", key="clear_profile_pic_button"):
                st.session_state.profile_pic = None
                st.info("Profile picture cleared.")
                st.rerun() # Rerun to update the displayed image immediately

    st.markdown("---") # Visual separator with more padding

    # --- Section 2: Appearance Settings (Moved global toggle to app.py) ---
    st.subheader("🌗 Appearance Settings")
    st.write("The global dark mode toggle is available in the sidebar.")
    st.markdown("<br>", unsafe_allow_html=True)
    # Removed the dark mode toggle from here as it's now in app.py for global control.
    # st.toggle("🌙 Enable Dark Mode", value=current_mode, key="dark_mode_ui_toggle")
    st.markdown("---")


    # --- Section 3: General Preferences ---
    st.subheader("📝 General Preferences")
    st.write("Set your preferred language, time zone, and notification options for a tailored experience.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Use columns to group related preferences side-by-side if they fit
    col_lang, col_notif = st.columns(2)

    with col_lang:
        st.markdown("##### Language Selection")
        language_options = ["English", "Spanish", "French", "German", "Japanese", "Mandarin", "Telugu", "Hindi", "Arabic", "Portuguese"]
        # Ensure the index is valid for the current language
        try:
            current_lang_index = language_options.index(st.session_state.language)
        except ValueError:
            current_lang_index = 0 # Default to English if current language is not in options

        selected_language = st.selectbox(
            "Preferred Language",
            language_options,
            index=current_lang_index,
            key="lang_select"
        )
        st.info(f"Your selected language is: **{selected_language}**")
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("##### Time Zone")
        time_zone_options = [
            "UTC", "America/New_York", "Europe/London", "Asia/Kolkata",
            "Asia/Tokyo", "Australia/Sydney", "America/Los_Angeles"
        ]
        try:
            current_tz_index = time_zone_options.index(st.session_state.time_zone)
        except ValueError:
            current_tz_index = 0 # Default to UTC

        selected_time_zone = st.selectbox(
            "Select Time Zone",
            time_zone_options,
            index=current_tz_index,
            key="time_zone_select"
        )
        st.info(f"Your selected time zone is: **{selected_time_zone}**")
        st.markdown("<br>", unsafe_allow_html=True)


    with col_notif:
        st.markdown("##### Notification Settings")
        enable_notifications = st.checkbox(
            "🔔 Receive Email Notifications",
            value=st.session_state.notifications,
            key="email_notif_checkbox"
        )
        if enable_notifications:
            st.write("You will receive email notifications for important updates.")
        else:
            st.write("Email notifications are currently disabled.")
        st.markdown("<br>", unsafe_allow_html=True)

        # You could add more notification options here, e.g., push notifications, SMS
        st.markdown("##### Other Notification Channels")
        st.checkbox("📱 Enable Push Notifications", value=False, key="push_notif_checkbox")
        st.checkbox("💬 Enable SMS Alerts", value=False, key="sms_notif_checkbox")
        st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("---")

    # --- Save Settings Button ---
    st.markdown("<br>", unsafe_allow_html=True) # Add space before the button instructions
    st.write("Remember to click **'Save Settings'** to apply all your changes permanently.")

    # Center the save button
    col_left, col_button, col_right = st.columns([1.5, 1, 1.5])
    with col_button:
        if st.button("💾 Save All Settings", key="save_button"):
            # Update session state with the latest values from the UI components
            st.session_state.user_name = user_name
            st.session_state.language = selected_language
            st.session_state.notifications = enable_notifications
            st.session_state.time_zone = selected_time_zone
            # Note: dark_mode is already handled by the st.toggle's rerun logic in app.py
            # In a real application, you'd save these settings to a database or config file
            st.success("🎉 All settings saved successfully! Your changes have been applied.")
            st.toast("Settings updated!", icon="✔️")
            # Optional: Add a fun effect to celebrate saving settings
            


    st.markdown("<br><br>", unsafe_allow_html=True) # More space after the button

    # --- Debug Info (Optional, but useful during development) ---
    with st.expander("🧪 View Application State (Debug Info)"):
        st.json({
            "dark_mode": st.session_state.dark_mode,
            "language": st.session_state.language,
            "notifications": st.session_state.notifications,
            "profile_pic_set": st.session_state.profile_pic is not None,
            "user_name": st.session_state.user_name,
            "time_zone": st.session_state.time_zone
        })
    st.markdown("<br>", unsafe_allow_html=True) # Space after expander

# No direct `if __name__ == "__main__":` block here, as it's meant to be imported.