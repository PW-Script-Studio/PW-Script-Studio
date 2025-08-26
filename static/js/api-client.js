// PW-Script-Studio API Client
// Zentrale API-Kommunikation für Frontend-Backend-Verbindung

const API_BASE_URL = '/api';

// CSRF-Token Handler für Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Zentrale API-Wrapper Funktion mit Error Handling
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };
    
    // Merge options
    const finalOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        console.log(`API Call: ${options.method || 'GET'} ${url}`);
        const response = await fetch(url, finalOptions);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log(`API Response:`, data);
        return data;
        
    } catch (error) {
        console.error('API Call failed:', error);
        showError(`API-Fehler: ${error.message}`);
        throw error;
    }
}

// Spezifische API-Funktionen für Aufträge
const AuftraegeAPI = {
    // Alle Aufträge laden
    async getAll() {
        return await apiCall('/auftraege/');
    },
    
    // Nur OFFENE Aufträge
    async getOffene() {
        return await apiCall('/auftraege/offene/');
    },
    
    // Nur AKTIVE Aufträge
    async getAktive() {
        return await apiCall('/auftraege/aktive/');
    },
    
    // Dashboard-Statistiken
    async getDashboardStats() {
        return await apiCall('/auftraege/dashboard_stats/');
    },
    
    // Neuen Auftrag erstellen
    async create(auftragData) {
        return await apiCall('/auftraege/', {
            method: 'POST',
            body: JSON.stringify(auftragData)
        });
    },
    
    // Auftrag aktualisieren
    async update(id, auftragData) {
        return await apiCall(`/auftraege/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(auftragData)
        });
    },
    
    // Auftrag löschen
    async delete(id) {
        return await apiCall(`/auftraege/${id}/`, {
            method: 'DELETE'
        });
    }
};

// API-Funktionen für Arbeitsproben (OFFENE Aufträge)
const ArbeitsprobenAPI = {
    async getAll(auftragId = null) {
        const endpoint = auftragId ? `/arbeitsproben/?auftrag=${auftragId}` : '/arbeitsproben/';
        return await apiCall(endpoint);
    },
    
    async getByQuality() {
        return await apiCall('/arbeitsproben/by_quality/');
    },
    
    async create(arbeitsprobeData) {
        return await apiCall('/arbeitsproben/', {
            method: 'POST',
            body: JSON.stringify(arbeitsprobeData)
        });
    }
};

// API-Funktionen für Scripts (AKTIVE Aufträge)
const ScriptsAPI = {
    async getAll(auftragId = null, week = null) {
        let endpoint = '/scripts/';
        const params = new URLSearchParams();
        if (auftragId) params.append('auftrag', auftragId);
        if (week) params.append('week', week);
        if (params.toString()) endpoint += '?' + params.toString();
        
        return await apiCall(endpoint);
    },
    
    async getByWeek() {
        return await apiCall('/scripts/by_week/');
    },
    
    async create(scriptData) {
        return await apiCall('/scripts/', {
            method: 'POST',
            body: JSON.stringify(scriptData)
        });
    },
    
    async addSerperCall(scriptId, cost = 0.01) {
        return await apiCall(`/scripts/${scriptId}/add_serper_call/`, {
            method: 'POST',
            body: JSON.stringify({ cost })
        });
    }
};

// Loading States Management
function showLoading(message = 'Lädt...') {
    // Entferne vorhandene Loading-Overlays
    hideLoading();
    
    const loader = document.createElement('div');
    loader.className = 'loading-overlay';
    loader.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.querySelector('.loading-overlay');
    if (loader) {
        loader.remove();
    }
}

// Error Handling
function showError(message, duration = 5000) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span class="error-icon">⚠️</span>
        <span class="error-text">${message}</span>
        <button class="error-close" onclick="this.parentElement.remove()">×</button>
    `;
    document.body.appendChild(errorDiv);
    
    // Auto-remove nach duration
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, duration);
}

// Success Messages
function showSuccess(message, duration = 3000) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <span class="success-icon">✅</span>
        <span class="success-text">${message}</span>
    `;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        if (successDiv.parentElement) {
            successDiv.remove();
        }
    }, duration);
}

// Utility: Generiere Auftrag-ID
function generiereAuftragID() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const time = String(now.getTime()).slice(-4);
    
    return `PW-${year}${month}${day}-${time}`;
}

console.log('🚀 API Client geladen - Frontend-Backend-Verbindung bereit!');
