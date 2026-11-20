
# Technical Approach — PR Review Intelligence Assistant

## 1. Overview

The PR Review Intelligence Assistant is a Python-based proof of concept designed to support engineering mentors during pull request review preparation.

It combines GitHub data ingestion, deterministic static analysis, LLM-based analysis, and a web dashboard.

The system provides structured feedback without executing submitted code or making automated merge decisions.

## 2. System Architecture

### Components

- Streamlit: user interface.
- FastAPI: API and orchestration entry point.
- GitHub REST API: retrieval of pull request metadata and file patches.
- Diff parser: extraction of added and deleted lines.
- Static analysis: deterministic pattern-based checks.
- LangGraph: orchestration of the AI review workflow.
- Groq: language model inference.
- Pydantic: structured output validation.

### Workflow

1. User submits a GitHub PR URL through Streamlit.
2. Streamlit sends the request to FastAPI.
3. GitHub client retrieves PR metadata and patches.
4. Diff parser extracts changed lines.
5. Static analyzer checks selected added Python lines.
6. Review context is assembled.
7. LangGraph executes the AI review node.
8. Groq generates structured JSON.
9. Pydantic validates the response.
10. FastAPI returns review results.
11. Streamlit renders the results.
12. User exports the report as Markdown.

## 3. Technology Selection

| Technology | Purpose | Reason |
|---|---|---|
| Python | Core development | Ecosystem for AI and backend development |
| FastAPI | Backend API | Validation, API documentation and asynchronous-ready framework |
| GitHub REST API | PR data ingestion | Retrieves public PR metadata and file changes |
| LangGraph | AI workflow orchestration | Structured graph-based workflow |
| Groq | LLM inference | Fast inference with accessible models |
| Pydantic | Schema validation | Validates structured review responses |
| Streamlit | Frontend | Rapid prototyping of interactive AI interfaces |
| pytest | Testing | Automated testing of core components |

## 4. Data Pipeline

### Input

A public GitHub pull request URL.

### Retrieval

The GitHub client extracts the repository owner, repository name and pull request number.

The client retrieves pull request metadata and changed file patches.

### Parsing

The diff parser extracts:

- Added lines.
- Deleted lines.
- New line numbers.

### Static analysis

Selected patterns are checked against added Python lines.

The current checks include:

- SEC001: eval usage.
- SEC002: exec usage.
- SEC003: subprocess with shell=True.
- SEC004: potential hardcoded credentials.
- CODE001: bare except.
- CODE002: print usage.

These checks are heuristic and may produce false positives or miss issues.

### AI analysis

The extracted changes and static findings are passed to the AI review workflow.

## 5. AI Architecture

The current LangGraph workflow contains an AI review node.

### Review node

The node:

1. Receives the PR title, description, changed code and static findings.
2. Constructs the review prompt.
3. Calls the Groq model.
4. Requests JSON-mode structured output.
5. Validates the response against the Pydantic AIAnalysis schema.
6. Returns the structured result.

### Review categories

- Summary.
- Risk level.
- Potential defects.
- Security and maintainability concerns.
- Recommendations.
- Test suggestions.
- Positive observations.
- Limitations.

The AI analysis is advisory and must be verified by a human reviewer.

## 6. Prompt Engineering

The system prompt emphasizes:

- Evidence-based analysis.
- No execution of submitted code.
- No invented file paths or line numbers.
- Treating submitted code and comments as untrusted content.
- Avoiding unnecessary findings.
- Clearly explaining potential issues.
- Educational and actionable recommendations.
- No automated approval or merging.

The prompt requests a structured JSON response aligned with the application's Pydantic schema.

## 7. API Design

### Endpoint

POST `/analyze`

### Input

```json
{
  "pr_url": "https://github.com/owner/repo/pull/123"
}
```

### Response

The API returns:

- Pull request metadata.
- Changed file summaries.
- Added lines.
- Deleted lines.
- Static findings.
- AI analysis.
- Change statistics.

The API is documented through FastAPI Swagger UI.

## 8. Frontend

The Streamlit dashboard provides:

- PR URL submission.
- Change statistics.
- AI summary.
- Risk level.
- AI findings.
- Evidence and recommendations.
- Test suggestions.
- Positive observations.
- Limitations.
- Static-analysis results.
- Changed-file summaries.
- Markdown report download.

## 9. Security Considerations

- API keys are stored in environment variables.
- API keys should not be committed to GitHub.
- Submitted code is treated as untrusted data.
- The system does not execute submitted code.
- The system does not approve, reject or merge PRs.
- AI findings are advisory.
- Input and context limits are applied.
- Public PR retrieval is the current MVP scope.

Further security improvements should include stronger input validation, evidence verification, request limits, authentication and access controls before deployment.

## 10. Limitations

- Only public GitHub PRs are currently supported.
- Some GitHub files may not contain patches.
- Static checks cover only selected patterns.
- AI findings may be incorrect or incomplete.
- AI-generated line references are not yet independently verified.
- Large PRs may require chunking and summarization.
- No arbitrary code execution or test-runner integration is implemented.
- No production deployment or user study has been completed.

## 11. Testing Strategy

The project uses pytest for testing core functionality.

The planned evaluation dataset contains 20–30 curated or synthetic PR examples.

Evaluation metrics include:

- Finding precision.
- Finding recall.
- False-positive rate.
- Evidence accuracy.
- Line-reference accuracy.
- Test-suggestion quality.
- Human-rated usefulness.
- Response latency.

These metrics will be measured during evaluation and are not currently claimed as achieved.

## 12. Future Improvements

- Multi-node LangGraph workflows.
- Evidence verification and filtering.
- Repository context retrieval.
- Chunked analysis of large PRs.
- RAG over coding standards.
- GitHub OAuth and private repository support.
- CI/CD integration.
- Automated test suggestion validation.
- Reviewer feedback and evaluation.
- Docker deployment.
- LangSmith tracing and observability.

## 13. Conclusion

The prototype demonstrates an AI-assisted pull request review-preparation workflow.

It integrates backend engineering, GitHub data retrieval, deterministic static analysis, structured LLM output, workflow orchestration, and a user-facing dashboard.

The architecture provides a foundation for further evaluation and improvement.
```

Save it.

---

<text color="success" weight="medium">After saving, tell me "saved". We'll then prepare your README, make sure the project is GitHub-ready, and complete the remaining assessment deliverables before the deadline.</text>