# Cafe Website

A Flask web application for discovering cafes with useful amenities and submitting new cafe suggestions for review. Includes an admin dashboard to approve or reject submissions before they appear on the website.

## Features

- Browse cafes and view their details, including location, seating, Wi-Fi, power outlets, restrooms, call-friendly spaces, and coffee prices.
- Submit new cafe suggestions through a form.
- Store cafe information and suggestions in a SQLite database.
- Admin login with protected dashboard access.
- Approve or reject pending cafe suggestions.
- Form validation and CSRF protection.
- Flash messages to provide feedback after actions.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- Flask-Login
- Flask-WTF
- WTForms
- Bootstrap 5
- python-dotenv

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   cd YOUR_REPOSITORY_NAME
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   macOS / Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:

   ```env
   SECRET_KEY=your-secret-key
   ADMIN_USERNAME=your-admin-username
   ADMIN_PASSWORD=your-admin-password
   ```

   Replace the example values with your own credentials. Keep your `.env` file private and never commit it to GitHub.

5. Run the application:

   ```bash
   python main.py
   ```

6. Open the local URL displayed in the terminal in your browser.

## Admin Dashboard

The admin dashboard allows the site owner to review submitted cafe suggestions. Only authenticated administrators can access the dashboard and approve or reject submissions.

## Database

The application uses SQLite to store cafe information and submitted suggestions. The database tables are created automatically when the application starts.

## Project Structure

```text
project/
├── main.py
├── cafes.db
├── templates/
│   ├── index.html
│   ├── suggest.html
│   ├── login.html
│   └── admin.html
├── static/
├── .env
├── .gitignore
└── requirements.txt
```

The exact files and folders may vary depending on the final project structure.
