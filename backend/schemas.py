
from typing import Literal
from pydantic import BaseModel, Field


Severity = Literal["critical", "high", "medium", "low", "info"]


class ReviewFinding(BaseModel):
    title: str
    severity: Severity
    file_path: str
    line_number: int | None = None
    code_evidence: str = ""
    explanation: str
    recommendation: str
    confidence: float = Field(ge=0, le=1, default=0.5)
    source: Literal["static_analysis", "ai_analysis"] = "ai_analysis"


class TestSuggestion(BaseModel):
    test_name: str
    purpose: str
    expected_result: str


class PRReview(BaseModel):
    summary: str
    risk_level: Literal["low", "medium", "high", "critical"]
    findings: list[ReviewFinding] = []
    test_suggestions: list[TestSuggestion] = []
    positive_observations: list[str] = []
    limitations: list[str] = []


class AIAnalysis(BaseModel):
    summary: str
    risk_level: Literal["low", "medium", "high", "critical"]
    findings: list[ReviewFinding] = []
    test_suggestions: list[TestSuggestion] = []
    positive_observations: list[str] = []
    limitations: list[str] = []
