from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from moisture_sensor import get_moisture_level
from waterPlant import water_plant
import threading
import time

app = Flask(__name__)

# Table structure with default values
table = {
    "moisture_level": "0",
    "next_check_time": datetime.now() + timedelta(minutes=10),
    "amount": "50",  # Default amount for automatic watering
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
        table["check_moisture"] = 1
    elif action == "water_plant":
        table["water_plant"] = 1
        table["watering_status"] = f"Watering soon with ({table['amount']}) ml of water"
    elif action == "update_amount":
        table["amount"] = request.form.get("amount", "50")
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
        time.sleep(1)
        now = datetime.now()

        if table["check_moisture"] == 1 or now >= table["next_check_time"]:
            moisture_level = get_moisture_level()

            moisture_level = max(0, min(100, moisture_level))

            table["moisture_level"] = moisture_level
            table["check_moisture"] = 0
            table["next_check_time"] = now + timedelta(minutes=10) 

            # Automatically water if moisture is below 30%
            if float(moisture_level) < 30:
                table["amount"] = "50"
                table["water_plant"] = 1
                table["watering_status"] = f"Watering with ({table['amount']}) ml due to low moisture"

        if table["water_plant"] == 1:
            print(f"Watering plant with {table['amount']} ml")
            water_plant(int(table["amount"]))
            table["watering_status"] = f"Watered with ({table['amount']}) ml at {now.strftime('%H:%M:%S')}"
            table["water_plant"] = 0

            moisture_level = get_moisture_level()

            # Clamp moisture level to be between 0 and 100
            moisture_level = max(0, min(100, moisture_level))

            table["moisture_level"] = moisture_level
            print(f"Updated moisture level after watering: {moisture_level}")

threading.Thread(target=monitor_table, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1024)
