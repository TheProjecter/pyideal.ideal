'''
Created on Oct 12, 2010

@author: EB020653
'''
import unittest
import os
import tempfile
from proyect_management import *


class Test_Proyect_Management(unittest.TestCase):
    prjm = None
    prj = None
    existingFile = None
    prj_path = None
    prj_file = None
    test_string = "#--Contenido de prueba del test--#"

    def setUp(self):
        self.prj_path = tempfile.mkdtemp(suffix="test", prefix="prj", dir=tempfile.gettempdir())
        existingFile = tempfile.TemporaryFile(mode="w+t", suffix="nf", prefix="prj", dir=self.prj_path)
        existingFile.file.write(self.test_string)
        prj_file = tempfile.TemporaryFile(mode="w+t", suffix="pf", prefix="prj", dir=self.prj_path)
        prj_file.file.flush()
        
    def tearDown(self):
        fl = os.listdir(self.prj_path)
        dl = list()
        for tf in fl:
            fs = os.path.abspath(tf)
            if os.path.isfile(fs):
                os.remove(fs)
            else:
                dl.append(fs)
                flist = os.listdir(fs)
                for nf in flist:
                    fl.append(os.path.join(fs, nf))
        for td in dl:
            if len(os.listdir(td)) == 0:
                os.rmdir(td)
        if len(dl) != 0:
            print 'No se borro todo :('

    def test_ProyectManager(self):
        self.assertEqual(self.prjm, None)
        self.prjm = ProyectManager(None)
        self.assertTrue(isinstance(self.prjm, ProyectManager))
        self.prj = self.prjm.newProyect("testprj", self.prj_path)
        self.assertTrue(isinstance(self.prj, Proyect))
        self.assertTrue(os.path.isfile(os.path.join(self.prj_path, "testprj.ideal")))
    
    def test_Proyect(self):
        pass
    
    def test_openedFile(self):    
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
