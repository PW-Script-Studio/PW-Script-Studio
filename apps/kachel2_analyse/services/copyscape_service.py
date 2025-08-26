"""
Copyscape API Service für Plagiatsprüfung
Für beide Workflows verfügbar (OFFEN und AKTIV)
"""
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class CopyscapeService:
    """
    Service für Copyscape API - Plagiatsprüfung
    """
    
    def __init__(self):
        self.api_key = settings.COPYSCAPE_API_KEY
        self.base_url = "https://www.copyscape.com/api/"
        
        if not self.api_key:
            logger.warning("COPYSCAPE_API_KEY nicht konfiguriert - Plagiatsprüfung nicht verfügbar")
    
    def check_plagiarism(self, text: str, title: str = "") -> dict:
        """
        Prüft Text auf Plagiate
        
        Args:
            text: Zu prüfender Text
            title: Titel des Textes (optional)
        
        Returns:
            dict mit Plagiatsprüfungs-Ergebnissen
        """
        if not self.api_key:
            return {
                'success': False,
                'error': 'Copyscape API Key nicht konfiguriert',
                'cost': 0.00
            }
        
        if len(text) < 100:
            return {
                'success': False,
                'error': 'Text zu kurz für Plagiatsprüfung (min. 100 Zeichen)',
                'cost': 0.00
            }
        
        try:
            logger.info(f"Copyscape Plagiatsprüfung für Text: {len(text)} Zeichen")
            
            # Copyscape API Parameter
            params = {
                'u': self.api_key,
                'o': 'csearch',
                't': text[:10000],  # Max 10k Zeichen
                'c': '1',  # Vollständige Suche
                'e': 'UTF-8'
            }
            
            response = requests.post(
                f"{self.base_url}",
                data=params,
                timeout=60
            )
            
            if response.status_code == 200:
                result_text = response.text
                
                # Einfache Auswertung der Copyscape-Antwort
                if 'No results found' in result_text:
                    plagiarism_score = 0
                    matches = []
                elif 'results found' in result_text:
                    # Vereinfachte Auswertung
                    plagiarism_score = self._calculate_plagiarism_score(result_text)
                    matches = self._extract_matches(result_text)
                else:
                    plagiarism_score = -1  # Unbekannt
                    matches = []
                
                logger.info(f"Copyscape erfolgreich - Score: {plagiarism_score}%")
                
                return {
                    'success': True,
                    'plagiarism_score': plagiarism_score,
                    'matches': matches,
                    'raw_response': result_text,
                    'cost': 0.05,  # Geschätzte Kosten pro Prüfung
                    'text_length': len(text)
                }
            else:
                logger.error(f"Copyscape API Fehler: {response.status_code}")
                return {
                    'success': False,
                    'error': f'API Fehler: {response.status_code}',
                    'cost': 0.00
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Copyscape Request Fehler: {e}")
            return {
                'success': False,
                'error': str(e),
                'cost': 0.00
            }
    
    def _calculate_plagiarism_score(self, response_text: str) -> int:
        """
        Berechnet Plagiatsscore aus Copyscape-Antwort
        """
        # Vereinfachte Implementierung
        # In der Realität würde man die XML-Antwort parsen
        if 'No results found' in response_text:
            return 0
        elif '1 result found' in response_text:
            return 25
        elif '2 results found' in response_text:
            return 50
        elif 'results found' in response_text:
            return 75
        else:
            return -1  # Unbekannt
    
    def _extract_matches(self, response_text: str) -> list:
        """
        Extrahiert gefundene Matches aus Copyscape-Antwort
        """
        # Vereinfachte Implementierung
        # In der Realität würde man die XML-Antwort parsen
        matches = []
        
        if 'result found' in response_text:
            matches.append({
                'url': 'Beispiel-URL (XML-Parsing erforderlich)',
                'title': 'Gefundener Match',
                'percentage': 'Unbekannt'
            })
        
        return matches
    
    def get_service_info(self) -> dict:
        """
        Gibt Informationen über den Copyscape Service zurück
        """
        return {
            'service': 'Copyscape',
            'available': bool(self.api_key),
            'cost_per_check': 0.05,
            'max_text_length': 10000,
            'min_text_length': 100,
            'supported_workflows': ['OFFEN', 'AKTIV']
        }
