# CyberSentinel — Real-Time Security Monitoring Lab

A personal Python cybersecurity project designed to practice Python while building a small **real-time security monitoring and threat-detection lab**.

## What changed from the first version?

The first version used simulated log entries. This version monitors **real HTTP requests received by the local Flask lab application** and stores detected alerts in SQLite.

Architecture:

Browser / local test request
→ Flask lab application
→ request monitoring
→ detection rules
→ SQLite
→ dashboard

## Current detections

- SQL Injection patterns
- XSS patterns
- Severity and risk score
- Timestamp, source IP and evidence
- SQLite alert history

This is an educational local lab. It is not a production SIEM or IDS.

## Run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

## Test the detection locally

Normal request:

http://127.0.0.1:5000/search?q=python

SQL injection test:

http://127.0.0.1:5000/search?q=%27%20OR%201%3D1

XSS test:

http://127.0.0.1:5000/search?q=%3Cscript%3Ealert(1)%3C/script%3E

These requests target only your own local lab application.

## Tests

```powershell
python -m pytest
```

Expected result:

```text
3 passed
```

## Technologies

Python, Flask, SQLite, Pytest, HTML/CSS

## Future improvements

- authentication and RBAC
- brute-force detection over time windows
- charts and alert filtering
- Docker
- Wazuh integration
- more robust parsing and detection rules
