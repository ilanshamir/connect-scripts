import sys
import json

sys.path.append("./")
from communication import getAPIRequest

def getAgentList():
    return getAPIRequest("/api/v2/agents")

def getAgentByAttrs(attr1Name, attr1Value, attr2Name = None, attr2Value = None):
    agents = getAgentList()
    return [obj for obj in agents if ((obj[attr1Name]==attr1Value) and ((attr2Name==None) or (obj[attr2Name]==attr2Value)))]