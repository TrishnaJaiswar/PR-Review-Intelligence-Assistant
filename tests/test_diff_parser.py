
from backend.diff_parser import parse_diff


def test_parse_diff():
    patch = """@@ -1,3 +1,4 @@
 def hello():
-    print("Hello")
+    print("Hello World")
+    return True
 """

    result = parse_diff(patch)

    assert len(result["added_lines"]) == 2
    assert result["added_lines"][0]["line_number"] == 2
    assert result["added_lines"][1]["line_number"] == 3
    assert len(result["deleted_lines"]) == 1
