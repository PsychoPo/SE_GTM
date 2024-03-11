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

		self.listWidget_tasks = ui.findChild(QtWidgets.QListWidget, "listWidget_tasks")

		self.action_add_task = ui.findChild(QtGui.QAction, "action_add_task")
		self.action_add_task.triggered.connect(self.open_create_task)

		self.action_list_achievements = ui.findChild(QtGui.QAction, "action_list_achievements")
		self.action_list_achievements.triggered.connect(self.open_list_achievements)

		self.action_show_statistics = ui.findChild(QtGui.QAction, "action_show_statistics")
		self.action_show_statistics.triggered.connect(self.open_statistics)

		self.action_change_theme = ui.findChild(QtGui.QAction, "action_change_theme")
		self.action_change_theme.triggered.connect(self.open_choose_theme)
	
	def open_create_task(self):
		'''Open the dialog creation task to add a new task'''

		#TODO ПЕРЕНОС ITEM !!!

		ui_create_task = getcwd() + "/ui/create_task.ui"
		loader = QtUiTools.QUiLoader()
		ui_create_task = QtCore.QFile(ui_create_task)
		ui_create_task.open(QtCore.QFile.ReadOnly)
		dialog_create_task = loader.load(ui_create_task)
		ui_create_task.close()

		textEdit_task_text = dialog_create_task.findChild(QtWidgets.QTextEdit, "textEdit_task_text")
		pushButton_create = dialog_create_task.findChild(QtWidgets.QPushButton, "pushButton_create")
		pushButton_cancel = dialog_create_task.findChild(QtWidgets.QPushButton, "pushButton_cancel")

		pushButton_create.clicked.connect(lambda: self.add_item_taskList(dialog_create_task, textEdit_task_text.toPlainText())) #self.add_item_taskList(dialog_create_task, "12312") #
		pushButton_cancel.clicked.connect(dialog_create_task.reject)

		dialog_create_task.exec()
	
	def add_item_taskList(self, dialog, task_text):
		if task_text == "":
			return
		else:
			item = QtWidgets.QListWidgetItem(task_text)
			item.setCheckState(QtCore.Qt.Unchecked)
			self.listWidget_tasks.addItem(item)
			dialog.reject()

	def open_list_achievements(self):
		'''Open the dialog list of achievements'''

		ui_list_achievements = getcwd() + "/ui/achievements.ui"
		loader = QtUiTools.QUiLoader()
		ui_list_achievements = QtCore.QFile(ui_list_achievements)
		ui_list_achievements.open(QtCore.QFile.ReadOnly)
		dialog_list_achievements = loader.load(ui_list_achievements)
		ui_list_achievements.close()

		dialog_list_achievements.exec()

	def open_statistics(self):
		'''Open the dialog of statistics'''

		ui_statistics = getcwd() + "/ui/statistics.ui"
		loader = QtUiTools.QUiLoader()
		ui_statistics = QtCore.QFile(ui_statistics)
		ui_statistics.open(QtCore.QFile.ReadOnly)
		dialog_statistics = loader.load(ui_statistics)
		ui_statistics.close()

		dialog_statistics.exec()

	def open_choose_theme(self):
		'''Open the dialog list of themes'''

		ui_choose_theme = getcwd() + "/ui/choose_theme.ui"
		loader = QtUiTools.QUiLoader()
		ui_choose_theme = QtCore.QFile(ui_choose_theme)
		ui_choose_theme.open(QtCore.QFile.ReadOnly)
		dialog_choose_theme = loader.load(ui_choose_theme)
		ui_choose_theme.close()

		dialog_choose_theme.exec()

def main():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()