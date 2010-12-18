'''
Created on Dec 12, 2010

@author: EB020653
'''
from sqlobject import SQLObject, StringCol, BoolCol, ForeignKey, connectionForURI


class Path(SQLObject):
    name = StringCol()
    path = StringCol()

class PluginList(SQLObject):
    name = StringCol()
    isactive = BoolCol(default=False)