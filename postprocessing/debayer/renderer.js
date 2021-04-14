const index = require('./index_renderer.js')
const debayer = require('./debayer_renderer.js')
const ipc = require('electron').ipcRenderer
let end_index = index.start(ipc)
let end_debayer = debayer.start(ipc)
