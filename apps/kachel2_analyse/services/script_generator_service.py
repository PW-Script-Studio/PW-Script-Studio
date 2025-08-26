"""
Script Generator Service - Gemeinsamer Service für beide Workflows
Nutzt die spezialisierten OpenRouter Services (Opus, Gemini, Sonnet)
Optimiert für PW-Script-Studio mit Django-Integration
"""

import logging
from typing import Dict, Optional
from django.conf import settings
from .openrouter.opus_service import OpusService
from .openrouter.gemini_service import GeminiService
from .openrouter.sonnet_service import SonnetService

logger = logging.getLogger(__name__)


class OpusScriptGenerator:
    """
    Gemeinsamer Script Generator für beide Workflows
    Nutzt spezialisierte OpenRouter Services basierend auf Qualitätsstufe
    """
    
    def __init__(self):
        """Initialize mit OpenRouter Services"""
        self.opus = OpusService()      # Höchste Qualität
        self.sonnet = SonnetService()  # Mittlere Qualität  
        self.gemini = GeminiService()  # Schnell und günstig
        
        # Qualitätsstufen-Mapping
        self.quality_services = {
            'bronze': self.gemini,
            'silber': self.sonnet,
            'gold': self.opus
        }
    
    def generate(self, title: str, description: str = "", keywords: str = "", 
                 word_count: int = 1000, quality: str = 'bronze') -> dict:
        """
        Generiert Script-Content basierend auf Qualitätsstufe
        
        Args:
            title: Titel des Scripts (generiert oder vom Kunden)
            description: Beschreibung/Briefing
            keywords: Keywords für den Content
            word_count: Gewünschte Wortanzahl
            quality: bronze/silber/gold
        
        Returns:
            dict mit generiertem Content und Metadaten
        """
        logger.info(f"Generiere Script: '{title}' (Qualität: {quality}, Wörter: {word_count})")
        
        # Service basierend auf Qualität auswählen
        service = self.quality_services.get(quality, self.gemini)
        
        # Prompt erstellen
        prompt = self._create_prompt(title, description, keywords, word_count, quality)
        
        # Token-Limit basierend auf Qualität
        max_tokens = {
            'bronze': 2000,
            'silber': 3000,
            'gold': 4000
        }.get(quality, 2000)
        
        try:
            # Content generieren
            result = service.generate_content(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            if result['success']:
                logger.info(f"Script erfolgreich generiert - {result['tokens_used']} Tokens")
                
                return {
                    'success': True,
                    'title': title,
                    'content': result['content'],
                    'quality': quality,
                    'word_count_target': word_count,
                    'word_count_actual': len(result['content'].split()),
                    'tokens_used': result['tokens_used'],
                    'cost': result['cost'],
                    'model': result['model'],
                    'service': service.__class__.__name__
                }
            else:
                logger.error(f"Script-Generierung fehlgeschlagen: {result['error']}")
                return {
                    'success': False,
                    'error': result['error'],
                    'cost': 0.00
                }
                
        except Exception as e:
            logger.error(f"Unerwarteter Fehler bei Script-Generierung: {e}")
            return {
                'success': False,
                'error': str(e),
                'cost': 0.00
            }

    def _create_prompt(self, title: str, description: str, keywords: str,
                       word_count: int, quality: str) -> str:
        """
        Erstellt optimierten Prompt basierend auf Qualitätsstufe
        """
        base_prompt = f"""
Erstelle ein hochwertiges Script mit folgendem Titel: "{title}"

Beschreibung/Briefing: {description}

Keywords: {keywords}

Anforderungen:
- Zielwortanzahl: {word_count} Wörter
- Qualitätsstufe: {quality}
- Professioneller, ansprechender Schreibstil
- Gut strukturiert mit klaren Abschnitten
- Zielgruppengerecht und informativ
"""

        # Qualitätsspezifische Ergänzungen
        if quality == 'bronze':
            base_prompt += """
- Fokus auf Klarheit und Verständlichkeit
- Direkte, einfache Sprache
- Grundlegende Struktur
"""
        elif quality == 'silber':
            base_prompt += """
- Erweiterte Struktur mit Übergängen
- Einbindung von Beispielen
- Ausgewogener Ton zwischen informativ und unterhaltsam
- Berücksichtigung aktueller Trends
"""
        elif quality == 'gold':
            base_prompt += """
- Höchste Qualität mit innovativen Ansätzen
- Tiefgreifende Analyse und Insights
- Perfekte Struktur mit fließenden Übergängen
- Einbindung aktueller Forschung und Trends
- Optimiert für maximale Wirkung
- Call-to-Actions und Engagement-Elemente
"""

        base_prompt += f"""

Erstelle das Script jetzt mit ca. {word_count} Wörtern:
"""

        return base_prompt

    def get_service_info(self) -> dict:
        """
        Gibt Informationen über den Script Generator zurück
        """
        return {
            'service': 'OpusScriptGenerator',
            'quality_levels': ['bronze', 'silber', 'gold'],
            'models': {
                'bronze': 'Google Gemini 2.5 Flash',
                'silber': 'Claude Sonnet 3.5',
                'gold': 'Claude Opus 4.1'
            },
            'supported_workflows': ['OFFEN', 'AKTIV']
        }
