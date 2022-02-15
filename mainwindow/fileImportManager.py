from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject
import config
import requests


class ImportFileSignals(QObject):
    importFileSuccessSignal = pyqtSignal(dict)
    importFileErrorSignal = pyqtSignal(dict)


class ImportFileWorker(QRunnable):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.importFileSignals = ImportFileSignals()
        self.login = args[0]
        self.url = args[1]
        self.method = args[2]
        self.body = kwargs.get('json')

    @pyqtSlot()
    def run(self):
        headers = {'Authorization': 'Bearer ' + self.login.getToken()}

        try:
            if self.method == 'get':
                res = requests.get(self.url, headers=headers)
            elif self.method == 'post':
                res = requests.post(self.url, headers=headers, json=self.body)
            res.raise_for_status()
            self.importFileSignals.importFileSuccessSignal.emit(res.json())
        except Exception as e:
            print(e)
            self.importFileSignals.importFileErrorSignal.emit(res.json())


class FileImportManager:
    def __init__(self, login):
        self.login = login

    def check_file_access_code(self, code):
        url = config.url + f"checkFileAccessCode/{code}"
        importFileWorker = ImportFileWorker(self.login, url, 'get')
        config.qPool.start(importFileWorker)
        return importFileWorker.importFileSignals

    def import_file(self, code, file_id):
        url = config.url + f"importFile"
        data = {'file_id': file_id,
                'access_code': code}
        importFileWorker = ImportFileWorker(self.login, url, 'post', json=data)
        config.qPool.start(importFileWorker)
        return importFileWorker.importFileSignals
