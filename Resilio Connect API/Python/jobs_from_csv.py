import csv
import time
import threading

from jobs import addSimpleSyncJob, getJobs

class jobsFromCSV:
    def __init__(self, csvFile, jobsMonitor, callbackFunction, concurrentJobsCount, monitorInterval):
        self.jobsList = []
        self.nextJob = 0
        self.jobsMonitor = jobsMonitor
        self.callbackFunction = callbackFunction
        self.concurrentJobsCount = concurrentJobsCount
        self.monitorInterval = monitorInterval
        threading.Thread(target=self.jobCreationThread).start()
        with open(csvFile, "r") as file:
            csvReader = csv.DictReader(file, skipinitialspace=True)
            for row in csvReader:
                self.jobsList.append(row)    
            print(self.jobsList)

    def addNextJob(self):
        if (self.nextJob < len(self.jobsList)):
            addSimpleSyncJob(
                self.jobsList[self.nextJob]['jobName'],
                self.jobsList[self.nextJob]['jobDescription'],
                self.callbackFunction,
                self.jobsList[self.nextJob]['ip1'],
                self.jobsList[self.nextJob]['name1'],
                self.jobsList[self.nextJob]['permission1'],
                self.jobsList[self.nextJob]['folder1'],
                self.jobsList[self.nextJob]['ip2'],
                self.jobsList[self.nextJob]['name2'],
                self.jobsList[self.nextJob]['permission2'],
                self.jobsList[self.nextJob]['folder2'],
                self.jobsMonitor
                )
            self.nextJob += 1

    def jobCreationThread(self):
        while (True):
            jobs = getJobs()
            while ((self.nextJob < len(self.jobsList)) and (len(jobs) < self.concurrentJobsCount)):
                self.addNextJob()
                jobs = getJobs()
            time.sleep(self.monitorInterval)
