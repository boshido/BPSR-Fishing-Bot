const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let botProcess = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 900,
        height: 700,
        minWidth: 600,
        minHeight: 500,
        backgroundColor: '#1a1a1a',
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true
        },
        autoHideMenuBar: true
    });

    mainWindow.loadFile('index.html');
}

// Lógica para encontrar o EXE do Python
function getBotPath() {
    const isDev = !app.isPackaged;
    const exeName = 'bpsr-fishingbot.exe';

    if (isDev) {
        // Em desenvolvimento, procura na pasta local resources
        return path.join(__dirname, 'resources', 'executables', exeName);
    } else {
        // Em produção (instalado), procura na pasta resources do Electron
        return path.join(process.resourcesPath, 'executables', exeName);
    }
}

// --- Eventos IPC (Comunicação UI -> Backend) ---

ipcMain.on('start-bot', (event) => {
    if (botProcess) return; // Evita abrir duas vezes

    const botPath = getBotPath();
    console.log("A iniciar bot em:", botPath);

    try {
        // Inicia o processo Python
        botProcess = spawn(botPath);

        // Envia mensagem de sucesso para a UI
        if (mainWindow) mainWindow.webContents.send('bot-status', 'running');

        // Captura o output normal (print)
        botProcess.stdout.on('data', (data) => {
            const message = data.toString();
            if (mainWindow) mainWindow.webContents.send('bot-log', message);
        });

        // Captura erros
        botProcess.stderr.on('data', (data) => {
            const message = data.toString();
            if (mainWindow) mainWindow.webContents.send('bot-log', `[ERRO] ${message}`);
        });

        // Quando o processo fecha
        botProcess.on('close', (code) => {
            if (mainWindow) {
                mainWindow.webContents.send('bot-log', `[SISTEMA] Bot desligado (Código: ${code})`);
                mainWindow.webContents.send('bot-status', 'stopped');
            }
            botProcess = null;
        });

    } catch (error) {
        if (mainWindow) mainWindow.webContents.send('bot-log', `[FALHA CRÍTICA] Não foi possível iniciar: ${error.message}`);
        botProcess = null;
    }
});

ipcMain.on('stop-bot', () => {
    if (botProcess) {
        botProcess.kill(); // Mata o processo
        botProcess = null;
        if (mainWindow) mainWindow.webContents.send('bot-status', 'stopped');
    }
});

// Ciclo de Vida da Aplicação
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    // Garante que o bot morre se fechares a janela
    if (botProcess) botProcess.kill();
    if (process.platform !== 'darwin') app.quit();
});