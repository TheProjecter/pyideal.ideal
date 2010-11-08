'''
Created on Oct 5, 2010

@author: EB020653
'''
from core import core

PLUGIN_NAME="proyect_management"
EVENTS_NAMES= ["pre_save", "post_save", "pre_open", "post_open",\
               "pre_read","post_read"]

class ConfigPlugin(object):
    """
        Contains specific plugin configuration.
    """
    __event_hash = None
    __app_config = None
    
    def __init__(self, app_cfg, events_dict):
        self.__event_hash = events_dict
        self.__app_config = app_cfg
    
    def get_hash(self, name):
        """
            Devuelve el hash de un event para poder dispararlo
        """
        return self.__event_hash[name]
    
    
#class opened
class SetupPlugin(object):
    """
        Setup the Initial Plugin config and check deps for it.
    """
    __app_cfg = None
    __plugin_config = None
    __events_names = None
    __callbacks = None
    __event_hash = None
    __core = None

    def __init__(self, app_config):
        """
        Constructor
        """
        self.__app_cfg=app_config
        """
            Creating Events
        """
        event_hash=dict()
        for event in EVENTS_NAMES:
            event_hash.update({event:core.new_event(self, PLUGIN_NAME, event)})
        self.__plugins_configs = ConfigPlugin(app_config, event_hash)
        
    
    def check_config_data(self):
        """
            Validate if the needed config exists.
        """
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
            pmtest = ProyectManager(self.__plugins_configs)
            pmtest = None
        except:
            return False
        return True #ProyectManager(self._cfg)
    
    def get_config(self):
        """
            Return the module config.
        """
        return self.__plugin_config
    
    def get_events(self):
        '''
            Returns a dictionary with event_name:auth_fire_callback_func
            auth_fire_callback_func can be None
        '''
        self.__events_names=('openedFile->pre_save', 'openedFile->post_save', )
        self.__callbacks=(None,)
        
        return dict(map(None, events_names, callbacks))