'''
Created on Oct 19, 2010

@author: EB020653
'''
from models import Paths, Plugins
from os.path import isfile, abspath, normpath
from sqlobject import connectionForURI

class AppConfig(object):
    '''
    Application Config
    '''
    __plugins=None
    __paths=None

    def __init__(self, app_config_file):
        '''
        Constructor
        '''
        if app_config_file is None:
            raise IOError ("First run?") #TODO: Crear archivo y cargar datos iniciales.
        app_config_file=abspath(normpath(app_config_file))
        if not isfile(app_config_file):
            raise IOError("No se encuentra el archivo especificado!")
        
        uri = "sqlite:/" + str(app_config_file)
        appdb = connectionForURI(uri)
        self.__plugins = Plugins
        self.__plugins.setConnection(appdb)
        self.__paths = Paths
        self.__paths.setConnection(appdb)
    
    #Generar metodos para interactuar con las opciones de configuracion...
    
    
    
    