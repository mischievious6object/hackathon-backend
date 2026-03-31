from flask import Flask, request, jsonify, send_file
from database import init_db
import models
import time
from flask_cors import CORS



app = Flask(__name__)
init_db()
CORS(app)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/tickets", methods=["POST"])
def create_ticket():
    try:
        data = request.json

        # auto timestamp if not provided
        if "date" not in data:
            data["date"] = int(time.time())

        models.create_ticket(data)

        return jsonify({"message": "Ticket created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/tickets", methods=["GET"])
def get_tickets():
    return jsonify(models.get_all_tickets())


@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    tickets = models.get_all_tickets()
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            return jsonify(t)

    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # allow local network access
    app.run(host="0.0.0.0", port=5000, debug=True)
