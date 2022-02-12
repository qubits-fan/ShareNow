from PyQt5 import QtWidgets, QtGui
from mainwindow.maindesign import Ui_MainWindow
from mainwindow.fileuploadDialogGui import FileUploadDialog
from mainwindow.fileUploadManager import FileUploadManager
import os


class MainWorkWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, login, *args, **kwargs):
        super(MainWorkWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionExportFile.triggered.connect(self.on_export_file_action)
        self.login = login
        self.fileUploadManager = FileUploadManager(self.login)

    def on_export_file_action(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "File to Export", "All files (*.*)")
        if file_path:
            f = open(file_path, 'rb')
            file_stat = os.stat(file_path)
        else:
            return

        dlg = FileUploadDialog(self)
        dlg.setFilePathInput(file_path)
        dlg.setFileNameInput(file_path.split('/')[-1].split('.')[0])
        dlg.setFileSizeInput(file_stat.st_size)
        dlg.setFileTypeInput(file_path.split('/')[-1].split('.')[-1])
        dlg.send_button.clicked.connect(lambda x: self.sending_file_to_server(dlg, f, file_stat.st_size))
        dlg.exec_()

    def sending_file_to_server(self, dlg, f, sz):
        file_instances = {'upload': f}
        metadata = {
            'size': sz,
            'type': dlg.file_type_input.text(),
            'file_info': dlg.file_info_text.toPlainText(),
            'name': dlg.file_name_input.text()
        }
        uploadSignals = self.fileUploadManager.uploadFile(file_instances, metadata)
        uploadSignals.successSignal.connect(self.on_file_upload_success_dialog)
        uploadSignals.failureSignal.connect(self.on_file_failure_dialog)

    def on_file_upload_success_dialog(self):
        button = QtWidgets.QMessageBox.information(self, "File Upload Status",
                                                   "File Uploaded Successfully, Show in exported file Section")

    def on_file_failure_dialog(self):
        button = QtWidgets.QMessageBox.warning(self,"File Upload Status","File Could not upload")
