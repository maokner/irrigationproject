from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from moisture_sensor import get_moisture_level
import threading
import time

app = Flask(__name__)

# Table structure
table = {
    "moisture_level": "0",
    "next_check_time": datetime.now() + timedelta(minutes=2),
    "amount": "0",
    "check_moisture": 0,
    "water_plant": 0,
    "watering_status": "No watering yet"
}

@app.route("/", methods=["GET"])
def home_view():
    return render_template("index.html",
                           moisture_level=table["moisture_level"],
                           next_check_time=table["next_check_time"].strftime("%H:%M:%S"),
                           amount=table["amount"],
                           watering_status=table["watering_status"])

@app.route("/table", methods=["GET"])
def table_view():
    return render_template("table.html",
                           moisture_level=table["moisture_level"],
                           next_check_time=table["next_check_time"].strftime("%H:%M:%S"),
                           amount=table["amount"],
                           check_moisture=table["check_moisture"],
                           water_plant=table["water_plant"])

@app.route("/update-table", methods=["POST"])
def update_table():
    action = request.form.get("action")
    if action == "check_moisture":
        table["check_moisture"] = 1  # Set the flag, to be handled by monitor_table
    elif action == "water_plant":
        table["water_plant"] = 1
        # Only update watering status when setting water_plant
        table["watering_status"] = f"Watering soon with ({table['amount']}) ml of water"
    elif action == "update_amount":
        # Update the water amount without triggering watering
        table["amount"] = request.form.get("amount", "0")
    return redirect(url_for("home_view"))

@app.route("/table-data", methods=["GET"])
def get_table_data():
    return {
        "moisture_level": table["moisture_level"],
        "next_check_time": table["next_check_time"].strftime("%H:%M:%S"),
        "amount": table["amount"],
        "check_moisture": table["check_moisture"],
        "water_plant": table["water_plant"],
        "watering_status": table["watering_status"]
    }

def monitor_table():
    while True:
        # Check every minute
        time.sleep(60)
        now = datetime.now()

        # Check moisture level if flagged or time conditions are met
        if table["check_moisture"] == 1 or now.minute >= table["next_check_time"].minute:
            table["moisture_level"] = get_moisture_level()
            table["check_moisture"] = 0  # Reset after checking
            table["next_check_time"] = now + timedelta(minutes=2)

        # Handle water plant if triggered
        if table["water_plant"] == 1:
            # Print the watering message and set the status to show it has watered
            print(f"Watering plant with {table['amount']} ml")
            table["watering_status"] = f"Watered with ({table['amount']}) ml at {now.strftime('%H:%M:%S')}"
            table["water_plant"] = 0

# Start monitoring in a separate thread
threading.Thread(target=monitor_table, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1024)
