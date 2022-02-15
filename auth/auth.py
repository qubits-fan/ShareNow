"""
  This is for the authentication for the server
"""

import requests
import datetime
import json
import config
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot, QThreadPool

signup_url = 'http://localhost:5000/signup'
login_url = 'http://localhost:5000/login'


class AuthWorkerSignal(QObject):
    completeSignal = pyqtSignal(dict)
    errorSignal = pyqtSignal(dict)


class AuthWorker(QRunnable):

    def __init__(self, *args, **kwargs):
        super(AuthWorker, self).__init__()
        self.authWorkerSignal = AuthWorkerSignal()
        self.url = args[0]
        self.data = kwargs['data']

    @pyqtSlot()
    def run(self):
        try:
            response = requests.post(self.url, json=self.data)
            response.raise_for_status()
            self.authWorkerSignal.completeSignal.emit(response.json())
        except Exception as e:
            self.authWorkerSignal.errorSignal.emit(response.json())


class LogIn:

    def __init__(self, email=None, password=None):
        self.token = None
        self.email = email
        self.password = password
        self.valid_till = None
        self.load_local_credential()
        self.workerPool = config.qPool

    def authenticate(self, email, password):
        worker = AuthWorker(login_url, data={'email': email, 'password': password})
        return worker

    def getToken(self):
        if self.token is None:
            return None
        elif self.valid_till < datetime.datetime.now().timestamp():
            return None
        return self.token

    def add_user(self, email, password):
        worker = AuthWorker(signup_url, data={'email': email, 'password': password})
        return worker

    def load_local_credential(self):
        try:
            with open('auth.json', "r") as f:
                login_data = json.load(f)
                self.token = login_data['token']
                self.valid_till = login_data['valid_till']
        except Exception:
            pass
