
import re


RULES = [
    {
        "id": "SEC001",
        "pattern": r"\beval\s*\(",
        "severity": "high",
        "message": "Use of eval() can execute arbitrary code.",
        "recommendation": "Avoid eval(). Use safe parsing or explicit logic."
    },
    {
        "id": "SEC002",
        "pattern": r"\bexec\s*\(",
        "severity": "high",
        "message": "Use of exec() can execute arbitrary code.",
        "recommendation": "Avoid exec() and use safer alternatives."
    },
    {
        "id": "SEC003",
        "pattern": r"\bsubprocess\.(?:run|Popen|call)\s*\([^)]*shell\s*=\s*True",
        "severity": "high",
        "message": "Shell execution with shell=True may introduce command injection.",
        "recommendation": "Prefer argument lists and shell=False."
    },
    {
        "id": "SEC004",
        "pattern": r"\b(?:password|api_key|secret)\s*=\s*['\"][^'\"]+['\"]",
        "severity": "high",
        "message": "Possible hardcoded secret or credential.",
        "recommendation": "Load secrets from environment variables."
    },
    {
        "id": "CODE001",
        "pattern": r"\bexcept\s*:",
        "severity": "medium",
        "message": "Bare except catches all exceptions.",
        "recommendation": "Catch specific exception types."
    },
    {
        "id": "CODE002",
        "pattern": r"\bprint\s*\(",
        "severity": "low",
        "message": "Print statement detected in changed code.",
        "recommendation": "Consider structured logging for application code."
    },
]


def analyze_added_lines(added_lines):
    findings = []

    for item in added_lines:
        code = item["content"]
        line_number = item["line_number"]

        for rule in RULES:
            if re.search(rule["pattern"], code):
                findings.append({
                    "rule_id": rule["id"],
                    "severity": rule["severity"],
                    "line_number": line_number,
                    "code": code.strip(),
                    "message": rule["message"],
                    "recommendation": rule["recommendation"],
                    "source": "static_analysis"
                })

    return findings
