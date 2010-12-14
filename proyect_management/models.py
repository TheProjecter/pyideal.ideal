'''
Created on Oct 6, 2010

@author: EB020653
'''
from sqlobject import SQLObject, StringCol, BoolCol, ForeignKey

class FileMetaData(SQLObject):
    mimetype = StringCol()
    hash = StringCol()

     
class FileData(SQLObject):
    name = StringCol()
    relative_path = ForeignKey("DirectoryData")
    displayed = BoolCol(default=False)
    metadata = ForeignKey("FileMetaData")


class DirectoryData(SQLObject):
    name = StringCol()
    relative_path = StringCol()
 
   
class ProyectData(SQLObject):
    name = StringCol()
    base_path = StringCol()
    version = StringCol()
    #files = ForeignKey("FileData")
    #directories = ForeignKey("DirectoryData")

