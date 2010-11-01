'''
Created on Oct 16, 2010

@author: EB020653
'''

from core.the_ev3nt_management import Ev3ntManager as EventManager

class kernel(object):
    __event_manager=None
    __plugin_config=None
    
    def __init__(self):
        self.__event_manager = EventManager()
        self.__plugin_config = dict()
    
    
    def new_event(self, plugin, event_name, event_permission_cb=None):
        evt='->'.join([plugin,event_name])
        return self.__event_manager.new_event(evt, event_permission_cb)
    
    def register_to_event(self, plugin, event_name, event_handler):
        evt='->'.join([plugin,event_name])
        return self.__event_manager.register_to_event(evt, event_handler)
    
    def fire_event(self, event_hash, *args, **kwargs):
        return self.__event_manager.fire_event(event_hash, *args, **kwargs)
    
    def get_event_control(self, plugin, event_name, event_token):
        evt='->'.join([plugin,event_name])
        return self.__event_manager.get_event_hash(evt, event_token)

    def get_plugin_config(self, plugin_name):
        return self.__plugin_config[plugin_name]