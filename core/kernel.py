'''
Created on Oct 16, 2010

@author: EB020653
'''

from core.the_ev3nt_management import Ev3ntManager as EventManager
from core.plugins.plugin_manager import PluginManager

class kernel(object):
    __event_manager = EventManager()
    __plugins_manager = PluginManager(None)
    __plugins_configs = dict()    
    
    def __init__(self):
        raise NotImplementedError("No, no, i'm a 'static' class")
    
    @classmethod
    def new_event(cls, plugin, event_name, event_permission_cb=None):
        evt='->'.join([plugin,event_name])
        return cls.__event_manager.new_event(evt, event_permission_cb)
    
    @classmethod
    def register_to_event(cls, plugin, event_name, event_handler):
        evt='->'.join([plugin,event_name])
        return cls.__event_manager.register_to_event(evt, event_handler)
    
    @classmethod
    def unregister_to_event(cls, plugin, event_name, event_handler):
        evt='->'.join([plugin,event_name])
        return cls.__event_manager.unregister_to_event(evt, event_handler)
    
    @classmethod
    def fire_event(cls, event_hash, *args, **kwargs):
        return cls.__event_manager.fire_event(event_hash, *args, **kwargs)
    
    @classmethod
    def get_event_control(cls, plugin, event_name, event_token):
        evt='->'.join([plugin,event_name])
        return cls.__event_manager.get_event_hash(evt, event_token)

    @classmethod
    def get_plugin_config(cls, plugin_name):
        return cls.__plugins_configs[plugin_name]
    
    @classmethod
    def activate_plugin(cls, plugin_name):
        return cls.__plugins_manager.activate_plugin(plugin_name)
    
    @classmethod
    def deactivate_plugin(cls, plugin_name):
        return cls.__plugins_manager.deactivate_plugin(plugin_name)