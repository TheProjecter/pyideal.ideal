'''
Created on Dec 17, 2010

@author: eb020653
'''
import mimetypes
import zipfile
import zlib
import gzip
import bz2
import tarfile
    

def is_zipfile(filename):
    return zipfile.is_zipfile(filename)

def is_gzipfile(filename):
    gz = gzip.GzipFile(filename)
    try:
        gz.read(1)
        gz.close()
    except:
        gz.close()
        return False
    return True

def is_bz2file(filename):
    bz = bz2.BZ2File(filename)
    try:
        bz.read(1)
        bz.close()
    except:
        bz.close()
        return False
    return True

def is_tarfile(filename):
    return tarfile.is_tarfile(filename)
        
