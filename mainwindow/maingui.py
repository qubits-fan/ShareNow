from PyQt5 import QtWidgets, QtGui
from mainwindow.maindesign import Ui_MainWindow
from mainwindow.fileuploadDialogGui import FileUploadDialog
from mainwindow.ExportedFileView.filedisplaywindowgui import FileDisplayWindow
from mainwindow.ExportedFileView.fileMetaDataManager import FileMetaDataManager
from mainwindow.FileSharingView.filesharingtabgui import FileSharingTab, DownloadersTableModel
from mainwindow.FileSharingView.file_sharing_manager import FileSharingManager
from mainwindow.fileimportdialoggui import FileImportDialog
from mainwindow.fileUploadManager import FileUploadManager
from mainwindow.fileImportManager import FileImportManager
import os
from datetime import datetime as dt


class MainWorkWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, login, *args, **kwargs):
        super(MainWorkWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionExportFile.triggered.connect(self.on_export_file_action)
        self.login = login
        self.fileUploadManager = FileUploadManager(self.login)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.on_close_current_tab)
        self.tabWidget.removeTab(1)
        self.tabWidget.setTabText(0, "General")
        # This error is more crucial
        # Never Make child to some class that is going to add in a parent

        # File Menus
        self.actionimportFile.triggered.connect(self.on_import_file_action)

        # HistoryMenus

        self.actionExportedFiles.triggered.connect(self.on_exported_files_action)

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

    def on_import_file_action(self):
        dlg = FileImportDialog(self)
        dlg.check_button.clicked.connect(lambda x, y=dlg: self.on_check_code_button(y))
        dlg.import_file_button.clicked.connect(lambda x, y=dlg: self.on_import_file_button(y))
        dlg.exec_()

    def on_check_code_button(self, dlg: FileImportDialog):
        access_code = dlg.access_code_input.text()
        file_import_manager = FileImportManager(self.login)
        check_code_signals = file_import_manager.check_file_access_code(access_code)
        check_code_signals.importFileSuccessSignal.connect(lambda x, y=dlg: self.on_check_code_success(x, y))
        check_code_signals.importFileErrorSignal.connect(self.on_check_code_error)

    def on_import_file_button(self, dlg: FileImportDialog):
        access_code = dlg.access_code_input.text()
        file_id = dlg.file_id
        file_import_manager = FileImportManager(self.login)
        import_file_signals = file_import_manager.import_file(access_code, file_id)
        import_file_signals.importFileSuccessSignal.connect(self.on_import_file_success)
        import_file_signals.importFileErrorSignal.connect(self.on_import_file_error)

    def on_import_file_success(self, x):
        button = QtWidgets.QMessageBox.information(self, "Imported File", "File Imported Successfully See in imported "
                                                                          "File Area")

    def on_import_file_error(self, x):
        button = QtWidgets.QMessageBox.warning(self, "Import File Error", res['message'])

    def on_check_code_success(self, res, dlg: FileImportDialog):
        print(res)
        button = QtWidgets.QMessageBox.information(self, "Access Code Correctness",
                                                   "Your Code has matched with a file you can now import this "
                                                   "file by clicking on import file button of dialog")
        dlg.file_name_label_2.setText(res['name'] + res['type'])
        dlg.file_size_label.setText(str(res['size']) + " bytes")
        dlg.file_id = res['file_id']
        # Add Owner Id Here in future here

    def on_check_code_error(self, res):
        button = QtWidgets.QMessageBox.warning(self, "Error in Access Code", res['message'])

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
        button = QtWidgets.QMessageBox.warning(self, "File Upload Status", "File Could not upload")

    # On Exported File

    def on_exported_files_action(self):
        file_display_window = FileDisplayWindow()
        i = self.tabWidget.addTab(file_display_window, "Exported Files widget")
        fileMetaDataDownload = FileMetaDataManager(self.login)
        downloadSignals = fileMetaDataDownload.download_Files_metadata()
        self.tabWidget.setCurrentIndex(i)
        cwidget = self.tabWidget.currentWidget()
        downloadSignals.metadataDownloadSuccessSignal.connect(
            lambda x, y=cwidget: self.on_meta_data_download_success(x, y))
        downloadSignals.metadataErrorSignal.connect(self.on_meta_data_download_error)

    def on_close_current_tab(self, i):
        if self.tabWidget.count() < 2:
            return
        self.tabWidget.removeTab(i)

    # Danger:::: Reverse Flow of Break in MVC
    def on_meta_data_download_success(self, res, display_widget):
        display_widget.add_files(res['message'], self.file_sharing_info_tab)
        display_widget.update_layout()

    def on_meta_data_download_error(self, err):
        print(err)

    def file_sharing_info_tab(self, file):
        print(file)
        i = self.tabWidget.addTab(FileSharingTab(file['name'], file['type']), f"Sharing/{file['name']}{file['type']}")
        self.tabWidget.setCurrentIndex(i)
        fileSharingInstance = self.tabWidget.currentWidget()
        fileSharingManager = FileSharingManager(self.login)
        fileSharingInstance.save_changes_button.clicked.connect(
            lambda x, y=fileSharingManager, z=fileSharingInstance, w=file['file_id']: self.on_sharing_details_save(y, z,
                                                                                                                   w))
        fileDownloadersSignals = fileSharingManager.get_file_downloaders(file['file_id'])
        fileDownloadersSignals.successSignals.connect(
            lambda x, y=fileSharingInstance: self.file_downloaders_success_signal(x, y))
        fileDownloadersSignals.errorSignals.connect(lambda err: print(err))

    def file_downloaders_success_signal(self, downloads, container):
        all_downloaders = [[download['download_times'], download['access_code']] for download in downloads]
        model = DownloadersTableModel(all_downloaders)
        container.downloaders_list_view.setModel(model)

    def on_sharing_details_save(self, manager: FileSharingManager, values_instance: FileSharingTab, file_id):
        new_values = {
            'max_download': values_instance.maximum_downloads_spinbox.value(),
            'access_code': values_instance.access_code_input.text(),
            'start_datetime': int(dt.timestamp(values_instance.start_datetime_input.dateTime().toPyDateTime())),
            'finish_datetime': int(dt.timestamp(values_instance.finish_datetime_input.dateTime().toPyDateTime().now()))
        }
        apiRequestSignals = manager.set_file_privileges(file_id, new_values)
        apiRequestSignals.successSignals.connect(self.on_setting_new_privileges)
        apiRequestSignals.errorSignals.connect(self.on_failing_new_privileges)

    def on_setting_new_privileges(self, x=None):
        button = QtWidgets.QMessageBox.information(self, "File Privileges Setting Status",
                                                   "New Privileges set for File Successfully")

    def on_failing_new_privileges(self, x=None):
        button = QtWidgets.QMessageBox.warning(self, "File Privileges Setting Status", "Error: In Setting File "
                                                                                       "Privileges")
