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
    
    def install_plugin(self, plugin_file_or_dir, activate=False):
        #TODO: mover todo a la ruta que corresponda
        pass
    
    def activate_plugin(self, plugin_name):
        #TODO: validar el path e instalar ocn pugin_name
        if not (plugin_name in self.__plugin_list.key()):
            raise ValueError("""No Existe el plugin!, Falta instalarlo?""")
        
    def __check_plugins(self):
        pass
    
    def __register_plugin_events(self, plugin_name):
        #TODO: Registrar eventos del plugin determinado.
        #asd=__import__(plugin_name, fromlist=['', ''])
        mod = self.__plugin_list[plugin_name]
        
    

