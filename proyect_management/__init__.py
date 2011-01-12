from config import PLUGIN_NAME
try:
    from pm import openedFile, ProyectManager, Proyect
except:
    raise ImportError("Ups!, something is not good with this plugin!(" + PLUGIN_NAME + ")")

"""
try:
    Core.activate_plugin(PLUGIN_NAME)
except:
    raise Exception ("Bullshit!")
"""



