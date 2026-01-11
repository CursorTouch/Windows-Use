import pytest
from unittest.mock import MagicMock, patch
import ast
import re

from langchain_core.messages import BaseMessage, HumanMessage
from windows_use.agent.views import AgentData, Action
from windows_use.agent.utils import read_file, extract_agent_data, image_message

class TestAgentUtils:
    """
    Tests for utility functions in windows_use.agent.utils.
    """

    @patch("builtins.open", new_callable=MagicMock)
    def test_read_file_success(self, mock_open):
        """
        Test `read_file` function for successful file reading.

        What is being tested:
            - The `open` function is called with the correct file path and mode.
            - The content read from the mock file is returned correctly.
        """
        mock_file = MagicMock()
        mock_file.read.return_value = "file content"
        mock_open.return_value.__enter__.return_value = mock_file

        content = read_file("dummy/path/file.txt")
        mock_open.assert_called_once_with("dummy/path/file.txt", "r")
        mock_file.read.assert_called_once()
        assert content == "file content"

    @patch("builtins.open", side_effect=IOError("File not found"))
    def test_read_file_io_error(self, mock_open):
        """
        Test `read_file` function when an IOError occurs.

        What is being tested:
            - An `IOError` raised by `open` is propagated correctly.
        """
        with pytest.raises(IOError, match="File not found"):
            read_file("nonexistent/path/file.txt")
        mock_open.assert_called_once_with("nonexistent/path/file.txt", "r")

    @pytest.mark.parametrize(
        "message_content, expected_memory, expected_evaluate, expected_thought, expected_action_name, expected_action_params",
        [
            (
                "<memory>mem</memory><evaluate>eval</evaluate><thought>thought</thought><action_name>act</action_name><action_input>{\"key\": \"value\"}</action_input>",
                "mem",
                "eval",
                "thought",
                "act",
                {"key": "value"},
            ),
            (
                "<thought>only thought</thought><action_name>tool</action_name><action_input>{}</action_input>",
                None,
                None,
                "only thought",
                "tool",
                {},
            ),
            (
                "<action_name>no_params</action_name><action_input>null</action_input>",
                None,
                None,
                None,
                "no_params",
                None,
            ),
            (
                "no xml tags",
                None,
                None,
                None,
                None,
                None,
            ),
            (
                "<action_name>invalid_json</action_name><action_input>{invalid}</action_input>",
                None,
                None,
                None,
                "invalid_json",
                "{invalid}",
            ),
            (
                "<action_name>empty_action</action_name><action_input></action_input>",
                None,
                None,
                None,
                "empty_action",
                {},
            ),
        ],
    )
    def test_extract_agent_data_various_inputs(
        self,
        message_content,
        expected_memory,
        expected_evaluate,
        expected_thought,
        expected_action_name,
        expected_action_params,
    ):
        """
        Test `extract_agent_data` with various message contents, including valid, partial, and invalid XML.

        What is being tested:
            - Correct extraction of memory, evaluate, thought, action name, and action parameters.
            - Handling of missing tags (returns None).
            - Handling of invalid JSON in action_input (returns raw string).
            - Correct instantiation of AgentData and Action objects.
        """
        mock_message = MagicMock(spec=BaseMessage)
        mock_message.content = message_content

        agent_data = extract_agent_data(mock_message)

        assert agent_data.memory == expected_memory
        assert agent_data.evaluate == expected_evaluate
        assert agent_data.thought == expected_thought

        if expected_action_name is not None:
            assert agent_data.action is not None
            assert agent_data.action.name == expected_action_name
            assert agent_data.action.params == expected_action_params
        else:
            assert agent_data.action is None

    @patch("windows_use.agent.utils.HumanMessage")
    def test_image_message(self, mock_human_message):
        """
        Test `image_message` function creates a HumanMessage with correct content structure.

        What is being tested:
            - `HumanMessage` is called with a list containing text and image_url dictionaries.
            - The prompt and image are correctly placed in the dictionaries.
        """
        mock_prompt = "This is a test prompt."
        mock_image = "base64_encoded_image_data"

        image_message(mock_prompt, mock_image)

        mock_human_message.assert_called_once_with(
            content=[
                {"type": "text", "text": mock_prompt},
                {"type": "image_url", "image_url": mock_image},
            ]
        )
