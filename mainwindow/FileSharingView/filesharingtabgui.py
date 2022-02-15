from mainwindow.FileSharingView.filesharingtabdisplay import Ui_Form
from PyQt5 import QtWidgets, QtGui, QtCore
from datetime import datetime as dt
import datetime
import res


class DownloadersTableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class FileSharingTab(QtWidgets.QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):
        super(FileSharingTab, self).__init__()
        self.setupUi(self)
        self.file_icon_label.setPixmap(QtGui.QPixmap(":/icons/file_icon.png"))
        self.file_icon_label.setScaledContents(True)
        self.file_name_label.setText(args[0] + args[1])
        self.maximum_downloads_spinbox.setValue(0)
        self.access_code_input.setText("Abhi Set Nahi Kiye")
        self.start_datetime_input.setCalendarPopup(True)
        self.finish_datetime_input.setCalendarPopup(True)
        self.start_datetime_input.setDate(dt.now())
        self.finish_datetime_input.setDate(dt.now())

