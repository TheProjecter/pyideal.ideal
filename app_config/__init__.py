from models import Path, connectionForURI

class app_config(object):
    _loaded = list()
    _not_loaded = list()
    __paths=None
    __app_cfg_db=None
    
    
    def __init__(self, appcfg_file):
        self.__paths=Path
        uri = "sqlite:/" + appcfg_file
        self.__app_cfg_db=connectionForURI(uri)
        self.__paths.setConnection(self.__app_cfg_db)
        self.__paths.createTable(ifNotExists=True)
    
    def get_plugin_list(self):
        return None
    
    def get_path(self, pathname):
        rs=self.__paths.selectBy(self.__paths.q.name == pathname)
        if rs.count()==0:
            return None
        return rs.getOne()['path']
    
    def add_new_path(self, pathname, path):
        new_path=Path(name=pathname, path=path)
        new_path.      
