
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="PR Review Intelligence",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 PR Review Intelligence Assistant")
st.caption("AI-powered pull request review preparation for engineering mentors.")

pr_url = st.text_input(
    "GitHub Pull Request URL",
    placeholder="https://github.com/owner/repo/pull/123"
)

if st.button("Analyze Pull Request", type="primary"):
    if not pr_url.strip():
        st.warning("Please enter a GitHub PR URL.")
    else:
        with st.spinner("Fetching PR and analyzing changes..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"pr_url": pr_url.strip()},
                    timeout=180
                )

                response.raise_for_status()
                data = response.json()

                st.session_state["review_data"] = data

            except requests.exceptions.RequestException as exc:
                st.error(f"Analysis failed: {exc}")

data = st.session_state.get("review_data")

if data:
    pr = data["pull_request"]
    ai = data.get("ai_analysis", {})

    st.divider()

    st.subheader(pr["title"])

    st.markdown(f"[View original pull request]({pr['url']})")

    col1, col2, col3, col4 = st.columns(4)

    stats = data["stats"]

    col1.metric("Changed files", stats["changed_files"])
    col2.metric("Added lines", stats["added_lines"])
    col3.metric("Deleted lines", stats["deleted_lines"])
    col4.metric("Static findings", stats["static_findings"])

    st.divider()

    st.subheader("AI Review")

    risk = ai.get("risk_level", "unknown")
    st.metric("Overall risk level", risk.upper())

    st.markdown("### Summary")
    st.write(ai.get("summary", "No summary available."))

    st.markdown("### AI Findings")

    findings = ai.get("findings", [])

    if findings:
        for finding in findings:
            with st.expander(
                f"{finding.get('severity', 'info').upper()} — "
                f"{finding.get('title', 'Untitled finding')}"
            ):
                st.write("**File:**", finding.get("file_path", "unknown"))

                line_number = finding.get("line_number")
                st.write(
                    "**Line:**",
                    line_number if line_number is not None else "Not specified"
                )

                st.write("**Evidence:**")
                st.code(finding.get("code_evidence", "") or "No evidence provided")

                st.write("**Explanation:**")
                st.write(finding.get("explanation", ""))

                st.write("**Recommendation:**")
                st.write(finding.get("recommendation", ""))

                st.write("**Confidence:**", finding.get("confidence", "N/A"))

    else:
        st.info("No AI findings reported.")

    st.markdown("### Test Suggestions")

    tests = ai.get("test_suggestions", [])

    if tests:
        for test in tests:
            st.markdown(f"**{test.get('test_name', 'Test')}**")
            st.write(test.get("purpose", ""))
            st.write("Expected:", test.get("expected_result", ""))
            st.divider()
    else:
        st.info("No test suggestions available.")

    st.markdown("### Positive Observations")

    positives = ai.get("positive_observations", [])

    if positives:
        for item in positives:
            st.markdown(f"- {item}")
    else:
        st.write("None reported.")

    st.markdown("### Limitations")

    limitations = ai.get("limitations", [])

    if limitations:
        for item in limitations:
            st.markdown(f"- {item}")
    else:
        st.write("No limitations reported.")

    st.divider()

    st.subheader("Static Analysis Findings")

    static_findings = data.get("static_findings", [])

    if static_findings:
        st.dataframe(
            static_findings,
            use_container_width=True
        )
    else:
        st.info("No deterministic static findings.")

    st.subheader("Changed Files")

    st.dataframe(
        data.get("files", []),
        use_container_width=True
    )

    st.subheader("Review Report Export")

    report_lines = [
        "# PR Review Intelligence Report",
        "",
        f"## {pr['title']}",
        "",
        f"PR URL: {pr['url']}",
        "",
        f"## Summary",
        ai.get("summary", "No summary"),
        "",
        f"## Risk Level",
        risk,
        "",
        "## AI Findings",
    ]

    for finding in findings:
        report_lines.extend([
            "",
            f"### {finding.get('title', 'Finding')}",
            f"- Severity: {finding.get('severity', 'unknown')}",
            f"- File: {finding.get('file_path', 'unknown')}",
            f"- Line: {finding.get('line_number', 'N/A')}",
            f"- Evidence: {finding.get('code_evidence', '')}",
            f"- Explanation: {finding.get('explanation', '')}",
            f"- Recommendation: {finding.get('recommendation', '')}",
        ])

    report_lines.extend(["", "## Test Suggestions"])

    for test in tests:
        report_lines.extend([
            "",
            f"### {test.get('test_name', 'Test')}",
            test.get("purpose", ""),
            f"Expected result: {test.get('expected_result', '')}",
        ])

    report_lines.extend(["", "## Positive Observations"])

    for item in positives:
        report_lines.append(f"- {item}")

    report_lines.extend(["", "## Limitations"])

    for item in limitations:
        report_lines.append(f"- {item}")

    markdown_report = "\n".join(report_lines)

    st.download_button(
        label="Download Review Report (.md)",
        data=markdown_report,
        file_name="pr_review_report.md",
        mime="text/markdown"
    )
