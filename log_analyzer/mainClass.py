from log_analyzer import analyzer
def main():
    path=r'C:\Users\akshdesh.ORADEV\Documents\books\python\work2\Problamatictime_Logs.zip'
    service="BICS" #This has to be a user input later
    analysis_obj=analyzer.analyzer(path,service)
    analysis_obj.unzip_files()
    analysis_obj.check_for_logs()

if __name__ == '__main__':
    main()