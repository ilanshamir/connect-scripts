import sys
import json
import os

sys.path.append("./")
from communication import initializeMCParams, getAPIRequest
from agents import getAgentList, getAgentByAttrs
from jobs import appendToJobAgentList, addJob, getJobRunID, startJob, deleteJob, jobsMonitor

def doSomethingWhenJobIsDone(jobID):
    print("function called after the Job " + str(jobID) + " was done")
    deleteJob(jobID)

def addSimpleSyncJob(jobName, jobDescription, callbackfunction,
                    agent1IP, agent1Name, agent1Permission, agent1Folder,
                    agent2IP, agent2Name, agent2Permission, agent2Folder):
    jobAgentList = []
    jobAgentList = appendToJobAgentList(jobAgentList, getAgentByAttrs("ip", agent1IP, "name", agent1Name)[0]['id'], agent1Permission, agent1Folder)   
    jobAgentList = appendToJobAgentList(jobAgentList, getAgentByAttrs("ip", agent2IP, "name", agent2Name)[0]['id'], agent2Permission, agent2Folder)   
    newJob = addJob(jobName, jobDescription, "sync", jobAgentList)
    newJobRunID = getJobRunID(newJob['id'])
    myJobsMonitor.addMonitoredJob(newJobRunID['data'][0]['id'], callbackfunction)

# initialize MC
initializeMCParams(os.getenv('RESILIO_MC_URL'), 8443, os.getenv('RESILIO_AUTH_TOKEN'))

# quick test that we can actually connect to this Management Console
print(getAPIRequest("/api/v2/info"))

# start the job monitor
myJobsMonitor = jobsMonitor(10)

# get the list of agents
agents = getAgentList()

# add a job
addSimpleSyncJob("Sync Job 1", "", doSomethingWhenJobIsDone,
            "54.183.114.75", "Server 1", "rw", "/tmp/v2",
            "54.183.114.75", "Server 2", "ro", "/tmp/v21")

addSimpleSyncJob("Sync Job 2", "", doSomethingWhenJobIsDone,
            "54.183.114.75", "Server 1", "rw", "/tmp/v3",
            "54.183.114.75", "Server 2", "ro", "/tmp/v31")

addSimpleSyncJob("Sync Job 3", "", doSomethingWhenJobIsDone,
            "54.183.114.75", "Server 1", "rw", "/tmp/v4",
            "54.183.114.75", "Server 2", "ro", "/tmp/v41")





