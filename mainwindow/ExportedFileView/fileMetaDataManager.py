import requests
import config
from PyQt5.QtCore import QObject, QRunnable, pyqtSlot, pyqtSignal, QThreadPool


class FilesMetaDataDownloadSignals(QObject):
    metadataDownloadSuccessSignal = pyqtSignal(dict)
    metadataErrorSignal = pyqtSignal(dict)


class FilesMetaDataDownloadWorker(QRunnable):

    def __init__(self, login, url):
        super(FilesMetaDataDownloadWorker,self).__init__()
        self.metadataDownloadSignal = FilesMetaDataDownloadSignals()
        self.login = login
        self.url = url

    @pyqtSlot()
    def run(self):
        headers = {'Authorization': 'Bearer ' + self.login.getToken()}
        try:
            res = requests.get(self.url, headers=headers)
            res.raise_for_status()
            metadatas = res.json()
            self.metadataDownloadSignal.metadataDownloadSuccessSignal.emit({'message': metadatas})
        except Exception as e:
            self.metadataDownloadSignal.metadataErrorSignal.emit(res.json())


class FileMetaDataManager:
    def __init__(self, login):
        self.login = login
        self.qPool = config.qPool
        self.url = config.url + 'getYourFiles'

    def download_Files_metadata(self):
        fileDownloadWorker = FilesMetaDataDownloadWorker(self.login, self.url)
        self.qPool.start(fileDownloadWorker)
        return fileDownloadWorker.metadataDownloadSignal
