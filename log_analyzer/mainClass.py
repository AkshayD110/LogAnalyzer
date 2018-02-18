from log_analyzer import analyzer
def main():
    path=r'C:\Users\akshdesh.ORADEV\Documents\books\python\work2\Problamatictime_Logs.zip'
    analysis_obj=analyzer.analyzer(path)
    analysis_obj.unzip_files()

if __name__ == '__main__':
    main()