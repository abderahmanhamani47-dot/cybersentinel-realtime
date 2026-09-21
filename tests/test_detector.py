from src.detector import analyze_request

class FakeRequest:
    def __init__(self, path, ip="127.0.0.1"):
        self.full_path = path
        self.remote_addr = ip

def test_sql_injection_detection():
    alert = analyze_request(FakeRequest("/search?q=' OR 1=1"))
    assert alert["type"] == "SQL_INJECTION_ATTEMPT"
    assert alert["score"] == 95

def test_xss_detection():
    alert = analyze_request(FakeRequest("/search?q=<script>alert(1)</script>"))
    assert alert["type"] == "XSS_ATTEMPT"
    assert alert["score"] == 75

def test_normal_request_is_not_alerted():
    assert analyze_request(FakeRequest("/search?q=python")) is None
