from models import Path, PluginList, connectionForURI


class app_config(object):
    __loaded = list()
    __not_loaded = list()
    __paths=None
    __pluginlist=None
    __app_cfg_db=None
    
    
    def __init__(self, appcfg_file):
        self.__paths=Path
        self.__pluginlist=PluginList
        uri = "sqlite:/" + appcfg_file
        self.__app_cfg_db=connectionForURI(uri)
        self.__paths.setConnection(self.__app_cfg_db)
        self.__paths.createTable(ifNotExists=True)
        self.__pluginlist.setConnection(self.__app_cfg_db)
        self.__pluginlist.createTable(ifNotExists=True)
        
    def set_defaults(self):
        self.add_new_path("plugins", "./plugins")
    
    def get_active_plugins(self):
        rs=self.__pluginlist.selectBy(self.__pluginlist.q.isactive==True)
        if rs.count()==0:
            return []
        return [r['name'] for r in rs]
    
    def set_plugin_as_active(self, name):
        rs=self.__pluginlist.selectBy(self.__pluginlist.q.name==name)
        if rs.count()==0:
            return False
        rs[0].isactive=True
        return True
    
    def set_plugin_as_inactive(self, name):
        rs=self.__pluginlist.selectBy(self.__pluginlist.q.name==name)
        if rs.count()==0:
            return False
        rs[0].isactive=False
        return True
        
    def add_new_plugin(self, name, isactive=False):
        PluginList(name=name, isactive=isactive)
    
    def get_path(self, pathname):
        rs=self.__paths.selectBy(self.__paths.q.name == pathname)
        if rs.count()==0:
            return None
        return rs.getOne()['path']
    
    def add_new_path(self, pathname, path):
        try:
            new_path=Path(name=pathname, path=path)
        except:
            return False
        return True      
