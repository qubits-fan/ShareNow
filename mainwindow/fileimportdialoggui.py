from PyQt5 import QtWidgets
from mainwindow.fileimportdialogdesign import Ui_Dialog


class FileImportDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(FileImportDialog, self).__init__(*args,**kwargs)
        self.setWindowTitle("Import File")
        self.setupUi(self)
        self.cancel_button.clicked.connect(lambda x: self.reject())
        self.file_id = None
