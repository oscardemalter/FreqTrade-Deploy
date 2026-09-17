const $ = id => document.getElementById(id);
let currentLang = 'fr', selectedAgent = 'jarvis', audioCtx = null, ecoMode = localStorage.getItem('ub_eco') === '1';

const dict = {
    fr: {
        agents_title: "ROBOTS AGENTS IA — 9/9",
        hero_title: "JARVIS — Cerveau Orchestrateur",
        hero_subtitle: "MojoCode AI • Scalping 24/7 • Futures • Risk Edge",
        lbl_mode: "Mode",
        lbl_connector: "Connecteur",
        lbl_min_invest: "Min. Invest",
        lbl_ai_status: "Statut IA",
        status_ai_val: "OPÉRATIONNEL",
        btn_settings: "Réglages",
        btn_academy: "Académie",
        btn_chat: "Chat IA",
        btn_radar: "Radar 50",
        terminal_title: "TERMINAL ULTRA-SÉCURISÉ ÜBERGESTALT",
        txt_radar_head: "📡 RADAR TOP 50 CRYPTOS",
        txt_signals_head: "🎯 SIGNAUX SQUEEZE & REVERSAL",
        txt_quote_head: "📜 SAGESSE TRADER",
        txt_logout: "Déconnexion",
        modal_settings_title: "⚙️ RÉGLAGES & CONFIGURATION SÉCURISÉE",
        lbl_security_pass: "🔐 Sécurité & Accès Confidentiel (Mot de passe)",
        btn_save_pass: "Mettre à jour le mot de passe",
        lbl_mode_switch_title: "🔀 Mode de Trading (Live vs Paper)",
        lbl_okx_conn_title: "🔗 Connexion OKX & Plateformes API (4 Options)",
        lbl_halo_risk: "🛡️ HALO Risk Management",
        lbl_freqtrade_engine: "🤖 FreqTrade Quant Integration",
        modal_academy_title: "🎓 ACADÉMIE TRADING MOJOCODE",
        modal_chat_title: "💬 CHAT INTERACTIF AGENT IA",
        btn_send_chat: "Envoyer"
    },
    en: {
        agents_title: "AI AGENT BOTS — 9/9",
        hero_title: "JARVIS — Central Brain",
        hero_subtitle: "MojoCode AI • Scalping 24/7 • Futures • Risk Edge",
        lbl_mode: "Mode",
        lbl_connector: "Connector",
        lbl_min_invest: "Min. Invest",
        lbl_ai_status: "AI Status",
        status_ai_val: "OPERATIONAL",
        btn_settings: "Settings",
        btn_academy: "Academy",
        btn_chat: "AI Chat",
        btn_radar: "Radar 50",
        terminal_title: "ÜBERGESTALT ULTRA-SECURE TERMINAL",
        txt_radar_head: "📡 RADAR TOP 50 CRYPTOS",
        txt_signals_head: "🎯 SQUEEZE & REVERSAL SIGNALS",
        txt_quote_head: "📜 TRADER WISDOM",
        txt_logout: "Logout",
        modal_settings_title: "⚙️ SETTINGS & SECURE CONFIGURATION",
        lbl_security_pass: "🔐 Security & Confidential Access (Password)",
        btn_save_pass: "Update Access Password",
        lbl_mode_switch_title: "🔀 Trading Mode (Live vs Paper)",
        lbl_okx_conn_title: "🔗 OKX Connection & API Platforms (4 Options)",
        lbl_halo_risk: "🛡️ HALO Risk Management",
        lbl_freqtrade_engine: "🤖 FreqTrade Quant Integration",
        modal_academy_title: "🎓 MOJOCODE TRADING ACADEMY",
        modal_chat_title: "💬 INTERACTIVE AI AGENT CHAT",
        btn_send_chat: "Send"
    }
};

function appendTerminal(m) {
    const t = $('terminal'); if (!t) return;
    const p = document.createElement('p'); p.textContent = m;
    const pr = t.querySelector('.prompt');
    if (pr) t.insertBefore(p, pr); else t.appendChild(p);
    t.scrollTop = t.scrollHeight;
}

function playTone(f, d) {
    try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const o = audioCtx.createOscillator(), g = audioCtx.createGain();
        o.frequency.value = f; g.gain.value = .06;
        o.connect(g); g.connect(audioCtx.destination);
        o.start(); g.gain.exponentialRampToValueAtTime(.001, audioCtx.currentTime + d);
        o.stop(audioCtx.currentTime + d);
    } catch (_) {}
}

function playSound(n) { playTone(n === 'signal' ? 880 : 660, .08); }
function toggleSound() { playSound('click'); }
function toggleEco() {
    ecoMode = !ecoMode;
    localStorage.setItem('ub_eco', ecoMode ? '1' : '0');
    document.body.classList.toggle('eco', ecoMode);
    appendTerminal(ecoMode ? '> Mode Éco Activé' : '> Mode Éco Désactivé');
}

function setLang(l) {
    currentLang = l;
    $('lang-fr').classList.toggle('active', l === 'fr');
    $('lang-en').classList.toggle('active', l === 'en');

    const t = dict[l] || dict.fr;
    for (let k in t) {
        if ($(k)) {
            if ($(k).tagName === 'INPUT') $(k).value = t[k];
            else $(k).textContent = t[k];
        }
    }

    // Translate Agent Roles
    document.querySelectorAll('.role-desc').forEach(el => {
        el.textContent = el.getAttribute('data-' + l) || el.getAttribute('data-fr');
    });

    // Translate Academy titles
    document.querySelectorAll('.level-title').forEach(el => {
        el.textContent = el.getAttribute('data-' + l) || el.getAttribute('data-fr');
    });

    appendTerminal(l === 'fr' ? '> Langue basculée en Français' : '> Language switched to English');
}

function updateClock() {
    const e = $('clock-time');
    if (e) e.textContent = new Date().toISOString().substr(11, 8);
}
setInterval(updateClock, 1000); updateClock();

function openSettings() { $('settings-modal').classList.remove('hidden'); refreshStatus(); }
function openAcademy() { $('academy-modal').classList.remove('hidden'); }
function openChat() { $('chat-modal').classList.remove('hidden'); }
function closeModal(id) { $(id).classList.add('hidden'); }
function show(id) { $(id).classList.toggle('hidden'); }

function selectAgent(id) {
    selectedAgent = id;
    document.querySelectorAll('.agent-card').forEach(c => c.classList.remove('selected'));
    const c = document.querySelector('.agent-card[data-agent="' + id + '"]');
    if (c) c.classList.add('selected');
    appendTerminal('> Agent sélectionné : ' + id.toUpperCase());
}

async function sendChat() {
    const i = $('chat-input'); const q = i.value.trim(); if (!q) return; i.value = '';
    const h = $('chat-history');
    h.innerHTML += '<div class="chat-msg user">Vous : ' + q + '</div>';

    try {
        const r = await (await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                agent_id: selectedAgent,
                question: q,
                lang: currentLang,
                deep: $('chat-deep').checked
            })
        })).json();

        h.innerHTML += '<div class="chat-msg agent"><strong>' + r.agent.toUpperCase() + '</strong> : ' + r.reply + '</div>';
        h.scrollTop = h.scrollHeight;
    } catch (e) {
        h.innerHTML += '<div class="chat-msg error">Erreur de communication avec l\'Agent.</div>';
    }
}

async function showLevel(id) {
    const c = $('lessons-container'); c.classList.remove('hidden');
    const levels = await (await fetch('/api/academy')).json();
    const lv = levels.find(x => x.id === id); if (!lv) return;

    const title = currentLang === 'fr' ? lv.title_fr : lv.title_en;
    let html = '<h3>' + title + '</h3>';

    lv.lessons.forEach(l => {
        const ltitle = currentLang === 'fr' ? l.title_fr : l.title_en;
        const lcontent = currentLang === 'fr' ? l.content_fr : l.content_en;
        html += '<div class="lesson-item" onclick="this.querySelector(\'.lesson-content\').classList.toggle(\'hidden\')"><h4>' + ltitle + '</h4><div class="lesson-content hidden">' + lcontent + '</div></div>';
    });
    c.innerHTML = html;
}

async function saveAccessPassword() {
    const pass = $('new-access-pass').value.trim();
    if (!pass) return alert('Veuillez saisir un mot de passe.');
    const r = await (await fetch('/api/settings/password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: pass })
    })).json();
    if (r.success) {
        alert('Mot de passe mis à jour avec succès !');
        $('new-access-pass').value = '';
        appendTerminal('> 🔐 Mot de passe mis à jour');
    } else {
        alert('Erreur: ' + (r.reason || 'Impossible de mettre à jour'));
    }
}

async function saveRisk() {
    await fetch('/api/settings/risk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ risk_pct: parseFloat($('set-risk').value), max_positions: parseInt($('set-positions').value) })
    });
    appendTerminal('> 🛡️ Paramètres de Risque HALO enregistrés');
}

async function refreshRadar() {
    const b = $('radar-list'); const sl = $('signals-list'); if (!b) return;
    try {
        const r = await (await fetch('/api/radar')).json();
        const wl = r.watchlist || [];

        b.innerHTML = wl.slice(0, 15).map(w =>
            '<div class="card"><span>' + w.symbol.replace('/USDT:USDT', '').replace('/USDT', '') + '</span><strong class="' + (w.pct >= 0 ? 'ok' : 'mode-live') + '">' + (w.pct >= 0 ? '+' : '') + w.pct + '%</strong></div>'
        ).join('') || '<p class="muted">Analyse en cours...</p>';

        const squeezes = wl.filter(w => w.squeeze || w.reversal !== "none");
        if (squeezes.length > 0) {
            sl.innerHTML = squeezes.map(s =>
                '<div class="card card-squeeze"><span>' + s.symbol.split('/')[0] + '</span><strong class="squeeze-tag">' + (s.squeeze ? 'SQUEEZE ' : '') + s.reversal.toUpperCase() + '</strong></div>'
            ).join('');
        } else {
            sl.innerHTML = '<p class="muted">Aucun Squeeze majeur sur les 50 Cryptos.</p>';
        }
    } catch (e) {
        b.innerHTML = '<p class="muted">Erreur de synchronisation Radar.</p>';
    }
}

async function refreshStatus() {
    try {
        const s = await (await fetch('/api/status')).json();
        const m = $('current-mode');
        if (m) {
            m.textContent = (s.trading_mode || 'paper').toUpperCase();
            m.className = s.trading_mode === 'live' ? 'mode-live' : 'mode-paper';
        }
        const sw = $('mode-live-switch'); if (sw) sw.checked = s.trading_mode === 'live';
        const ml = $('mode-label'); if (ml) ml.textContent = s.trading_mode === 'live' ? 'LIVE (Trading Réel)' : 'PAPER (Démo Simulée)';
        const vb = $('verification-badge'); if (vb && s.verification) vb.textContent = 'Pine Script v6 Verification: ' + (s.verification.verified ? 'VÉRIFIÉ ✅' : 'En attente ⏳');
        const ft = $('ft-status'); if (ft) ft.textContent = 'Bridge FreqTrade: ' + (s.bridge && s.bridge.running ? 'ACTIF 🟢' : 'INACTIF 🔴');
    } catch (e) {}
}

async function toggleMode(wantLive) {
    if (wantLive) {
        if (!confirm('ATTENTION: Passage en TRADING RÉEL. Des fonds réels seront engagés. Continuer ?')) { refreshStatus(); return; }
        if (prompt('Tapez exactement : LIVE pour confirmer') !== 'LIVE') { refreshStatus(); return; }
    } else {
        if (!confirm('Repasser en mode PAPER (Démo simulée) ?')) { refreshStatus(); return; }
    }
    const d = await (await fetch('/api/settings/mode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: wantLive ? 'live' : 'paper', confirm_live: wantLive })
    })).json();
    appendTerminal(d.success ? '> 🔀 NOUVEAU MODE = ' + d.mode.toUpperCase() : '> ⛔ Erreur: ' + (d.reason || 'Refus'));
    refreshStatus();
}

async function saveOkxKeys() {
    const r = await (await fetch('/api/okx/keys', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: $('okx-key').value, api_secret: $('okx-secret').value, passphrase: $('okx-pass').value })
    })).json();
    appendTerminal(r.success ? '> ✅ Clés OKX enregistrées & vérifiées' : '> ❌ Erreur OKX: ' + (r.msg || r.reason));
    refreshStatus();
}

async function fastConnect() {
    const r = await (await fetch('/api/okx/fast_connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: $('okx-key').value, api_secret: $('okx-secret').value, passphrase: $('okx-pass').value, demo: $('okx-demo').checked })
    })).json();
    appendTerminal(r.success ? '> ⚡ Fast Connect OKX réussi !' : '> ❌ Connexion échouée: ' + (r.msg || r.reason));
    refreshStatus();
}

function oauthStart() { location.href = '/api/okx/oauth/start'; }

async function saveSignalBot() {
    const r = await (await fetch('/api/okx/signalbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: $('sb-url').value, secret: $('sb-secret').value })
    })).json();
    appendTerminal(r.success ? '> 📡 Webhook Signal Bot OKX configuré' : '> ❌ Erreur: ' + r.reason);
}

async function saveWallet() {
    const r = await (await fetch('/api/okx/wallet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: $('w-addr').value, chain: $('w-chain').value })
    })).json();
    appendTerminal(r.success ? '> 👛 Web3 Wallet connecté' : '> ❌ Erreur: ' + r.reason);
}

async function startFtBridge() {
    const s = await (await fetch('/api/status')).json(); let cl = false;
    if (s.trading_mode === 'live') {
        if (!confirm('Démarrer FreqTrade en Mode RÉEL ?')) return;
        if (prompt('Tapez : LIVE') !== 'LIVE') return; cl = true;
    }
    const r = await (await fetch('/api/freqtrade/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ confirm_live: cl })
    })).json();
    appendTerminal(r.success ? '> 🤖 FreqTrade démarré' : '> ❌ Erreur FreqTrade: ' + r.reason);
    refreshStatus();
}

async function stopFtBridge() {
    await fetch('/api/freqtrade/stop', { method: 'POST' });
    appendTerminal('> 🤖 FreqTrade arrêté');
    refreshStatus();
}

async function runFtBacktest() {
    const r = await (await fetch('/api/freqtrade/backtest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ days: 30 })
    })).json();
    appendTerminal(r.success ? '> 📊 Backtest FreqTrade terminé' : '> ❌ Erreur Backtest: ' + r.reason);
}

document.addEventListener('DOMContentLoaded', () => {
    refreshStatus();
    refreshRadar();
    setInterval(refreshRadar, ecoMode ? 60000 : 20000);
    appendTerminal('> Übergestalt v2026 en ligne — Mode PAPER Sécurisé par défaut.');
});
