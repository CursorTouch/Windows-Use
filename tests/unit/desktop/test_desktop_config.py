import pytest
from typing import Set

from windows_use.desktop.config import AVOIDED_APPS, EXCLUDED_APPS

class TestDesktopConfig:
    """
    Tests for the configuration variables in windows_use.desktop.config.
    """

    def test_avoided_apps_type(self):
        """
        Test that AVOIDED_APPS is a set.
        """
        assert isinstance(AVOIDED_APPS, Set)

    def test_avoided_apps_content(self):
        """
        Test the content of AVOIDED_APPS.
        """
        assert "Recording toolbar" in AVOIDED_APPS
        assert len(AVOIDED_APPS) == 1

    def test_excluded_apps_type(self):
        """
        Test that EXCLUDED_APPS is a set.
        """
        assert isinstance(EXCLUDED_APPS, Set)

    def test_excluded_apps_content(self):
        """
        Test the content of EXCLUDED_APPS, including the union with AVOIDED_APPS.
        """
        assert "Program Manager" in EXCLUDED_APPS
        assert "Taskbar" in EXCLUDED_APPS
        assert "Recording toolbar" in EXCLUDED_APPS
        assert len(EXCLUDED_APPS) == 3 # "Program Manager", "Taskbar", "Recording toolbar"

    def test_excluded_apps_union_with_avoided_apps(self):
        """
        Test that EXCLUDED_APPS is correctly formed by unioning with AVOIDED_APPS.
        """
        expected_excluded = set(["Program Manager", "Taskbar"]).union(AVOIDED_APPS)
        assert EXCLUDED_APPS == expected_excluded
