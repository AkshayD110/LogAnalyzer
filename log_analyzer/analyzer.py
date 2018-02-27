import os
import zipfile
import re
from pathlib import Path
import pandas as pd
from collections import defaultdict, Counter
import csv
import fnmatch

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


        "logic to build the end Single dictionary"
        for items in all_files:
            if items in self.expected_log_dict[self.service]:
                self.results_container[items].append('Yes')
            else:
                self.results_container[items].append('No')
        print(self.results_container)

    def find_errors_warnings(self):
        print("====Getting all Errors and Warnings====")
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

        #print(self.results_container)

    def top_five_errors(self):
        errors_deft_dict=defaultdict(list)
        tempList=[]
        log_path=self.unziped_file_location()
        os.chdir(log_path)
        all_files=os.listdir(log_path)
        error_pattern=["Error", "error", "ERROR"]
        for item in all_files:
            with open(item) as file:
                for line in file.readlines():
                    for phrase in error_pattern:
                        if phrase in line:
                            errors_deft_dict[item].append(line)
                            tempList.append(line)
        print(len(errors_deft_dict))
        for i in range(len(errors_deft_dict)):
            print(errors_deft_dict[i])



    def write_to_csvfile(self):
        print("====Generting the summary report====")
        single_list_results=[]
        dict_result=dict(self.results_container)
        sl_no_count=1
        for key, value in dict_result.items():
            tmp=[]
            tmp.append(sl_no_count)
            tmp.append(key)
            for i in range(len(value)):
                tmp.append(value[i])
            single_list_results.append(tmp)
            sl_no_count+=1

        with open('datafile.csv', 'w', newline='') as file:
            writer=csv.writer(file)
            writer.writerow(['Sl No','Logfile', 'Present(Yes/No)', 'Error Count', 'Warning Count'])
            for item in single_list_results:
                writer.writerow(item)



    def conver_to_html(self):
        df=pd.read_csv("datafile.csv")
        df.to_html("SummaryFile.html")
        print("====The summary file has been generated====")

    "An implementation to take user time input. Coming up next"
    def time_parser(self):
        pass

