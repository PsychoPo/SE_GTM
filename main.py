from os import getcwd
from PySide6 import QtWidgets, QtUiTools, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
	'''MainWindow class'''
	def __init__(self):
		super().__init__()

		ui_file = getcwd() + "/ui/gtm_main.ui"
		loader = QtUiTools.QUiLoader()
		ui_file = QtCore.QFile(ui_file)
		ui_file.open(QtCore.QFile.ReadOnly)
		ui = loader.load(ui_file)
		ui_file.close()

		self.setCentralWidget(ui)

		self.action_add_task = ui.findChild(QtGui.QAction, "action_add_task")
		self.action_add_task.triggered.connect(self.open_create_task)

		self.action_list_achievements = ui.findChild(QtGui.QAction, "action_list_achievements")
		self.action_list_achievements.triggered.connect(self.open_list_achievements)

		self.action_show_statistics = ui.findChild(QtGui.QAction, "action_show_statistics")
		self.action_show_statistics.triggered.connect(self.open_statistics)
	
	def open_statistics(self):
		'''Open the dialog of statistics'''

		ui_statistics = getcwd() + "/ui/statistics.ui"
		loader = QtUiTools.QUiLoader()
		ui_statistics = QtCore.QFile(ui_statistics)
		ui_statistics.open(QtCore.QFile.ReadOnly)
		dialog_statistics = loader.load(ui_statistics)
		ui_statistics.close()

		dialog_statistics.exec()

	def open_list_achievements(self):
		'''Open the dialog of list achievements'''

		ui_list_achievements = getcwd() + "/ui/achievements.ui"
		loader = QtUiTools.QUiLoader()
		ui_list_achievements = QtCore.QFile(ui_list_achievements)
		ui_list_achievements.open(QtCore.QFile.ReadOnly)
		dialog_list_achievements = loader.load(ui_list_achievements)
		ui_list_achievements.close()

		dialog_list_achievements.exec()

	def open_create_task(self):
		'''Open the dialog create_task to create and add new task'''

		ui_create_task = getcwd() + "/ui/create_task.ui"
		loader = QtUiTools.QUiLoader()
		ui_create_task = QtCore.QFile(ui_create_task)
		ui_create_task.open(QtCore.QFile.ReadOnly)
		dialog_create_task = loader.load(ui_create_task)
		ui_create_task.close()

		dialog_create_task.exec()

def main():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()