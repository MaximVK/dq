from importlib.metadata import entry_points


class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        for entry_point in entry_points().get('dq.plugins', []):
            plugin = entry_point.load()
            self.plugins[entry_point.name] = plugin

    # Methods to get adapters and environments from plugins
    def get_environment_class(self, plugin_name):
        return self.plugins[plugin_name].environment_class

    def get_adapter_class(self, plugin_name):
        return self.plugins[plugin_name].adapter_class

