from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path


app = Flask(__name__)

# Base folder of the project
BASE_DIR = Path(__file__).resolve().parent

# SQLite database file path
DATABASE = BASE_DIR / "emergency_alerts.db"


def init_db():
    """
    Create the alerts table if it does not already exist.
    This function runs automatically when the app starts.
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def get_all_alerts():
    """
    Read all alerts from the database.
    Latest alerts are shown first.
    """
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, user_name, message, created_at
        FROM alerts
        ORDER BY id DESC
        """
    )
    alerts = cursor.fetchall()

    connection.close()
    return alerts


def add_alert(user_name, message):
    """
    Insert a new emergency alert into the database.
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO alerts (user_name, message)
        VALUES (?, ?)
        """,
        (user_name, message),
    )

    connection.commit()
    connection.close()


@app.route("/")
def home():
    """
    Main page:
    - Show the alert form
    - Show all previous alerts
    """
    alerts = get_all_alerts()
    return render_template("index.html", alerts=alerts)


@app.route("/send-alert", methods=["POST"])
def send_alert():
    """
    Handle form submission and save the alert.
    """
    user_name = request.form.get("user_name", "").strip()
    message = request.form.get("message", "").strip()

    # Basic validation to avoid empty form submission
    if user_name and message:
        add_alert(user_name, message)

    return redirect(url_for("home"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)
