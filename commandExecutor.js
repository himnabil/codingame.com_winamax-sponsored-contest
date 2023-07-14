const { spawn } = require('child_process');
const fs = require('fs');

function executeCommand(inputFilePath, command, args, stderrFilePath) {
    return new Promise((resolve, reject) => {
        let outputData = '';

        const commandProcess = spawn(command, args);

        const inputFileStream = fs.createReadStream(inputFilePath);
        inputFileStream.pipe(commandProcess.stdin);

        commandProcess.stdout.on('data', (data) => {
            outputData += data;
        });

        const stderrFileStream = fs.createWriteStream(stderrFilePath);
        commandProcess.stderr.pipe(stderrFileStream);

        commandProcess.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`command exited with code ${code}`));
            } else {
                resolve(outputData);
            }
        });
    });
}

module.exports = executeCommand;
