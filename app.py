from flask import Flask, render_template, jsonify
import pandas as pd
import glob
import os

app = Flask(__name__)

DATA_FOLDER = "data"   # folder where your CERT CSV files are stored

def load_cert_data():
    """Read and combine all CSV files from the data folder safely."""
    csv_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
    dfs = []

    for f in csv_files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file:
                df = pd.read_csv(file)
                df["source_file"] = os.path.basename(f)
                dfs.append(df)
        except Exception as e:
            print(f"⚠️ Skipping {f}: {e}")

    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        return combined
    else:
        print("❌ No valid CSV files found.")
        return pd.DataFrame()

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/api/live")
def api_live():
    """Return real-time stats from CERT data."""
    df = load_cert_data()

    if df.empty:
        return jsonify({"active_threats": 0, "high_risk_users": 0, "avg_score": 0})

    active_threats = len(df)

    if "user" in df.columns and "event_type" in df.columns:
        user_activity = df.groupby("user")["event_type"].nunique()
        high_risk_users = (user_activity > 2).sum()
        avg_score = round(user_activity.mean(), 2)
    else:
        high_risk_users = 0
        avg_score = 0

    return jsonify({
        "active_threats": int(active_threats),
        "high_risk_users": int(high_risk_users),
        "avg_score": float(avg_score)
    })

if __name__ == "__main__":
    app.run(debug=True)
