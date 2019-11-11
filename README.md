# Plugin Manager

## About Plugin Manager

Plugin Manager is a little Python library I created based off of Michael Cotterell Simple Python Plugin Manager. I have changed a significant bit of how it works and updated it to work with Python 3.7 using more appropriate Python libraries. I originally tried forking off of his project, but ran into some issues. I have decided to keep use of his copy write license since it is still similar in many ways. Plugin Manager lets you create a plugins directory with which it will load all .py files inside of it. You then can load all of them or specific ones by name. I have found this to be very useful in my projects and I hope it will help you as well.

## Usage

1. Initialize the plugin manager

	``` shell
	plugin_manager = PluginManager(plugin_folder=\<INSERT PLUGINS DIR PATH HERE\>)
	```
	
2. Import the plugins in the plugins directory

	``` shell
	plugin_manager.import_all_plugins()
	```
	
	or
	
	``` shell
	plugin_manager.import_plugin(plugin_name=\<INSERT PLUGIN NAME\>)
	```
3. Get the imported plugin

	```shell
	plugin_module = plugin_manager.get_imported_plugin_module(args.plugin_name)
    class_ = getattr(plugin_module, "Plugin")
    current_plugin = class_()
	```
	
4. execute the plugin

	```shell
    if current_plugin:
        current_plugin.execute()
	```
	
## PLUGIN REQUIREMENTS

- Plugins are dependent on there file names. For example a plugin file "foo.py" would be named "foo".
- A plugin must be a class named Plugin. For example "Class Plugin:"
- A plugin must also contain and execute method:
- Plugins must be .py files.

## Future Plans

- If I get around to it I will try and set it up to be installed and as a pip wheel.
