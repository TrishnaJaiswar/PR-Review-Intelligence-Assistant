
from backend.github_client import parse_pr_url


def test_parse_pr_url():
    owner, repo, number = parse_pr_url(
        "https://github.com/pallets/flask/pull/1"
    )

    assert owner == "pallets"
    assert repo == "flask"
    assert number == 1
