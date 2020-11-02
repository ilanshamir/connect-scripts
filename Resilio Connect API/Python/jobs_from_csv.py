import csv
import time
import threading

from jobs import addSimpleSyncJob, getJobs, getJobsByAttrs, getJobRunID

class jobsFromCSV:
    def __init__(self, csvFile, jobsMonitor, callbackFunction, concurrentJobsCount, monitorInterval):
        self.jobsList = []
        self.nextJob = 0
        self.jobsMonitor = jobsMonitor
        self.callbackFunction = callbackFunction
        self.concurrentJobsCount = concurrentJobsCount
        self.monitorInterval = monitorInterval
        with open(csvFile, "r") as file:
            csvReader = csv.DictReader(file, skipinitialspace=True)
            for row in csvReader:
                row['sentForExecution'] = False         # use this to track if the job was already sent for execution
                self.jobsList.append(row)    
            print(self.jobsList)
        self.syncCurrentState()
        threading.Thread(target=self.jobCreationThread).start()

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
            self.jobsList[self.nextJob]['sentForExecution'] = True
            self.nextJob += 1

    def syncCurrentState(self):
        for index in range(len(self.jobsList)):
            jobExists = getJobsByAttrs("name", self.jobsList[index]['jobName'])
            if (jobExists):
                # TO DO: log it
                self.jobsList[index]['sentForExecution'] = True
                jobRunID = getJobRunID(jobExists[0]['id'])
                self.jobsMonitor.addMonitoredJob(jobRunID['data'][0]['id'], self.callbackFunction)

    def jobCreationThread(self):
        while (True):
            jobs = getJobs()
            while ((self.nextJob < len(self.jobsList)) and (len(jobs) < self.concurrentJobsCount)):
                jobExists = getJobsByAttrs("name", self.jobsList[self.nextJob]['jobName'])
                # was it executed before?
                if (self.jobsList[self.nextJob]['sentForExecution']):
                    # TO DO: log it
                    self.nextJob += 1
                elif (not jobExists):
                    self.addNextJob()
                    jobs = getJobs()
                else:
                    # TO DO: log it
                    self.jobsList[self.nextJob]['sentForExecution'] = True
                    jobRunID = getJobRunID(jobExists[0]['id'])
                    self.jobsMonitor.addMonitoredJob(jobRunID['data'][0]['id'], self.callbackFunction)
                    self.nextJob += 1
            time.sleep(self.monitorInterval)
