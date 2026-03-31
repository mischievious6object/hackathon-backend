from database import get_connection

# enumerations
SEVERITY = {"low", "medium", "high", "critical"}
STATUS = {"open", "in_progress", "closed"}
CATEGORY = {"MIC", "MIM", "brandmelding", "ongeval/bijna-incident", "agressie/geweld", "it"}

# check if the ticket is valid, most of these are done on the clientside, but an additional check is better.
def validate_ticket(data):
    if len(data["title"]) > 200: #we dont want users making long ticket names, thats what the description is for!
        raise ValueError("Title too long")

    if "description" in data and len(data["description"]) > 2000: # 2000 is a soft spot for voice descriptions, we dont want users to rant their worklife into the database because their dog died or something
        raise ValueError("Description too long")

    if data["severity"] not in SEVERITY:
        raise ValueError("Invalid severity")

    if data["status"] not in STATUS:
        raise ValueError("Invalid status")

    if data["category"] not in CATEGORY:
        raise ValueError("Invalid category")

# makes a ticket
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        data.get("emailTeamLeader"),
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
