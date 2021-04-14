module.exports = {
    start: start
}
const ipc = require('electron').ipcMain
const {chunksToLinesAsync, streamWrite} = require('@rauschma/stringio');
let running = true;
let pythonProcess = null;
let mainWindow = null;
let done = false;
let closed = false;

function start(src, dst, event, mw) {
    mainWindow = mw;
    const spawn = require("child_process").spawn;
    
    pythonProcess = spawn('python3', ["python/cut.py", '--input', src, '--out', dst]);
    push(pythonProcess.stdout, event)
 
    pythonProcess.on('exit', (code) => {
        if(!closed){
            event.sender.send('done')
            done = true
        }
    })
    mainWindow.on('closed', function() {
        if(!done){
            streamWrite(pythonProcess.stdin, "1\n")
        }
        closed = true
    })
    
}

ipc.on('toggle', function (event, derp) {
    running = !running;
    if(running){
        streamWrite(pythonProcess.stdin, "1\n")
    } else {
        streamWrite(pythonProcess.stdin, "0\n")
    }
})
ipc.on('backward_step', function (event, derp) {
    if(!running){
        streamWrite(pythonProcess.stdin, "2\n")
    }
})

ipc.on('add_cut', function (event, derp) {
    if(!running){
        streamWrite(pythonProcess.stdin, "4\n")
    }
})

ipc.on('forward_step', function (event, derp) {
    if(!running){
        streamWrite(pythonProcess.stdin, "3\n")
    }
})

ipc.on('kill_cut', function (event, derp) {
    if(!running){
        streamWrite(pythonProcess.stdin, "5\n")
    }
})


async function push(readable, event) {
    //if(!done){
        for await (const line of chunksToLinesAsync(readable)){
            let S = line.replace("\n", "")
            if (S.includes('frame: ')){
                let out = S.replace('frame: ', "")
                let arr = out.split(" ")
                event.sender.send('update-status', 'frame', arr[0])
                
            }
            if (S.includes('image: ')){
                let out = S.replace('image: ', "")
                let arr = out.split(" ")
                event.sender.send('update-image', 'image', arr[0])   
            }
        }
    //}
}
