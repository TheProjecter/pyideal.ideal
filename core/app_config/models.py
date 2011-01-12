'''
Created on Dec 12, 2010

@author: EB020653
'''
from sqlobject import SQLObject, StringCol, BoolCol, ForeignKey, connectionForURI

#Por lo pronto solo guardariamos estos datos en la app.
#Sugerencias de mas data bienvenidas!.
#calculo que el UI extenderia este schema con info del 
# layout de la aplicacion, y demas yerbas...
#Tal vez algun plugin que necesite guardar info a nivel general.
#Tipo ubicacion de archivos del sistema para algunas herramientas,
# o tambien puede ser combinaciones de colores para el editor,
# etc.

class Path(SQLObject):
    name = StringCol()
    path = StringCol()

class PluginList(SQLObject):
    name = StringCol()
    isactive = BoolCol(default=False)
