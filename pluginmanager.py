import collections
import importlib
import importlib.util
import logging
import pathlib
import sys


class PluginManager:
    """
    A basic python plugin manager based off of https://gist.github.com/mepcotterell/6004997
    Rewritten using ImportLib and pathlib and updated to Python 3
    This will allow users to make plugin folders place any number of plugins in them, grab the module and then
    using getattr initialize and object from that module
    """

    def __init__(self, plugin_folder, log=logging, max_loaded_plugins=0):
        """
        This is the initialization method. User must set the plugin folder location. They can also set their own logging
        should they have their own. Finally they can also set the max number of lodable plugins if they want.
        :param plugin_folder: Base dir for plugins.
        :param log: Python logging.
        :param max_loaded_plugins: The max number of loadable plugins.
        """
        self.__logging = log
        self.__plugin_folder = plugin_folder
        self.__imported_plugins = collections.OrderedDict({})
        self.__max_loaded_plugins = max_loaded_plugins

        # !!!IMPORTANT: This line insures that the plugin directory gets added to the path so that it can be seen.
        # if not included the plugins folder may not be detected.
        sys.path.append(plugin_folder)

    def get_available_plugins(self):
        """
        grabs the available plugins in the plugins dir.
        :return: dictionary of available plugins.
        """
        plugins = dict()
        for module in pathlib.Path(self.__plugin_folder).glob("*.py"):
            plugins[module.stem] = {'name': module.stem,
                                    'info': module.parent
                                    }
        return plugins

    def get_imported_plugins(self):
        """
        grabs the already imported plugins.
        :return: dictionary of imported plugins.
        """
        return self.__imported_plugins

    def get_imported_plugin_module(self, plugin_name):
        """
        gets the module of an already loaded plugin.
        :param plugin_name: the name of the plugin you want the module for
        :return: the module of the requested plugin
        """
        if plugin_name:
            plugin = self.__imported_plugins.get(plugin_name)
            module = plugin.get('module')
            return module

    def import_plugin(self, plugin_name):
        """
        Imports a requested plugin from the plugins dir.
        :param plugin_name: the name of the plugin you want to import
        :return: None
        """
        plugins = self.get_available_plugins()

        if plugin_name in plugins:
            if plugin_name not in self.__imported_plugins:
                if self.__max_loaded_plugins <= 0:
                    # module_path = pathlib.Path(self.__plugin_folder).as_posix().replace("/", '.')
                    module = importlib.import_module(f"{plugin_name}", self.__plugin_folder)
                    self.__imported_plugins[plugin_name] = {
                        'name': plugin_name,
                        'info': plugins[plugin_name]['info'],
                        'module': module
                    }
                    self.__logging.info(f"{plugin_name} imported successfully.")
                elif self.__imported_plugins.__len__() >= self.__max_loaded_plugins:
                    self.__logging.warning(f"{self.__max_loaded_plugins} number of imported plugins reached, "
                                           f"please remove a loaded plugin or increase max number of "
                                           f"plugins to load another")
            else:
                self.__logging.warning(f"{plugin_name} is already loaded.")
        else:
            self.__logging.error(f"{plugin_name} not found in {self.__plugin_folder}")
            raise Exception(f"{plugin_name} not found in {self.__plugin_folder}")

    def import_all_plugins(self):
        """
        Imports all plugins in the plugin dir.
        :return: None
        """
        plugins = self.get_available_plugins()

        for plugin_name in plugins:
            if plugin_name not in self.__imported_plugins:
                if self.__max_loaded_plugins <= 0:
                    # module_path = pathlib.Path(self.__plugin_folder).as_posix().replace('/', '.')
                    module = importlib.import_module(f"{plugin_name}")
                    self.__imported_plugins[plugin_name] = {
                        'name': plugin_name,
                        'info': plugins[plugin_name]['info'],
                        'module': module
                    }
                    self.__logging.info(f"{plugin_name} imported successfully.")
                elif self.__imported_plugins.__len__() >= self.__max_loaded_plugins:
                    self.__logging.warning(f"{self.__max_loaded_plugins} number of imported plugins reached, "
                                           f"please remove a loaded plugin or increase max number of "
                                           f"plugins to load another")
            else:
                self.__logging.warning(f"{plugin_name} is already loaded.")

    def remove_plugin(self, plugin_name):
        """
        Removes a loaded plugin
        :param plugin_name: the name of the plugin to be removed
        :return: None
        """
        del self.__imported_plugins[plugin_name]
        self.__logging.info(f"{plugin_name} removed successfully.")
