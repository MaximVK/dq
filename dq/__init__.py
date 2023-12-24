from importlib.metadata import entry_points

def load_database_adapters():
    adapters = {}
    for entry_point in entry_points().get('dqlite.database_adapters', []):
        adapter = entry_point.load()
        adapters[entry_point.name] = adapter
    return adapters


adapters = load_database_adapters()