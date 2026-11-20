
import re


def parse_diff(patch: str):
    """
    Extract added and deleted lines from a unified Git diff.
    Added lines include their new-file line numbers.
    """

    added_lines = []
    deleted_lines = []
    current_line = None

    for line in patch.splitlines():

        # Detect the beginning of a diff hunk
        if line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,\d+)?", line)

            if match:
                current_line = int(match.group(1))

        elif line.startswith("+++"):
            continue

        elif line.startswith("---"):
            continue

        elif line.startswith("+") and current_line is not None:
            added_lines.append({
                "line_number": current_line,
                "content": line[1:]
            })
            current_line += 1

        elif line.startswith("-"):
            deleted_lines.append(line[1:])

        elif line.startswith(" "):
            if current_line is not None:
                current_line += 1

    return {
        "added_lines": added_lines,
        "deleted_lines": deleted_lines
    }
