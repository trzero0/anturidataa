import {spawn} from "child_process";

const executePython = (script, args = [] as any) => {
    const py = spawn('python', [script, ...args]);

    return new Promise((resolve, reject) => {
        let output = '';

        py.stdout.on('data', (data) => {
            output += data.toString();  // Capture raw data from Python script
            console.log('Raw output:', data.toString());  // Log raw output for debugging
        });

        py.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
            reject(`Error in Python script: ${data}`);
        });

        py.on('exit', (code) => {
            if (code === 0) {
                try {
                    console.log('Raw output to parse:', output);  // Log the full output for debugging
                    resolve(JSON.parse(output));  // Try parsing the JSON output
                } catch (err) {
                    reject(`Failed to parse JSON output: ${err.message}`);
                }
            } else {
                reject(`Python script exited with code ${code}`);
            }
        });
    });
};

export default executePython