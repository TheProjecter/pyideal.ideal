from config import PLUGIN_NAME, SetupPlugin
from core import core
try:
    from pm import openedFile, ProyectManager, Proyect
except:
    raise ImportError("Ups!, something is not good with this plugin!("+PLUGIN_NAME+")")

try:
    core.activate_plugin(PLUGIN_NAME)
except:
    raise Exception ("Bullshit!")