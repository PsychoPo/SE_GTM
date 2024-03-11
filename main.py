from os import getcwd
from PySide6 import QtWidgets, QtUiTools, QtCore

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

def main():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()