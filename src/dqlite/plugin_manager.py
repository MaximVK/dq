import logging
from importlib.metadata import entry_points, EntryPoint

logger = logging.getLogger(__name__)


class PluginManager:

    def __init__(self):
        """
        Initialize the PluginManager, setting up an empty dictionary to hold plugins
        and loading all plugins found in the 'dqlite.plugins' entry point group.
        """
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        """
        Load the plugin classes from entry points in the 'dqlite.plugins' group,
        handle potential exceptions during loading, and log the events.
        """
        for entry_point in entry_points().get('dqlite.plugins', []):
            try:
                plugin = entry_point.load()
                self.plugins[entry_point.name] = plugin
                logger.info(f"Successfully loaded plugin {entry_point.name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {entry_point.name}: {str(e)}")

    def get_plugin_class(self, plugin_name: str, class_attr: str):
        """
        Generic method to get a specified class ('environment_class', 'adapter_class', etc.)
        from a plugin. Handles cases where the plugin or class does not exist.
        """
        try:
            plugin = self.plugins[plugin_name]
        except KeyError:
            logger.error(f"Plugin {plugin_name} not found.")
            return None

        try:
            plugin_class = getattr(plugin, class_attr)
        except AttributeError:
            logger.error(f"Plugin {plugin_name} does not have a {class_attr}.")
            return None

        return plugin_class

    def get_environment_class(self, plugin_name: str):
        """
        Get the 'environment_class' attribute from a plugin.
        """
        return self.get_plugin_class(plugin_name, 'environment_class')

    def get_adapter_class(self, plugin_name: str):
        """
        Get the 'adapter_class' attribute from a plugin.
        """
        return self.get_plugin_class(plugin_name, 'adapter_class')