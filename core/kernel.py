'''
Created on Oct 16, 2010

@author: EB020653
'''
import version
from core.app_config import app_config
from core.the_ev3nt_management import Ev3ntManager as EventManager
from core.plugins.plugin_manager import PluginManager

class Core(object):
    __event_manager = EventManager()
    __plugins_manager = PluginManager(app_config(version.APP_CONFIG_NAME))
    __plugins_configs = None   
    
    def __init__(self):
        raise NotImplementedError("No, no, i'm a 'static' class")
    
    @classmethod
    def new_event(cls, plugin, event_name, event_permission_cb=None):
        evt = '->'.join([plugin, event_name])
        return cls.__event_manager.new_event(evt, event_permission_cb)
    
    @classmethod
    def register_to_event(cls, plugin, event_name, event_handler):
        evt = '->'.join([plugin, event_name])
        return cls.__event_manager.register_to_event(evt, event_handler)
    
    @classmethod
    def unregister_to_event(cls, plugin, event_name, event_handler):
        evt = '->'.join([plugin, event_name])
        return cls.__event_manager.unregister_to_event(evt, event_handler)
    
    @classmethod
    def fire_event(cls, event_hash, *args, **kwargs):
        return cls.__event_manager.fire_event(event_hash, *args, **kwargs)
    
    @classmethod
    def get_event_control(cls, plugin, event_name, event_token):
        evt = '->'.join([plugin, event_name])
        return cls.__event_manager.get_event_hash(evt, event_token)

    @classmethod
    def get_app_config(cls):
        return  
    
    @classmethod
    def get_plugin_list(cls):
        return cls.__plugins_manager.get_all_names()
    
    @classmethod
    def get_active_plugin_list(cls):
        return cls.__plugins_manager.get_active_names()
    
    @classmethod
    def get_plugin(cls, plugin_name):
        return cls.__plugins_manager.get_plugin(plugin_name)
    
    @classmethod
    def activate_plugin(cls, plugin_name):
        events_to_reg = cls.__plugins_manager.activate_plugin(plugin_name)
        for e in events_to_reg:
            cls.new_event(plugin_name, e[0], e[1])
    
    @classmethod
    def deactivate_plugin(cls, plugin_name):
        return cls.__plugins_manager.deactivate_plugin(plugin_name)
    
    @classmethod
    def install_plugin(cls, dir_or_file):
        return cls.__plugins_manager.install_plugin(dir_or_file)
    
    @classmethod
    def uninstall_plugin(cls, plugin_name):
        return cls.__plugins_manager.uninstall_plugin(plugin_name)
