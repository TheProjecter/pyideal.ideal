'''
Created on Oct 17, 2010

@author: EB020653
'''
#from yapsy import PluginManager
 
from os.path import isdir, isfile
from os import listdir
from shutil import copytree
import tempfile
from utils import is_zipfile, is_bz2file, is_gzipfile, is_tarfile
import zipfile
import gzip
import bz2
from tarfile import TarFile, CompressionError


class PluginManager(object):
    __app_config=None
    __plugin_list=None
    __plugin_path=None
    
    def __init__(self, app_config):
        self.__app_config = app_config
        self.__plugin_list = app_config.get_plugin_list()
        self.__plugin_path = app_config.get_path("plugin_path")
        pass
    
    # here?
    def reconfigure(self, app_config): 
        self.__app_config = app_config
    
    def __handle_file(self, plugin_file):
        # Uncompress the file.
        temp_dir=tempfile.gettempdir()
        if is_zipfile(plugin_file):
            compress_fd=zipfile.ZipFile(plugin_file, allowZip64=True)
            compress_fd.extractall(path=temp_dir)
        elif is_bz2file(plugin_file):
            #first check if we can handle as tar.bz2 (big chances)
            try:
                compress_fd=TarFile(name=plugin_file, mode="r:bz2")
                compress_fd.extractall(path=temp_dir)
            except CompressionError:
                print "Upz!, fail in compressed file handling, Retrying"
                try:
                    compress_fd=bz2.BZ2File(plugin_file)
                    tmp_fd=tempfile.TemporaryFile(suffix=".tar", prefix="ncmprs")
                    tmp_fd.file.write(compress_fd.read())
                    tmp_fd.file.flush()
                    tar_fd=TarFile.taropen(name=None, fileobj=tmp_fd)
                    tar_fd.extractall(path=temp_dir)
                    tar_fd.close()
                    tmp_fd.close()
                except:
                    print "Upz!, fail in compressed file handling, Again! :("
                    return None
        elif is_gzipfile(plugin_file):
            #first check if we can handle as tar.gz (big chances)
            try:
                compress_fd=TarFile(name=plugin_file, mode="r:gz")
                compress_fd.extractall(path=temp_dir)
            except CompressionError:
                print "Upz!, fail in compressed file handling, Retrying"
                try:
                    compress_fd=gzip.GzipFile(plugin_file)
                    tmp_fd=tempfile.TemporaryFile(suffix=".tar", prefix="ncmprs")
                    tmp_fd.file.write(compress_fd.read())
                    tmp_fd.file.flush()
                    tar_fd=TarFile.taropen(name=None, fileobj=tmp_fd)
                    tar_fd.extractall(path=temp_dir)
                    tar_fd.close()
                    tmp_fd.close()
                except:
                    print "Upz!, fail in compressed file handling, Again! :("
                    return None
        return self.__handle_dir(temp_dir)
    
    def __handle_dir(self, plugin_dir):
        try:
            copytree(plugin_dir, self.__plugin_path)
        except:
            return False
        return True
    
    def install_plugin(self, plugin_file_or_dir, enable=False):
        '''
            Installs the plugin, needs a zip file, or a directory.
            Enable if the plugins installs ok.
        '''
        if isfile(plugin_file_or_dir):
            plugin_name=self.__handle_file(plugin_file_or_dir)
        elif isdir(plugin_file_or_dir):
            plugin_name=self.__handle_dir(plugin_file_or_dir)
        else:
            raise TypeError("Needs to be a compressed file or a directory!")
        self.__app_config.add_new_plugin(plugin_name, enable)
        
    def uninstall_plugin(self, plugin_name):
        '''
            Uninstalls the plugin. Kill all the files! :P
        '''
        self.deactivate_plugin(plugin_name)
        #TODO: mover todo a la ruta que corresponda
        print("Delete all the files!")
    
    def activate_plugin(self, plugin_name):
        '''
            Activate (load) the plugin
        '''
        #TODO: Things...
        self.__register_plugin_events(plugin_name)
        #TODO: More Things...
        #If all is fine, so:
        self.__app_config.set_plugin_as_active(plugin_name)
    
    def deactivate_plugin(self, plugin_name):
        '''
            Deactivate (unload) the plugin
        '''
        #TODO: Things...
        self.__unregister_plugin_events(plugin_name)
        #TODO: More Things...
        #If all is fine so:
        self.__app_config.set_plugin_as_inactive(plugin_name)
    
    def check_plugins(self):
        '''
            Check the plugins instalation. Only on app start.
        '''
        #TODO; Check current active plugins integrity!.
        print ("TODO: So, actually: It's all ok!")
        return True
    
    def __register_plugin_events(self, plugin_name):
        '''
            Register the plugins events on core!.
        '''
        #TODO: Registrar eventos del plugin determinado.
        #asd=__import__(plugin_name, fromlist=['', ''])
        plugin = self.__plugin_list[plugin_name]
        __import__(plugin)
        
    def __unregister_plugin_events(self, plugin_name):
        '''
            Register the plugins events on core!.
        '''
        #TODO: Desregistrar eventos del plugin determinado.
        #asd=__import__(plugin_name, fromlist=['', ''])
        mod = self.__plugin_list[plugin_name]

