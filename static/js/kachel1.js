// Kachel 1 - Auftragsverwaltung JavaScript - API Version

// Globale Auftragsdaten (werden von API geladen)
let auftraege = {
    offen: [],
    aktiv: [],
    archiv: []
};

// Alle Aufträge von API laden
async function ladeAuftraege() {
    try {
        showLoading('Aufträge werden geladen...');

        const data = await AuftraegeAPI.getAll();
        console.log('Aufträge geladen:', data);

        // Aufträge nach Status sortieren
        auftraege = {
            offen: data.results.filter(a => a.status === 'OFFEN'),
            aktiv: data.results.filter(a => a.status === 'AKTIV'),
            archiv: data.results.filter(a => ['ABGESCHLOSSEN', 'ABGESAGT'].includes(a.status))
        };

        // UI aktualisieren
        aktualisiereAnzeige();
        hideLoading();

    } catch (error) {
        hideLoading();
        console.error('Fehler beim Laden der Aufträge:', error);
        showError('Aufträge konnten nicht geladen werden');
    }
}

// Auftrag anlegen (über API)
async function auftragAnlegen() {
    const titel = document.getElementById('auftragTitel').value.trim();
    const beschreibung = document.getElementById('auftragBeschreibung').value.trim();

    if (!titel) {
        showError('Bitte einen Auftragstitel eingeben!');
        return;
    }

    if (!beschreibung) {
        showError('Bitte eine Beschreibung eingeben!');
        return;
    }

    const auftragData = {
        id: generiereAuftragID(),
        titel: titel,
        beschreibung: beschreibung,
        status: 'OFFEN',
        prioritaet: 'MITTEL'
    };

    try {
        showLoading('Auftrag wird gespeichert...');

        const neuerAuftrag = await AuftraegeAPI.create(auftragData);
        console.log('Auftrag erstellt:', neuerAuftrag);

        // Eingabefelder leeren
        document.getElementById('auftragTitel').value = '';
        document.getElementById('auftragBeschreibung').value = '';

        // Aufträge neu laden
        await ladeAuftraege();

        hideLoading();
        showSuccess('Auftrag erfolgreich angelegt!');

    } catch (error) {
        hideLoading();
        console.error('Fehler beim Erstellen des Auftrags:', error);
        showError('Auftrag konnte nicht gespeichert werden');
    }
}

// Auftrag zusagen (Status ändern über API)
async function auftragZusagen(auftragId) {
    try {
        showLoading('Auftrag wird zugesagt...');

        const auftragData = {
            status: 'AKTIV'
        };

        await AuftraegeAPI.update(auftragId, auftragData);
        await ladeAuftraege(); // Neu laden

        hideLoading();
        showSuccess('Auftrag zugesagt!');

    } catch (error) {
        hideLoading();
        console.error('Fehler beim Zusagen:', error);
        showError('Auftrag konnte nicht zugesagt werden');
    }
}

// Auftrag absagen (Status ändern über API)
async function auftragAbsagen(auftragId) {
    try {
        showLoading('Auftrag wird abgesagt...');

        const auftragData = {
            status: 'ABGESAGT'
        };

        await AuftraegeAPI.update(auftragId, auftragData);
        await ladeAuftraege(); // Neu laden

        hideLoading();
        showSuccess('Auftrag abgesagt');

    } catch (error) {
        hideLoading();
        console.error('Fehler beim Absagen:', error);
        showError('Auftrag konnte nicht abgesagt werden');
    }
}

// Auftrag abschließen (Status ändern über API)
async function auftragAbschliessen(auftragId) {
    try {
        showLoading('Auftrag wird abgeschlossen...');

        const auftragData = {
            status: 'ABGESCHLOSSEN'
        };

        await AuftraegeAPI.update(auftragId, auftragData);
        await ladeAuftraege(); // Neu laden

        hideLoading();
        showSuccess('Auftrag abgeschlossen!');

    } catch (error) {
        hideLoading();
        console.error('Fehler beim Abschließen:', error);
        showError('Auftrag konnte nicht abgeschlossen werden');
    }
}

// In andere Kachel laden (über URL-Parameter)
function ladeInKachel(kachelNr, status) {
    const relevantAuftraege = status === 'offen' ? auftraege.offen : auftraege.aktiv;

    if (relevantAuftraege.length === 0) {
        showError(`Keine ${status === 'offen' ? 'offenen' : 'aktiven'} Aufträge vorhanden!`);
        return;
    }

    // Weiterleitung zu Kachel mit Status-Parameter
    console.log(`Lade ${relevantAuftraege.length} ${status} Aufträge in Kachel ${kachelNr}`);
    showSuccess(`${relevantAuftraege.length} Aufträge werden in Kachel ${kachelNr} geladen...`);

    // Weiterleitung mit Status-Parameter (API wird dort die Daten laden)
    window.location.href = `/kachel${kachelNr}/?status=${status}`;
}

        // Anzeige aktualisieren
        function aktualisiereAnzeige() {
            // Offene Aufträge
            const offeneContainer = document.getElementById('offeneAuftraege');
            offeneContainer.innerHTML = auftraege.offen.map(auftrag => `
                <div class="auftrag">
                    <div class="auftrag-header">
                        <span class="auftrag-titel">${auftrag.titel}</span>
                        <span class="auftrag-id">${auftrag.id}</span>
                    </div>
                    <div class="auftrag-status">Status: ${auftrag.status}</div>
                    <div style="color: #aaa; font-size: 0.9em; margin: 5px 0;">${auftrag.beschreibung}</div>
                    <div class="auftrag-buttons">
                        <button class="btn btn-zusage" onclick="auftragZusagen('${auftrag.id}')">✓ Zusage</button>
                        <button class="btn btn-absage" onclick="auftragAbsagen('${auftrag.id}')">✗ Absage</button>
                    </div>
                </div>
            `).join('');
            
            // Aktive Aufträge
            const aktiveContainer = document.getElementById('aktiveAuftraege');
            aktiveContainer.innerHTML = auftraege.aktiv.map(auftrag => `
                <div class="auftrag">
                    <div class="auftrag-header">
                        <span class="auftrag-titel">${auftrag.titel}</span>
                        <span class="auftrag-id">${auftrag.id}</span>
                    </div>
                    <div class="auftrag-status">Status: ${auftrag.status}</div>
                    <div style="color: #aaa; font-size: 0.9em; margin: 5px 0;">${auftrag.beschreibung}</div>
                    <div style="color: #81c784; font-size: 0.85em; margin: 5px 0;">Zugesagt: ${auftrag.zugesagtAm}</div>
                    <div class="auftrag-buttons">
                        <button class="btn btn-abschliessen" onclick="auftragAbschliessen('${auftrag.id}')">✓ Auftrag Abschließen</button>
                    </div>
                </div>
            `).join('');
            
            // Archiv
            const archivContainer = document.getElementById('archivAuftraege');
            archivContainer.innerHTML = auftraege.archiv.map(auftrag => `
                <div class="auftrag" style="opacity: 0.7;">
                    <div class="auftrag-header">
                        <span class="auftrag-titel">${auftrag.titel}</span>
                        <span class="auftrag-id">${auftrag.id}</span>
                    </div>
                    <div class="auftrag-status">Status: ${auftrag.status}</div>
                    <div style="color: #aaa; font-size: 0.9em; margin: 5px 0;">${auftrag.beschreibung}</div>
                    <div style="color: ${auftrag.status === 'ABGESCHLOSSEN' ? '#81c784' : '#ef5350'}; font-size: 0.85em; margin: 5px 0;">
                        ${auftrag.status === 'ABGESCHLOSSEN' ? 'Abgeschlossen' : 'Abgesagt'}: 
                        ${auftrag.abgeschlossenAm || auftrag.abgesagtAm}
                    </div>
                </div>
            `).join('');
        }

        // Notification anzeigen
        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 25px;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                z-index: 1000;
                animation: slideInRight 0.3s ease;
                box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            `;
            
            switch(type) {
                case 'success':
                    notification.style.background = 'linear-gradient(45deg, #4caf50, #66bb6a)';
                    break;
                case 'error':
                    notification.style.background = 'linear-gradient(45deg, #f44336, #ef5350)';
                    break;
                case 'info':
                    notification.style.background = 'linear-gradient(45deg, #2196f3, #42a5f5)';
                    break;
            }
            
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }

        // Animation Styles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);

        // Enter-Taste für Auftrag anlegen (nur im Titel-Feld)
        document.getElementById('auftragTitel').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                auftragAnlegen();
            }
        });

        // Demo-Daten entfernt - Daten kommen jetzt von API

        // Beim Laden der Seite - API-Daten laden
        document.addEventListener('DOMContentLoaded', async function() {
            console.log('🚀 Kachel 1 - Auftragsverwaltung geladen');

            // Aufträge von API laden
            await ladeAuftraege();

            // Auto-Refresh alle 60 Sekunden
            setInterval(ladeAuftraege, 60000);
        });