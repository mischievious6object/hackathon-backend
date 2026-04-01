 
import models
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_tickets():
    while True:
        try:
            clear_screen()
            print(f"--- Ticket Status Monitor (Refreshed: {time.ctime()}) ---")

            tickets = models.get_all_tickets()

            if not tickets:
                print("No tickets found in the database.")
            else:
                # Print a simple header
                print(f"{'ID':<5} | {'Date':<20} | {'Status/Info'}")
                print("-" * 40)

                for t in tickets:
                    t_id = t.get('ticket_id', 'N/A')
                    t_date = time.ctime(t.get('date', 0))
                    # You can add more fields here as needed
                    print(f"{t_id:<5} | {t_date:<20} | {t.get('description', 'No info')}")

            print("\nPress Ctrl+C to stop.")
            time.sleep(5)

        except Exception as e:
            print(f"Error reading database: {e}")
            time.sleep(10)

if __name__ == "__main__":
    display_tickets()
