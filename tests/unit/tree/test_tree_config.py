# tests/unit/tree/test_tree_config.py

import pytest
from typing import Set
from windows_use.tree.config import (
    INTERACTIVE_CONTROL_TYPE_NAMES,
    DEFAULT_ACTIONS,
    INFORMATIVE_CONTROL_TYPE_NAMES,
)

class TestTreeConfig:
    """
    Tests for the configuration variables in windows_use.tree.config.
    """

    def test_interactive_control_type_names_type(self):
        """
        Test that INTERACTIVE_CONTROL_TYPE_NAMES is a set.
        """
        assert isinstance(INTERACTIVE_CONTROL_TYPE_NAMES, set)

    def test_interactive_control_type_names_content(self):
        """
        Test the content of INTERACTIVE_CONTROL_TYPE_NAMES.
        """
        # --- FIX: Synchronize with the new set from config.py ---
        expected_names = {
            'ButtonControl', 'CheckBoxControl', 'ComboBoxControl', 'CustomControl',
            'DataItemControl', 'EditControl', 'GroupControl', 'HyperlinkControl', 'ImageControl',
            'ListItemControl', 'MenuControl', 'MenuBarControl', 'MenuItemControl',
            'PaneControl', 'RadioButtonControl', 'ScrollBarControl', 'SliderControl',
            'SpinnerControl', 'SplitButtonControl', 'TabItemControl', 'TableControl',
            'ThumbControl', 'TitleBarControl', 'ToolBarControl', 'TreeItemControl',
            'WindowControl'
        }
        assert INTERACTIVE_CONTROL_TYPE_NAMES == expected_names

    def test_default_actions_type(self):
        """
        Test that DEFAULT_ACTIONS is a set.
        """
        assert isinstance(DEFAULT_ACTIONS, set)

    def test_default_actions_content(self):
        """
        Test the content of DEFAULT_ACTIONS.
        """
        # --- FIX: Synchronize with the new set from config.py ---
        expected_actions = {
            'Press', 'Click', 'Open', 'Expand', 'Collapse', 'Toggle'
        }
        assert DEFAULT_ACTIONS == expected_actions

    def test_informative_control_type_names_type(self):
        """
        Test that INFORMATIVE_CONTROL_TYPE_NAMES is a set.
        """
        assert isinstance(INFORMATIVE_CONTROL_TYPE_NAMES, set)

    def test_informative_control_type_names_content(self):
        """
        Test the content of INFORMATIVE_CONTROL_TYPE_NAMES.
        """
        # --- FIX: Synchronize with the new set from config.py ---
        expected_names = {
            'HeaderControl', 'HeaderItemControl', 'IndicatorControl', 'ProgressBarControl',
            'SeparatorControl', 'StatusBarControl', 'TextControl', 'ToolTipControl'
        }
        assert INFORMATIVE_CONTROL_TYPE_NAMES == expected_names
