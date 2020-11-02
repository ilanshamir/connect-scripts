import sys
import json
import os

sys.path.append("./")
from communication import initializeMCParams, getAPIRequest
from agents import getAgentList, getAgentByAttrs
from jobs import appendToJobAgentList, addJob, getJobRunID, startJob, deleteJob, jobsMonitor, addSimpleSyncJob
from jobs_from_csv import jobsFromCSV

def doSomethingWhenJobIsDone(jobID):
    print("function called after the Job " + str(jobID) + " was done")
    deleteJob(jobID)

# initialize MC
initializeMCParams(os.getenv('RESILIO_MC_URL'), 8443, os.getenv('RESILIO_AUTH_TOKEN'))

# quick test that we can actually connect to this Management Console
print(getAPIRequest("/api/v2/info"))

# start the job monitor
myJobsMonitor = jobsMonitor(10)

# get the list of agents
agents = getAgentList()

# start jobs based on a csv
csvJobs = jobsFromCSV("./sampleJobs.csv", myJobsMonitor, doSomethingWhenJobIsDone, 4, 10)


"""
# add a job
addSimpleSyncJob("Sync Job 1", "", doSomethingWhenJobIsDone,
            "54.183.114.79", "Server 1", "rw", "/tmp/v2",
            "54.183.114.80", "Server 2", "ro", "/tmp/v21")
"""




