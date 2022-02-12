from PyQt5 import QtCore, QtWidgets, QtGui, uic
import sys
from auth.loginsignup import LogInSignUpDesign


class LogInSignUpWindow(QtWidgets.QMainWindow, LogInSignUpDesign):

    def __init__(self, *args, **kwargs):
        super(LogInSignUpWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.state_change_button.setCheckable(True)
        self.state_change_button.clicked.connect(self.on_state_change)
        self.is_login_state = True

    def on_state_change(self, x):
        if x is True:
            self.state_change_button.setText("Back to LogIn")
            self.is_login_state = False
        else:
            self.state_change_button.setText("Back to SignUp")
            self.is_login_state = True
