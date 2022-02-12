from PyQt5 import QtWidgets
import sys
from auth.authgui import LogInSignUpWindow
from auth.auth import LogIn
from mainwindow.maingui import MainWorkWindow
import json
import config


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config.url = 'http://localhost:5000/'
        self.login_window = LogInSignUpWindow()
        self.login = LogIn()
        self.mainWorkWindow = MainWorkWindow(self.login)


        if self.login.getToken() is None:
            self.setCentralWidget(self.login_window)
            self.login_window.submit_button.clicked.connect(self.on_login)
        else:
            self.setCentralWidget(self.mainWorkWindow)

    def on_login(self):
        email = self.login_window.email_input.text()
        password = self.login_window.password_input.text()
        self.login_window.submit_button.setEnabled(False)

        try:
            if self.login_window.is_login_state:
                login_worker = self.login.authenticate(email, password)
                login_worker.authWorkerSignal.completeSignal.connect(self.on_auth_success)
                login_worker.authWorkerSignal.errorSignal.connect(self.on_auth_error)
                self.login.workerPool.start(login_worker)
            else:
                signup_worker = self.login.add_user(email, password)
                signup_worker.authWorkerSignal.completeSignal.connect(self.on_auth_success)
                signup_worker.authWorkerSignal.errorSignal.connect(self.on_auth_error)
                self.login.workerPool.start(signup_worker)

        except Exception as e:
            print(e)

    def on_auth_success(self, res):
        self.login.token = res['token']
        self.login.valid_till = res['expires']
        try:
            with open('auth.json','w') as f:
                json.dump({'valid_till': self.login.valid_till,'token':self.login.token},f)
        except Exception:
            pass
        print(res)
        self.login_window.submit_button.setEnabled(True)
        self.setCentralWidget(self.mainWorkWindow)

    def on_auth_error(self, e):
        print(e)
        self.login_window.submit_button.setEnabled(True)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("ShareNow")
window.show()

app.exec_()
