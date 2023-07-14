const fs = require('fs');
const yaml = require('js-yaml');

function readConfig(configFilePath) {
    const yamlStr = fs.readFileSync(configFilePath, 'utf8');
    return yaml.load(yamlStr);
}
module.exports = { readConfig };
