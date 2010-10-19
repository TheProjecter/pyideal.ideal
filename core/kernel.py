'''
Created on Oct 16, 2010

@author: EB020653
'''

from core.the_ev3nt_management import Ev3ntManager as EventManager

class kernel(object):
    __event_manager=None
    
    def __init__(self):
        self.__event_manager = EventManager()
    
    
    def new_event(self, plugin, event_name, event_permission_cb=None):
        pass
    
    def register_to_event(self, plugin, event_name, event_handler):
        pass
    
    def fire_event(self, plugin, event_hash, *args, **kwargs):
        pass
    