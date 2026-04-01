from flask import Flask, request, jsonify, send_file
from database import init_db
import models
import time
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
init_db()
CORS(app)

#allow index.html access, show a minmalistic html without css
@app.route("/")
def index():
    return send_file("index.html")

#creates a ticket
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

# get all tickets stored in the db
@app.route("/tickets", methods=["GET"])
def get_tickets():
    return jsonify(models.get_all_tickets())

#get ticket index by id
@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    tickets = models.get_all_tickets()
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            return jsonify(t)

    return jsonify({"error": "Not found"}), 404

#modify a ticket, like changing open tickets to closed
@app.route("/tickets/<int:ticket_id>", methods=["PATCH"])
def patch_ticket(ticket_id):
    data = request.json

    # expecting syntax: {"column": string, "value": new value}
    column = data.get("column")
    value = data.get("value")

    if not column:
        return jsonify({"error": "Missing 'column' in request body"}), 400

    try:
        success = models.update_ticket_field(ticket_id, column, value)

        if success:
            return jsonify({"message": f"Ticket {ticket_id} updated successfully"}), 200
        else:
            return jsonify({"error": "Ticket not found"}), 404

    except ValueError as ve:
        # catch invalid names
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.errorhandler(HTTPException)
def handle_exception(e):
   # get response
    response = e.get_response()

    # send a json to the client
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,  # the reason why
    }).data

    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    # allow local network access
    app.run(host="0.0.0.0", port=5000, debug=True)
