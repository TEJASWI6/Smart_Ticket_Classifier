import csv
import os
import re
import smtplib
import uuid
from datetime import datetime
from email.mime.text import MIMEText

import joblib
import streamlit as st
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def main():
    st.markdown("<h1 class='main-title'>📩 Submit Your Issue</h1>", unsafe_allow_html=True)

    # ✅ Load Model + Tokenizer + Label Encoder
    model_path = "models/bert_ticket_model"
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    label_encoder = joblib.load("models/label_encoder.pkl")
    
    # ✅ Email Credentials
    EMAIL = "eddalatejaswi@gmail.com"
    APP_PASSWORD = "vtdl tqhb vxyp rozr"


    # ✅ Predict Category
    def predict_category(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            pred_id = torch.argmax(probs, dim=1).item()
        category = [k for k, v in label_encoder.items() if v == pred_id][0]
        confidence = round(probs[0][pred_id].item(), 3)
        return category, confidence

    # ✅ Email Body
    def get_email_body(category, email, ticket_num):
        messages = {
            "Billing Issue": f"Hi {email},\n\nWe've received your billing-related complaint. Our finance team is reviewing it and will get back to you shortly.\n\nCategory: Billing Issue\nTicket Number: {ticket_num}\n\nRegards,\nSmart Support Team",
            "Technical Support": f"Hi {email},\n\nThank you for reporting a technical issue. Our technical support team is on it and will assist you soon.\n\nCategory: Technical Support\nTicket Number: {ticket_num}\n\nBest,\nSmart Support Team",
            "Account Problem": f"Hi {email},\n\nWe noticed your complaint relates to account access or security. Our account services team is now looking into it.\n\nCategory: Account Problem\nTicket Number: {ticket_num}\n\nThanks,\nSmart Support Team",
            "Service Delay": f"Hi {email},\n\nWe’ve logged your complaint about a delay in service. Our operations team is working to resolve this as fast as possible.\n\nCategory: Service Delay\nTicket Number: {ticket_num}\n\nRegards,\nSmart Support Team",
        }
        return messages.get(category, f"Hi {email},\n\nThank you for submitting your complaint. Our team will review your issue and respond accordingly.\n\nCategory: {category}\nTicket Number: {ticket_num}\n\nThank you,\nSmart Support Team")

    # ✅ Send Email
    def send_email(to_email, subject, body):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL, APP_PASSWORD)
                smtp.send_message(msg)
            return True
        except Exception as e:
            st.error(f"❌ Email failed: {e}")
            return False

    # ✅ Input Fields
    email = st.text_input("📧 Your Email")
    message = st.text_area("💬 Describe your issue:")

    # ✅ Submit Button
    if st.button("Submit Complaint", key="submit_complaint_btn"):
        if not email.strip() or not message.strip():
            st.warning("⚠️ Please enter both email and complaint.")
        else:
            category, confidence = predict_category(message)

            # ✅ Generate Unique Ticket Number
            def generate_ticket_num():
                datecode = datetime.now().strftime('%Y%m%d')
                randpart = uuid.uuid4().hex[:6].upper()
                return f"TCKT-{datecode}-{randpart}"

            ticket_num = generate_ticket_num()
            email_body = get_email_body(category, email, ticket_num)
            email_sent = send_email(email, "🛠 Issue Received", email_body)

            # ✅ Write to Logs
            os.makedirs("logs", exist_ok=True)
            log_path = "logs/predictions.csv"
            file_exists = os.path.isfile(log_path)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            role = st.session_state.get("user_role", "user")

            try:
                with open(log_path, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=[
                        "ticket_num", "email", "text", "category", "confidence", "timestamp",
                        "user_role", "status", "notes", "priority", "user_confirmation"
                    ])
                    if not file_exists or os.stat(log_path).st_size == 0:
                        writer.writeheader()
                    writer.writerow({
                        "ticket_num": ticket_num,
                        "email": email,
                        "text": message.strip().replace("\n", " "),
                        "category": category,
                        "confidence": confidence,
                        "timestamp": timestamp,
                        "user_role": role,
                        "status": "Unresolved",
                        "notes": "",
                        "priority": "Medium",
                        "user_confirmation": "Pending"
                    })
                st.success(f"✅ Issue classified as **{category}**. Your Ticket Number is `{ticket_num}`.")
                if email_sent:
                    st.info("📩 Confirmation email sent with your ticket number.")
            except Exception as e:
                st.error(f"❌ Could not save log: {e}")

    # --- Ticket Status Checker UI (always shown, allows user to check ANY time) ---
    st.markdown("---")
    st.markdown("### 🔎 Check Ticket Status")
    ticket_input = st.text_input("Enter your Ticket Number to check status:")

    if st.button("Check Status", key="unique_ticket_status_check"):
        ticket_number_pattern = r"^TCKT-\d{8}-[A-F0-9]{6}$"
        if not ticket_input.strip():
            st.warning("Please enter a ticket number.")
        elif not re.match(ticket_number_pattern, ticket_input.strip()):
            st.error("❌ Please enter a valid ticket number in the format TCKT-YYYYMMDD-XXXXXX.")
        else:
            found = False
            log_path = "logs/predictions.csv"
            try:
                if not os.path.isfile(log_path):
                    st.error("❌ Ticket log file not found.")
                else:
                    with open(log_path, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            ticket_in_csv = row.get("ticket_num", "").strip()
                            if ticket_in_csv == ticket_input.strip():
                                found = True
                                status = row.get('status', 'Unknown')
                                category = row.get('category', '')
                                timestamp = row.get('timestamp', '')
                                notes = row.get('notes', '') or 'No notes yet.'
                                st.info(
                                    f"**Status:** {status}\n\n"
                                    f"**Category:** {category}\n\n"
                                    f"**Submitted:** {timestamp}\n\n"
                                    f"**Notes:** {notes}"
                                )
                                break
                    if not found:
                        st.error("❌ Ticket number not found. Please check and try again.")
            except Exception as e:
                st.error(f"❌ Could not read log: {e}")

if __name__ == "__main__":
    main()
