module.exports = {
    start: start
}
function start(ipc) {

    document.querySelector('#srcbtn').addEventListener('click', function (event) {
         ipc.send('open-file-dialog', 'src')
    });

    document.querySelector('#dstbtn').addEventListener('click', function (event) {
        ipc.send('open-file-dialog', 'dst')
    });

    ipc.on('selected-directory', function (event, tag, path) {
        let id = tag + "-directory"
        document.getElementById(id).innerHTML = `${path}`
    });


    document.querySelector('#debayer').addEventListener('click', function (event) {
        let src = document.getElementById('src-directory').innerHTML
        let dst = document.getElementById('dst-directory').innerHTML
        if(src=="Choose Directory"){
            alert("Add an input directory")
            return
        }
        if(dst=="Choose Directory"){
            alert("Add an output directory")
            return
        }
        ipc.send('debayer-files', src, dst)
    });
    return function _end() { end() }
}
function end(ipc) {
    ipc.removeListener('selected-directory')
}

const ipc = require('electron').ipcRenderer
let end_f = start(ipc)
