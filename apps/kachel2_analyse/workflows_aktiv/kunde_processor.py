"""
Processor für AKTIVE Aufträge (Kundenprojekte)
Nutzt den gemeinsamen Script Generator aus services/

WICHTIG:
- Titel wird vom KUNDEN vorgegeben (NICHT generieren!)
- MIT Serper API für Research
- Fokus auf wöchentliche Organisation
"""
import logging
from django.conf import settings
from apps.kachel2_analyse.services.script_generator_service import OpusScriptGenerator
from apps.kachel2_analyse.services.serper_service import SerperService

logger = logging.getLogger(__name__)

class KundeProcessor:
    """
    Verarbeitet AKTIVE Aufträge (Kundenprojekte)
    
    WORKFLOW: AKTIV (Kundenprojekte)
    - Titel vom Kunden vorgegeben (NICHT generieren!)
    - MIT Serper API für Research
    - Wöchentliche Organisation
    """
    
    def __init__(self):
        self.script_generator = OpusScriptGenerator()
        self.serper = SerperService()  # NUR für aktive Aufträge!
    
    def process_kunde_auftrag(self, kunde_title: str, kunde_briefing: str, 
                               word_count: int = 1000, quality: str = 'gold') -> dict:
        """
        Verarbeitet Kundenauftrag mit Online-Research
        
        Args:
            kunde_title: VOM KUNDEN vorgegebener Titel (NICHT generieren!)
            kunde_briefing: Briefing vom Kunden
            word_count: Gewünschte Wortanzahl
            quality: Qualitätsstufe (bronze/silber/gold)
        
        Returns:
            dict mit Script-Inhalt und Research-Daten
        """
        logger.info(f"Verarbeite AKTIVEN Kundenauftrag: '{kunde_title}'")
        
        # WICHTIG: Titel wird NICHT generiert, sondern vom Kunden übernommen!
        if not kunde_title:
            raise ValueError("Kunde-Titel ist erforderlich für aktive Aufträge!")
        
        try:
            # 1. Online-Research mit Serper API (NUR für aktive Aufträge!)
            research_data = self._conduct_research(kunde_title)
            
            # 2. Script generieren mit KUNDE-TITEL (nicht generiert!)
            result = self.script_generator.generate(
                title=kunde_title,  # VOM KUNDEN!
                description=kunde_briefing,
                keywords=self._extract_keywords_from_research(research_data),
                word_count=word_count,
                quality=quality
            )
            
            # 3. Research-Daten hinzufügen
            result['research_data'] = research_data
            result['workflow_type'] = 'AKTIV'
            result['title_source'] = 'VOM_KUNDEN'
            
            logger.info(f"AKTIVER Auftrag erfolgreich verarbeitet: '{kunde_title}'")
            return result
            
        except Exception as e:
            logger.error(f"Fehler bei AKTIVEM Auftrag '{kunde_title}': {e}")
            return {
                'success': False,
                'error': str(e),
                'workflow_type': 'AKTIV'
            }
    
    def _conduct_research(self, kunde_title: str) -> dict:
        """
        Führt Research mit Serper API durch (NUR für aktive Aufträge!)
        """
        logger.info("Starte Research mit Serper API für AKTIVEN Auftrag")
        
        try:
            # KRITISCH: Serper API nur für AKTIVE Aufträge!
            result = self.serper.search(
                query=kunde_title,
                workflow_type='AKTIV',
                auftrag_status='AKTIV'
            )
            
            if result['success']:
                logger.info(f"Research erfolgreich für: {kunde_title}")
                return result['data']
            else:
                logger.warning(f"Research fehlgeschlagen: {result['error']}")
                return {}
                
        except Exception as e:
            logger.error(f"Research-Fehler: {e}")
            return {}
    
    def _extract_keywords_from_research(self, research_data: dict) -> str:
        """
        Extrahiert Keywords aus Research-Daten
        """
        keywords = []
        
        if 'organic' in research_data:
            for result in research_data['organic'][:3]:
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                
                # Einfache Keyword-Extraktion
                text = f"{title} {snippet}".lower()
                words = text.split()
                
                # Häufige Wörter sammeln (vereinfacht)
                for word in words:
                    if len(word) > 4 and word.isalpha():
                        keywords.append(word)
        
        # Top 5 Keywords zurückgeben
        return ', '.join(list(set(keywords))[:5])
    
    def validate_kunde_input(self, kunde_title: str, kunde_briefing: str) -> dict:
        """
        Validiert Kunden-Input für aktive Aufträge
        """
        errors = []
        
        if not kunde_title or len(kunde_title.strip()) < 5:
            errors.append("Kunde-Titel muss mindestens 5 Zeichen haben")
        
        if not kunde_briefing or len(kunde_briefing.strip()) < 20:
            errors.append("Kunde-Briefing muss mindestens 20 Zeichen haben")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def get_workflow_info(self) -> dict:
        """
        Gibt Informationen über den AKTIVEN Workflow zurück
        """
        return {
            'workflow_type': 'AKTIV',
            'description': 'Kundenprojekte',
            'title_source': 'VOM_KUNDEN',
            'serper_api': True,
            'openrouter_api': True,
            'organization': 'WÖCHENTLICH',
            'research_required': True,
            'quality_default': 'gold'
        }
