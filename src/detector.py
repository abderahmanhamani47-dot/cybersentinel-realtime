import re
from datetime import datetime
from urllib.parse import unquote

SQLI_PATTERNS = [
    r"\bunion\s+select\b",
    r"'?\s*or\s+1\s*=\s*1",
    r"\bsleep\s*\(",
    r"\binformation_schema\b",
    r"\bdrop\s+table\b",
]

XSS_PATTERNS = [
    r"<\s*script\b",
    r"javascript\s*:",
    r"\bonerror\s*=",
    r"\bonload\s*=",
]


def _match(patterns, value):
    for pattern in patterns:
        if re.search(pattern, value, re.IGNORECASE):
            return pattern
    return None


def analyze_request(req):
    # Read the real HTTP request received by the local Flask lab.
    raw = req.full_path

    # Decode URL-encoded characters such as %27, %20, %3C, etc.
    decoded = unquote(raw)

    source_ip = req.remote_addr or "127.0.0.1"

    sql = _match(SQLI_PATTERNS, decoded)

    if sql:
        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "ip": source_ip,
            "type": "SQL_INJECTION_ATTEMPT",
            "severity": "CRITICAL",
            "score": 95,
            "evidence": decoded[:300],
        }

    xss = _match(XSS_PATTERNS, decoded)

    if xss:
        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "ip": source_ip,
            "type": "XSS_ATTEMPT",
            "severity": "HIGH",
            "score": 75,
            "evidence": decoded[:300],
        }

    return None