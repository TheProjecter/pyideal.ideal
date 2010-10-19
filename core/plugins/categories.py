'''
Created on Oct 17, 2010

@author: EB020653
'''
from yapsy import IPlugin


class Generic(IPlugin):
    '''
    classdocs
    '''
    name="Generic Plugin"

    def __init__(self):
        '''
        Constructor
        '''
        pass


class TextManipulation(IPlugin):
    '''
    classdocs
    '''
    name="Text Manipulation"

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    
class FileManipulation(IPlugin):
    '''
    classdocs
    '''
    name="File Manipulation"

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
class ProyectManipulation(object):
    pass    