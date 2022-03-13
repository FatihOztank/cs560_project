from sut_interface import SUT
import os
import subprocess
import re
import datetime

# change the value of project_folder variable into address of this project folder
project_folder = "/home/fatih/Documents/dersler/cs560/cont_static_analsis_prot/"
elasticsearch_folder = project_folder + "elasticsearch"

def getTagName(tagdate):
    bashCommand = "git tag --format='%(creatordate:short)%09%(refname:strip=2)' | grep " + str(tagdate)
    directory = elasticsearch_folder
    process = subprocess.run(bashCommand,shell=True, check=True, cwd=directory, capture_output=True)
    output = process.stdout.decode("UTF-8")

    delimiters = "\n", "\t"
    regexPattern = '|'.join(map(re.escape, delimiters))

    versionList = re.split(regexPattern, output)
    print(versionList[-2])

class Elasticsearch_src(SUT):
    def __init__(self,datetime_obj):
        self.tagdate = datetime_obj

    def download(self):
        try:
            bashCommand = "git tag --format='%(creatordate:short)%09%(refname:strip=2)' | grep " + str(self.tagdate)
            directory = elasticsearch_folder
            process = subprocess.run(bashCommand,shell=True, check=True, cwd=directory, capture_output=True)
            output = process.stdout.decode("UTF-8")   
        except:
            return False

        delimiters = "\n", "\t"
        regexPattern = '|'.join(map(re.escape, delimiters))

        versionList = re.split(regexPattern, output)
        print(versionList[-2])

        bashCommand = "git reset --hard"
        directory = elasticsearch_folder
        process = subprocess.run(bashCommand,shell=True, check=True, cwd=directory)

        try:
            bashCommand = "git checkout tags/" + versionList[-2]
            directory = elasticsearch_folder
            process = subprocess.run(bashCommand,shell=True, check=True, cwd=directory)
        except:
            print("A problem occured")
            return False

        return True
    
    def configure(self):
        pass

    def build(self):
        try:
            bashCommand = "./gradlew jar"
            directory = elasticsearch_folder
            process = subprocess.run(bashCommand,shell=True, check=True, cwd=directory)
        except:
            #print("A problem occured")
            raise ValueError("change java version!!")
            return


    def applyDepAnalysis(self):
        try:
            bashCommand = "jdeps  ./ > " + project_folder + "elasticsearchReports/dep_analysis_report" + str(self.tagdate)
            directory = elasticsearch_folder + "/server"
            process = subprocess.run(bashCommand,shell=True, check=True, cwd=directory)
        except:
            print("A problem occured")
            return

if __name__ == "__main__":
    build_date = datetime.date(2021,12,13)
    today = datetime.date.today()
    #release_date = datetime.date(2021, 8, 3)
    while build_date < today:
        sut = Elasticsearch_src(build_date)
        if(sut.download()):
            try:
                sut.build()
                sut.applyDepAnalysis()
            except ValueError as ve:
                print(ve, build_date)
                break

        build_date += datetime.timedelta(days=1)
