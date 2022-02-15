import requests
import config
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject


class FileSharingSignals(QObject):
    successSignals = pyqtSignal(dict)
    errorSignals = pyqtSignal(dict)


class FileSharingDetailsWorker(QRunnable):

    def __init__(self, *args, **kwargs):
        super(FileSharingDetailsWorker, self).__init__()
        self.fileSharingSignals = FileSharingSignals()
        self.login = args[0]
        self.url = args[1]
        self.method = args[2]
        self.body = kwargs.get('json')

    @pyqtSlot()
    def run(self):
        try:
            headers = {'Authorization': 'Bearer ' + self.login.getToken()}
            if self.method == 'get':
                res = requests.get(self.url, headers=headers)
            elif self.method == 'post':
                res = requests.post(self.url, headers=headers, json=self.body)
            res.raise_for_status()
            self.fileSharingSignals.successSignals.emit(res.json())
        except Exception as e:
            print(e)
            self.fileSharingSignals.errorSignals.emit({'message': 'A Dep error from server'})


class FileSharingManager:

    def __init__(self, login):
        self.login = login

    def get_file_downloaders(self, file_id):
        url = config.url + f"{file_id}/getFileDownloaders"
        fileSharingDetailsWorker = FileSharingDetailsWorker(self.login, url,'get')
        config.qPool.start(fileSharingDetailsWorker)
        return fileSharingDetailsWorker.fileSharingSignals

    def set_file_privileges(self, file_id,new_privileges):
        url = config.url + f"updateFileAccessPrivileges/{file_id}"
        setFilePrivilegesWorker = FileSharingDetailsWorker(self.login,url,'post',json=new_privileges)
        config.qPool.start(setFilePrivilegesWorker)
        return setFilePrivilegesWorker.fileSharingSignals
