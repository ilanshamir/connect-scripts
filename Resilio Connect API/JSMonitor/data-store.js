// @ts-check
module.exports = {
    setAgentProperty,
    getAgentProperty,
    setJobProperty,
    getJobProperty,
};

var agents = {},
    jobs = {},
    dict = Object.assign({}, agents, jobs);

function setAgentProperty(id, propertyName, value,) {
    if (!dict.hasOwnProperty(id)) {
        dict[id] = {[propertyName]: value};
    } else {
        dict[id][propertyName] = value;
    }
}

function getAgentProperty(id, propertyName) {
    if (dict.hasOwnProperty(id) && dict[id].hasOwnProperty(propertyName)) {
        return dict[id][propertyName];
    } else {
        throw "No such id or propertyName - " + id + "," + propertyName;
    }
}

function setJobProperty(id, propertyName, value) {
    if (!jobs.hasOwnProperty(id)) {
        jobs[id] = {[propertyName]: value};
    } else {
        jobs[id][propertyName] = value;
    }
}

function getJobProperty(id, propertyName) {
    if (jobs.hasOwnProperty(id) && jobs[id].hasOwnProperty(propertyName)) {
        return jobs[id][propertyName];
    } else {
        throw "No such id or propertyName";
    }    
}
