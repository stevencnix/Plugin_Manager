from pluginmanager import PluginManager
import argparse

parser = argparse.ArgumentParser(
    description='This is an example for the plugin manager.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--plugin_dir', metavar='PATH', type=str, required=True,
                    help='Path to your plugins dir')

parser.add_argument('--plugin_name', metavar='CHARS', type=str, required=True,
                    help='Name of the plugin to use. The name will be the file name.')


def main():
    args = parser.parse_args()

    # Initialize the plugin manager by giving it the plugin directory path.
    # Then import all the plugins in the directory. You can also import individual plugins.
    plugin_manager = PluginManager(plugin_folder=args.plugin_dir)
    plugin_manager.import_plugin(args.plugin_name)

    # Plugin manager imports all plugins in the plugin at runtime. The user then tells it which plugin to use based
    # off of the file name of the plugin.
    plugin_module = plugin_manager.get_imported_plugin_module(args.plugin_name)
    class_ = getattr(plugin_module, "Plugin")
    current_plugin = class_()

    # Do a quick check to make sure the plugin exists and if it does execute it.
    if current_plugin:
        current_plugin.execute()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Example has crashed. Error: {e}")
