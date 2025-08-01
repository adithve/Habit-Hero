#  Habit Tracker

A full-stack habit tracker web application built using **ReactJS** (frontend) and **Django REST Framework** (backend).  
It helps users build routines, track progress, and visualize habits with helpful analytics.

---

##  Features

-  **User Authentication** (JWT Token-based)
-  **Add Habits** with name, frequency, category, and start date
-  **Toggle Habit Completion** – Mark habits as completed for the day
-  **Analytics** – Current streak, longest streak, success rate, and best days
-  **Categorize Habits** – e.g., Health, Work, Learning
-  **Check-ins & Notes** – Daily habit notes
-  **Edit / Delete Habits**
-  **Per-user Data Isolation** – Each user accesses only their data

---

## 🛠️ Setup Instructions

### 🔧 Prerequisites

- Python 3.8+
- Node.js 14+
- MySQL/PostgreSQL/SQLite
- `pip`, `npm`, `virtualenv`

---

###  Backend Setup (Django)

```bash
# Clone the repository
cd habitbaackend

# Create virtual environment
python -m venv env
source env/bin/activate  # or use env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations and create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run the development server
python manage.py runserver

###  Frontend (React.js)
# Navigate to frontend directory
cd habit-tracker

# Install dependencies
npm install

# Start the development server
npm start
