
from agent import Agent


def main():
    agent = Agent()
    router = agent.router

    test_cases = [
        # Application management
        ("Open Notepad", "open_app"),
        ("Close Chrome", "close_app"),
        ("Switch to Chrome", "focus_app"),
        ("List all running applications", "list_running_apps"),

        # Browser and web
        ("Open GitHub", "open_url"),
        ("Search the web for Python tutorials", "search_web"),
        ("Get the readable text from this webpage", "get_page_text"),
        ("Go back to the previous browser page", "go_back"),

        # Date, time and system information
        ("What time is it?", "get_time"),
        ("What is today's date?", "get_date"),
        ("Check my laptop battery level", "get_battery"),

        # Volume and brightness
        ("Set volume to 50 percent", "set_volume"),
        ("Mute the volume", "mute_volume"),
        ("Unmute the volume", "unmute_volume"),
        ("Increase the volume", "increase_volume"),
        ("Decrease the volume", "decrease_volume"),
        ("Set brightness to 60 percent", "set_brightness"),
        ("Increase screen brightness", "increase_brightness"),
        ("Decrease screen brightness", "decrease_brightness"),

        # File management
        ("List files in Downloads", "list_files"),
        ("Find the file agent.py", "find_file"),
        ("Read the contents of agent.py", "read_file"),
        ("Create a new file named test.txt", "create_file"),
        ("Write Hello World into test.txt", "write_file"),
        ("Rename test.txt to demo.txt", "rename_file"),
        ("Copy test.txt to Downloads", "copy_file"),
        ("Move test.txt to Documents", "move_file"),
        ("Delete test.txt", "delete_file"),
        ("Get information about agent.py", "get_file_info"),
        ("Create a folder named Projects", "create_folder"),

        # Clipboard
        ("Read the clipboard contents", "read_clipboard"),
        ("Copy Hello World to the clipboard", "write_clipboard"),
        ("Clear the clipboard", "clear_clipboard"),

        # Keyboard, mouse and screenshot
        ("Type Hello World", "type_text"),
        ("Press the Enter key", "press_key"),
        ("Press Ctrl Shift Escape", "hotkey"),
        ("Click at coordinates 500 and 300", "click"),
        ("Scroll down", "scroll"),
        ("Take a screenshot", "take_screenshot"),
    ]

    passed = 0
    failed = 0

    print("\n" + "=" * 65)
    print("VOXMATE - COMPLETE SEMANTIC ROUTER TEST")
    print("=" * 65)

    for index, (request, expected_tool) in enumerate(test_cases, 1):

        selected = router.select_tools(request)

        selected_names = [
            tool["name"] for tool in selected
        ]

        if expected_tool in selected_names:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"

        print("\n" + "-" * 65)
        print(f"TEST {index}/{len(test_cases)}: {request}")
        print(f"EXPECTED:  {expected_tool}")
        print(f"SELECTED:  {', '.join(selected_names)}")
        print(f"RESULT:    {status}")

    print("\n" + "=" * 65)
    print("FINAL ROUTING TEST RESULTS")
    print("=" * 65)

    print(f"Total tests: {len(test_cases)}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")

    accuracy = (passed / len(test_cases)) * 100

    print(f"Accuracy:    {accuracy:.2f}%")

    print("=" * 65)


if __name__ == "__main__":
    main()
