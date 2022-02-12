import requests
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot
import config
import pdb


class FileUploadSignals(QObject):
    successSignal = pyqtSignal(dict)
    failureSignal = pyqtSignal(dict)
    progressSignal = pyqtSignal(dict)


class FileUploadWorker(QRunnable):

    def __init__(self, *args, **kwargs):
        super(FileUploadWorker, self).__init__()
        self.fileUploadSignals = FileUploadSignals()
        self.files = kwargs['files']
        self.data = kwargs['data']
        self.token = args[0].getToken()
        self.url = args[1]

    @pyqtSlot()
    def run(self):
        token = self.token
        url = self.url

        try:
            headers = {'Authorization': 'Bearer '+token}
            response = requests.post(url, files=self.files,data=self.data,headers=headers)
            response.raise_for_status()
            self.fileUploadSignals.successSignal.emit(response.json())
        except Exception as e:
            self.fileUploadSignals.failureSignal.emit(response.json())
            print(e)


class FileUploadManager:
    def __init__(self, login):
        self.qPool = QThreadPool()
        self.login = login
        self.url = config.url + 'fileUpload'

    def uploadFile(self, file_instance,metadata):
        newWorker = FileUploadWorker(self.login, self.url, files=file_instance,data=metadata)
        self.qPool.start(newWorker)
        return newWorker.fileUploadSignals
