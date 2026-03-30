from database import get_connection

# ENUMS
SEVERITY = {"low", "medium", "high", "critical"}
STATUS = {"open", "in_progress", "closed"}
CATEGORY = {"hardware", "software", "network", "other"}


def validate_ticket(data):
    if len(data["title"]) > 200:
        raise ValueError("Title too long")

    if "description" in data and len(data["description"]) > 2000:
        raise ValueError("Description too long")

    if data["severity"] not in SEVERITY:
        raise ValueError("Invalid severity")

    if data["status"] not in STATUS:
        raise ValueError("Invalid status")

    if data["category"] not in CATEGORY:
        raise ValueError("Invalid category")


def create_ticket(data):
    validate_ticket(data)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (
            title, description, employee, client, date,
            severity, status, category,
            room_id, latitude, longitude, email_team_leader, address
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data.get("description", ""),
        data.get("employee"),
        data.get("client"),
        data["date"],
        data["severity"],
        data["status"],
        data["category"],
        data.get("roomID"),
        data.get("latitude"),
        data.get("longitude"),
        data.get("emailTeamLeader")
        data.get("address")
    ))

    conn.commit()
    conn.close()


def get_all_tickets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return tickets