const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
    startBot: () => ipcRenderer.send('start-bot'),
    stopBot: () => ipcRenderer.send('stop-bot'),

    // Receber logs do backend
    onLog: (callback) => ipcRenderer.on('bot-log', (event, message) => callback(message)),

    // Receber atualizações de estado (Running/Stopped)
    onStatusChange: (callback) => ipcRenderer.on('bot-status', (event, status) => callback(status))
});