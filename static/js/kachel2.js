// Kachel 2 - Analyse JavaScript

// Daten aus Kachel 1
        let geladeneAuftraege = {
            offen: [],
            aktiv: []
        };
        
        // Ausgewählte Qualität
        let qualitaetOffen = null;
        let qualitaetAktiv = null;
        
        // Aktuell bearbeiteter Auftrag
        let aktuellerAuftrag = null;

        // LocalStorage leeren
        function clearLocalStorage() {
            if(confirm('Möchten Sie wirklich alle gespeicherten Aufträge löschen?')) {
                localStorage.removeItem('kachel2_auftraege');
                location.reload();
            }
        }
        
        // Beim Laden der Seite prüfen
        document.addEventListener('DOMContentLoaded', function() {
            // Nur echte Daten aus Kachel 1 laden
            ladeAuftraege();
        });

        // Aufträge aus localStorage laden
        function ladeAuftraege() {
            try {
                const offenData = localStorage.getItem('kachel2_auftraege');
                if (offenData) {
                    const parsed = JSON.parse(offenData);
                    
                    // ZUERST: Beide Bereiche ausblenden
                    document.getElementById('offenerBereich').classList.add('hidden');
                    document.getElementById('aktiverBereich').classList.add('hidden');
                    
                    // Beide Status-Indikatoren inaktiv setzen
                    document.getElementById('statusOffen').classList.add('inactive');
                    document.getElementById('statusOffen').classList.remove('active');
                    document.getElementById('statusAktiv').classList.add('inactive');
                    document.getElementById('statusAktiv').classList.remove('active');
                    
                    // DANN: Nur den relevanten Bereich einblenden
                    if (parsed.status === 'offen') {
                        // Offene Aufträge laden
                        geladeneAuftraege.offen = parsed.auftraege;
                        document.getElementById('offenCount').textContent = parsed.auftraege.length;
                        
                        // Status-Anzeige aktualisieren
                        document.getElementById('statusOffen').classList.remove('inactive');
                        document.getElementById('statusOffen').classList.add('active');
                        
                        // NUR offenen Bereich zeigen
                        document.getElementById('offenerBereich').classList.remove('hidden');
                        
                        // Ersten Auftrag anzeigen
                        if (parsed.auftraege.length > 0) {
                            zeigeOffenenAuftrag(parsed.auftraege[0]);
                        }
                        
                    } else if (parsed.status === 'aktiv') {
                        // Aktive Aufträge laden
                        geladeneAuftraege.aktiv = parsed.auftraege;
                        document.getElementById('aktivCount').textContent = parsed.auftraege.length;
                        
                        // Status-Anzeige aktualisieren
                        document.getElementById('statusAktiv').classList.remove('inactive');
                        document.getElementById('statusAktiv').classList.add('active');
                        
                        // NUR aktiven Bereich zeigen
                        document.getElementById('aktiverBereich').classList.remove('hidden');
                        
                        // Ersten Auftrag anzeigen
                        if (parsed.auftraege.length > 0) {
                            zeigeAktivenAuftrag(parsed.auftraege[0]);
                        }
                    }
                } else {
                    // Keine Daten vorhanden - alles leer lassen
                    document.getElementById('offenTitel').textContent = 'Kein Auftrag geladen';
                    document.getElementById('offenId').textContent = '-';
                    document.getElementById('offenBeschreibung').textContent = 'Bitte laden Sie einen Auftrag aus Kachel 1';
                    
                    document.getElementById('aktivTitel').textContent = 'Kein Auftrag geladen';
                    document.getElementById('aktivId').textContent = '-';
                    document.getElementById('aktivBeschreibung').textContent = 'Bitte laden Sie einen Auftrag aus Kachel 1';
                }
            } catch(e) {
                console.error('Fehler beim Laden der Aufträge:', e);
            }
        }
        
        // Demo-Daten für Tests
        function ladeDemoDaten() {
            // Demo-Auftrag erstellen
            const demoOffen = {
                status: 'offen',
                auftraege: [{
                    id: 'PW-1001',
                    titel: 'E-Commerce Platform Development',
                    beschreibung: 'Entwicklung einer modernen E-Commerce Plattform mit React und Node.js, inklusive Zahlungsintegration und Admin-Dashboard',
                    status: 'OFFEN',
                    erstelltAm: '26.08.2025, 14:30:00'
                }]
            };
            
            // Demo-Daten in localStorage speichern
            localStorage.setItem('kachel2_auftraege', JSON.stringify(demoOffen));
            
            // Beide Bereiche ausblenden
            document.getElementById('offenerBereich').classList.add('hidden');
            document.getElementById('aktiverBereich').classList.add('hidden');
            
            // Offenen Bereich aktivieren
            geladeneAuftraege.offen = demoOffen.auftraege;
            document.getElementById('offenCount').textContent = demoOffen.auftraege.length;
            document.getElementById('statusOffen').classList.remove('inactive');
            document.getElementById('statusOffen').classList.add('active');
            document.getElementById('statusAktiv').classList.add('inactive');
            document.getElementById('offenerBereich').classList.remove('hidden');
            
            // Ersten Auftrag anzeigen
            zeigeOffenenAuftrag(demoOffen.auftraege[0]);
            
            // Beispiel Upwork-Text vorausfüllen
            document.getElementById('upworkBeschreibung').value = `We need an experienced developer to build a modern e-commerce platform.

Requirements:
- React.js for frontend
- Node.js/Express for backend
- Payment gateway integration (Stripe)
- Admin dashboard
- Mobile responsive design
- User authentication
- Product catalog with search
- Shopping cart functionality

Budget: $5000-$8000
Timeline: 6-8 weeks`;
            
            showNotification('Demo-Auftrag geladen! Du kannst jetzt den Workflow testen.', 'info');
        }

        // Manuell zwischen Bereichen wechseln
        function wechsleZuOffen() {
            if (geladeneAuftraege.offen.length === 0) {
                showNotification('Keine offenen Aufträge vorhanden!', 'error');
                return;
            }
            
            // Bereiche umschalten
            document.getElementById('aktiverBereich').classList.add('hidden');
            document.getElementById('offenerBereich').classList.remove('hidden');
            
            // Status aktualisieren
            document.getElementById('statusOffen').classList.remove('inactive');
            document.getElementById('statusOffen').classList.add('active');
            document.getElementById('statusAktiv').classList.add('inactive');
            document.getElementById('statusAktiv').classList.remove('active');
        }
        
        function wechsleZuAktiv() {
            if (geladeneAuftraege.aktiv.length === 0) {
                showNotification('Keine aktiven Aufträge vorhanden!', 'error');
                return;
            }
            
            // Bereiche umschalten
            document.getElementById('offenerBereich').classList.add('hidden');
            document.getElementById('aktiverBereich').classList.remove('hidden');
            
            // Status aktualisieren
            document.getElementById('statusAktiv').classList.remove('inactive');
            document.getElementById('statusAktiv').classList.add('active');
            document.getElementById('statusOffen').classList.add('inactive');
            document.getElementById('statusOffen').classList.remove('active');
        }

        // Offenen Auftrag anzeigen
        function zeigeOffenenAuftrag(auftrag) {
            aktuellerAuftrag = auftrag;
            document.getElementById('offenTitel').textContent = auftrag.titel;
            document.getElementById('offenId').textContent = auftrag.id;
            document.getElementById('offenBeschreibung').textContent = auftrag.beschreibung;
        }

        // Aktiven Auftrag anzeigen
        function zeigeAktivenAuftrag(auftrag) {
            aktuellerAuftrag = auftrag;
            document.getElementById('aktivTitel').textContent = auftrag.titel || '-';
            document.getElementById('aktivId').textContent = auftrag.id || '-';
            document.getElementById('aktivBeschreibung').textContent = auftrag.beschreibung || '-';
            // Bei aktiven Aufträgen müssen Script-Titel und Beschreibung vom Kunden neu eingegeben werden
        }

        // OFFENER BEREICH FUNKTIONEN
        function setQualitaetOffen(qualitaet) {
            qualitaetOffen = qualitaet;
            document.querySelectorAll('#offenerBereich .qualitaet-option').forEach(el => {
                el.classList.remove('selected');
            });
            event.target.classList.add('selected');
        }

        function analysiereOffenenAuftrag() {
            const beschreibung = document.getElementById('upworkBeschreibung').value;
            const sprache = document.getElementById('spracheOffen').value;
            
            if (!beschreibung) {
                alert('Bitte Upwork Beschreibung eingeben!');
                return;
            }
            
            // Analyse durchführen
            showLoading('Analysiere Upwork-Auftrag mit Opus 4.1...');
            
            setTimeout(() => {
                // Hier würde die echte API-Analyse stattfinden
                document.getElementById('probeTitel').textContent = 'Wird analysiert...';
                document.getElementById('probeBeschreibung').textContent = 'Analyse läuft...';
                document.getElementById('probeKeywords').textContent = 'Keywords werden extrahiert...';
                
                hideLoading();
                showNotification('Analyse mit Opus 4.1 bereit für nächsten Schritt!', 'success');
            }, 2000);
        }

        function erstelleArbeitsprobe() {
            if (!qualitaetOffen) {
                alert('Bitte Qualität auswählen!');
                return;
            }
            
            const wortanzahl = document.getElementById('wortanzahlOffen').value;
            
            // Bestimme KI basierend auf Qualität
            let kiModule = '';
            switch(qualitaetOffen) {
                case 'bronze':
                    kiModule = 'Gemini 2.5 Pro (3 Hooks) + Opus 4.1';
                    break;
                case 'silber':
                    kiModule = 'Gemini 2.5 Pro (5 Hooks) + Opus 4.1 + Sonnet 4';
                    break;
                case 'gold':
                    kiModule = 'Gemini 2.5 Pro (7 Hooks) + Opus 4.1 + Sonnet 4 + Serper API';
                    break;
            }
            
            showLoading(`Erstelle Arbeitsprobe mit ${kiModule}...`);
            
            setTimeout(() => {
                // Hier würde die echte API-Generierung stattfinden
                document.getElementById('finalProbeTitel').textContent = 'Arbeitsprobe wird erstellt...';
                document.getElementById('finalProbeText').textContent = 'Content wird generiert...';
                
                // Plagiatsprüfung Platzhalter
                setPlagiatAnzeige('offen', 0);
                
                hideLoading();
                showNotification('Bereit für API-Generierung!', 'info');
            }, 2000);
        }

        // AKTIVER BEREICH FUNKTIONEN
        function setQualitaetAktiv(qualitaet) {
            qualitaetAktiv = qualitaet;
            document.querySelectorAll('#aktiverBereich .qualitaet-option').forEach(el => {
                el.classList.remove('selected');
            });
            event.target.classList.add('selected');
        }

        function analysiereAktivenAuftrag() {
            const scriptTitel = document.getElementById('scriptTitelKunde').value;
            const beschreibung = document.getElementById('beschreibungKunde').value;
            const sprache = document.getElementById('spracheAktiv').value;
            
            if (!scriptTitel || !beschreibung) {
                alert('Bitte alle Felder ausfüllen!');
                return;
            }
            
            showLoading('Führe Online-Recherche durch (Serper + Opus 4.1)...');
            
            setTimeout(() => {
                // Hier würde die echte API-Recherche stattfinden
                document.getElementById('scriptTitel').textContent = scriptTitel;
                document.getElementById('scriptBeschreibung').textContent = 'Recherche läuft...';
                
                hideLoading();
                showNotification('Bereit für Script-Erstellung!', 'success');
            }, 2000);
        }

        function erstelleScript() {
            if (!qualitaetAktiv) {
                alert('Bitte Qualität auswählen!');
                return;
            }
            
            const wortanzahl = document.getElementById('wortanzahlAktiv').value;
            
            // Bestimme KI basierend auf Qualität
            let kiModule = '';
            switch(qualitaetAktiv) {
                case 'bronze':
                    kiModule = 'Gemini 2.5 Pro (3 Hooks) + Opus 4.1';
                    break;
                case 'silber':
                    kiModule = 'Gemini 2.5 Pro (5 Hooks) + Opus 4.1 + Sonnet 4 + Copyscape';
                    break;
                case 'gold':
                    kiModule = 'Gemini 2.5 Pro (7 Hooks) + Opus 4.1 + Sonnet 4 + Serper API + Copyscape';
                    break;
            }
            
            showLoading(`Erstelle Script mit ${kiModule}...`);
            
            setTimeout(() => {
                // Hier würde die echte API-Generierung stattfinden
                document.getElementById('finalScriptTitel').textContent = 'Script wird erstellt...';
                document.getElementById('finalScriptText').textContent = 'Content wird generiert...';
                
                // Plagiatsprüfung Platzhalter
                setPlagiatAnzeige('aktiv', 0);
                
                hideLoading();
                showNotification('Bereit für API-Generierung!', 'info');
            }, 2000);
        }

        // Plagiat Anzeige setzen
        function setPlagiatAnzeige(typ, prozent) {
            const element = typ === 'offen' ? 
                document.getElementById('plagiatOffen') : 
                document.getElementById('plagiatAktiv');
            
            element.style.width = prozent + '%';
            element.textContent = prozent + '% Original';
            
            // Farbe basierend auf Wert
            element.classList.remove('warning', 'danger');
            if (prozent < 60) {
                element.classList.add('danger');
            } else if (prozent < 80) {
                element.classList.add('warning');
            }
        }

        // In Kachel 1 speichern
        function speichereInKachel1(typ) {
            showNotification('Speichere in Kachel 1...', 'info');
            
            // Hier würde die Speicherlogik kommen
            setTimeout(() => {
                // Spalten zurücksetzen
                resetSpalten(typ);
                showNotification('Erfolgreich in Kachel 1 gespeichert!', 'success');
            }, 1500);
        }

        // Spalten zurücksetzen
        function resetSpalten(typ) {
            if (typ === 'offen') {
                document.getElementById('upworkBeschreibung').value = '';
                document.getElementById('probeTitel').textContent = '-';
                document.getElementById('probeBeschreibung').textContent = '-';
                document.getElementById('probeKeywords').textContent = '-';
                document.getElementById('finalProbeTitel').textContent = '-';
                document.getElementById('finalProbeText').textContent = 'Hier erscheint die erstellte Arbeitsprobe...';
                document.getElementById('wortanzahlOffen').value = '1000';
                qualitaetOffen = null;
                document.querySelectorAll('#offenerBereich .qualitaet-option').forEach(el => {
                    el.classList.remove('selected');
                });
                setPlagiatAnzeige('offen', 0);
            } else {
                document.getElementById('scriptTitelKunde').value = '';
                document.getElementById('beschreibungKunde').value = '';
                document.getElementById('scriptTitel').textContent = '-';
                document.getElementById('scriptBeschreibung').textContent = '-';
                document.getElementById('finalScriptTitel').textContent = '-';
                document.getElementById('finalScriptText').textContent = 'Hier erscheint das erstellte Script...';
                document.getElementById('wortanzahlAktiv').value = '1000';
                qualitaetAktiv = null;
                document.querySelectorAll('#aktiverBereich .qualitaet-option').forEach(el => {
                    el.classList.remove('selected');
                });
                setPlagiatAnzeige('aktiv', 0);
            }
        }

        // Hilfsfunktionen
        function showLoading(message) {
            const loading = document.createElement('div');
            loading.id = 'loadingOverlay';
            loading.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            `;
            loading.innerHTML = `
                <div class="loading-spinner"></div>
                <div style="color: white; margin-top: 20px; font-size: 1.2em;">${message}</div>
            `;
            document.body.appendChild(loading);
        }

        function hideLoading() {
            const loading = document.getElementById('loadingOverlay');
            if (loading) {
                loading.remove();
            }
        }

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

        // Animations
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