from flask import Flask, render_template, jsonify
import pandas as pd
import os
import time

app = Flask(__name__)

DATA_PATH = "data/user.csv"

def read_data():
    try:
        if os.path.exists(DATA_PATH):
            # Open the file in read-only mode to avoid locking conflicts
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                df = pd.read_csv(file)
            return df
        else:
            return pd.DataFrame(columns=["UserID", "LoginCount", "AccessLevel", "ThreatScore"])
    except PermissionError:
        print("⚠️ Permission error: make sure user.csv is not open in Excel or another app.")
        return pd.DataFrame(columns=["UserID", "LoginCount", "AccessLevel", "ThreatScore"])
    except Exception as e:
        print(f"⚠️ Error reading {DATA_PATH}: {e}")
        return pd.DataFrame(columns=["UserID", "LoginCount", "AccessLevel", "ThreatScore"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    df = read_data()
    if not df.empty:
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify([])

if __name__ == '__main__':
    # Optional: wait for file to become readable
    for _ in range(3):
        try:
            read_data()
            break
        except PermissionError:
            print("Retrying file access...")
            time.sleep(1)
    app.run(debug=True)
