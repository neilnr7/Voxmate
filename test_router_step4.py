
from tools.registry import ToolRegistry
from tools.router import SemanticToolRouter

from tools.apps import open_app
from tools.browser import search_web
from tools.files import find_file
from tools.system import (
    increase_brightness,
    decrease_brightness,
)


# Build a small registry using actual project functions.
registry = ToolRegistry()

registry.register("open_app", open_app)
registry.register("search_web", search_web)
registry.register("find_file", find_file)
registry.register("increase_brightness", increase_brightness)
registry.register("decrease_brightness", decrease_brightness)

router = SemanticToolRouter(registry)


# Rule-based routing tests.
test_cases = [
    ("Open Microsoft Edge", "open_app"),
    ("Search the web for Python", "search_web"),
    ("Search for the file report.pdf", "find_file"),
    ("Find the document notes.docx", "find_file"),
    ("Increase brightness", "increase_brightness"),
    ("Brightness higher", "increase_brightness"),
    ("Decrease brightness", "decrease_brightness"),
    ("Dim the brightness", "decrease_brightness"),
    ("Increase volume", "increase_volume"),
    ("Turn up the volume", "increase_volume"),
    ("Decrease volume", "decrease_volume"),
    ("Turn down the volume", "decrease_volume"),
]

print("\n========== RULE-BASED ROUTER TESTS ==========\n")

passed = 0

for query, expected in test_cases:
    actual = router.get_rule_based_tool(query)
    success = actual == expected

    if success:
        passed += 1

    print(
        f"{'PASS' if success else 'FAIL'} | "
        f"{query} | Expected: {expected} | Actual: {actual}"
    )

print(f"\nRule-based result: {passed}/{len(test_cases)} passed.")


# Compound request splitting tests.
split_cases = [
    ("Open Edge and search the web", 2),
    ("Open Notepad then type hello", 2),
    ("Find notes and ideas.txt", 1),
]

print("\n========== REQUEST SPLITTING TESTS ==========\n")

split_passed = 0

for query, expected_count in split_cases:
    actual_parts = router.split_request(query)
    success = len(actual_parts) == expected_count

    if success:
        split_passed += 1

    print(
        f"{'PASS' if success else 'FAIL'} | "
        f"{query} | Parts: {actual_parts}"
    )

print(
    f"\nRequest splitting result: "
    f"{split_passed}/{len(split_cases)} passed."
)

print("\n============================================")
