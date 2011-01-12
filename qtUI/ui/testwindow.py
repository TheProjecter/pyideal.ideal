# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow, QPushButton
from PyQt4.QtCore import pyqtSignature, QString

from Ui_testwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.show()
	
	def add_plugin_ui (Widget):
		self.frameLayout.addWidget(Widget)
