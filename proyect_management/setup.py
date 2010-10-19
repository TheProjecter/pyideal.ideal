'''
Created on Oct 5, 2010

@author: EB020653
'''
#from exceptions import IOError


#class opened
class SetupPlugin(object):
    '''
    classdocs
    '''
    __app_cfg = None

    def __init__(self, app_config):
        '''
        Constructor
        '''
        self.__app_cfg=app_config
        
    
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
        
