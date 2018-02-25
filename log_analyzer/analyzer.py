import os
import zipfile
import re
from pathlib import Path
import pandas as pd
from collections import defaultdict

class analyzer(object):

    """it is imp to build the below dict properly as per user requirement"""
    results_container = defaultdict(list)
    expected_log_dict={'BICS':['opmn.log', 'opmn.out', 'bi_server1.log', 'bi_server1.out',
                               'bi_server1-diagnostic.log', 'sawlog0.log', 'obips1.out', 'obis1-diagnostic.log',
                               'obis1.out', 'obis1-query.log', 'nqscheduler.log', 'nqserver.log'],
                       'ICS':['bi_server1.out', 'bi_server1.log']}

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

    def unziped_file_location(self):
        logs_path = os.path.split(self.zippath)
        word = re.split(r'\.(?!\d)', logs_path[1])
        logs_path = os.path.join(logs_path[0], word[0])
        return logs_path

    def check_for_logs(self):
        log_path=self.unziped_file_location()
        file_presence={}
        all_files=os.listdir(log_path)
        print(all_files)

        "To check if the service entere is valid"
        if self.service in self.expected_log_dict.keys():
            pass
        else:
            raise ValueError(f"The service Entered is not valid. Program supports the services:{self.expected_log_dict.keys()}")

        "Logic to check if the log file is present"
        """
        for item in all_files:
            if item in self.expected_log_dict[self.service]:
                file_presence[item]='Yes'
            else:
                file_presence[item]='No'

        print(file_presence)
        """
        "alternative logic to build the end Single dictionary"


        for items in all_files:
            if items in self.expected_log_dict[self.service]:
                self.results_container[items].append('Yes')
            else:
                self.results_container[items].append('No')
        print(self.results_container)

    def find_errors_warnings(self):
        error_count=0
        warning_count=0
        log_path=self.unziped_file_location()
        os.chdir(log_path)
        all_files=os.listdir(log_path)
        for item in all_files:
            with open(item) as file:
                content=file.read()
                error_count=sum(1 for match in re.finditer(r"(?i)ERROR", content))
                warning_count=sum(1 for match in re.finditer(r"(?i)warning", content))
            self.results_container[item].append(error_count)
            self.results_container[item].append(warning_count)

        print(self.results_container)

    def conver_to_html(self):
        df=pd.read_csv("datafile.csv")
        df.to_html("SummaryFile.html")

    "An implementation to take user time input. Coming up next"
    def time_parser(self):
        pass

