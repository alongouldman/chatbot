var axios = require('axios');

var axiosInstance = axios.create({
    baseURL: window.location.protocol + '//' + window.location.hostname + ':' + 5000
});

module.exports = axiosInstance;