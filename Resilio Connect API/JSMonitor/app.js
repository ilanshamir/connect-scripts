// @ts-check


const { initializeMCParams, getAPIRequest } = require('./communication');
const { getAgentProperty, setAgentProperty } = require('./data-store');
const { getJobProperty, setJobProperty } = require('./data-store');
const { enumerateAgents } = require('./data-store');
const { updateAgentList, updateJobsPerAgent } = require('./agents');
const { initializeTexting, SendMessage } = require ('./messaging');
const { findArrayDiff } = require('./utils');

//const { getAgentName, isAgentOnline, getAgentJobList } = require('./agents');

initializeMCParams("demo29.resilio.com", 8443, "6BZK5YQ6ER72NWP2GB7MYKEGA2AQZUXCCEVU7G7H4JTDGLDRNPMA");
console.log("some fake api response: " + getAPIRequest("/api/v2/jobs"));

updateAgentList();

setTimeout(function(){console.log (getAgentProperty( 1, "name"));}, 3000);
setTimeout(function(){console.log (getAgentProperty(1, "status"));}, 3000);

updateJobsPerAgent();

initializeTexting('+12029725018', process.env.TWILIOSID, process.env.TWILIOTOKEN);

endMessage('+15103652913', 'hello dawg');

setTimeout(function(){console.log (getJobProperty(2, "agents"));}, 3000);

setTimeout(function() {console.log(enumerateAgents());}, 5000);

console.log(findArrayDiff([1, 5, 17, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160], [1, 5, 17, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 165]));

