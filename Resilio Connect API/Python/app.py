import sys
import json
import os
import logging
import getopt

sys.path.append("./")
from communication import initializeMCParams, getAPIRequest
from agents import getAgentList, getAgentByAttrs
from jobs import appendToJobAgentList, addJob, getJobRunID, startJob, deleteJob, jobsMonitor, addSimpleSyncJob, getJobRunStatus, getJobByID
from jobs_from_csv import jobsFromCSV

# default values
csvFileName = "./jobs.csv"
mcURL = os.getenv('RESILIO_MC_URL')
mcAuth = os.getenv('RESILIO_AUTH_TOKEN')
jobCount = 4
logFile = "./pymc.log"

def doSomethingWhenJobIsDone(jobID, runID):
    print("function called after the Job " + str(jobID) + " was done")
    logging.info("Job " + str(jobID) + " was completed and will be deleted")
    jobDetails = getJobByID(jobID)
    logging.info(json.dumps(jobDetails))
    runResult = getJobRunStatus(runID)
    logging.info(json.dumps(runResult))
    deleteJob(jobID)

# TO DO: change this to take command line arguments for csv file name, how many jobs, mc url, auth token
def getArgs():
    global csvFileName
    global mcURL
    global mcAuth
    global jobCount
    global logFile
    argumentList = sys.argv[1:]
    options = "c:j:m:a:o:h"
    long_options = ["csvfile", "jobcount", "mcaddress", "authtoken", "output", "help"]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-c", "--csvfile"):
                csvFileName = currentValue
            elif currentArgument in ("-j", "--jobcount"):
                jobCount = int(currentValue)
            elif currentArgument in ("-m", "--mcaddress"):
                mcURL = currentValue
            elif currentArgument in ("-a", "--authtoken"):
                mcAuth = currentValue
            elif currentArgument in ("-o", "--output"):
                logFile = currentValue
            elif currentArgument in ("-h", "--help"):
                print ("Diplaying Help")
    except getopt.error as err:
        # output error, and return with an error code
        sys.exit(str(err))

# read the command line args
getArgs()

# configure a log file
logging.basicConfig(filename=logFile, filemode='a', level=logging.INFO)

# initialize MC
initializeMCParams(mcURL, 8443, mcAuth)

# quick test that we can actually connect to this Management Console
print(getAPIRequest("/api/v2/info"))

# start the job monitor
myJobsMonitor = jobsMonitor(10)

# get the list of agents
agents = getAgentList()

# start jobs based on a csv
csvJobs = jobsFromCSV(csvFileName, myJobsMonitor, doSomethingWhenJobIsDone, jobCount, 10)


"""
# add a job
addSimpleSyncJob("Sync Job 1", "", doSomethingWhenJobIsDone,
            "54.183.114.75", "Server 1", "rw", "/tmp/v2",
            "54.183.114.75", "Server 2", "ro", "/tmp/v21")
"""




