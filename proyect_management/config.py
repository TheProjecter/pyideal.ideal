'''
Created on Oct 5, 2010

@author: EB020653
'''

PLUGIN_NAME = "proyect_management"


class ConfigPlugin(object):
    """
        Contains specific plugin configuration.
    """
    __event_hash = None
    __app_config = None
    
    def __init__(self, events_dict):
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
    #__events_names = None
    __callbacks = None
    __event_hash = None
    __core = None
    
    __EVENTS_NAMES = [ #Event Name : Auth_Cb
                      {"openedFile->pre_save" : None}, 
                      {"openedFile->post_save" : None}, 
                      {"openedFile->pre_open" : None}, 
                      {"openedFile->post_open" : None}, 
                      {"openedFile->pre_read" : None}, 
                      {"openedFile->post_read" : None},
                      ]

    def __init__(self):
        """
        Constructor
        """
        self.__plugins_configs = ConfigPlugin(app_config, event_hash)
        pass
    
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
    
    def get_config(self, event_hash):
        """
            Return the module config.
        """
        if self.__plugin_config is None:
            self.__plugin_config=ConfigPlugin(self.__app_cfg, event_hash)
        return self.__plugin_config
    
    def get_events(self):
        return self.__EVENTS_NAMES