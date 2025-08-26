"""
Serper API Service - NUR für AKTIVE Aufträge!

KRITISCH: Dieser Service darf NUR bei aktiven Kundenprojekten verwendet werden.
Für offene Aufträge (Bewerbungen) ist die Serper API VERBOTEN!
"""
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class SerperService:
    """
    Service für Serper API - Research für AKTIVE Aufträge
    """
    
    def __init__(self):
        self.api_key = settings.SERPER_API_KEY
        self.base_url = "https://google.serper.dev"
        
        if not self.api_key:
            raise ValueError("SERPER_API_KEY nicht konfiguriert!")
    
    def search(self, query, workflow_type=None, auftrag_status=None):
        """
        Führt Google-Suche über Serper API durch
        
        SICHERHEITSCHECK: Nur für AKTIVE Aufträge erlaubt!
        """
        # KRITISCHER SICHERHEITSCHECK
        if workflow_type != 'AKTIV' or auftrag_status != 'AKTIV':
            raise Exception(
                "FEHLER: Serper API ist NUR für AKTIVE Aufträge erlaubt! "
                f"Workflow: {workflow_type}, Status: {auftrag_status}"
            )
        
        logger.info(f"Serper API Aufruf für AKTIVEN Auftrag: {query}")
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'gl': 'de',  # Deutschland
            'hl': 'de',  # Deutsch
            'num': 10
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Serper API erfolgreich: {len(data.get('organic', []))} Ergebnisse")
            
            return {
                'success': True,
                'data': data,
                'cost': 0.01,  # Geschätzte Kosten pro Aufruf
                'query': query
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Serper API Fehler: {e}")
            return {
                'success': False,
                'error': str(e),
                'cost': 0.00
            }
    
    def get_news(self, query, workflow_type=None, auftrag_status=None):
        """
        Holt aktuelle News über Serper API
        
        SICHERHEITSCHECK: Nur für AKTIVE Aufträge erlaubt!
        """
        # KRITISCHER SICHERHEITSCHECK
        if workflow_type != 'AKTIV' or auftrag_status != 'AKTIV':
            raise Exception(
                "FEHLER: Serper API ist NUR für AKTIVE Aufträge erlaubt! "
                f"Workflow: {workflow_type}, Status: {auftrag_status}"
            )
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'gl': 'de',
            'hl': 'de'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/news",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return {
                'success': True,
                'data': response.json(),
                'cost': 0.01
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Serper News API Fehler: {e}")
            return {
                'success': False,
                'error': str(e),
                'cost': 0.00
            }
