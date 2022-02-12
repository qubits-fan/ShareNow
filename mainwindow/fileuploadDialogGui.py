from PyQt5 import QtWidgets, QtGui
from mainwindow.fileuploaddialogdesign import Ui_Dialog
import res


class FileUploadDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(FileUploadDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.file_icon_label.setPixmap(QtGui.QPixmap(":/icons/file_upload.png"))
        self.file_icon_label.setScaledContents(True)
        self.cancel_button.clicked.connect(self.on_cancel_button)
        self.send_button.clicked.connect(self.on_send_button)

    def setFilePathInput(self, path_input):
        self.file_path_input.setText(path_input)

    def setFileNameInput(self, name_input):
        self.file_name_input.setText(name_input)

    def setFileSizeInput(self, size_input):
        self.file_size_input.setText(str(size_input) + " " + "bytes")

    def setFileTypeInput(self, file_type_input):
        self.file_type_input.setText("." + file_type_input)

    def on_cancel_button(self):
        self.reject()

    def on_send_button(self):
        self.reject()
