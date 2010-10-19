'''
Created on Oct 19, 2010

@author: EB020653
'''
from sqlobject import SQLObject, StringCol, ForeignKey, BoolCol

#Por lo pronto solo guardariamos estos datos en la app.
#Sugerencias de mas data bienvenidas!.
#calculo que el UI extenderia este schema con info del 
# layout de la aplicacion, y demas yerbas...
#Tal vez algun plugin que necesite guardar info a nivel general.
#Tipo ubicacion de archivos del sistema para algunas herramientas,
# o tambien puede ser combinaciones de colores para el editor,
# etc.

class Paths(SQLObject):
    path = StringCol()
    description = StringCol()


class Plugins(SQLObject):
    name = StringCol()
    install_path = ForeignKey("Paths")
    active = BoolCol(default=False)


        