from models import Path, PluginList
from sqlobject import connectionForURI
from os import path
from sys import platform
#from util import bootstrap_config



class app_config(object):
    __loaded = list()
    __not_loaded = list()
    __paths = None
    __pluginlist = None
    __app_cfg_db = None
    __base_path = None
    
    
    def __init__(self, appcfg_file):
        self.__paths = Path
        self.__pluginlist = PluginList
        #REVIEW: Is this the best way to tackle this?:
        # http://sqlobject.org/SQLObject.html#declaring-a-connection
        if platform == "win32":
            appcfg_file = appcfg_file.replace("\\", "/")
            appcfg_file = appcfg_file.replace(r"\\", r"/")
            (drive, filepath) = path.splitdrive(appcfg_file)
            uri = "sqlite:/"
            if drive == '':
                appcfg_file = path.abspath(filepath)
                if path.isfile(appcfg_file):
                    (drive, filepath) = path.splitdrive(appcfg_file)
            if ":" in drive:
                uri = uri + "".join([drive.replace(":", "|"), filepath])
            else:
                uri = uri + appcfg_file
        else:
            uri = uri + appcfg_file
        print uri
        self.__app_cfg_db = connectionForURI(uri)
        self.__paths.setConnection(self.__app_cfg_db)
        self.__paths.createTable(ifNotExists=True)
        self.__pluginlist.setConnection(self.__app_cfg_db)
        self.__pluginlist.createTable(ifNotExists=True)
        
    def get_active_plugins(self):
        rs = self.__pluginlist.selectBy(self.__pluginlist.isactive == True)
        if rs.count() == 0:
            return []
        return [r.name for r in rs]
    
    def set_plugin_as_active(self, name):
        rs = self.__pluginlist.selectBy(self.__pluginlist.name == name)
        if rs.count() == 0:
            return False
        rs[0].isactive = True
        return True
    
    def set_plugin_as_inactive(self, name):
        rs = self.__pluginlist.selectBy(self.__pluginlist.name == name)
        if rs.count() == 0:
            return False
        rs[0].isactive = False
        return True
    
    def get_plugin_list(self):
        rs = self.__pluginlist.select()
        if rs.count() == 0:
            return []
        return [r.name for r in rs]
        
    def add_new_plugin(self, name, isactive=False):
        PluginList(name=name, isactive=isactive)
    
    def get_path(self, pathname):  
        rs = self.__paths.select(clause="name == '{0}'".format(pathname))
        if rs.count() == 0:
            return None
        result_path = rs.getOne().path
        result_path = result_path.strip()
        if pathname == 'base_dir':
            return path.normpath(result_path)
        if self.__base_path is None and pathname != 'base_dir':
            self.__base_path = self.get_path('base_dir')
            if self.__base_path is None:
                self.__base_path = ''  
        return path.normpath(path.join(self.__base_path, result_path))
    
    def get_all_paths(self):    
        rs = self.__paths.select()
        return list(rs.lazyIter())
    
    def add_new_path(self, pathname, the_path):
        try:
            Path(name=pathname, path=the_path)
        except:
            return False
        return True      
