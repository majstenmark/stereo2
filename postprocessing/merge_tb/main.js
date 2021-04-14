// Modules to control application life and create native browser window
const {app, BrowserWindow} = require('electron')
const path = require('path')


// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    icon: __dirname + "/icon.png",
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
        nodeIntegration: true
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('index.html')

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) createWindow()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

const dialog = require('electron').dialog
const ipc = require('electron').ipcMain

ipc.on('open-file-dialog', function (event, tag) {
  dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory']
  }, function (files) {
    if (files) event.sender.send(`selected-directory`, tag, files)
  })
})

ipc.on('list-files', function (event, src) {
    const spawn = require("child_process").spawn;

    const pythonProcess = spawn('python', ["listf.py", src]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(data.toString()); // Do something with the data returned from python script
    });
})
ipc.on('merge-files', function (event, src, dst, onefile, top) {
    mainWindow.loadFile('merge.html')
    //event.sender.send('start', 'debayer')
    const merge = require('./merge.js')
    merge.start(src, dst, event, mainWindow, onefile, top);
})
