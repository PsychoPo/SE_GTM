from os import getcwd
from PySide6 import QtWidgets, QtUiTools, QtCore, QtGui
from datetime import datetime
import res.res_rc

class TimeQuest(QtWidgets.QMainWindow):
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

		self.action_change_theme = ui.findChild(QtGui.QAction, "action_change_theme")
		self.action_change_theme.triggered.connect(self.open_choose_theme)

		self.label_datetime = ui.findChild(QtWidgets.QLabel, "label_datetime")
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(lambda: self.label_datetime.setText(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
		self.timer.start(1000)
		self.label_datetime.setText(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

		self.label_timecoins = ui.findChild(QtWidgets.QLabel, "label_timecoins")
		
		self.listWidget_tasks = ui.findChild(QtWidgets.QListWidget, "listWidget_tasks")
		self.listWidget_tasks.itemChanged.connect(self.update_progress_bar)
		
		self.progressBar_done_tasks = ui.findChild(QtWidgets.QProgressBar, "progressBar_done_tasks")
		self.update_progress_bar()

	def update_progress_bar(self):
		'''Filling up the progress bar'''
		checked_count = 0
		for i in range(self.listWidget_tasks.count()):
			item = self.listWidget_tasks.item(i)
			if item.checkState() == QtCore.Qt.Checked:
				checked_count += 1
		
		max_value = self.listWidget_tasks.count()
		self.progressBar_done_tasks.setMaximum(max_value)
		self.progressBar_done_tasks.setValue(checked_count)

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
		pushButton_create.clicked.connect(lambda: self.add_item_taskList(dialog_create_task, textEdit_task_text.toPlainText()))

		pushButton_cancel = dialog_create_task.findChild(QtWidgets.QPushButton, "pushButton_cancel")
		pushButton_cancel.clicked.connect(dialog_create_task.reject)

		dialog_create_task.exec()
	
	def add_item_taskList(self, dialog, task_text):
		'''Add new task to listWidget and close the dialog'''
		if task_text == "":
			return
		else:
			item = QtWidgets.QListWidgetItem(task_text)
			item.setCheckState(QtCore.Qt.Unchecked)
			self.listWidget_tasks.addItem(item)
			dialog.reject()
			self.update_progress_bar()

	def open_list_achievements(self):
		'''Open the dialog list of achievements'''

		ui_list_achievements = getcwd() + "/ui/achievements.ui"
		loader = QtUiTools.QUiLoader()
		ui_list_achievements = QtCore.QFile(ui_list_achievements)
		ui_list_achievements.open(QtCore.QFile.ReadOnly)
		dialog_list_achievements = loader.load(ui_list_achievements)
		ui_list_achievements.close()

		pushButton_back = dialog_list_achievements.findChild(QtWidgets.QPushButton, "pushButton_back")
		pushButton_back.clicked.connect(dialog_list_achievements.reject)

		dialog_list_achievements.exec()

	def open_statistics(self):
		'''Open the dialog of statistics'''

		ui_statistics = getcwd() + "/ui/statistics.ui"
		loader = QtUiTools.QUiLoader()
		ui_statistics = QtCore.QFile(ui_statistics)
		ui_statistics.open(QtCore.QFile.ReadOnly)
		dialog_statistics = loader.load(ui_statistics)
		ui_statistics.close()

		pushButton_back = dialog_statistics.findChild(QtWidgets.QPushButton, "pushButton_back")
		pushButton_back.clicked.connect(dialog_statistics.reject)

		dialog_statistics.exec()

	def open_choose_theme(self):
		'''Open the dialog list of themes'''

		ui_choose_theme = getcwd() + "/ui/choose_theme.ui"
		loader = QtUiTools.QUiLoader()
		ui_choose_theme = QtCore.QFile(ui_choose_theme)
		ui_choose_theme.open(QtCore.QFile.ReadOnly)
		dialog_choose_theme = loader.load(ui_choose_theme)
		ui_choose_theme.close()

		pushButton_back = dialog_choose_theme.findChild(QtWidgets.QPushButton, "pushButton_back")
		pushButton_back.clicked.connect(dialog_choose_theme.reject)

		dialog_choose_theme.exec()

def main():
    app = QtWidgets.QApplication([])
    window = TimeQuest()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()