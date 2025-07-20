# 🎫 Smart Ticket Classifier with Resolution Confirmation System

A complete end-to-end ML-powered ticket classification and management system that automates the process of complaint handling, assigns priorities, enables admin resolution tracking, and confirms complaint closure with user consent via email.

---

## 🚀 Project Highlights

- ✅ Automates classification of customer complaints (e.g., Billing, Delivery)
- ✅ Assigns priority based on complaint type
- ✅ Sends complaint details to admins via email
- ✅ Lets users track complaints via unique ticket number
- ✅ Includes admin panel for resolving and updating complaints
- ✅ Confirms resolution through user email confirmation (Yes/No)
- ✅ Ensures double-confirmed resolution between user & admin

---

## 🧩 Problem Statement

Companies receive hundreds of complaints daily. Sorting, prioritizing, and managing them manually is inefficient and prone to delay.

This project addresses that with a smart ML solution that automates ticket classification, resolution, and confirmation.

---

## 🛠️ Tech Stack

### 🎨 Frontend
- `HTML`, `CSS`
- `Streamlit` – for admin dashboard interface

### 🧠 ML & NLP
- `Transformers`, `BERT`
- `Scikit-learn`, `joblib`, `.pkl` – for classification pipeline

### 📬 Backend & Integration
- `Python`, `Pandas`, `CSV` – for backend logic & storage
- `SMTP` – for confirmation emails with Yes/No links

---

## 📦 Features

| Feature                     | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Complaint Submission       | User enters complaint & gets a unique ticket number                         |
| Complaint Classification   | BERT-based classifier predicts the complaint category                       |
| Priority Assignment        | Automatically sets priority (e.g., Billing = High)                          |
| Admin Panel (Streamlit)    | Admin can view, update, reopen or resolve complaints                        |
| Email Alerts               | Complaints are emailed to the admin with ticket details                     |
| User Status Tracker        | Users can check status using their email or ticket number                   |
| User Confirmation System   | Users get a Yes/No email to confirm if their issue is resolved 
