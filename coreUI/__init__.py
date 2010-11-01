from exceptions import NotImplementedError
from UI import MainWindow


class coreUI(object):
	__window_app=MainWindow()
	
	@classmethod
	def add_plugin_ui (cls, widget):
		cls.__window_app.the_real_add_plugin_ui(widget)

	@classmethod
	def set_mainwindow(cls, mainwin):
		cls.__window_app = mainwin
