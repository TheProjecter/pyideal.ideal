#!/usr/bin/python

import sys
from PyQt4.QtGui import QApplication

from ui.testwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mh = MainWindow()
    sys.exit(app.exec_())
