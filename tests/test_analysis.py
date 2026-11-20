
from backend.static_analysis import analyze_added_lines


def test_detect_eval():
    added_lines = [
        {
            "line_number": 10,
            "content": "result = eval(user_input)"
        }
    ]

    findings = analyze_added_lines(added_lines)

    assert len(findings) == 1
    assert findings[0]["rule_id"] == "SEC001"
    assert findings[0]["severity"] == "high"


def test_detect_print():
    added_lines = [
        {
            "line_number": 5,
            "content": 'print("hello")'
        }
    ]

    findings = analyze_added_lines(added_lines)

    assert any(item["rule_id"] == "CODE002" for item in findings)


def test_clean_code():
    added_lines = [
        {
            "line_number": 1,
            "content": "total = 10 + 20"
        }
    ]

    findings = analyze_added_lines(added_lines)

    assert findings == []
