# tests/unit/tree/test_tree_config.py

import pytest
from windows_use.agent.tree.config import (
    INTERACTIVE_CONTROL_TYPE_NAMES,
    DEFAULT_ACTIONS,
    INFORMATIVE_CONTROL_TYPE_NAMES,
)

class TestTreeConfig:
    def test_interactive_control_type_names_type(self):
        assert isinstance(INTERACTIVE_CONTROL_TYPE_NAMES, set)

    def test_interactive_control_type_names_content(self):
        expected_names = {
            'ButtonControl', 'ListItemControl', 'MenuItemControl', 'EditControl',
            'CheckBoxControl', 'RadioButtonControl', 'ComboBoxControl',
            'HyperlinkControl', 'SplitButtonControl', 'TabItemControl',
            'TreeItemControl', 'DataItemControl', 'HeaderItemControl',
            'TextBoxControl', 'SpinnerControl', 'ScrollBarControl'
        }
        assert INTERACTIVE_CONTROL_TYPE_NAMES == expected_names

    def test_default_actions_content(self):
        expected_actions = {'Click', 'Press', 'Jump', 'Check', 'Uncheck', 'Double Click'}
        assert DEFAULT_ACTIONS == expected_actions

    def test_informative_control_type_names_content(self):
        expected_names = {'TextControl', 'ImageControl', 'StatusBarControl'}
        assert INFORMATIVE_CONTROL_TYPE_NAMES == expected_names
