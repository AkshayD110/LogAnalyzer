import os
import zipfile

class analyzer(object):

    'This class analysis the logs'
    def __init__(self, zippath):
        self._zippath=zippath

    def __repr__(self):
        return f'{self.__class__.__name__} Class analyzing logs from {zippath}'

    @property
    def zippath(self):
        return self._zippath

    @zippath.setter
    def zippath(self, zippath):
        self._zippath=zippath

    def unzip_files(self):
        with zipfile.ZipFile(self._zippath, 'r') as zip_ref:
            logs_extractpath=os.path.split(self._zippath)
            zip_ref.extractall(logs_extractpath[0])


    def check_for_logs(self):
        pass


