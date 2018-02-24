import os
import zipfile
import re
from pathlib import Path
import pandas as pd

class analyzer(object):

    expected_log_dict={'BICS':['opmn.log', 'opmn.out', 'bi_server1.log', 'bi_server1.out',
                               'bi_server1-diagnostic.log', 'sawlog0.log', 'obips1.out', 'obis1-diagnostic.log',
                               'obis1.out', 'obis1-query.log', 'nqscheduler.log']}

    'This class analysis the logs'
    def __init__(self, zippath, service):
        self.zippath=zippath
        self.service=service

    def __repr__(self):
        return f'{self.__class__.__name__} Class analyzing logs from {self.zippath}, for the service - {self.service}'

    @property
    def zippath(self):
        return self._zippath

    @zippath.setter
    def zippath(self, zippath):
        file_to_analyze=Path(zippath)
        if file_to_analyze.exists():
            self._zippath = zippath
        else:
            raise FileNotFoundError("Check the file path. Can't find the zip file in the path.")

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self,service):
        self._service = service  # need to check if the service looking for exists in json later here

    def unzip_files(self):
        with zipfile.ZipFile(self.zippath, 'r') as zip_ref:
            logs_extractpath=os.path.split(self.zippath)
            zip_ref.extractall(logs_extractpath[0])


    def check_for_logs(self):
        list_of_files_present=[]
        logs_path=os.path.split(self.zippath)
        word = re.split(r'\.(?!\d)', logs_path[1])
        #logs_path=logs_path[0].join(word[0])
        logs_path=os.path.join(logs_path[0], word[0])
        all_files=os.listdir(logs_path)
        try:
            if self.service in self.expected_log_dict:
                return True

    def conver_to_html(self):
        df=pd.read_csv("datafile.csv")
        df.to_html("SummaryFile.html")







    def time_parser(self):
        pass



