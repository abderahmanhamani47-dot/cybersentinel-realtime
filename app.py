from flask import Flask, request, render_template, jsonify
from src.detector import analyze_request
from src.storage import init_db, save_alert, get_alerts, get_stats

app = Flask(__name__)
init_db()

@app.after_request
def monitor_request(response):
    # Monitor requests made to this local lab application.
    alert = analyze_request(request)
    if alert:
        save_alert(alert)
    return response

@app.route("/")
def dashboard():
    alerts = get_alerts()
    stats = get_stats()
    return render_template("dashboard.html", alerts=alerts, stats=stats)

@app.route("/login", methods=["GET", "POST"])
def login():
    return "Local lab login endpoint"

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return f"Search result for: {query}"

@app.route("/api/alerts")
def api_alerts():
    return jsonify({"alerts": get_alerts(), "stats": get_stats()})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
