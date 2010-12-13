

EXTRA_CONFIG = (
{"name": "BaseMetaData", "filename":"basemetadata.py"},
)

    
class startup_config(object):
    _loaded = list()
    _not_loaded = list()
    extra_sql = list()
    
    def __init__(self):
        for configmod in EXTRA_CONFIG:
            try:
                tempmod = __import__(configmod["filename"])
                self._loaded.append(configmod)
                self.extra_sql.append(tempmod.PROYECT_STARTUP_EXTRA_SQL)
            except ImportError:
                self._not_loaded.append(configmod)
            
