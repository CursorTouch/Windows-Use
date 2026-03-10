# tests/unit/desktop/test_desktop_config.py

import pytest
from windows_use.agent.desktop.config import AVOIDED_APPS, EXCLUDED_APPS

class TestDesktopConfig:
    def test_avoided_apps_type(self):
        assert isinstance(AVOIDED_APPS, set)

    def test_avoided_apps_content(self):
        assert "AgentUI" in AVOIDED_APPS

    def test_excluded_apps_type(self):
        assert isinstance(EXCLUDED_APPS, set)

    def test_excluded_apps_content(self):
        assert "Progman" in EXCLUDED_APPS
        assert "Shell_TrayWnd" in EXCLUDED_APPS
        assert "Windows.UI.Core.CoreWindow" in EXCLUDED_APPS
