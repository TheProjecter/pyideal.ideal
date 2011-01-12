'''
Created on Oct 17, 2010

@author: EB020653
'''
#from yapsy import PluginManager
import os
import zipfile
import gzip
import bz2
import tempfile
import md5
from os import path
from shutil import copytree
from utils import is_zipfile, is_bz2file, is_gzipfile, is_tarfile
from tarfile import TarFile, CompressionError
import knee



class PluginManager(object):
    __app_config = None
    __plugin_mod = None
    
    def __init__(self, app_config):
        self.__app_config = app_config
        self.__plugin_mod = dict()
    
    def get_plugins_path(self):
        return self.__app_config.get_path('plugins_install')
    
    def get_active_names(self):
        return self.__app_config.get_active_plugins()
    
    def get_all_names(self):
        return self.__app_config.get_plugin_list()
        
    # here?
    def reconfigure(self, app_config): 
        self.__app_config = app_config

    def __handle_file(self, plugin_file):
        # Uncompress the file.
        temp_dir = tempfile.gettempdir()
        if is_zipfile(plugin_file):
            compress_fd = zipfile.ZipFile(plugin_file, allowZip64=True)
            compress_fd.extractall(path=temp_dir)
        elif is_bz2file(plugin_file):
            #first check if we can handle as tar.bz2 (big chances)
            try:
                compress_fd = TarFile(name=plugin_file, mode="r:bz2")
                compress_fd.extractall(path=temp_dir)
            except CompressionError:
                print "Upz!, fail in compressed file handling, Retrying"
                try:
                    compress_fd = bz2.BZ2File(plugin_file)
                    tmp_fd = tempfile.TemporaryFile(suffix=".tar", prefix="ncmprs")
                    tmp_fd.file.write(compress_fd.read())
                    tmp_fd.file.flush()
                    tar_fd = TarFile.taropen(name=None, fileobj=tmp_fd)
                    tar_fd.extractall(path=temp_dir)
                    tar_fd.close()
                    tmp_fd.close()
                except:
                    print "Upz!, fail in compressed file handling, Again! :("
                    return None
        elif is_gzipfile(plugin_file):
            #first check if we can handle as tar.gz (big chances)
            try:
                compress_fd = TarFile(name=plugin_file, mode="r:gz")
                compress_fd.extractall(path=temp_dir)
            except CompressionError:
                print "Upz!, fail in compressed file handling, Retrying"
                try:
                    compress_fd = gzip.GzipFile(plugin_file)
                    tmp_fd = tempfile.TemporaryFile(suffix=".tar", prefix="ncmprs")
                    tmp_fd.file.write(compress_fd.read())
                    tmp_fd.file.flush()
                    tar_fd = TarFile.taropen(name=None, fileobj=tmp_fd)
                    tar_fd.extractall(path=temp_dir)
                    tar_fd.close()
                    tmp_fd.close()
                except:
                    print "Upz!, fail in compressed file handling, Again! :("
                    return None
        return self.__handle_dir(temp_dir)
    
    def __handle_dir(self, plugin_dir):
        #try:
        print "CopyTree: {0} -> {1}".format(plugin_dir, self.get_plugins_path())
        import sys
        sys.stdout.flush()
        (base_path, plg_dest) = os.path.split(os.path.normpath(plugin_dir))
        print "bp:", base_path
        base_path = os.path.normpath(base_path)
        print "pd:", plg_dest
        plg_dest = os.path.normpath(plg_dest)
        print "CopyTree: {0} -> {1}".format(plugin_dir, os.path.join(self.get_plugins_path(), plg_dest))
        copytree(plugin_dir, os.path.join(self.get_plugins_path(), plg_dest))
        #except:
        #    return None
        
        return os.path.join(self.get_plugins_path(), plg_dest)
    
    def install_plugin(self, plugin_file_or_dir, enable=False):
        '''
            Installs the plugin, needs a zip file, or a directory.
            Enable if the plugins installs ok.
        '''
        if path.isfile(plugin_file_or_dir):
            print "IsFile!"
            module_path = self.__handle_file(plugin_file_or_dir)
        elif path.isdir(plugin_file_or_dir):
            print "IsDir!"
            module_path = self.__handle_dir(plugin_file_or_dir)
        else:
            raise TypeError("Needs to be a compressed file or a directory!")
        print "module_path:{0}".format(module_path)
        module_path = os.path.join(module_path, '__init__.py')
        try:
            module_dir = os.path.dirname(module_path)
            module_file = os.path.basename(module_path)
            base_import = os.path.basename(module_dir)
            mod = __import__(base_import+".config", globals(), locals(), [module_dir])
        except ImportError, x:
            print ("Upz!, ImportError!")
            raise
        except:
            print ("Upz!, Error importing module but not an ImportError?!")
            raise
        
        self.__plugin_mod.update({ mod.PLUGIN_NAME : None , 'active' : False})
        if enable:
            self.activate_plugin(mod.PLUGIN_NAME)
        self.__app_config.add_new_plugin(mod.PLUGIN_NAME)
        
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
        #self.__register_plugin_events(plugin_name)
        #TODO: More Things...
        plugin=__import__(plugin_name, globals(), locals(), [])
        self.__plugin_mod.update({plugin_name : plugin, 'active' : True })
        #self.__register_plugin_events(plugin_name)
        #If all is fine, so:
        self.__app_config.set_plugin_as_active(plugin_name)
        return plugin.config.SetupPlugin()
    
    def deactivate_plugin(self, plugin_name):
        '''
            Deactivate (unload) the plugin
        '''
        #TODO: Things...
        
        #self.__unregister_plugin_events(plugin_name)
        #TODO: More Things...
        plugin=self.__plugin_mod.pop(plugin_name)
        del plugin
        #If all is fine so:
        self.__app_config.set_plugin_as_inactive(plugin_name)
        
    
    def check_plugins(self):
        '''
            Check the plugins instalation. Only on app start.
        '''
        #TODO; Check current active plugins integrity!.
        print ("TODO: So, actually: It's all ok!")
        return True
    
    def get_plugin(self, plugin_name):
        if plugin_name not in self.__plugin_mod.keys():
            return None
        return self.__plugin_mod[plugin_name]
    
    """
    def __register_plugin_events(self, plugin_name):
        '''
            Register the plugins events on core!.
        '''
        #TODO: Registrar eventos del plugin determinado.
        #asd=__import__(plugin_name, fromlist=['', ''])
        plugin = self.__plugin_mod[plugin_name]
        plugin_setup=plugin.config.SetupPlugin()
        events=plugin_setup.get_events()
        for e in events:
            
        
        
    def __unregister_plugin_events(self, plugin_name):
        '''
            Register the plugins events on core!.
        '''
        #TODO: Desregistrar eventos del plugin determinado.
        #asd=__import__(plugin_name, fromlist=['', ''])
        plugin = self.__plugin_mod[plugin_name]
    """
