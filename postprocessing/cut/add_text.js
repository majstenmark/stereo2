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

const CHANGE_FRAME = 10
const CLOSE = 11
const ADD_TEXT= 12
const TEXT_LEFT= 13
const TEXT_RIGHT= 14
const TEXT_UP= 15
const TEXT_DOWN= 16
const TEXT_SAVE = 17
const CHANGE_DOWN = 18
const CHANGE_UP = 19
const TO_GENERATE = 20
const GENERATE = 21


function start(src, dst, event, mw) {
    mainWindow = mw;
    if(pythonProcess != null){ 
        return
    }
    const spawn = require("child_process").spawn;
    
    pythonProcess = spawn('python3', ["python/edit.py", '--input', src, '--out', dst]);
    push(pythonProcess.stdout, event)
 
    pythonProcess.on('exit', (code) => {
        if(!closed){
            event.sender.send('done')
            pythonProcess = null
            event.sender.send('update-status', 'frame', 'Python process exited')
            done = true
        }
    })
    mainWindow.on('closed', function() {
        if(!done){
            streamWrite(pythonProcess.stdin, CLOSE + "\n")
        }
        closed = true
    })
    
}


ipc.on('change_frame', function (event, frame) {
    streamWrite(pythonProcess.stdin, CHANGE_FRAME + "\n")
    streamWrite(pythonProcess.stdin, `${frame}`  + "\n")
    
})

ipc.on('add_text', function (event, text) {
    streamWrite(pythonProcess.stdin, ADD_TEXT + "\n")

   // streamWrite(pythonProcess.stdin, "Help text\n")
    streamWrite(pythonProcess.stdin, `${text}`  + "\n")
    
})

ipc.on('text_left', function (event, derp) {
    
        streamWrite(pythonProcess.stdin, TEXT_LEFT + "\n")
    
})

ipc.on('text_right', function (event, derp) {
    
        streamWrite(pythonProcess.stdin, TEXT_RIGHT + "\n")
    
})


ipc.on('text_up', function (event, derp) {
   
        streamWrite(pythonProcess.stdin,  TEXT_UP + "\n")
    
})


ipc.on('generate', function (event, text) {

    streamWrite(pythonProcess.stdin, TO_GENERATE + "\n")
    streamWrite(pythonProcess.stdin, `${text}`  + "\n")
})


ipc.on('change_down', function (event, derp) {
    
        streamWrite(pythonProcess.stdin, CHANGE_DOWN + "\n")
    
})


ipc.on('change_up', function (event, derp) {
  
        streamWrite(pythonProcess.stdin, CHANGE_UP + "\n")
    
})

ipc.on('text_save', function (event, derp) {
   
        streamWrite(pythonProcess.stdin, TEXT_SAVE + "\n")
    
})

async function push(readable, event) {
    //if(!done){
        for await (const line of chunksToLinesAsync(readable)){
            let S = line.replace("\n", "")
            if (S.includes('text: ')){
                let out = S.replace('text: ', "")
                let arr = out.split(" ")
                event.sender.send('update-image', 'image', arr[0])   
            }
            if (S.includes('frame: ')){
                let out = S.replace('frame: ', "")
                //let arr = out.split(" ")
                event.sender.send('update-status', 'frame', out)
                
            }
        }
    //}
}
