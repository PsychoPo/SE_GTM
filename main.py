from os import getcwd, execl
from sys import executable, argv
from PySide6 import QtWidgets, QtUiTools, QtCore, QtGui
from datetime import datetime
import res.res_rc
from sqlite3 import connect, Cursor

# TODO выбор темы и ее смена

class TimeQuest(QtWidgets.QMainWindow):
	'''MainWindow class'''
	def __init__(self):
		super().__init__()

		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()
		cursor.execute("UPDATE statistics SET logons = logons + 1")

		cursor.execute("SELECT * FROM statistics")
		row = cursor.fetchone()
		if row[0] >= 50:
			cursor.execute("UPDATE achievements SET done = 1 WHERE id = 7")
			cursor.execute("UPDATE themes SET available = 1 WHERE id = 5")
		if row[0] >= 100:
			cursor.execute("UPDATE achievements SET done = 1 WHERE id = 8 ")
			cursor.execute("UPDATE themes SET available = 1 WHERE id = 6")
		if row[0] >= 150:
			cursor.execute("UPDATE achievements SET done = 1 WHERE id = 9 ")
			cursor.execute("UPDATE themes SET available = 1 WHERE id = 7")

		cursor.execute("SELECT path FROM themes WHERE used = 1")
		self.path_theme = cursor.fetchone()

		conn.commit()
		conn.close()

		self.path_create_task = getcwd() + self.path_theme[0] + "create_task.ui"
		self.path_list_achievements = getcwd() + self.path_theme[0] + "achievements.ui"
		self.path_statistics = getcwd() + self.path_theme[0] + "statistics.ui"
		self.path_accept_restart_statistics = getcwd() + self.path_theme[0] + "accept_restart_statistics.ui"
		self.path_choose_theme = getcwd() + self.path_theme[0] + "choose_theme.ui"
		self.path_main = getcwd() + self.path_theme[0] + "gtm_main.ui"
		
		loader = QtUiTools.QUiLoader()
		ui_file = QtCore.QFile(self.path_main)
		ui_file.open(QtCore.QFile.ReadOnly)
		ui = loader.load(ui_file)
		ui_file.close()

		self.setCentralWidget(ui)

		self.action_add_task = ui.findChild(QtGui.QAction, "action_add_task")
		self.action_add_task.triggered.connect(self.open_create_task)

		self.action_add_task = ui.findChild(QtGui.QAction, "action_delete_task")
		self.action_add_task.triggered.connect(self.delete_task)

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

		self.listWidget_tasks = ui.findChild(QtWidgets.QListWidget, "listWidget_tasks")
		self.listWidget_tasks.itemChanged.connect(self.update_progress_bar)
		self.listWidget_tasks.itemChanged.connect(self.count_done_tasks)
		self.fill_tasks_from_db()
		
		self.progressBar_done_tasks = ui.findChild(QtWidgets.QProgressBar, "progressBar_done_tasks")
		self.update_progress_bar()

		self.todayis()

		QtCore.QCoreApplication.instance().aboutToQuit.connect(self.on_closing)

	def on_closing(self):
		'''Saving data on closing the app'''
		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()

		cursor.execute("DELETE FROM tasks")

		for i in range(self.listWidget_tasks.count()):
			item = self.listWidget_tasks.item(i)
			if item.checkState() == QtCore.Qt.Checked:
				cursor.execute("INSERT INTO tasks (task, done) VALUES (?, ?)", (item.text(), 1))
			else:
				cursor.execute("INSERT INTO tasks (task, done) VALUES (?, ?)", (item.text(), 0))
		conn.commit()

		conn.close()

	def fill_tasks_from_db(self):
		'''Filling tasks from db to listWidget'''

		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()

		cursor.execute("SELECT * FROM tasks")
		rows = cursor.fetchall()
		for row in rows:
			item = QtWidgets.QListWidgetItem(row[1])
			if row[2] == 0:
				item.setCheckState(QtCore.Qt.Unchecked)
			else:
				item.setCheckState(QtCore.Qt.Checked)
			item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
			self.listWidget_tasks.addItem(item)

		conn.close()

	def todayis(self):
		'''Set today is "day" && set achievements'''

		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()

		cursor.execute("SELECT todayis FROM statistics")
		todayis = cursor.fetchone()
		if todayis[0] == datetime.now().day:
			pass
		elif todayis[0] + 1 == datetime.now().day:
			cursor.execute("UPDATE statistics SET todayis = ?", (str(datetime.now().day),))
			cursor.execute("UPDATE statistics SET count_everyday_logons = count_everyday_logons + 1")
			cursor.execute("SELECT count_everyday_logons FROM statistics")
			count_everyday_logons = cursor.fetchone()
			if count_everyday_logons[0] >= 5:
				cursor.execute("UPDATE achievements SET done = 1 WHERE id = 4")
				cursor.execute("UPDATE themes SET available = 1 WHERE id = 8")
			if count_everyday_logons[0] >= 10:
				cursor.execute("UPDATE achievements SET done = 1 WHERE id = 5")
				cursor.execute("UPDATE themes SET available = 1 WHERE id = 9")
			if count_everyday_logons[0] >= 15:
				cursor.execute("UPDATE achievements SET done = 1 WHERE id = 6")
				cursor.execute("UPDATE themes SET available = 1 WHERE id = 10")
		else:
			cursor.execute("UPDATE statistics SET todayis = ?", (str(datetime.now().day),))
			cursor.execute("UPDATE statistics SET count_everyday_logons = 0")

		conn.commit()
		conn.close()

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

	def count_done_tasks(self):
		'''Counting done tasks and set achievements if true'''

		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()
		cursor.execute("UPDATE statistics SET done_tasks = done_tasks + 1")

		cursor.execute("SELECT * FROM statistics")
		row = cursor.fetchone()
		if row[1] >= 5:
			cursor.execute("UPDATE achievements SET done = 1 WHERE id = 1")
			cursor.execute("UPDATE themes SET available = 1 WHERE id = 2")
		if row[1] >= 10:
			cursor.execute("UPDATE achievements SET done = 1 WHERE id = 2 ")
			cursor.execute("UPDATE themes SET available = 1 WHERE id = 3")
		if row[1] >= 15:
			cursor.execute("UPDATE achievements SET done = 1 WHERE id = 3 ")
			cursor.execute("UPDATE themes SET available = 1 WHERE id = 4")

		conn.commit()
		conn.close()

	def open_create_task(self):
		'''Open the dialog creation task to add a new task'''

		loader = QtUiTools.QUiLoader()
		ui_create_task = QtCore.QFile(self.path_create_task)
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
			item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
			self.listWidget_tasks.addItem(item)

			dialog.reject()
			self.update_progress_bar()

	def delete_task(self):
		'''Deleting task'''
		item = self.listWidget_tasks.currentItem()
		if item:
			row = self.listWidget_tasks.row(item)
			self.listWidget_tasks.takeItem(row)

	def open_list_achievements(self):
		'''Open the dialog list of achievements'''

		loader = QtUiTools.QUiLoader()
		ui_list_achievements = QtCore.QFile(self.path_list_achievements)
		ui_list_achievements.open(QtCore.QFile.ReadOnly)
		dialog_list_achievements = loader.load(ui_list_achievements)
		ui_list_achievements.close()

		pushButton_back = dialog_list_achievements.findChild(QtWidgets.QPushButton, "pushButton_back")
		pushButton_back.clicked.connect(dialog_list_achievements.reject)

		listWidget_not_done = dialog_list_achievements.findChild(QtWidgets.QListWidget, "listWidget_not_done")
		listWidget_done = dialog_list_achievements.findChild(QtWidgets.QListWidget, "listWidget_done")

		self.fill_achievements_from_db(listWidget_not_done, listWidget_done)

		dialog_list_achievements.exec()

	def fill_achievements_from_db(self, listWidget_not_done, listWidget_done):
		'''Filling achievements from db to listWidgets'''

		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()

		if cursor.execute("SELECT COUNT(*) FROM achievements WHERE done = 1").fetchone()[0] == 9:
			cursor.execute("UPDATE achievements SET done = 1 WHERE id = 10")
			cursor.execute("UPDATE themes SET available = 1 WHERE id = 11")
			conn.commit()

		cursor.execute("SELECT * FROM achievements")
		rows = cursor.fetchall()
		for row in rows:
			item = QtWidgets.QListWidgetItem(row[1])
			if row[2] == 0:
				listWidget_not_done.addItem(item)
			else:
				listWidget_done.addItem(item)

		conn.close()

	def open_statistics(self):
		'''Open the dialog of statistics'''

		loader = QtUiTools.QUiLoader()
		ui_statistics = QtCore.QFile(self.path_statistics)
		ui_statistics.open(QtCore.QFile.ReadOnly)
		dialog_statistics = loader.load(ui_statistics)
		ui_statistics.close()

		pushButton_back = dialog_statistics.findChild(QtWidgets.QPushButton, "pushButton_back")
		pushButton_back.clicked.connect(dialog_statistics.reject)

		pushButton_restart_statistics = dialog_statistics.findChild(QtWidgets.QPushButton, "pushButton_restart_statistics")
		pushButton_restart_statistics.clicked.connect(lambda: self.open_accept_restart_statistics(dialog_statistics))

		label_count_visits = dialog_statistics.findChild(QtWidgets.QLabel, "label_count_visits")
		label_count_tasks = dialog_statistics.findChild(QtWidgets.QLabel, "label_count_tasks")
		label_count_achievements = dialog_statistics.findChild(QtWidgets.QLabel, "label_count_achievements")
		label_count_themes = dialog_statistics.findChild(QtWidgets.QLabel, "label_count_themes")

		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()

		count_achievements = cursor.execute("SELECT COUNT(*) FROM achievements WHERE done = 1").fetchone()[0]
		cursor.execute("UPDATE statistics SET get_achievements = ?", (count_achievements,))

		count_themes = cursor.execute("SELECT COUNT(*) FROM themes WHERE available = 1").fetchone()[0]
		cursor.execute("UPDATE statistics SET get_themes = ?", (count_themes,))

		conn.commit()

		cursor.execute("SELECT * FROM statistics")
		row = cursor.fetchone()

		label_count_visits.setText(str(row[0]))
		label_count_tasks.setText(str(row[1]))
		label_count_achievements.setText(str(row[2]))
		label_count_themes.setText(str(row[3]))

		conn.close()
		dialog_statistics.exec()
	
	def open_accept_restart_statistics(self, dialog):
		'''Open the dialog accepting restart statistics'''

		loader = QtUiTools.QUiLoader()
		ui_accept_restart_statistics = QtCore.QFile(self.path_accept_restart_statistics)
		ui_accept_restart_statistics.open(QtCore.QFile.ReadOnly)
		dialog_accept_restart_statistics = loader.load(ui_accept_restart_statistics)
		ui_accept_restart_statistics.close()

		pushButton_no = dialog_accept_restart_statistics.findChild(QtWidgets.QPushButton, "pushButton_no")
		pushButton_no.clicked.connect(dialog_accept_restart_statistics.reject)

		pushButton_yes = dialog_accept_restart_statistics.findChild(QtWidgets.QPushButton, "pushButton_yes")
		pushButton_yes.clicked.connect(lambda: self.restart_statistics(dialog_accept_restart_statistics, dialog))

		dialog_accept_restart_statistics.exec()
	
	def restart_statistics(self, dialog, dialog_stats):
		'''Restart statistics from db'''
		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()
		cursor.execute(" UPDATE statistics SET logons = 0, done_tasks = 0, get_achievements = 0, get_themes = 0, todayis = 0, count_everyday_logons = 0 ")
		cursor.execute(" UPDATE achievements SET done = 0 WHERE done = 1 ")
		cursor.execute(" UPDATE themes SET available = 0 WHERE available = 1 ")
		cursor.execute(" UPDATE themes SET used = 0 WHERE used = 1 ")
		cursor.execute(" UPDATE themes SET available = 1 WHERE id = 1 ")
		cursor.execute(" UPDATE themes SET used = 1 WHERE id = 1 ")
		conn.commit()
		conn.close()

		dialog.reject()
		dialog_stats.reject()

	def open_choose_theme(self):
		'''Open the dialog list of themes'''

		loader = QtUiTools.QUiLoader()
		ui_choose_theme = QtCore.QFile(self.path_choose_theme)
		ui_choose_theme.open(QtCore.QFile.ReadOnly)
		dialog_choose_theme = loader.load(ui_choose_theme)
		ui_choose_theme.close()

		pushButton_back = dialog_choose_theme.findChild(QtWidgets.QPushButton, "pushButton_back")
		pushButton_back.clicked.connect(dialog_choose_theme.reject)

		listWidget_list_of_themes = dialog_choose_theme.findChild(QtWidgets.QListWidget, "listWidget_list_of_themes")

		self.load_themes(listWidget_list_of_themes)

		listWidget_list_of_themes.itemActivated.connect(self.theme_activated)

		dialog_choose_theme.exec()

	def load_themes(self, listWidget_list_of_themes):
		'''Loading themes from bd'''

		conn = connect('SQLite//main_db.db')
		cursor = conn.cursor()

		cursor.execute("SELECT name FROM themes WHERE available = 1")
		names = cursor.fetchall()
		for name in names:
			item = QtWidgets.QListWidgetItem(name[0])
			listWidget_list_of_themes.addItem(item)

		conn.close()
	
	def reload_app(self):
		'''Reloading app'''
		QtWidgets.QApplication.quit()
		execl(executable, executable, *argv)

	def theme_activated(self, item):
		'''Signal to change theme in db'''
		msg_box_yesno = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question,
                                    "Вопрос",
                                    "Вы действительно хотите выполнить это действие? Будет выполнена перезагрузка приложения!",
                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		ret = msg_box_yesno.exec()
		if (ret == QtWidgets.QMessageBox.Yes):
			conn = connect('SQLite//main_db.db')
			cursor = conn.cursor()

			cursor.execute("UPDATE themes SET used = 0 WHERE used = 1")
			cursor.execute("UPDATE themes SET used = 1 WHERE name = ?", (item.text(), ))
			conn.commit()

			self.reload_app()

			conn.close()

def main():
    app = QtWidgets.QApplication([])
    window = TimeQuest()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()