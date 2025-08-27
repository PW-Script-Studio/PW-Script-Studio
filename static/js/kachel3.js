// Kachel 3 - Export JavaScript

/*
        ========================================
        KACHEL 3 - AUSGABE & EXPORT SYSTEM
        ========================================
        
        WICHTIGE SYSTEM-REGELN:
        1. Es kann immer nur EIN Auftrag geladen sein (entweder offen ODER aktiv)
        2. Dieser EINE Auftrag hat seine Inhalte in Wochenblöcken organisiert
        3. Offener Auftrag: 2-3 Arbeitsproben (für Bewerbung)
        4. Aktiver Auftrag: 1-7 Scripts pro Woche (kann über Monate gehen!)
        
        DATENFLUSS:
        Kachel 1 → Kachel 3 (niemals direkt aus Kachel 2!)
        
        STRUKTUR:
        - ENTWEDER: 1 offener Auftrag mit Arbeitsproben in Wochenblöcken
        - ODER: 1 aktiver Auftrag mit Scripts in Wochenblöcken
        - NIEMALS: Mehrere Aufträge oder gemischte Anzeige
        ========================================
        */

        // ===== DATEN STRUKTUR =====
        let datenbank = {
            offen: {
                auftrag: null,  // NUR EIN offener Auftrag
                wochenBloecke: {}  // Arbeitsproben dieses EINEN Auftrags nach Wochen
            },
            aktiv: {
                auftrag: null,  // NUR EIN aktiver Auftrag
                wochenBloecke: {}  // Scripts dieses EINEN Auftrags nach Wochen
            }
        };

        // Aktuell ausgewählte Items
        let aktuelleAuswahl = {
            wochenblock: null,
            detail: null,
            inhalt: null,
            typ: null  // 'offen' oder 'aktiv'
        };

        // ===== INITIALISIERUNG =====
        document.addEventListener('DOMContentLoaded', async function() {
            console.log('🚀 Kachel 3 - Export geladen');
            await ladeExportDaten();
            zeigeOffenenBereich();  // Standard: Offene Aufträge anzeigen
        });

        // ===== DATEN LADEN =====
        async function ladeExportDaten() {
            try {
                showLoading('Export-Daten werden geladen...');

                // OFFENE Aufträge (Bewerbungen) laden
                const offeneData = await AuftraegeAPI.getOffene();
                if (offeneData.auftraege && offeneData.auftraege.length > 0) {
                    // Ersten OFFENEN Auftrag als Beispiel laden
                    datenbank.offen.auftrag = offeneData.auftraege[0];
                    console.log('✅ Offener Auftrag von API geladen:', datenbank.offen.auftrag.titel);
                }

                // AKTIVE Aufträge (Kundenprojekte) laden
                const aktiveData = await AuftraegeAPI.getAktive();
                if (aktiveData.auftraege && aktiveData.auftraege.length > 0) {
                    // Ersten AKTIVEN Auftrag als Beispiel laden
                    datenbank.aktiv.auftrag = aktiveData.auftraege[0];
                    console.log('✅ Aktiver Auftrag von API geladen:', datenbank.aktiv.auftrag.titel);
                }

                console.log('Export-Daten von API geladen:', datenbank);

                hideLoading();
                showSuccess('Export-Daten erfolgreich geladen!');

            } catch (error) {
                hideLoading();
                console.error('Fehler beim Laden der Export-Daten:', error);
                showError('Export-Daten konnten nicht geladen werden');

                // Fallback: Demo-Daten erstellen
                erstelleDemoDaten();
            }
        }

        function erstelleDemoDaten() {
            // ===== KEINE DEMO-DATEN - System startet leer =====
            // Warte auf echte Daten aus Kachel 1
            
            // Leere Datenbank initialisieren
            datenbank.offen.auftrag = null;
            datenbank.offen.wochenBloecke = {};
            
            datenbank.aktiv.auftrag = null;
            datenbank.aktiv.wochenBloecke = {};
            
            console.log('📭 Kachel 3 bereit - warte auf Daten aus Kachel 1');
        }

        // ===== BEREICH WECHSEL - NUR EINER KANN AKTIV SEIN! =====
        function wechsleZuOffen() {
            // VERSTECKE aktiven Bereich KOMPLETT
            document.getElementById('aktiverBereich').classList.add('hidden');
            document.getElementById('aktiverBereich').style.display = 'none';
            
            // ZEIGE NUR offenen Bereich
            document.getElementById('offenerBereich').classList.remove('hidden');
            document.getElementById('offenerBereich').style.display = 'grid';
            
            // Update Status-Anzeige - NUR EINER ist aktiv!
            document.getElementById('statusOffen').classList.add('active');
            document.getElementById('statusOffen').classList.remove('inactive');
            document.getElementById('statusOffen').style.background = 'linear-gradient(45deg, #2196f3, #42a5f5)';
            
            // Aktiv-Button wird komplett inaktiv
            document.getElementById('statusAktiv').classList.remove('active');
            document.getElementById('statusAktiv').classList.add('inactive');
            document.getElementById('statusAktiv').style.background = 'rgba(100, 100, 100, 0.3)';
            
            aktuelleAuswahl.typ = 'offen';
            
            // Reset alle Auswahlen beim Wechsel
            aktuelleAuswahl.wochenblock = null;
            aktuelleAuswahl.detail = null;
            aktuelleAuswahl.inhalt = null;
            
            zeigeOffeneAuftraege();
        }

        function wechsleZuAktiv() {
            // VERSTECKE offenen Bereich KOMPLETT
            document.getElementById('offenerBereich').classList.add('hidden');
            document.getElementById('offenerBereich').style.display = 'none';
            
            // ZEIGE NUR aktiven Bereich
            document.getElementById('aktiverBereich').classList.remove('hidden');
            document.getElementById('aktiverBereich').style.display = 'grid';
            
            // Update Status-Anzeige - NUR EINER ist aktiv!
            document.getElementById('statusAktiv').classList.add('active');
            document.getElementById('statusAktiv').classList.remove('inactive');
            document.getElementById('statusAktiv').style.background = 'linear-gradient(45deg, #4caf50, #66bb6a)';
            
            // Offen-Button wird komplett inaktiv
            document.getElementById('statusOffen').classList.remove('active');
            document.getElementById('statusOffen').classList.add('inactive');
            document.getElementById('statusOffen').style.background = 'rgba(100, 100, 100, 0.3)';
            
            aktuelleAuswahl.typ = 'aktiv';
            
            // Reset alle Auswahlen beim Wechsel
            aktuelleAuswahl.wochenblock = null;
            aktuelleAuswahl.detail = null;
            aktuelleAuswahl.inhalt = null;
            
            zeigeAktiveAuftraege();
        }

        function zeigeOffenenBereich() {
            // Standard beim Start: Offene Aufträge
            wechsleZuOffen();
        }

        // ===== SPALTE 1: AUFTRÄGE ANZEIGEN =====
        function zeigeOffeneAuftraege() {
            const container = document.getElementById('offeneAuftraege');
            container.innerHTML = '';
            
            // Prüfe ob ein offener Auftrag geladen ist
            if (!datenbank.offen.auftrag) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 3em; margin-bottom: 20px;">📭</div>
                        <div style="font-size: 1.2em; color: #ffc107;">Kein offener Auftrag vorhanden</div>
                        <div style="color: #888; margin-top: 10px;">
                            Bitte in Kachel 1 einen offenen Auftrag<br>
                            mit "In Kachel 3 laden" exportieren
                        </div>
                    </div>
                `;
                return;
            }
            
            // Info-Header für DEN EINEN offenen Auftrag
            const infoBlock = document.createElement('div');
            infoBlock.style.cssText = 'background: rgba(33, 150, 243, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #2196f3;';
            infoBlock.innerHTML = `
                <div style="color: #2196f3; font-weight: bold;">📌 Offener Auftrag:</div>
                <div style="color: #ffc107; font-size: 1.1em; margin-top: 5px;">${datenbank.offen.auftrag.titel}</div>
                <div style="color: #aaa; font-size: 0.9em;">ID: ${datenbank.offen.auftrag.id}</div>
            `;
            container.appendChild(infoBlock);
            
            // Zeige alle Wochenblöcke für diesen EINEN Auftrag
            Object.keys(datenbank.offen.wochenBloecke).forEach(woche => {
                const wochenData = datenbank.offen.wochenBloecke[woche];
                const block = document.createElement('div');
                block.className = 'wochenblock';
                
                const arbeitsprobenCount = wochenData.arbeitsproben ? wochenData.arbeitsproben.length : 0;
                
                block.innerHTML = `
                    <div class="wochenblock-title">
                        Arbeitsprobe
                    </div>
                    <div class="wochenblock-date">
                        📅 ${woche}
                    </div>
                    <div style="color: #4caf50; font-size: 0.85em; margin-top: 5px;">
                        ${arbeitsprobenCount} Arbeitsprobe${arbeitsprobenCount !== 1 ? 'n' : ''}
                    </div>
                `;
                block.onclick = () => zeigeOffeneDetails(wochenData, block);
                container.appendChild(block);
            });
        }

        function zeigeAktiveAuftraege() {
            const container = document.getElementById('aktiveAuftraege');
            container.innerHTML = '';
            
            // Prüfe ob ein aktiver Auftrag geladen ist
            if (!datenbank.aktiv.auftrag) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 3em; margin-bottom: 20px;">📭</div>
                        <div style="font-size: 1.2em; color: #4caf50;">Kein aktiver Auftrag vorhanden</div>
                        <div style="color: #888; margin-top: 10px;">
                            Bitte in Kachel 1 einen aktiven Auftrag<br>
                            mit "In Kachel 3 laden" exportieren
                        </div>
                    </div>
                `;
                return;
            }
            
            // Info-Header für DEN EINEN aktiven Auftrag
            const infoBlock = document.createElement('div');
            infoBlock.style.cssText = 'background: rgba(76, 175, 80, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #4caf50;';
            infoBlock.innerHTML = `
                <div style="color: #4caf50; font-weight: bold;">📌 Aktiver Auftrag:</div>
                <div style="color: #ffc107; font-size: 1.1em; margin-top: 5px;">${datenbank.aktiv.auftrag.titel}</div>
                <div style="color: #aaa; font-size: 0.9em;">ID: ${datenbank.aktiv.auftrag.id} | Kunde: ${datenbank.aktiv.auftrag.kunde}</div>
                <div style="color: #888; font-size: 0.85em; margin-top: 5px;">
                    Laufzeit: ${datenbank.aktiv.auftrag.laufzeit || 'unbegrenzt'} | 
                    Scripts/Woche: ${datenbank.aktiv.auftrag.scriptProWoche || 'variabel'}
                </div>
            `;
            container.appendChild(infoBlock);
            
            // Zeige alle Wochenblöcke für diesen EINEN Auftrag (können viele sein!)
            Object.keys(datenbank.aktiv.wochenBloecke).sort().reverse().forEach(woche => {
                const wochenData = datenbank.aktiv.wochenBloecke[woche];
                const block = document.createElement('div');
                block.className = 'wochenblock';
                
                const scriptCount = wochenData.scripts ? wochenData.scripts.length : 0;
                
                block.innerHTML = `
                    <div class="wochenblock-title">
                        Woche ${woche.split(' - ')[0]}
                    </div>
                    <div class="wochenblock-date">
                        📅 ${woche}
                    </div>
                    <div style="color: #4caf50; font-size: 0.85em; margin-top: 5px;">
                        ${scriptCount} Script${scriptCount !== 1 ? 's' : ''} erstellt
                    </div>
                `;
                block.onclick = () => zeigeAktiveDetails(wochenData, block);
                container.appendChild(block);
            });
            
            // Zeige Statistik am Ende
            const totalScripts = Object.values(datenbank.aktiv.wochenBloecke).reduce((sum, woche) => {
                return sum + (woche.scripts ? woche.scripts.length : 0);
            }, 0);
            
            const statsBlock = document.createElement('div');
            statsBlock.style.cssText = 'background: rgba(255, 111, 0, 0.1); padding: 10px; border-radius: 8px; margin-top: 15px; text-align: center;';
            statsBlock.innerHTML = `
                <div style="color: #ff9800; font-weight: bold;">📊 Gesamt: ${totalScripts} Scripts</div>
            `;
            container.appendChild(statsBlock);
        }

        // ===== SPALTE 2: DETAILS ANZEIGEN =====
        function zeigeOffeneDetails(wochenData, blockElement) {
            // Update active state
            document.querySelectorAll('#offeneAuftraege .wochenblock').forEach(el => {
                el.classList.remove('active');
            });
            blockElement.classList.add('active');
            
            aktuelleAuswahl.wochenblock = wochenData;
            
            const container = document.getElementById('offeneDetails');
            container.innerHTML = '';
            
            // Zeige alle Arbeitsproben dieser Woche
            if (wochenData.arbeitsproben && wochenData.arbeitsproben.length > 0) {
                wochenData.arbeitsproben.forEach(probe => {
                    const item = document.createElement('div');
                    item.className = `detail-item ${probe.qualitaet}`;
                    item.innerHTML = `
                        <span class="quality-label ${probe.qualitaet}">
                            ${probe.qualitaet === 'gold' ? '🥇 Gold' : 
                              probe.qualitaet === 'silber' ? '🥈 Silber' : '🥉 Bronze'}
                        </span>
                        am ${probe.datum}
                        <div style="color: #aaa; font-size: 0.9em; margin-top: 5px;">
                            ${probe.titel}
                        </div>
                    `;
                    item.onclick = () => zeigeArbeitsprobe(probe);
                    container.appendChild(item);
                });
            }
        }

        function zeigeAktiveDetails(wochenData, blockElement) {
            // Update active state
            document.querySelectorAll('#aktiveAuftraege .wochenblock').forEach(el => {
                el.classList.remove('active');
            });
            blockElement.classList.add('active');
            
            aktuelleAuswahl.wochenblock = wochenData;
            
            const container = document.getElementById('aktiveDetails');
            container.innerHTML = '';
            
            // Zeige alle Scripts dieser Woche
            if (wochenData.scripts && wochenData.scripts.length > 0) {
                wochenData.scripts.forEach(script => {
                    const item = document.createElement('div');
                    item.className = `detail-item ${script.qualitaet}`;
                    item.innerHTML = `
                        <span class="quality-label ${script.qualitaet}">
                            ${script.qualitaet === 'gold' ? '🥇 Gold' : 
                              script.qualitaet === 'silber' ? '🥈 Silber' : '🥉 Bronze'}
                        </span>
                        am ${script.datum}
                        <div style="color: #aaa; font-size: 0.9em; margin-top: 5px;">
                            ${script.titel}
                        </div>
                    `;
                    item.onclick = () => zeigeScript(script);
                    container.appendChild(item);
                });
            }
        }

        // ===== SPALTE 3: INHALT ANZEIGEN =====
        function zeigeArbeitsprobe(probe) {
            aktuelleAuswahl.detail = probe;
            aktuelleAuswahl.inhalt = probe.inhalt;
            
            const container = document.getElementById('arbeitsprobeAnzeige');
            container.innerHTML = `
                <div class="script-container">
                    <div class="script-title">${probe.titel}</div>
                    <div class="script-text">${probe.inhalt}</div>
                </div>
            `;
            
            // Enable download buttons
            document.getElementById('pdfBtnOffen').disabled = false;
            document.getElementById('htmlBtnOffen').disabled = false;
        }

        function zeigeScript(script) {
            aktuelleAuswahl.detail = script;
            aktuelleAuswahl.inhalt = script.inhalt;
            
            const container = document.getElementById('scriptAnzeige');
            container.innerHTML = `
                <div class="script-container">
                    <div class="script-title">${script.titel}</div>
                    <div class="script-text">${script.inhalt}</div>
                </div>
            `;
            
            // Enable download buttons
            document.getElementById('pdfBtnAktiv').disabled = false;
            document.getElementById('htmlBtnAktiv').disabled = false;
        }

        // ===== DOWNLOAD FUNKTIONEN =====
        async function downloadPDF(typ) {
            if (!aktuelleAuswahl.detail) {
                showNotification('Bitte erst einen Auftrag auswählen!', 'error');
                return;
            }

            showNotification('PDF wird mit DocRaptor generiert...', 'info');

            try {
                // Bestimme Export-Typ basierend auf Workflow
                let exportType = 'arbeitsprobe'; // Default für OFFENE Aufträge

                if (typ === 'aktiv' || aktuelleAuswahl.detail.status === 'AKTIV') {
                    exportType = 'script'; // Für AKTIVE Aufträge
                }

                console.log(`PDF-Export gestartet: Auftrag ${aktuelleAuswahl.detail.id}, Typ: ${exportType}`);

                // DocRaptor API-Call über Django-Backend
                const response = await fetch(`/kachel3/pdf/${aktuelleAuswahl.detail.id}/?type=${exportType}`, {
                    method: 'GET',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`HTTP ${response.status}: ${errorText}`);
                }

                // PDF-Blob erhalten
                const blob = await response.blob();

                // Download initiieren
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${aktuelleAuswahl.detail.id}_${exportType}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);

                showNotification('PDF erfolgreich heruntergeladen!', 'success');

            } catch (error) {
                console.error('PDF-Export Fehler:', error);
                showNotification(`PDF-Export fehlgeschlagen: ${error.message}`, 'error');
            }
        }

        function downloadHTML(typ) {
            if (!aktuelleAuswahl.detail) return;
            
            // Generiere HTML mit Template
            const htmlTemplate = generateHTMLTemplate(
                aktuelleAuswahl.detail.titel,
                aktuelleAuswahl.inhalt,
                aktuelleAuswahl.detail.qualitaet
            );
            
            // Download HTML
            const blob = new Blob([htmlTemplate], { type: 'text/html' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.download = `${aktuelleAuswahl.detail.titel.replace(/\s+/g, '_')}.html`;
            link.href = url;
            link.click();
            
            showNotification('HTML erfolgreich heruntergeladen!', 'success');
        }

        function generateHTMLTemplate(title, content, quality) {
            return `<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 60px;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .quality-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            ${quality === 'gold' ? 'background: linear-gradient(45deg, #ffd700, #ffed4e); color: #333;' : 
              quality === 'silber' ? 'background: linear-gradient(45deg, #c0c0c0, #e8e8e8); color: #333;' : 
              'background: linear-gradient(45deg, #cd7f32, #daa520); color: white;'}
        }
        .content {
            white-space: pre-wrap;
            line-height: 1.8;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>${title}</h1>
        <span class="quality-badge">${quality.toUpperCase()} QUALITY</span>
        <div class="content">${content}</div>
        <div class="footer">
            Generated by PW-Script-Studio • ${new Date().toLocaleDateString('de-DE')}
        </div>
    </div>
</body>
</html>`;
        }

        // ===== NOTIFICATION SYSTEM =====
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
                z-index: 10000;
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
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);