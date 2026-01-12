const btnStart = document.getElementById('btnStart');
const btnStop = document.getElementById('btnStop');
const logsDiv = document.getElementById('logs');
const statusBadge = document.getElementById('status-indicator');

// --- Controlos de Botões ---

btnStart.addEventListener('click', () => {
    window.api.startBot();
});

btnStop.addEventListener('click', () => {
    window.api.stopBot();
});

// --- Receber Logs ---
window.api.onLog((message) => {
    // Evita duplicar quebras de linha
    const cleanMessage = message.trim();
    if (!cleanMessage) return;

    const entry = document.createElement('div');
    entry.className = 'log-entry';

    // Pequena coloração baseada no conteúdo
    if (cleanMessage.includes('[ERRO]') || cleanMessage.includes('Traceback')) {
        entry.style.color = '#ff6b6b';
    } else if (cleanMessage.includes('✅')) {
        entry.style.color = '#69f0ae';
    } else if (cleanMessage.includes('🎣')) {
        entry.style.color = '#40c4ff';
    }

    entry.innerText = cleanMessage;
    logsDiv.appendChild(entry);

    // Auto-scroll para o fundo
    logsDiv.scrollTop = logsDiv.scrollHeight;
});

// --- Atualizar Estado da UI ---
window.api.onStatusChange((status) => {
    if (status === 'running') {
        statusBadge.textContent = "A EXECUTAR";
        statusBadge.className = "status running";

        btnStart.disabled = true;
        btnStop.disabled = false;
        btnStart.style.opacity = "0.5";
    } else {
        statusBadge.textContent = "PARADO";
        statusBadge.className = "status stopped";

        btnStart.disabled = false;
        btnStop.disabled = true;
        btnStart.style.opacity = "1";
    }
});