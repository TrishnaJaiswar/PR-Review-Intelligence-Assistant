
import re
import requests


GITHUB_API = "https://api.github.com"


def parse_pr_url(pr_url: str):
    pattern = r"^https://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.match(pattern, pr_url.strip())

    if not match:
        raise ValueError("Invalid GitHub Pull Request URL")

    owner, repo, pr_number = match.groups()

    return owner, repo, int(pr_number)


def get_pull_request(pr_url: str):
    owner, repo, pr_number = parse_pr_url(pr_url)

    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"

    response = requests.get(
        url,
        headers={"Accept": "application/vnd.github+json"},
        timeout=20
    )

    response.raise_for_status()
    pr = response.json()

    files_url = f"{url}/files"
    files_response = requests.get(
        files_url,
        headers={"Accept": "application/vnd.github+json"},
        timeout=20
    )

    files_response.raise_for_status()

    return {
        "title": pr.get("title"),
        "description": pr.get("body") or "No description provided",
        "author": pr.get("user", {}).get("login"),
        "state": pr.get("state"),
        "url": pr.get("html_url"),
        "changed_files": [
            {
                "filename": file.get("filename"),
                "status": file.get("status"),
                "additions": file.get("additions"),
                "deletions": file.get("deletions"),
                "patch": file.get("patch", "Patch unavailable")
            }
            for file in files_response.json()
        ]
    }
