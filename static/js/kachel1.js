// Kachel 1 - Auftragsverwaltung JavaScript

// Auftragsdaten speichern
        let auftraege = {
            offen: [],
            aktiv: [],
            archiv: []
        };
        
        let naechsteId = 1001; // Startet bei ID 1001

        // Auftrag anlegen
        function auftragAnlegen() {
            const titel = document.getElementById('auftragTitel').value.trim();
            const beschreibung = document.getElementById('auftragBeschreibung').value.trim();
            
            if (!titel) {
                alert('Bitte einen Auftragstitel eingeben!');
                return;
            }
            
            if (!beschreibung) {
                alert('Bitte eine Beschreibung eingeben!');
                return;
            }
            
            const neuerAuftrag = {
                id: `PW-${naechsteId++}`,
                titel: titel,
                beschreibung: beschreibung,
                status: 'OFFEN',
                erstelltAm: new Date().toLocaleString('de-DE')
            };
            
            auftraege.offen.push(neuerAuftrag);
            
            // Eingabefelder leeren
            document.getElementById('auftragTitel').value = '';
            document.getElementById('auftragBeschreibung').value = '';
            
            // UI aktualisieren
            aktualisiereAnzeige();
            
            // Visuelle Bestätigung
            showNotification('Auftrag erfolgreich angelegt!', 'success');
        }

        // Auftrag zusagen
        function auftragZusagen(auftragId) {
            const index = auftraege.offen.findIndex(a => a.id === auftragId);
            if (index !== -1) {
                const auftrag = auftraege.offen.splice(index, 1)[0];
                auftrag.status = 'AKTIV';
                auftrag.zugesagtAm = new Date().toLocaleString('de-DE');
                auftraege.aktiv.push(auftrag);
                aktualisiereAnzeige();
                showNotification('Auftrag zugesagt!', 'success');
            }
        }

        // Auftrag absagen
        function auftragAbsagen(auftragId) {
            const index = auftraege.offen.findIndex(a => a.id === auftragId);
            if (index !== -1) {
                const auftrag = auftraege.offen.splice(index, 1)[0];
                auftrag.status = 'ABGESAGT';
                auftrag.abgesagtAm = new Date().toLocaleString('de-DE');
                auftraege.archiv.push(auftrag);
                aktualisiereAnzeige();
                showNotification('Auftrag abgesagt!', 'error');
            }
        }

        // Auftrag abschließen
        function auftragAbschliessen(auftragId) {
            const index = auftraege.aktiv.findIndex(a => a.id === auftragId);
            if (index !== -1) {
                const auftrag = auftraege.aktiv.splice(index, 1)[0];
                auftrag.status = 'ABGESCHLOSSEN';
                auftrag.abgeschlossenAm = new Date().toLocaleString('de-DE');
                auftraege.archiv.push(auftrag);
                aktualisiereAnzeige();
                showNotification('Auftrag abgeschlossen!', 'success');
            }
        }

        // In andere Kachel laden
        function ladeInKachel(kachelNr, status) {
            const relevantAuftraege = status === 'offen' ? auftraege.offen : auftraege.aktiv;
            
            if (relevantAuftraege.length === 0) {
                alert(`Keine ${status === 'offen' ? 'offenen' : 'aktiven'} Aufträge vorhanden!`);
                return;
            }
            
            // Hier würde normalerweise die Weiterleitung erfolgen
            console.log(`Lade ${relevantAuftraege.length} ${status} Aufträge in Kachel ${kachelNr}`);
            showNotification(`${relevantAuftraege.length} Aufträge werden in Kachel ${kachelNr} geladen...`, 'info');
            
            // In echter Anwendung würde hier die Datenübertragung stattfinden
            // z.B. localStorage oder API-Call
            localStorage.setItem(`kachel${kachelNr}_auftraege`, JSON.stringify({
                auftraege: relevantAuftraege,
                status: status
            }));
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

        // Demo-Daten beim Start
        function ladeDemoDaten() {
            auftraege.offen = [
                {
                    id: 'PW-1000',
                    titel: 'Website Redesign',
                    beschreibung: 'Komplette Überarbeitung der Firmenwebsite',
                    status: 'OFFEN',
                    erstelltAm: '25.08.2025, 10:30:00'
                }
            ];
            
            auftraege.aktiv = [
                {
                    id: 'PW-999',
                    titel: 'API Integration',
                    beschreibung: 'REST API für Kundendaten',
                    status: 'AKTIV',
                    erstelltAm: '24.08.2025, 14:15:00',
                    zugesagtAm: '24.08.2025, 15:00:00'
                }
            ];
            
            auftraege.archiv = [
                {
                    id: 'PW-998',
                    titel: 'Datenbank Optimierung',
                    beschreibung: 'Performance Verbesserung',
                    status: 'ABGESCHLOSSEN',
                    erstelltAm: '23.08.2025, 09:00:00',
                    zugesagtAm: '23.08.2025, 09:30:00',
                    abgeschlossenAm: '24.08.2025, 16:45:00'
                }
            ];
            
            aktualisiereAnzeige();
        }

        // Beim Laden der Seite
        document.addEventListener('DOMContentLoaded', function() {
            ladeDemoDaten();
        });