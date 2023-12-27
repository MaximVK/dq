import argparse
import toml
from importlib import import_module
from pathlib import Path

def load_plugins():
    base_path = Path(__file__).parent.parent.parent
    config = toml.load(base_path / "pyproject.toml")
    plugins = config["tool"]["dq"]["plugins"]

    loaded_plugins = []

    for plugin_path in plugins.values():
        module_name, class_name = plugin_path.split(":")
        module = import_module(module_name)
        plugin_class = getattr(module, class_name)
        loaded_plugins.append(plugin_class())

    return loaded_plugins


def main():
    plugins = load_plugins()
    for plugin in plugins:
        plugin.saysomething()

    parser = argparse.ArgumentParser(description="DQ Lite")
    parser.add_argument("--name", help="Enter your name")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()