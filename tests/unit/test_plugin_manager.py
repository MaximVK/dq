import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from dqlite.plugin_manager import PluginManager  # Replace with your actual module import


@patch('dqlite.plugin_manager.entry_points')
def test_successful_plugin_loading(mock_entry_points):
    # Mocking EntryPoint objects
    mock_entry_point = MagicMock()
    mock_entry_point.name = 'test_plugin'
    mock_entry_point.load.return_value = MagicMock()

    mock_entry_points.return_value = {'dqlite.plugins': [mock_entry_point]}

    manager = PluginManager()
    assert 'test_plugin' in manager.plugins
    assert len(manager.plugins) > 0
    mock_entry_points.assert_called()


def test_get_existing_plugin_class():
    test_plugin = MagicMock()
    test_plugin.environment_class = MagicMock()
    manager = PluginManager()
    manager.plugins = {'test_plugin': test_plugin}  # Set the attribute on the instance
    assert manager.get_environment_class('test_plugin') is not None


class CustomMock(MagicMock):
    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattr__(name)
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

@patch('dqlite.entry_points')
def test_get_nonexistent_class_from_plugin(mock_entry_points):
    # Create a CustomMock for the plugin
    test_plugin = CustomMock()
    test_plugin.name = 'test_plugin'

    # Simulate the plugin being loaded
    mock_entry_points.return_value = {'dqlite.plugins': [test_plugin]}

    manager = PluginManager()
    manager.plugins = {'test_plugin': test_plugin}

    # Test for nonexistent class attribute
    plugin_class = manager.get_plugin_class('test_plugin', 'nonexistent_class')
    assert plugin_class is None
