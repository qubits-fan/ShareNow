from PyQt5 import QtWidgets, QtGui

import res


class FileView(QtWidgets.QWidget):
    def __init__(self, file_dict):
        super().__init__()
        self.file_name = QtWidgets.QLabel()
        self.file_icon = QtWidgets.QLabel()
        self.file_icon.setPixmap(QtGui.QPixmap(":/icons/file_icon.png"))
        self.file_icon.setFixedHeight(100)
        self.file_icon.setFixedHeight(80)
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

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass


class FileDisplayWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.files = []
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

    def add_file(self, file):
        new_file = FileView(file)
        self.files.append(new_file)
        self.update_layout()

    def update_layout(self):
        # Add Some Good Stuff
        pass
