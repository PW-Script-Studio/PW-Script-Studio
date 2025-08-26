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

// Initialisierung
document.addEventListener('DOMContentLoaded', function() {
    createBubbles();
    
    // Zufällige Lava-Bewegung für jede Kachel
    const kacheln = document.querySelectorAll('.kachel');
    kacheln.forEach((kachel, index) => {
        kachel.style.setProperty('--angle', `${index * 120}deg`);
    });
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
