
from flask import Blueprint, jsonify, request

from service.models import get_connection, row_to_dict

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts_bp.post("")
def create_account():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO accounts (name, email) VALUES (?, ?)",
                (name, email),
            )
            row = connection.execute(
                "SELECT * FROM accounts WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()

        return jsonify(row_to_dict(row)), 201
    except Exception:
        return jsonify({"error": "Unable to create account"}), 409


@accounts_bp.get("")
def list_accounts():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM accounts ORDER BY id"
        ).fetchall()

    return jsonify([row_to_dict(row) for row in rows]), 200


@accounts_bp.get("/<int:account_id>")
def read_account(account_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM accounts WHERE id = ?",
            (account_id,),
        ).fetchone()

    if row is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(row_to_dict(row)), 200


@accounts_bp.put("/<int:account_id>")
def update_account(account_id):
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                "UPDATE accounts SET name = ?, email = ? WHERE id = ?",
                (name, email, account_id),
            )

            if cursor.rowcount == 0:
                return jsonify({"error": "Account not found"}), 404

            row = connection.execute(
                "SELECT * FROM accounts WHERE id = ?",
                (account_id,),
            ).fetchone()

        return jsonify(row_to_dict(row)), 200
    except Exception:
        return jsonify({"error": "Unable to update account"}), 409


@accounts_bp.delete("/<int:account_id>")
def delete_account(account_id):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM accounts WHERE id = ?",
            (account_id,),
        )

    if cursor.rowcount == 0:
        return jsonify({"error": "Account not found"}), 404

    return "", 204
