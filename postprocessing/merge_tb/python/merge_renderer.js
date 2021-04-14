module.exports = {
    start: start
}

function start(ipc) {
    ipc.on('update-progress', function (event, id, val, max) {
        let e_id = id + "-progress"
        let progress = document.getElementById(e_id)
        progress.max = max
        progress.value = val
    });
    ipc.on('update-status', function (event, id, val) {
        let h_id = id + "-status"
        document.getElementById(h_id).innerHTML = `${val}`
    });
    let pause_btn = document.querySelector('#toggle_play')
    ipc.on('done', function (event) {
        pause_btn.innerHTML = "Finish"
        pause_btn.removeEventListener('click', toggle)
        pause_btn.addEventListener('click', function (event) {
            ipc.send('done')
        });
    });
    pause_btn.addEventListener('click', toggle);
    return function _end(){ end() }
}
function toggle(event) {
    let pause_btn = document.querySelector('#toggle_play')
    console.log('toggle');
    ipc.send('toggle', 'herp')
    console.log(pause_btn.value);
    if(pause_btn.innerHTML == "Pause") {
        pause_btn.innerHTML = "Resume"
    } else{
        pause_btn.innerHTML = "Pause"
    }
}
function end(ipc) {
    ipc.removeListener('update-progress');
    ipc.removeListener('done');
}

const ipc = require('electron').ipcRenderer
let end_f = start(ipc)
