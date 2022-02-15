from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSignal
import math
import res


class FileView(QtWidgets.QWidget):
    def __init__(self, file_dict):
        super().__init__()
        self.file_name = QtWidgets.QLabel()
        self.file_icon = QtWidgets.QLabel()
        self.file_icon.setPixmap(QtGui.QPixmap(":/icons/file_icon.png"))
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.setMinimumHeight(100)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.file_icon)
        self.layout.addWidget(self.file_name)
        self.setLayout(self.layout)
        self.file_id = file_dict['file_id']
        self.name = file_dict['name']
        self.size = file_dict['size']
        self.type = file_dict['type']
        self.file_info = file_dict['file_info']
        self.file_name.setText(self.name + '.' + self.type)
        self.file_sharing_action = QAction("Change Sharing Details",self)
        self.file_sharing_action.setStatusTip("You can see and modify file sharing details here")




    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        pass

    def contextMenuEvent(self, e) -> None:
        context = QtWidgets.QMenu(self)
        context.addAction(QAction("Download File Locally", self))
        context.addAction(QAction("See File Details", self))
        context.addAction(self.file_sharing_action)
        context.exec_(e.globalPos())


class FileDisplayWindow(QtWidgets.QScrollArea):

    def __init__(self):
        super().__init__()
        self.files = []
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.setWidget(self.widget)
        self.widget.setLayout(self.layout)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def add_files(self, files,open_action):
        for file in files:
            new_file = FileView(file)
            new_file.file_sharing_action.triggered.connect(lambda x,y=file: open_action(y))
            self.files.append(new_file)

    def update_layout(self):
        n = len(self.files)
        for x in range(0, math.ceil(n/2)):
            for y in range(0,2):
                if len(self.files) != 0:
                    self.layout.addWidget(self.files.pop(0),x,y)

