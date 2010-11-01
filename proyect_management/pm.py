'''
Created on Oct 8, 2010
@author: EB020653
'''
import os
import mimetypes
from os import path
from version import VSYSNUMBER
from platform import system
from sqlobject import *
from models import *
from utils import *
from core import core

OUR_PRY_EXT = "ideal"
PMVERSION = "0.3"

CURRENT_FILE_OP = enum("idle", "opening", "closing", "saving", "reading")
        

class openedFile(object):
    __fdb = None
    __prj = None
    __contens = None
    __dirty = False
    __plugin_conf = None
    __events=None
    
    #For events status:
    __current_op = CURRENT_FILE_OP.IDLE
    
    def pre_save(self, *args, **kwargs):
        return core.fire_event(self.__plugin_conf.get_hash("pre_save"), *args, **kwargs )
    
    def post_save(self, *args, **kwargs):
        return core.fire_event(self.__plugin_conf.get_hash("post_save"), *args, **kwargs)
    
    def pre_open(self, *args, **kwargs):
        return core.fire_event(self.__plugin_conf.get_hash("pre_open"), *args, **kwargs )
    
    def post_open(self, *args, **kwargs):
        return core.fire_event(self.__plugin_conf.get_hash("pre_open"), *args, **kwargs )
    
    def pre_read(self, *args, **kwargs):
        return core.fire_event(self.__plugin_conf.get_hash("pre_read"), *args, **kwargs )
    
    def post_read(self, *args, **kwargs):
        return core.fire_event(self.__plugin_conf.get_hash("pre_read"), *args, **kwargs )
    
    
    def __init__(self, filedb, prj):
        self.__fdb = filedb
        self.__prj = prj
        self.__plugin_conf=core.get_plugin_config(PLUGIN_NAME)
        self.open()
    
    @property
    def hash(self):
        return self.__fdb.throughTo.metadata.hash
    
    @property    
    def name(self):
        return self.__fdb.name

    @property
    def full_filename(self):
        return path.join(self.__prj.get_base_path(), self.__fdb.relative_path, self.__fdb.name)
    
    @property
    def contens(self):
        if self.__contens is None:
            return ""
        return self.__contens
    
    @contens.setter
    def contens(self, value):
        self.__dirty = True
        self.__contens = value
        return True
    
    def need_a_save(self):
        return self.__dirty
    
    def open(self):
        if self.__current_op == CURRENT_FILE_OP.IDLE:
            self.__current_op = CURRENT_FILE_OP.OPENING
        self.pre_open()
        f = open(self.full_filename, "r")       
        self.__contens = f.read()
        f.close()
        self.__fdb.displayed = 1
        self.post_open()
        if self.__current_op == CURRENT_FILE_OP.OPENING:
            self.__current_op = CURRENT_FILE_OP.IDLE

    def read(self, start_at=None, to=None, skipCache=False):
        if self.__current_op == CURRENT_FILE_OP.IDLE:
            self.__current_op = CURRENT_FILE_OP.READING
        self.pre_read()
        if skipCache:            
            f = open(self.full_filename, "r")
            self.contens(f.read())
            f.close()
        if start_at == None:
                return self.contens()
        r_to = len(self.contens())
        if r_to > to:
            r_to = to
        if start_at < 0 or start_at > r_to:
            start_at = 0 
        self.post_read()
        if self.__current_op == CURRENT_FILE_OP.READING:
                self.__current_op = CURRENT_FILE_OP.IDLE   
        return self.contens()[start_at:to]
        
        
    def save(self, contens=None, overwrite=False, failIfMissing=False):
        if contens is None:
            if not self.__dirty:
                return False
        else:
            self.__contens = contens
        if self.__current_op == CURRENT_FILE_OP.IDLE:
            self.__current_op = CURRENT_FILE_OP.SAVING
        self.pre_save()
        the_file = self.full_filename 
        if failIfMissing:
            if os.path.isfile(the_file):
                raise IOError("No se encuentra el archivo especificado!")
        if not overwrite:
            current_file_hash = sha1(open(the_file, "r").read()).hexadigest()
            if self.__fdb.throughTo.hash != current_file_hash:
                raise ValueError("El archivo a sido modificado!")
        tf = open(the_file, "w")
        tf.write(self.__contens)
        tf.close()
        self.__fdb.troughTo.metadata.hash = hash_data(self.__contens)
        self.__dirty = False
        self.post_save()
        if self.__current_op == CURRENT_FILE_OP.SAVING:
            self.__current_op = CURRENT_FILE_OP.IDLE
        return True
    
    def close(self, saveIfChanged=True, ignoreChanges=True):
        if self.__current_op == CURRENT_FILE_OP.IDLE:
            self.__current_op = CURRENT_FILE_OP.CLOSING
        if self.__dirty:
            if saveIfChanged:
                self.save()
            if not ignoreChanges:
                return False
        self.__fdb.displayed = 0
        if self.__current_op == CURRENT_FILE_OP.CLOSING:
            self.__current_op = CURRENT_FILE_OP.IDLE
        
    def __eq__(self, theOther):
        return self.hash == theOther.hash
        

class Proyect(object):
    __files = None
    __dirs = None
    __opened_files = list()
    __cfg = None
    __cnx = None
    __prj = None
    
    def __init__(self, cnx, prj):
        self.__cnx = cnx
        self.__prj = prj
        self.__files = FileData
        self.__files.setConnection(cnx)        
        self.__dirs = DirectoryData
        self.__dirs.setConnection(cnx)
        
       
    def __get_opened_filenames(self):
        all_opened = self.__files.selectBy(display=1)
        base_path = self.get_base_path()
        list_files = list()
        for opened_file in all_opened:
            list_files.append(os.path.join(base_path, opened_file.relative_path.name, opened_file.name))
        return list_files
        
    def get_base_path(self):
        #return self.__base_path("base_path", self.__assd<adsa)
        return self.__prj.get(1).base_path
    
    def __addDir(self, pathname):
        (the_path, lastpath) = os.path.split(pathname)
        assert the_path != ""
        assert lastpath != ""
        common_path = path.commonprefix([self.get_base_path(), the_path])
        relative_path = the_path.replace(common_path, "")
        return DirectoryData(name=lastpath, relative_path=relative_path)
        
    def __addFile(self, filename):
        print filename
        (the_path, file) = path.split(filename)
        assert file != ""
        assert the_path != ""
        common_path = path.commonprefix([self.get_base_path(), the_path])
        full_relative_path=the_path.replace(common_path, "")
        (start_path, relative_path) = os.path.split(full_relative_path)
        return FileData(name=file, relative_path=self.__dirs.selectBy("""name={0}""".format(relative_path)), metadata=None) 
    
    def _setOpen(self, file, hash):
        #self.__app_cfg.set("OpenFiles", file, hash)
        fdb = self.__files.selectBy(name=file)
        fdb.displayed = True
        fdb.throughTo.metadata.hash = hash
        return fdb
    
    def addDirectory(self, dirname, recursive=True):
        dirname = path.normpath(dirname)
        assert path.exists(dirname)
        fullfilelist = list()
        fullfilelist.append(dirname)
        filelist = os.listdir(dirname)
        for item in filelist:
            if path.isfile(item):
                fullfilelist.append(item)
                self.__addFile(item)
            elif path.isdir(item):
                fullfilelist.append(item)
                self.__addDir(item)
                if recursive:
                    filelist.append(os.listdir(path.join(dirname, item)))
 
    def AddFile(self, filename, relative_path=None, openIt=False):
        if relative_path is None:
            the_filename = path.normpath(path.join(self.get_base_path(), path.relpath(filename, self.get_base_path())))
        else:
            the_filename = path.normpath(path.join(self.get_base_path(), path.relpath(self.get_base_path(), relative_path), filename))     
        assert os.path.isfile(the_filename)
        fdb = self.__addFile(the_filename)
        guessedtype = mimetypes.guess_type(the_filename)
        mimetype = ""
        for i in guessedtype:
            if not (i is None):
                if mimetype != "":
                    mimetype += "-"
                mimetype += i
        if fdb.metadata is None:
            fdb.metadata = FileMetaData(mimetype=mimetype, hash=get_hash_for(the_filename))
        else:
            fdb.metadata.mimetype = mimetype
            fdb.hash = get_hash_for(the_filename)
        if openIt:
            fo = self.openFile(fdb.name, fdb.relative_path)
            return fo
        return True
    
    def listDirectory(self, directory):
        dirs = self.__dirs.select("""directorydata.name = {0} or directorydata.relative_path like '{0}%'""".format(directory))
        files = self.__files.select("""filedata.directory=directorydata.id and directorydata.name={0}""".format(directory), clauseTables=['DirectoryData'])
        results = list()
        for d in  dirs.orderBy("name"):
            results.append(d.name + '/')
        for f in files.orderBy("filedata.name"):
            results.append(f.name)
        return results
        
    def openFile(self, file, path=None):
        if path is None:
            files = self.__files.select("""name={0] and relative_path={1}""".format(file, path))
        else:
            files = self.__files.select("""name={0}""".format(file))
        if files.count() > 1:
            raise KeyError("Debe indicar la ruta!!")
        if files.count() == 0:
            raise KeyError("El archivo no existe en el proyecto!!")     
        afile = files.getOne(None)
        if afile is None:
            raise ValueError("Crap!")
        the_file = path.join(self.get_base_path(), afile["relative_path"], afile["name"])
        if not os.path.isfile(the_file):
            raise IOError ("File not Exist!")
        fo = openedFile(afile, self)
        self.__opened_files.append(fo)
        return fo
    
    def newFile(self, filename):
        open(filename, "w").close()
        tf = self.AddFile(filename, openIt=True)
        return tf

    def saveAll(self, overwrite=False, failIfMissing=False):
        for of in self.__opened_files:
            of.save(overwrite, failIfMissing)
    
    def closeAll(self, saveIfChanged=True, ignoreChanges=True):
        for of in self.__opened_files:
            of.close(saveIfChanged, ignoreChanges) 
        



class ProyectManager(object):
    __app_cfg = None
    
    
    def __init__(self, app_cfg):
        self.__app_cfg = app_cfg
    
    def __file_check(self, filename, create=False, overwrite=False):
        filename = path.normpath(path.abspath(filename))
        if path.isfile(filename):
            if overwrite:
                open(filename, "wb").close()
        else:
            if create:
                open(filename, "wb").close()
            else:
                return None
        if system().lower() == "windows":
            filename = filename.replace(':', '|')
        return filename

    
    def __upgrade_version (self, cfg):
        return False #Se usa para upgradear el formato de archivo.
    
    def newProyect(self, name, basepath, overwrite=False):
        the_path = path.abspath(basepath)
        filename = path.join(the_path, name + path.extsep + OUR_PRY_EXT)
        proyect_file = self.__file_check(filename, create=True, overwrite=overwrite)
        if proyect_file is None:
            raise IOError("No se pudo crear el archivo! - " + filename)
        uri = "sqlite:/" + str(proyect_file)
        prjdb = connectionForURI(uri)
        ProyectData.setConnection(prjdb)
        ProyectData.createTable()
        DirectoryData.setConnection(prjdb)
        DirectoryData.createTable()
        FileMetaData.setConnection(prjdb)
        FileMetaData.createTable()
        FileData.setConnection(prjdb)
        FileData.createTable()
        prj_info = ProyectData(name=name, base_path=the_path, version=PMVERSION)
        return Proyect(prjdb, prj_info)
        
    
    def openProyect(self, filename, path=None):
        if path is None:
            the_path = path.abspath(filename)
        else:
            the_path = path.normpath(path.abspath(path.join(path, filename)))
        proyect_file = self.__file_check(the_path, create=False, overwrite=False)
        if proyect_file is None:
            raise IOError("No se pudo encontrar el archivo! - " + filename)
        uri = "sqlite:/" + str(proyect_file)
        prjdb = connectionForURI(uri)
        ProyectData.setConnection(prjdb)
        DirectoryData.setConnection(prjdb)
        FileMetaData.setConnection(prjdb)
        FileData.setConnection(prjdb)
        prj_info = ProyectData.select().getOne()
        return Proyect(prjdb, prj_info)
        



