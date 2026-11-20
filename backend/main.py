
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.graph import run_ai_review
from backend.github_client import get_pull_request
from backend.diff_parser import parse_diff
from backend.static_analysis import analyze_added_lines


app = FastAPI(
    title="PR Review Intelligence Assistant",
    description="Evidence-based PR review preparation assistant",
    version="0.1.0"
)


class AnalyzeRequest(BaseModel):
    pr_url: str = Field(min_length=1)


@app.get("/")
def root():
    return {
        "message": "PR Review Intelligence Assistant API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
def analyze_pr(request: AnalyzeRequest):
    try:
        pr_data = get_pull_request(request.pr_url)

        all_added_lines = []
        all_deleted_lines = []
        all_static_findings = []
        file_summaries = []
        changed_code_parts = []

        for file in pr_data["changed_files"]:
            filename = file["filename"]
            patch = file.get("patch", "")

            file_summaries.append({
                "filename": filename,
                "status": file["status"],
                "additions": file["additions"],
                "deletions": file["deletions"]
            })

            if not patch or patch == "Patch unavailable":
                continue

            parsed = parse_diff(patch)

            added_lines = parsed["added_lines"]
            deleted_lines = parsed["deleted_lines"]

            all_added_lines.extend(added_lines)
            all_deleted_lines.extend(deleted_lines)

            # Prepare added lines for AI analysis
            for line in added_lines:
                changed_code_parts.append(
                    f"File: {filename}\n"
                    f"Line {line['line_number']}: {line['content']}"
                )

            # Run deterministic static analysis on Python files
            if filename.endswith(".py"):
                findings = analyze_added_lines(added_lines)

                for finding in findings:
                    finding["file_path"] = filename

                all_static_findings.extend(findings)

        # Build code context for AI
        changed_code = "\n".join(changed_code_parts)

        # Run AI review
        ai_analysis = run_ai_review(
            title=pr_data["title"],
            description=pr_data.get("description", ""),
            changed_code=changed_code,
            static_findings=all_static_findings,
        )

        return {
            "pull_request": {
                "title": pr_data["title"],
                "description": pr_data["description"],
                "author": pr_data["author"],
                "state": pr_data["state"],
                "url": pr_data["url"]
            },
            "files": file_summaries,
            "added_lines": all_added_lines,
            "deleted_lines": all_deleted_lines,
            "static_findings": all_static_findings,
            "ai_analysis": ai_analysis,
            "stats": {
                "changed_files": len(file_summaries),
                "added_lines": len(all_added_lines),
                "deleted_lines": len(all_deleted_lines),
                "static_findings": len(all_static_findings)
            }
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        status_code = 502

        if hasattr(exc, "response") and exc.response is not None:
            status_code = exc.response.status_code

        raise HTTPException(
            status_code=status_code,
            detail=f"GitHub API or processing error: {str(exc)}"
        )
