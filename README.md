# 🏥 Healthcare Appointment Manager

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Google Calendar API](https://img.shields.io/badge/Google%20Calendar-4285F4?style=for-the-badge&logo=google-calendar&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)

A robust, Flask-based web application designed to streamline the healthcare experience for both patients and doctors. This platform manages appointments, delivers automated medication reminders via email, and seamlessly syncs with Google Calendar.

## ✨ Key Features

* **Role-Based Dashboards:** Dedicated interfaces for Patients and Doctors.
* **Smart Scheduling:** Book, view, and manage medical appointments.
* **Automated Medication Reminders:** Background jobs powered by `APScheduler` send timely email notifications to patients to ensure medication adherence.
* **Google Calendar Integration:** Secure OAuth 2.0 (PKCE compliant) flow allows patients to automatically sync their upcoming appointments to their personal Google Calendar.
* **AI Post-Visit Summaries:** Automated summaries generated after consultations to help patients understand their care plan.

## 🛠️ Technology Stack

* **Backend:** Python, Flask
* **Database:** SQLAlchemy, SQLite
* **Authentication:** Flask-Login, Google OAuth 2.0 (`google-auth-oauthlib`)
* **Task Scheduling:** APScheduler
* **Frontend:** HTML5, Tailwind CSS, Jinja2 Templates

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* Google Cloud Console account (for Calendar API credentials)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/healthcare-appointment-manager.git
   cd healthcare-appointment-manager
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv HAMvenv
   source HAMvenv/bin/activate  # On Windows use: HAMvenv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   * Create a `.env` file in the root directory and add your secret keys (e.g., `SECRET_KEY`, Database URIs).
   * Download your Google OAuth 2.0 credentials from the Google Cloud Console and save the file as `client_secret.json` in the root directory. *(Note: Ensure this file is added to your `.gitignore`)*.

5. **Initialize the Database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the Application:**
   ```bash
   python run.py
   ```
   *The application will be available at `http://localhost:5000`.* 

> **Important Note on Google OAuth:** When testing locally, ensure you access the app via `http://localhost:5000` rather than `http://127.0.0.1:5000` to prevent `InvalidGrantError` (Missing code verifier) session mismatches.

## 🔒 Security
* OAuth secrets and session variables are strictly excluded from version control.
* Implements PKCE (Proof Key for Code Exchange) for secure OAuth flows.

## 📄 License
This project is licensed under the MIT License.
