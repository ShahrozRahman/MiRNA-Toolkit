from mirna_toolkit.utils.plugins import PluginRegistry


def test_plugin_registry_register_and_get():
    registry = PluginRegistry()

    def plugin(x):
        return x + 1

    registry.register("adder", plugin)
    assert registry.get("adder")(1) == 2
    assert registry.list_plugins() == ["adder"]
