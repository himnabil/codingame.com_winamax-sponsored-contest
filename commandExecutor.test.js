const fs = require('fs');
const path = require('path');
const executeCommand = require('./commandExecutor');
const { readConfig } = require('./config');

describe('Command Executor', () => {
    const configFilePath = './config.yml';
    const { command, args } = readConfig(configFilePath);

    const testDirPath = './files'; // replace with your test files directory
    const stderrDirPath = './stderr'; // replace with your stderr files directory

    const files = fs.readdirSync(testDirPath);
    const inputFiles = files.filter(file => file.startsWith('input'));
    const expectedFiles = files.filter(file => file.startsWith('expected'));

    if (inputFiles.length !== expectedFiles.length) {
        console.error('Mismatch in number of input and expected output files');
        return;
    }

    inputFiles.forEach((inputFile, index) => {
        it(`should execute command and produce correct output for ${inputFile}`, async () => {
            const inputFilePath = path.join(testDirPath, inputFile);
            const expectedFilePath = path.join(testDirPath, expectedFiles[index]);

            const stderrFileName = 'stderr' + inputFile.replace('input', '');
            const stderrFilePath = path.join(stderrDirPath, stderrFileName);

            const output = await executeCommand(inputFilePath, command, args, stderrFilePath);

            const expected = fs.readFileSync(expectedFilePath, 'utf8');

            expect(output).toEqual(expected);
        });
    });
});
