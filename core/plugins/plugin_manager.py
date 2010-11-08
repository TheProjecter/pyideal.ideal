'''
Created on Oct 17, 2010

@author: EB020653
'''
#from yapsy import PluginManager

from os.path import isdir

#class Core_PluginManager(PluginManager):
#    def __init__(self):
#        pass


class PluginManager(object):
    __app_config=None
    __plugin_list=None
    __plugin_path=None
    
    def __init__(self, app_config):
        self.__app_config = app_config
        self.__plugin_list = app_config.get_plugin_list()
        self.__plugin_path = app_config.get_path("plugin_path")
    
    # here?
    def reconfigure(self, app_config): 
        self.__app_config = app_config
    
    def install_plugin(self, plugin_file_or_dir, enable=False):
        '''
            Installs the plugin, needs a zip file, or a directory.
            Enable if the plugins installs ok.
        '''
        #TODO: mover todo a la ruta que corresponda
        pass
    
    def uninstall_plugin(self, plugin_name, enable=False):
        '''
            Uninstalls the plugin. Kill all the files! :P
        '''
        #TODO: mover todo a la ruta que corresponda
        pass
    
    def activate_plugin(self, plugin_name):
        '''
            Activate (load) the plugin
        '''
        #TODO: Things...
        self.__register_plugin_events(plugin_name)
        #TODO: More Things...
    
    def deactivate_plugin(self, plugin_name):
        '''
            Deactivate (unload) the plugin
        '''
        #TODO: Things...
        self.__unregister_plugin_events(plugin_name)
        #TODO: More Things...
    
    def __check_plugins(self):
        '''
            Check the plugins instalation. Only on app start.
        '''
        pass
    
    def __register_plugin_events(self, plugin_name):
        '''
            Register the plugins events on core!.
        '''
        #TODO: Registrar eventos del plugin determinado.
        #asd=__import__(plugin_name, fromlist=['', ''])
        plugin = self.__plugin_list[plugin_name]
        __import__(plugin)
        
    def __unregister_plugin_events(self, plugin_name):
        '''
            Register the plugins events on core!.
        '''
        #TODO: Desregistrar eventos del plugin determinado.
        #asd=__import__(plugin_name, fromlist=['', ''])
        mod = self.__plugin_list[plugin_name]

