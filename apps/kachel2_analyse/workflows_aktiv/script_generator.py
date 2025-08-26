"""
Script Generator für AKTIVE Aufträge (Kundenprojekte)

WICHTIG:
- Titel wird vom KUNDEN vorgegeben (NICHT generieren!)
- MIT Serper API für Research
- Fokus auf wöchentliche Organisation
"""
import logging
from django.conf import settings
from apps.kachel2_analyse.services.serper_service import SerperService
from apps.kachel2_analyse.services.openrouter.openrouter_service import OpenRouterService

logger = logging.getLogger(__name__)

class ScriptGenerator:
    """
    Generiert Scripts für aktive Kundenprojekte
    
    WORKFLOW: AKTIV (Kundenprojekte)
    - Titel vom Kunden vorgegeben (NICHT generieren!)
    - MIT Serper API für Research
    - Wöchentliche Organisation
    """
    
    def __init__(self):
        self.serper = SerperService()
        self.openrouter = OpenRouterService()
    
    def generate_script(self, kunde_title, kunde_briefing, keywords=None, week_number=None):
        """
        Generiert Script für aktiven Kundenauftrag
        
        Args:
            kunde_title: VOM KUNDEN vorgegebener Titel (NICHT generieren!)
            kunde_briefing: Briefing vom Kunden
            keywords: Keywords vom Kunden
            week_number: Wochennummer für Organisation
        
        Returns:
            dict mit Script-Inhalt und Research-Daten
        """
        logger.info(f"Generiere Script für AKTIVEN Auftrag: '{kunde_title}' (Woche {week_number})")
        
        # WICHTIG: Titel wird NICHT generiert, sondern vom Kunden übernommen!
        if not kunde_title:
            raise ValueError("Kunde-Titel ist erforderlich für aktive Aufträge!")
        
        try:
            # 1. Research mit Serper API (NUR für aktive Aufträge!)
            research_data = self._conduct_research(kunde_title, keywords)
            
            # 2. Script-Content generieren basierend auf Research
            script_content = self._generate_content(
                kunde_title=kunde_title,
                kunde_briefing=kunde_briefing,
                research_data=research_data,
                keywords=keywords
            )
            
            total_cost = research_data['total_cost'] + script_content['cost']
            
            logger.info(f"Script generiert - Titel: '{kunde_title}', Kosten: ${total_cost:.2f}")
            
            return {
                'success': True,
                'kunde_title': kunde_title,  # Vom Kunden, NICHT generiert!
                'content': script_content['content'],
                'research_data': research_data['data'],
                'week_number': week_number,
                'total_cost': total_cost,
                'serper_calls': research_data['api_calls'],
                'workflow_type': 'AKTIV'
            }
            
        except Exception as e:
            logger.error(f"Fehler bei Script-Generierung: {e}")
            return {
                'success': False,
                'error': str(e),
                'total_cost': 0.00
            }
    
    def _conduct_research(self, kunde_title, keywords=None):
        """
        Führt Research mit Serper API durch (NUR für aktive Aufträge!)
        """
        logger.info("Starte Research mit Serper API für AKTIVEN Auftrag")
        
        research_queries = [kunde_title]
        if keywords:
            research_queries.extend(keywords.split(','))
        
        all_research_data = []
        total_cost = 0.00
        api_calls = 0
        
        for query in research_queries[:3]:  # Max 3 Queries
            query = query.strip()
            if not query:
                continue
                
            # KRITISCH: Serper API nur für AKTIVE Aufträge!
            result = self.serper.search(
                query=query,
                workflow_type='AKTIV',
                auftrag_status='AKTIV'
            )
            
            if result['success']:
                all_research_data.append({
                    'query': query,
                    'results': result['data']
                })
                total_cost += result['cost']
                api_calls += 1
            else:
                logger.warning(f"Research fehlgeschlagen für Query: {query}")
        
        return {
            'data': all_research_data,
            'total_cost': total_cost,
            'api_calls': api_calls
        }
    
    def _generate_content(self, kunde_title, kunde_briefing, research_data, keywords=None):
        """
        Generiert Script-Content basierend auf Research-Daten
        """
        # Research-Zusammenfassung für Prompt
        research_summary = ""
        for research in research_data['data']:
            research_summary += f"\nQuery: {research['query']}\n"
            for result in research['results'].get('organic', [])[:3]:
                research_summary += f"- {result.get('title', '')}: {result.get('snippet', '')}\n"
        
        prompt = f"""
        Erstelle ein hochwertiges Script basierend auf folgenden Informationen:
        
        TITEL (vom Kunden vorgegeben): {kunde_title}
        
        KUNDEN-BRIEFING:
        {kunde_briefing}
        
        KEYWORDS: {keywords or 'Keine spezifischen Keywords'}
        
        RESEARCH-DATEN:
        {research_summary}
        
        Erstelle ein umfassendes, gut strukturiertes Script (1000-1500 Wörter), das:
        1. Den vom Kunden vorgegebenen Titel exakt verwendet
        2. Das Briefing vollständig umsetzt
        3. Die Research-Daten intelligent einbindet
        4. Professionell und zielgruppengerecht geschrieben ist
        5. Aktuelle Informationen und Trends berücksichtigt
        
        Das Script soll höchste Qualität haben und den Kundenerwartungen entsprechen.
        """
        
        response = self.openrouter.generate_content(
            prompt=prompt,
            model_quality='gold'  # Höchste Qualität für Kundenprojekte
        )
        
        return response
