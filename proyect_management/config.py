'''
Created on Oct 5, 2010

@author: EB020653
'''
#from exceptions import IOError
#import config
from core import core

PLUGIN_NAME="proyect_management"

class ConfigPlugin(object):
    __event_hash = None
    
    def __init__(self):
        self.__event_hash = dict()
    
    def add_event(self, d):
        self.__event_hash.update(d)
    
    def get_hash(self, name):
        return self.__event_hash[name]
    
    
#class opened
class SetupPlugin(object):
    '''
    classdocs
    '''
    __app_cfg = None
    __plugin_cfg = None
    __event_hash = None
    __core = None

    def __init__(self, app_config):
        '''
        Constructor
        '''
        self.__app_cfg=app_config
        self.__plugin_cfg = ConfigPlugin()
        self.__event_hash=dict()
        
    
    def check_config_data(self):
        pass   
    
    def reconfigure(self, app_config):
        """
            Reconfigure the plugin with the new parameters
            saved at application level.
        """
        self.__app_cfg = app_config
        return True
    
    def start_me_up(self, *args, **kwargs):
        """
            Try to init the plugin importing the required
            modules and executing all the configuration
            functions that it's needed.
        """
        try:
            from proyect_management import ProyectManager
            pmtest = ProyectManager(self.__app_config)
            pmtest = None
        except:
            return False
        return True #ProyectManager(self._cfg)
    
    def register_events(self):
        self.__plugin_cfg.add_event({"pre_save":core.new_event(self, PLUGIN_NAME, "pre_save")})
        self.__plugin_cfg.add_event({"post_save":core.new_event(self, PLUGIN_NAME, "post_save")})
        self.__plugin_cfg.add_event({"pre_open":core.new_event(self, PLUGIN_NAME, "pre_open")})
        self.__plugin_cfg.add_event({"post_open":core.new_event(self, PLUGIN_NAME, "post_open")})
        self.__plugin_cfg.add_event({"pre_read":core.new_event(self, PLUGIN_NAME, "pre_read")})
        self.__plugin_cfg.add_event({"post_read":core.new_event(self, PLUGIN_NAME, "post_read")})
        
    def get_config(self):
        return self.__plugin_cfg
        
    def list_events(self):
        return {"pre_save":None, "post_save":None}



