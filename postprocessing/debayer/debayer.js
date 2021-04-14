module.exports = {
    start: start
}
const ipc = require('electron').ipcMain
const {chunksToLinesAsync, streamWrite} = require('@rauschma/stringio');
let running = true;
let pythonProcess = null;
let mainWindow = null;
function start(src, dst, event, mw) {
    mainWindow = mw;
    const spawn = require("child_process").spawn;

    
    pythonProcess = spawn('python3', ["python/debayering.py", src, '--out', dst]);
    push(pythonProcess.stdout, event)
    let done = false
    pythonProcess.on('exit', (code) => {
        event.sender.send('done')
        done = true
    })
    mainWindow.on('closed', function() {
        if(!done){
            streamWrite(pythonProcess.stdin, "1\n")
        }
    })
}
ipc.on('done', function (event) {
    mainWindow.loadFile('index.html')
})
ipc.on('toggle', function (event, derp) {
    running = !running;
    if(running){
        streamWrite(pythonProcess.stdin, "1\n")
    } else {
        streamWrite(pythonProcess.stdin, "0\n")
    }
})

async function push(readable, event) {
    for await (const line of chunksToLinesAsync(readable)){
        let S = line.replace("\n", "")
        if (S.includes('frame: ')){
            let out = S.replace('frame: ', "")
            let arr = out.split(" ")
            event.sender.send('update-progress', 'frame', +arr[0] + 0, +arr[1] + 0)
            event.sender.send('update-status', 'frame', arr[0])
        }
        if (S.includes('file: ')){
            let out = S.replace('file: ', "")
            let arr = out.split(" ")
            event.sender.send('update-progress', 'file', +arr[0] + 0, +arr[1] + 0)
            event.sender.send('update-status', 'file', arr[2])
        }
    }
}
