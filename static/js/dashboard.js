// Dashboard JavaScript - PW-Script-Studio

// Lava Bubbles generieren
function createBubbles() {
    const bubbleContainers = document.querySelectorAll('.lava-bubbles');
    
    bubbleContainers.forEach(container => {
        for(let i = 0; i < 5; i++) {
            const bubble = document.createElement('div');
            bubble.className = 'bubble';
            
            const size = Math.random() * 20 + 10;
            bubble.style.width = size + 'px';
            bubble.style.height = size + 'px';
            bubble.style.left = Math.random() * 100 + '%';
            bubble.style.animationDelay = Math.random() * 8 + 's';
            bubble.style.animationDuration = (Math.random() * 4 + 6) + 's';
            
            container.appendChild(bubble);
        }
    });
}

// Click Handler
function handleClick(kachel) {
    console.log('Kachel geklickt:', kachel);
    
    // Pulsierender Effekt beim Klick
    event.currentTarget.style.animation = 'pulse 0.5s';
    setTimeout(() => {
        event.currentTarget.style.animation = '';
    }, 500);
    
    // Hier kannst du weitere Aktionen hinzufügen
    switch(kachel) {
        case 'kachel1':
            // Aufträge Modul öffnen
            window.location.href = '/kachel1/';
            break;
        case 'kachel2':
            // Analyse Modul öffnen
            window.location.href = '/kachel2/';
            break;
        case 'kachel3':
            // PDF/Contact Modul öffnen
            window.location.href = '/kachel3/';
            break;
    }
}

// Dashboard-Statistiken von API laden
async function ladeDashboardStats() {
    try {
        showLoading('Dashboard-Daten werden geladen...');

        const stats = await AuftraegeAPI.getDashboardStats();
        console.log('Dashboard Stats geladen:', stats);

        // Update Kachel-Inhalte mit echten Daten
        updateDashboardKacheln(stats);

        hideLoading();
        showSuccess('Dashboard erfolgreich aktualisiert!');

    } catch (error) {
        hideLoading();
        console.error('Fehler beim Laden der Dashboard-Stats:', error);
        showError('Dashboard-Daten konnten nicht geladen werden');

        // Fallback: Zeige Demo-Daten
        showDemoDaten();
    }
}

// Dashboard-Kacheln mit API-Daten aktualisieren
function updateDashboardKacheln(stats) {
    // Kachel 1 - Auftragsverwaltung
    const kachel1Content = document.querySelector('.kachel:nth-child(1) .kachel-content');
    if (kachel1Content) {
        kachel1Content.innerHTML = `
            <div class="kachel-item">
                <span class="kachel-icon">📋</span>
                Gesamt: ${stats.total_auftraege} Aufträge
            </div>
            <div class="kachel-item">
                <span class="kachel-icon">🔓</span>
                Offen: ${stats.offene_auftraege} Bewerbungen
            </div>
            <div class="kachel-item">
                <span class="kachel-icon">🔥</span>
                Aktiv: ${stats.aktive_auftraege} Kundenprojekte
            </div>
            <div class="kachel-item">
                <span class="kachel-icon">✅</span>
                Abgeschlossen: ${stats.abgeschlossene_auftraege}
            </div>
        `;
    }

    // Kachel 2 - Analyse
    const kachel2Content = document.querySelector('.kachel:nth-child(2) .kachel-content');
    if (kachel2Content) {
        kachel2Content.innerHTML = `
            <div class="kachel-item">
                <span class="kachel-icon">📝</span>
                Arbeitsproben: ${stats.total_arbeitsproben}
            </div>
            <div class="kachel-item">
                <span class="kachel-icon">🎬</span>
                Scripts: ${stats.total_scripts}
            </div>
            <div class="kachel-item">
                <span class="kachel-icon">💰</span>
                API-Kosten: $${stats.api_kosten_gesamt}
            </div>
            <div class="kachel-item">
                <span class="kachel-icon">🔍</span>
                Serper-Kosten: $${stats.serper_kosten_gesamt}
            </div>
        `;
    }

    // Kachel 3 - Export (bleibt erstmal statisch)
    const kachel3Content = document.querySelector('.kachel:nth-child(3) .kachel-content');
    if (kachel3Content) {
        kachel3Content.innerHTML = `
            <div class="kachel-item">
                <span class="kachel-icon">📄</span>
                PDF-Export bereit
            </div>
            <div class="kachel-item">
                <span class="kachel-icon">📧</span>
                E-Mail-Versand aktiv
            </div>
            <div class="kachel-item">
                <span class="kachel-icon">📊</span>
                Reports verfügbar
            </div>
        `;
    }
}

// Fallback Demo-Daten anzeigen
function showDemoDaten() {
    const demoStats = {
        total_auftraege: 3,
        offene_auftraege: 2,
        aktive_auftraege: 1,
        abgeschlossene_auftraege: 0,
        total_arbeitsproben: 1,
        total_scripts: 1,
        api_kosten_gesamt: '0.93',
        serper_kosten_gesamt: '0.02'
    };

    updateDashboardKacheln(demoStats);
    showError('Demo-Daten werden angezeigt - API nicht erreichbar');
}

// Initialisierung
document.addEventListener('DOMContentLoaded', async function() {
    createBubbles();

    // Zufällige Lava-Bewegung für jede Kachel
    const kacheln = document.querySelectorAll('.kachel');
    kacheln.forEach((kachel, index) => {
        kachel.style.setProperty('--angle', `${index * 120}deg`);
    });

    // Dashboard-Daten von API laden
    await ladeDashboardStats();

    // Auto-Refresh alle 30 Sekunden
    setInterval(ladeDashboardStats, 30000);
});

// Dynamische Lava-Farben bei Hover
document.querySelectorAll('.kachel').forEach(kachel => {
    kachel.addEventListener('mouseenter', function() {
        this.style.filter = 'brightness(1.1)';
    });
    
    kachel.addEventListener('mouseleave', function() {
        this.style.filter = 'brightness(1)';
    });
});
