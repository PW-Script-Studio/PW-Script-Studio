"""
Upwork Job Analyzer für OFFENE Aufträge (Bewerbungen)

WICHTIG: 
- Titel wird GENERIERT (nicht vom Kunden vorgegeben)
- KEINE Serper API Nutzung
- Fokus auf Qualitätsstufen und Kosten-Tracking
"""
import logging
from django.conf import settings
from apps.kachel2_analyse.services.openrouter.openrouter_service import OpenRouterService

logger = logging.getLogger(__name__)

class UpworkAnalyzer:
    """
    Analysiert Upwork-Jobs und generiert Arbeitsproben für Bewerbungen
    
    WORKFLOW: OFFEN (Bewerbungen)
    - Titel wird automatisch generiert
    - KEINE Serper API (das ist für aktive Aufträge!)
    - Qualitätsstufen: Bronze/Silber/Gold
    """
    
    def __init__(self):
        self.openrouter = OpenRouterService()
    
    def analyze_job_posting(self, job_description, quality_level='bronze'):
        """
        Analysiert Upwork Job-Posting und generiert passende Arbeitsprobe
        
        Args:
            job_description: Beschreibung des Upwork-Jobs
            quality_level: bronze/silber/gold (bestimmt API-Kosten)
        
        Returns:
            dict mit generiertem Titel und Inhalt
        """
        logger.info(f"Analysiere Upwork-Job für OFFENEN Auftrag (Qualität: {quality_level})")
        
        # SICHERHEITSCHECK: Keine Serper API für offene Aufträge!
        if 'serper' in job_description.lower():
            logger.warning("WARNUNG: Serper API Erwähnung in offenem Auftrag erkannt!")
        
        # Prompt für Titel-Generierung
        title_prompt = f"""
        Analysiere diese Upwork-Jobbeschreibung und generiere einen passenden Titel für eine Arbeitsprobe:
        
        Job-Beschreibung:
        {job_description}
        
        Generiere einen präzisen, professionellen Titel (max. 100 Zeichen) für eine Arbeitsprobe, 
        die zeigt, dass ich für diesen Job qualifiziert bin.
        
        Antworte nur mit dem Titel, keine Erklärungen.
        """
        
        # Content-Prompt basierend auf Qualitätsstufe
        content_prompts = {
            'bronze': f"""
            Erstelle eine kurze Arbeitsprobe (300-500 Wörter) basierend auf dieser Jobbeschreibung:
            {job_description}
            
            Die Arbeitsprobe soll zeigen, dass ich die Anforderungen verstehe und umsetzen kann.
            Fokus auf Klarheit und Professionalität.
            """,
            'silber': f"""
            Erstelle eine detaillierte Arbeitsprobe (500-800 Wörter) basierend auf dieser Jobbeschreibung:
            {job_description}
            
            Die Arbeitsprobe soll meine Expertise demonstrieren und konkrete Lösungsansätze zeigen.
            Inkludiere relevante Beispiele und Best Practices.
            """,
            'gold': f"""
            Erstelle eine umfassende, hochwertige Arbeitsprobe (800-1200 Wörter) basierend auf dieser Jobbeschreibung:
            {job_description}
            
            Die Arbeitsprobe soll meine Expertise auf höchstem Niveau demonstrieren.
            Inkludiere detaillierte Analysen, konkrete Strategien und innovative Ansätze.
            Zeige tiefes Verständnis der Branche und aktueller Trends.
            """
        }
        
        try:
            # Titel generieren
            title_response = self.openrouter.generate_content(
                prompt=title_prompt,
                model_quality=quality_level
            )
            
            if not title_response['success']:
                raise Exception(f"Titel-Generierung fehlgeschlagen: {title_response['error']}")
            
            generated_title = title_response['content'].strip()
            
            # Content generieren
            content_response = self.openrouter.generate_content(
                prompt=content_prompts[quality_level],
                model_quality=quality_level
            )
            
            if not content_response['success']:
                raise Exception(f"Content-Generierung fehlgeschlagen: {content_response['error']}")
            
            total_cost = title_response['cost'] + content_response['cost']
            
            logger.info(f"Arbeitsprobe generiert - Titel: '{generated_title}', Kosten: ${total_cost:.2f}")
            
            return {
                'success': True,
                'generated_title': generated_title,
                'content': content_response['content'],
                'quality_level': quality_level,
                'total_cost': total_cost,
                'api_calls': 2,  # Titel + Content
                'workflow_type': 'OFFEN'
            }
            
        except Exception as e:
            logger.error(f"Fehler bei Upwork-Analyse: {e}")
            return {
                'success': False,
                'error': str(e),
                'total_cost': 0.00
            }
    
    def get_quality_costs(self):
        """
        Gibt die Kosten für verschiedene Qualitätsstufen zurück
        """
        return {
            'bronze': 0.35,
            'silber': 0.63,
            'gold': 0.93
        }
