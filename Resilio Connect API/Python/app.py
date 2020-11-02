import sys
import json
import os
import logging

sys.path.append("./")
from communication import initializeMCParams, getAPIRequest
from agents import getAgentList, getAgentByAttrs
from jobs import appendToJobAgentList, addJob, getJobRunID, startJob, deleteJob, jobsMonitor, addSimpleSyncJob, getJobRunStatus, getJobByID
from jobs_from_csv import jobsFromCSV

def doSomethingWhenJobIsDone(jobID, runID):
    print("function called after the Job " + str(jobID) + " was done")
    logging.info("Job " + str(jobID) + " was completed and will be deleted")
    jobDetails = getJobByID(jobID)
    logging.info(json.dumps(jobDetails))
    runResult = getJobRunStatus(runID)
    logging.info(json.dumps(runResult))
    deleteJob(jobID)

# configure a log file
logging.basicConfig(filename='./pymc.log', filemode='a', level=logging.INFO)

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
            "54.183.114.75", "Server 1", "rw", "/tmp/v2",
            "54.183.114.75", "Server 2", "ro", "/tmp/v21")
"""




