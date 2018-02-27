from log_analyzer import analyzer


def main():
    path=r'C:\Users\akshdesh.ORADEV\Documents\books\python\work2\Problamatictime_Logs.zip' #This will be user input
    # later
    service="BICS" #This has to be a user input later
    service=service.upper()
    analysis_obj=analyzer.analyzer(path,service)
    analysis_obj.unzip_files()
    analysis_obj.check_for_logs()
    analysis_obj.find_errors_warnings()
    analysis_obj.write_to_csvfile()
    analysis_obj.top_five_errors()
    analysis_obj.conver_to_html()

if __name__ == '__main__':
    main()