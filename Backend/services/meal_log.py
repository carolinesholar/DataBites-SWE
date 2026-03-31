#Core logic for cerating, reading, updating, and deleting food log entries
from unittest.loader import VALID_MODULE_NAME

from flask import Blueprint, request, jsonify
import sqlite3
import os
from datetime import datetime

# Create a Blueprint for meal logging
meal_log_bp = Blueprint('meal_log', __name__)

# Path to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.abspath(os.path.join(BASE_DIR, "../../DataBase/databites.db"))

VALID_MEAL_TYPES = {"breakfast", "lunch", "dinner", "snack", "other"}


def get_db_connection():
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@meal_log_bp.route("/log_food", methods=["POST"])
def log_food():
    data = request.get_json()

    if not data:
        return jsonify({"error": "invalid or missing JSON body"}), 400

    user_id = data.get("user_id")
    food_name = data.get("food_name", "").strip()
    logged_at = data.get("logged_at")
    meal_type = data.get("meal_type")
    mood = data.get("mood")
    notes = data.get("notes")

    if isinstance(meal_type, str):
        meal_type = meal_type.strip().lower()

    if isinstance(mood, str):
        mood = mood.strip()

    if isinstance(notes, str):
        notes = notes.strip()

    if not user_id or not food_name:
        return jsonify({"error": "missing required fields: user_id or food_name"}), 400

    if not logged_at:
        logged_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if meal_type and meal_type not in VALID_MEAL_TYPES:
        return jsonify({"error": "invalid meal_type"}), 400

    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO food_logs (user_id, food_name, logged_at, meal_type, mood, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, food_name, logged_at, meal_type, mood, notes))

        log_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO food_log_audit (log_id, user_id, action, food_name, logged_at, meal_type, mood, notes)
            VALUES (?, ?, 'create', ?, ?, ?, ?, ?)
        """, (log_id, user_id, food_name, logged_at, meal_type, mood, notes))

        conn.commit()

        return jsonify({
            "message": "food logged successfully",
            "log": {
                "log_id": log_id,
                "user_id": user_id,
                "food_name": food_name,
                "logged_at": logged_at,
                "meal_type": meal_type,
                "mood": mood,
                "notes": notes
            }
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "invalid user_id or invalid field values"}), 400

    except Exception:
        return jsonify({"error": "internal server error"}), 500

    finally:
        if conn:
            conn.close()