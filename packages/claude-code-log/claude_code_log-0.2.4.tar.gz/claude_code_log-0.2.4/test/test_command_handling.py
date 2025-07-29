#!/usr/bin/env python3
"""Test cases for command message handling and parsing."""

import json
import tempfile
from pathlib import Path
from claude_code_log.converter import (
    load_transcript,
    generate_html,
)


def test_system_message_command_handling():
    """Test that system messages with command names are shown in expandable details."""
    command_message = {
        "type": "user",
        "timestamp": "2025-06-11T22:44:17.436Z",
        "parentUuid": None,
        "isSidechain": False,
        "userType": "human",
        "cwd": "/tmp",
        "sessionId": "test_session",
        "version": "1.0.0",
        "uuid": "test_cmd_001",
        "message": {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": '<command-message>init is analyzing your codebase…</command-message>\n<command-name>init</command-name>\n<command-args></command-args>\n<command-contents>{"type": "text", "text": "Please analyze this codebase..."}</command-contents>',
                }
            ],
        },
    }

    # Test that command messages are processed correctly end-to-end
    # (We can't test extraction directly on raw dicts because they need to be parsed first)

    # Test HTML generation
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(json.dumps(command_message) + "\n")
        f.flush()
        test_file_path = Path(f.name)

    try:
        messages = load_transcript(test_file_path)
        html = generate_html(messages, "Test Transcript")

        # Should contain details element with command name
        assert "<details>" in html, "Should contain details element"
        assert "<strong>Command:</strong> init" in html, (
            "Should show command name in summary"
        )
        assert "class='message system'" in html, "Should have system CSS class"

        print(
            "✓ Test passed: System messages with commands are shown in expandable details"
        )

    finally:
        test_file_path.unlink()


if __name__ == "__main__":
    test_system_message_command_handling()
    print("\n✅ All command handling tests passed!")
