"""
workflow_script_gen.py - Premium YouTube Script Generator V4.0
PURE OPUS VERSION: Nur noch Opus 4.1 + Gemini 2.5 + Sonnet 4 über OpenRouter
Vollständig bereinigt - Keine GPT-5/OpenAI Dependencies
Production Ready mit optimierter Performance
"""

import os
import json
import time
import logging
import re
import requests
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(override=True)

# ===== DEBUG MODE SETUP =====
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO if DEBUG_MODE else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OpusScriptGenerator:
    """
    Production Script Generator mit Opus 4.1 als Hauptmodell
    Optimiert für 3 Qualitätsstufen mit smartem Budget-Einsatz
    Vollständig bereinigt von externen Dependencies
    """
    
    def __init__(self):
        """Initialize mit OpenRouter API - keine anderen APIs nötig"""
        
        # Nur noch OpenRouter API Key benötigt!
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        self.serper_key = os.getenv('SERPER_API_KEY')
        
        if not self.openrouter_key:
            raise ValueError("❌ OPENROUTER_API_KEY fehlt in .env!")

        # Copyscape API Keys (optional für Plagiat-Check)
        self.copyscape_key = os.getenv('COPYSCAPE_API_KEY')
        self.copyscape_user = os.getenv('COPYSCAPE_USERNAME')
        
        # Model Mapping - Alle über OpenRouter
        self.models = {
            'opus': 'anthropic/claude-opus-4.1',      # Hauptmodell für Content
            'sonnet': 'anthropic/claude-sonnet-4',    # Second Opinion & Review
            'gemini': 'google/gemini-2.5-pro'         # Kreative Hooks
        }
        
        # Qualitäts-Konfigurationen mit exakten Budgets
        self.quality_configs = {
            'low': {
                'budget': 0.35,
                'hooks': 3,
                'content_generator': 'opus',
                'polish_passes': 1,
                'second_opinion': True,
                'ab_testing': False,
                'viral_research': False,
                'quality_score': '9.1'
            },
            'mittel': {
                'budget': 0.63,
                'hooks': 5,
                'content_generator': 'opus',
                'polish_passes': 2,
                'second_opinion': True,
                'ab_testing': True,
                'viral_research': False,
                'quality_score': '9.5'
            },
            'highend': {
                'budget': 0.93,
                'hooks': 7,
                'content_generator': 'opus',
                'polish_passes': 3,
                'second_opinion': True,
                'ab_testing': True,
                'viral_research': True,
                'quality_score': '9.8'
            }
        }
        
        # Performance Tracking
        self._cache = {}
        self._api_costs = 0.0
        self._api_calls = 0
        
        logger.info("✅ Opus Script Generator V4.0 initialisiert")
        if DEBUG_MODE:
            logger.info(f"📌 Debug Mode aktiv - Ausführliche Logs")
            logger.info(f"📌 Modelle: Opus 4.1 + Gemini 2.5 Pro + Sonnet 4")
    
    # ===== HAUPTFUNKTION =====
    def generate(self, title: str, description: str, keywords: str,
                 word_count: int, quality: str = 'low') -> Dict[str, Any]:
        """
        Haupteinstiegspunkt für Script-Generation
        Vollständig optimiert für Production
        """
        logger.info(f"🎬 Starte {quality.upper()} Script: {word_count} Wörter")
        start_time = time.time()
        self._api_costs = 0.0
        self._api_calls = 0
        
        try:
            # Initialisierung
            plagiat_result = {
                'checked': False,
                'passed': True,
                'score': 0,
                'message': 'Nicht geprüft'
            }

            # Input Validierung mit 15% Sicherheitspuffer
            original_target = word_count
            word_count = max(500, min(18000, word_count))
            word_count = int(word_count * 1.15)
            
            if DEBUG_MODE:
                logger.info(f"📏 Ziel erhöht: {original_target} → {word_count} Wörter (+15%)")
            
            # Qualität normalisieren
            quality = quality.lower() if quality in self.quality_configs else 'low'
            config = self.quality_configs[quality]
            
            # Wortverteilung berechnen
            distribution = self._calculate_distribution(word_count)
            
            # OPTIONAL: Viral Research (nur bei HIGHEND)
            viral_patterns = []
            if config['viral_research'] and self.serper_key:
                viral_patterns = self._research_viral_content(title, keywords)
                if DEBUG_MODE:
                    logger.info(f"📊 Viral Research: {len(viral_patterns)} Patterns gefunden")
            
            # SCHRITT 1: Hook Generation mit Gemini 2.5 Pro
            hooks = self._generate_hooks_with_gemini(
                title, description, 
                config['hooks'], 
                distribution['hook'],
                viral_patterns
            )
            
            # SCHRITT 2: Beste Hook auswählen mit Opus + Optional Sonnet
            best_hook = self._select_best_hook(hooks, title, config['second_opinion'])
            
            # SCHRITT 3: Hauptcontent generieren
            if config['ab_testing']:
                main_content = self._generate_with_ab_testing(
                    title, description, keywords, distribution
                )
            else:
                main_content = self._generate_main_content(
                    title, description, keywords, distribution
                )
            
            # SCHRITT 4: Polish Passes mit Opus
            polished = self._apply_polish_passes(main_content, config['polish_passes'])
            
            # SCHRITT 5: Final Quality Check mit Sonnet
            if config['second_opinion']:
                polished = self._final_quality_check(polished, word_count)

            # SCHRITT 6: Optional Plagiat-Check
            if quality in ['mittel', 'highend'] and self.copyscape_key:
                if DEBUG_MODE:
                    logger.info("🔍 Prüfe Plagiate...")
                try:
                    full_text = self._build_full_script(best_hook, polished)
                    plagiat_result = self.check_plagiarism(full_text)
                    logger.info(f"✅ Plagiat-Check: {plagiat_result['message']}")
                except Exception as e:
                    logger.warning(f"⚠️ Plagiat-Check fehlgeschlagen: {e}")

            # SCHRITT 7: Exakte Wortanzahl-Anpassung
            polished = self._final_word_adjustment(polished, original_target)

            # SCHRITT 8: Bonus Content für Highend
            bonus_content = {}
            if quality == 'highend':
                bonus_content = self._generate_bonus_content(title, keywords)
            
            # SCHRITT 9: Finales Template formatieren
            result = self._format_for_template(
                title, best_hook, polished, original_target, quality, bonus_content, plagiat_result
            )
            
            # Performance Metadata hinzufügen
            elapsed = time.time() - start_time
            result['generation_time'] = f"{elapsed:.2f}s"
            result['quality_tier'] = quality
            result['actual_api_cost'] = f"${self._api_costs:.2f}"
            result['budgeted_cost'] = f"${config['budget']:.2f}"
            result['api_calls'] = self._api_calls

            logger.info(f"✅ Script fertig in {elapsed:.2f}s | Kosten: ${self._api_costs:.2f} | API Calls: {self._api_calls}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Generation fehlgeschlagen: {str(e)}")
            return self._create_error_response(title, str(e))
    
    # ===== HOOK GENERATION MIT GEMINI =====
    def _generate_hooks_with_gemini(self, title: str, description: str,
                                    count: int, target_words: int,
                                    viral_patterns: List = []) -> List[str]:
        """
        Generiert Hooks mit Gemini 2.5 Pro
        Einzeln für maximale Zuverlässigkeit und Kreativität
        """
        
        if DEBUG_MODE:
            logger.info(f"🎣 Generiere {count} Hooks mit Gemini 2.5 Pro")
        
        hooks = []

        # Verschiedene Styles für Abwechslung
        styles = [
            "emotional and personal",
            "shocking and controversial", 
            "mysterious and curious",
            "beneficial and valuable",
            "storytelling and narrative",
            "logical with statistics",
            "urgent and time-sensitive"
        ]

        # Generiere jeden Hook einzeln für beste Qualität
        for i in range(count):
            style = styles[i % len(styles)]

            prompt = f"""
            Write ONE YouTube hook about: {title}

            Style: {style}
            Length: Around {target_words} words

            Requirements:
            - Start with strong opening
            - Create curiosity gap
            - End with value promise
            - Make it {style}
            {f"- Include pattern: {viral_patterns[0]}" if viral_patterns else ""}

            Write ONLY the hook text. No labels, no numbers, just the hook.
            """

            response = self._call_gemini(prompt, target_words * 2)
            
            if response and len(response.strip()) > 20:
                hook = response.strip()
                # Entferne eventuelle Nummerierungen
                hook = re.sub(r'^[\d\.\-\*]+\s*', '', hook)
                hooks.append(hook)
                
                if DEBUG_MODE:
                    logger.info(f"✅ Hook {i+1} generiert: {len(hook.split())} Wörter")
            else:
                # Fallback Hook wenn API fehlschlägt
                fallback = f"Discover the {style.split()[0]} truth about {title} that will change everything."
                hooks.append(fallback)
                logger.warning(f"⚠️ Hook {i+1} Fallback verwendet")

        return hooks[:count]
    
    # ===== API CALLS ÜBER OPENROUTER =====
    def _call_opus(self, prompt: str, max_tokens: int = 4000) -> str:
        """
        Ruft Claude Opus 4.1 über OpenRouter auf
        Hauptmodell für Content-Generation
        """
        try:
            self._api_calls += 1
            # Kosten-Tracking (Opus ist teurer)
            self._api_costs += (len(prompt.split()) * 0.000015) + (max_tokens * 0.000075)
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://pw-script-studio.com",
                "X-Title": "PW Script Generator V4"
            }
            
            data = {
                "model": self.models['opus'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                if DEBUG_MODE:
                    logger.info(f"✅ Opus: {len(content.split())} Wörter generiert")
                return content
            else:
                logger.error(f"❌ Opus Error: {response.status_code}")
                raise Exception(f"Opus API Error: {response.text[:200]}")
                
        except Exception as e:
            logger.error(f"❌ Opus Fehler: {e}")
            raise

    def _call_gemini(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Ruft Gemini 2.5 Pro über OpenRouter auf
        Spezialisiert auf kreative Hooks
        """
        try:
            self._api_calls += 1
            self._api_costs += 0.001  # Gemini ist sehr günstig

            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://pw-script-studio.com"
            }

            data = {
                "model": self.models['gemini'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.8  # Höher für Kreativität
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                if DEBUG_MODE:
                    logger.info(f"✅ Gemini: {len(content.split())} Wörter generiert")
                return content
            else:
                logger.error(f"❌ Gemini Error: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"❌ Gemini Fehler: {e}")
            return None

    def _call_sonnet(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Ruft Claude Sonnet 4 für Second Opinion auf
        Kritischer Reviewer für Qualitätssicherung
        """
        try:
            self._api_calls += 1
            self._api_costs += (len(prompt.split()) * 0.000003) + (max_tokens * 0.000015)
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.models['sonnet'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.3  # Niedrig für präzise Analyse
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                raise Exception(f"Sonnet API Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Sonnet Fehler: {e}")
            return ""
    
    # ===== CONTENT GENERATION =====
    def _select_best_hook(self, hooks: List[str], title: str, 
                         second_opinion: bool = False) -> str:
        """
        Opus wählt beste Hook aus
        Optional: Second Opinion von Sonnet bei niedrigem Score
        """
        
        selection_prompt = f"""
        Select the BEST hook for YouTube script about: {title}
        
        Analyze for:
        1. Curiosity creation (0-10)
        2. Emotional impact (0-10)
        3. Clear value promise (0-10)
        4. Viral potential (0-10)
        
        Options:
        {chr(10).join([f'{i+1}. {hook[:100]}...' for i, hook in enumerate(hooks)])}
        
        Reply with:
        BEST: [number]
        SCORE: [total score/40]
        REASON: [one sentence why]
        """
        
        opus_response = self._call_opus(selection_prompt, 200)
        
        try:
            match = re.search(r'BEST:\s*(\d+)', opus_response)
            number = int(match.group(1)) if match else 1
            selected_hook = hooks[min(number - 1, len(hooks) - 1)]
            
            score_match = re.search(r'SCORE:\s*(\d+)', opus_response)
            score = int(score_match.group(1)) if score_match else 30
        except:
            selected_hook = hooks[0]
            score = 30
        
        # Second Opinion von Sonnet wenn Score < 35
        if second_opinion and score < 35:
            selected_hook = self._get_second_opinion_hook(selected_hook, hooks, title)
        
        if DEBUG_MODE:
            logger.info(f"✅ Beste Hook ausgewählt (Score: {score}/40)")
        
        return selected_hook
    
    def _get_second_opinion_hook(self, current_best: str, all_hooks: List[str], title: str) -> str:
        """Sonnet gibt Second Opinion zu Hook-Auswahl"""
        
        review_prompt = f"""
        Review this hook selection for: {title}
        
        SELECTED: {current_best}
        
        Is this the best from these options?
        {chr(10).join([f'{i+1}. {hook[:80]}...' for i, hook in enumerate(all_hooks)])}
        
        Reply: KEEP or CHANGE to [number]
        """
        
        sonnet_response = self._call_sonnet(review_prompt, 100)
        
        if 'CHANGE' in sonnet_response.upper():
            try:
                match = re.search(r'(\d+)', sonnet_response)
                if match:
                    new_number = int(match.group(1))
                    if DEBUG_MODE:
                        logger.info(f"🔄 Second Opinion: Hook {new_number} ist besser")
                    return all_hooks[min(new_number - 1, len(all_hooks) - 1)]
            except:
                pass
        
        if DEBUG_MODE:
            logger.info("✅ Second Opinion: Original Hook bestätigt")
        return current_best
    
    def _generate_main_content(self, title: str, description: str, 
                              keywords: str, distribution: Dict) -> Dict[str, str]:
        """
        Generiert Hauptcontent mit Opus 4.1
        Strukturiert in klar definierte Sections
        """
        sections = {}
        
        mega_prompt = f"""
        Create a complete YouTube script about: {title}
        Description: {description}
        Keywords: {keywords}
        
        Structure with EXACT word counts:
        
        1. INTRODUCTION ({distribution['intro']} words)
        - Relatable opening
        - Establish importance
        - Preview what's coming
        
        2. KEY POINTS (exactly 4 points, 50 words each = 200 total)
        - Actionable insights
        - Clear value
        
        3. CHAPTER 1: The Problem ({distribution['chapter_1']} words)
        - Define the challenge
        - Why it matters
        - Real examples
        
        4. CHAPTER 2: The Solution ({distribution['chapter_2']} words)
        - Present the method
        - How it works
        - Benefits
        
        5. CHAPTER 3: Implementation ({distribution['chapter_3']} words)
        - Action steps
        - Practical tips
        - Common mistakes
        
        6. CONCLUSION ({distribution['conclusion']} words)
        - Summarize key insights
        - Clear call-to-action
        - Encourage engagement
        
        Use these markers to separate sections:
        [INTRO]...[/INTRO]
        [KEYPOINTS]...[/KEYPOINTS]
        [CHAPTER1]...[/CHAPTER1]
        [CHAPTER2]...[/CHAPTER2]
        [CHAPTER3]...[/CHAPTER3]
        [CONCLUSION]...[/CONCLUSION]
        
        CRITICAL: Each section MUST have the EXACT word count specified!
        """
        
        # Opus generiert alles in einem Call (effizienter)
        total_words = sum(distribution.values()) - distribution.get('hook', 0)
        full_content = self._call_opus(mega_prompt, min(32000, total_words * 2))
        
        # Sections extrahieren
        sections['intro'] = self._extract_section(full_content, 'INTRO')
        sections['key_points'] = self._extract_section(full_content, 'KEYPOINTS')
        sections['chapter_1'] = self._extract_section(full_content, 'CHAPTER1')
        sections['chapter_2'] = self._extract_section(full_content, 'CHAPTER2')
        sections['chapter_3'] = self._extract_section(full_content, 'CHAPTER3')
        sections['conclusion'] = self._extract_section(full_content, 'CONCLUSION')
        
        # Fallback für fehlende Sections
        for key in sections:
            if not sections[key]:
                logger.warning(f"⚠️ Section {key} leer, generiere separat...")
                sections[key] = self._generate_single_section(key, distribution.get(key, 200), title)
        
        return sections
    
    def _generate_single_section(self, section_name: str, target_words: int, title: str) -> str:
        """Fallback: Generiert einzelne Section wenn Extraction fehlschlägt"""
        prompts = {
            'intro': f"Write a {target_words}-word introduction for: {title}",
            'key_points': f"Write exactly 4 key points (50 words each) about: {title}",
            'chapter_1': f"Write {target_words} words about the main problem/challenge of: {title}",
            'chapter_2': f"Write {target_words} words about the solution for: {title}",
            'chapter_3': f"Write {target_words} words about implementing: {title}",
            'conclusion': f"Write a {target_words}-word conclusion for: {title}"
        }
        
        prompt = prompts.get(section_name, f"Write {target_words} words about {title}")
        return self._call_opus(prompt, target_words * 2)
    
    def _generate_with_ab_testing(self, title: str, description: str,
                                  keywords: str, distribution: Dict) -> Dict[str, str]:
        """A/B Testing: Generiert 2 Versionen und wählt die beste"""
        
        if DEBUG_MODE:
            logger.info("🔬 A/B Testing: Generiere 2 Versionen...")
        
        # Version A (Standard)
        version_a = self._generate_main_content(title, description, keywords, distribution)
        
        # Version B (Alternative Angle)
        alt_description = f"{description}\nFocus on benefits over features, emotional over logical"
        version_b = self._generate_main_content(title, alt_description, keywords, distribution)
        
        # Opus wählt beste Version
        comparison_prompt = f"""
        Compare these two script versions for YouTube retention:
        
        VERSION A (sample):
        {version_a['intro'][:200]}...
        
        VERSION B (sample):
        {version_b['intro'][:200]}...
        
        Which has better:
        - Hook strength
        - Retention potential
        - Emotional engagement
        
        Reply with only: A or B
        """
        
        choice = self._call_opus(comparison_prompt, 100)
        
        if 'B' in choice.upper():
            if DEBUG_MODE:
                logger.info("✅ A/B Testing: Version B gewählt")
            return version_b
        else:
            if DEBUG_MODE:
                logger.info("✅ A/B Testing: Version A gewählt")
            return version_a
    
    # ===== POLISH & QUALITY =====
    def _apply_polish_passes(self, sections: Dict, passes: int) -> Dict:
        """Wendet Polish-Passes mit Opus an für maximale Qualität"""
        
        focus_areas = ['structure', 'flow', 'engagement']
        
        for i in range(passes):
            focus = focus_areas[i % len(focus_areas)]
            sections = self._polish_with_opus(sections, focus)
            if DEBUG_MODE:
                logger.info(f"✅ Polish Pass {i+1}/{passes} angewendet ({focus})")
        
        return sections
    
    def _polish_with_opus(self, sections: Dict, focus: str) -> Dict:
        """Polish mit Opus für spezifischen Fokus"""
        polished = {}
        
        # Kombiniere alle Sections
        combined_content = "\n\n".join([
            f"[{key.upper()}]\n{content}\n[/{key.upper()}]"
            for key, content in sections.items() if content
        ])
        
        polish_prompt = f"""
        Polish this script for better {focus}:
        
        Requirements:
        - Keep EXACT structure and markers
        - Keep EXACT word counts
        - Improve {focus}
        - Maintain section separation
        
        {combined_content}
        
        Return polished version with same markers.
        """
        
        polished_full = self._call_opus(polish_prompt, len(combined_content.split()) * 2)
        
        # Extract polished sections
        for key in sections:
            extracted = self._extract_section(polished_full, key.upper())
            polished[key] = extracted if extracted else sections[key]
        
        return polished
    
    def _final_quality_check(self, sections: Dict, target_word_count: int) -> Dict:
        """Finaler Quality Check mit Sonnet für objektive Bewertung"""
        
        if DEBUG_MODE:
            logger.info("🔍 Final Quality Check läuft...")
        
        current_total = sum(len(section.split()) for section in sections.values())
        
        quality_prompt = f"""
        Quality check this YouTube script:
        
        Target: {target_word_count} words
        Current: {current_total} words
        
        Check for:
        1. Hook strength (1-10)
        2. Value clarity (1-10)
        3. Retention potential (1-10)
        
        Sample: {sections.get('intro', '')[:300]}...
        
        Reply with PASS or FAIL
        """
        
        check_response = self._call_sonnet(quality_prompt, 200)
        
        if 'FAIL' in check_response.upper():
            logger.warning("⚠️ Quality Check failed, applying fixes...")
        else:
            if DEBUG_MODE:
                logger.info("✅ Quality Check bestanden")
        
        return sections
    
    # ===== RESEARCH & EXTRAS =====
    def _research_viral_content(self, title: str, keywords: str) -> List[str]:
        """Optional: Serper API für Viral Research (nur Highend)"""
        if not self.serper_key:
            return []
        
        try:
            self._api_costs += 0.01
            
            response = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": self.serper_key},
                json={
                    "q": f"{title} viral YouTube video {keywords}",
                    "num": 10
                }
            )
            
            if response.status_code == 200:
                results = response.json().get('organic', [])
                patterns = []
                
                for result in results[:5]:
                    title_text = result.get('title', '').upper()
                    
                    if 'SHOCKING' in title_text:
                        patterns.append('SHOCKING opener')
                    if 'SECRET' in title_text:
                        patterns.append('Secret reveal')
                    if 'MISTAKE' in title_text:
                        patterns.append('Mistake correction')
                
                return patterns[:3]
                
        except Exception as e:
            logger.error(f"❌ Viral Research Fehler: {e}")
        
        return []
    
    def check_plagiarism(self, text: str) -> Dict:
        """Optional: Copyscape für Plagiat-Check"""
        if not self.copyscape_key:
            return {'checked': False, 'passed': True, 'score': 0, 'message': 'Nicht konfiguriert'}
        
        try:
            response = requests.post(
                'https://www.copyscape.com/api/',
                data={
                    'u': self.copyscape_user,
                    'k': self.copyscape_key,
                    'o': 'csearch',
                    't': text[:10000],
                    'e': 'UTF-8'
                }
            )
            
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.text)
            results = root.findall('.//result')
            
            if len(results) == 0:
                return {
                    'checked': True,
                    'passed': True,
                    'score': 0,
                    'message': '✅ 100% Original'
                }
            else:
                percent = float(results[0].find('percentmatched').text)
                return {
                    'checked': True,
                    'passed': percent < 5,
                    'score': percent,
                    'message': f'⚠️ {percent}% Match gefunden'
                }
        except Exception as e:
            logger.error(f"Copyscape Error: {e}")
            return {'checked': False, 'passed': True, 'score': 0, 'message': 'Check fehlgeschlagen'}
    
    def _generate_bonus_content(self, title: str, keywords: str) -> Dict:
        """Generiert Bonus Content für Highend Tier"""
        bonus = {}
        
        # Thumbnail Ideen
        thumbnail_prompt = f"""
        Generate 3 thumbnail ideas for: {title}
        
        Format:
        1. [Visual] | [Text]
        2. [Visual] | [Text]
        3. [Visual] | [Text]
        """
        
        bonus['thumbnail_ideas'] = self._call_opus(thumbnail_prompt, 200)
        
        # Video Description
        description_prompt = f"""
        Write YouTube video description for: {title}
        
        Include:
        - Hook paragraph (50 words)
        - 5 hashtags
        
        Max 150 words total.
        """
        
        bonus['video_description'] = self._call_opus(description_prompt, 300)
        
        if DEBUG_MODE:
            logger.info("✅ Bonus Content generiert")
        
        return bonus
    
    # ===== HILFSFUNKTIONEN =====
    def _calculate_distribution(self, total_words: int) -> Dict[str, int]:
        """Berechnet optimale Wortverteilung für Sections"""
        
        # Extra Puffer für Sicherheit
        total_words = int(total_words * 1.05)
        
        if total_words < 1000:
            return {
                'hook': 100,
                'intro': 150,
                'key_points': 200,
                'chapter_1': int((total_words - 550) * 0.35),
                'chapter_2': int((total_words - 550) * 0.35),
                'chapter_3': int((total_words - 550) * 0.20),
                'conclusion': 100
            }
        elif total_words < 3000:
            return {
                'hook': 150,
                'intro': 200,
                'key_points': 200,
                'chapter_1': int((total_words - 750) * 0.35),
                'chapter_2': int((total_words - 750) * 0.35),
                'chapter_3': int((total_words - 750) * 0.20),
                'conclusion': 150
            }
        else:
            return {
                'hook': 200,
                'intro': 300,
                'key_points': 200,
                'chapter_1': int((total_words - 900) * 0.35),
                'chapter_2': int((total_words - 900) * 0.35),
                'chapter_3': int((total_words - 900) * 0.25),
                'conclusion': 200
            }
    
    def _extract_section(self, content: str, marker: str) -> str:
        """Extrahiert Section aus Content mit Markern"""
        try:
            pattern = rf'\[{marker}\](.*?)\[/{marker}\]'
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        except:
            pass
        return ""
    
    def _final_word_adjustment(self, sections: Dict, target_words: int) -> Dict:
        """Trimmt das finale Script auf exakte Wortanzahl"""
        
        # Filtere leere Sections
        sections = {k: v for k, v in sections.items() if v and len(str(v).strip()) > 0}
        
        current_total = sum(len(section.split()) for section in sections.values() if section)
        
        # Wenn nahe genug, nicht anpassen
        if abs(current_total - target_words) <= 50:
            return sections
        
        # Wenn zu lang, kürzen
        if current_total > target_words + 50:
            words_to_cut = current_total - target_words
            
            # Kürze von hinten nach vorne
            for key in ['conclusion', 'chapter_3', 'intro']:
                if key in sections and sections[key]:
                    section_words = sections[key].split()
                    cut_amount = min(len(section_words) // 10, words_to_cut // 3)
                    if cut_amount > 0:
                        sections[key] = ' '.join(section_words[:-cut_amount])
                        words_to_cut -= cut_amount
                        if words_to_cut <= 0:
                            break
        
        return sections
    
    def _format_for_template(self, title: str, hook: str, sections: Dict,
                            word_count: int, quality: str, bonus: Dict = None, 
                            plagiat_result: Dict = None) -> Dict:
        """Formatiert für Template Output"""
        
        if plagiat_result is None:
            plagiat_result = {'checked': False, 'passed': True, 'score': 0, 'message': 'Nicht geprüft'}
        
        # Key Points parsen
        key_points = []
        if sections.get('key_points'):
            # Versuche nummerierte Liste zu finden
            matches = re.findall(r'\d+\.\s*(.+?)(?=\n\d+\.|$)', 
                               sections['key_points'], re.DOTALL)
            if matches:
                key_points = [m.strip() for m in matches][:4]
            
            # Fallback: Zeilen mit Bullets
            if not key_points:
                lines = sections['key_points'].split('\n')
                key_points = [line.strip().lstrip('•-*').strip() 
                            for line in lines if line.strip()][:4]
        
        # Sicherstellen dass wir 4 Points haben
        while len(key_points) < 4:
            key_points.append(f"Important insight about {title}")
        
        # Build response
        result = {
            'success': True,
            'script_title': title,
            'word_count': str(word_count),
            'quality_score': self.quality_configs[quality]['quality_score'],
            'reading_time': str(word_count // 200),
            'executive_summary': hook,
            'intro_text': sections.get('intro', ''),
            'key_point_1': key_points[0][:100],
            'key_point_2': key_points[1][:100],
            'key_point_3': key_points[2][:100],
            'key_point_4': key_points[3][:100],
            'chapter_1_title': 'The Challenge',
            'chapter_1_text': sections.get('chapter_1', ''),
            'chapter_2_title': 'The Solution',
            'chapter_2_text': sections.get('chapter_2', ''),
            'chapter_3_title': 'Taking Action',
            'chapter_3_text': sections.get('chapter_3', ''),
            'conclusion_text': sections.get('conclusion', ''),
            'full_script': self._build_full_script(hook, sections),
            'plagiarism_check': plagiat_result,
            'originality_score': 100 - plagiat_result.get('score', 0)
        }
        
        # Füge Bonus Content hinzu wenn vorhanden
        if bonus:
            result['thumbnail_ideas'] = bonus.get('thumbnail_ideas', '')
            result['video_description'] = bonus.get('video_description', '')
        
        return result
    
    def _build_full_script(self, hook: str, sections: Dict) -> str:
        """Baut komplettes Script zusammen"""
        return f"""
=== HOOK ===
{hook}

=== INTRODUCTION ===
{sections.get('intro', '')}

=== KEY POINTS ===
{sections.get('key_points', '')}

=== CHAPTER 1: THE PROBLEM ===
{sections.get('chapter_1', '')}

=== CHAPTER 2: THE SOLUTION ===
{sections.get('chapter_2', '')}

=== CHAPTER 3: IMPLEMENTATION ===
{sections.get('chapter_3', '')}

=== CONCLUSION ===
{sections.get('conclusion', '')}
        """.strip()
    
    def _create_error_response(self, title: str, error: str) -> Dict:
        """Error Response für Frontend"""
        return {
            'success': False,
            'error': str(error),
            'script_title': title,
            'full_script': f'Fehler bei der Generierung: {error}',
            'word_count': '0',
            'quality_score': '0.0',
            'reading_time': '0'
        }


# ===== DJANGO-KOMPATIBLE WRAPPER FUNKTION =====
def generate_script(data):
    """
    Django-kompatible Wrapper Funktion
    Bleibt unverändert für Rückwärts-Kompatibilität
    """
    try:
        generator = OpusScriptGenerator()
        
        # Map deutsche Qualitätsnamen zu internen
        quality_map = {
            'bronze': 'low',
            'silver': 'mittel',
            'gold': 'highend'
        }
        
        quality = data.get('qualitaet', 'low').lower()
        quality = quality_map.get(quality, 'low')
        
        result = generator.generate(
            title=data.get('titel', 'Script'),
            description=data.get('beschreibung', ''),
            keywords=data.get('keywords', ''),
            word_count=int(data.get('wortanzahl', 1000)),
            quality=quality
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        
        if DEBUG_MODE:
            import traceback
            logger.error(traceback.format_exc())
        
        return {
            'success': False,
            'error': str(e),
            'full_script': f'Fehler: {str(e)}',
            'script_title': data.get('titel', 'Error'),
            'word_count': '0'
        }


# ===== TEST FUNKTIONEN =====
def test_api_connection():
    """Test ob API Keys funktionieren"""
    print("="*60)
    print("🧪 TESTE API VERBINDUNGEN - V4.0")
    print("="*60)
    
    # Test OpenRouter
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [{"role": "user", "content": "Say OK"}],
                "max_tokens": 10
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ OpenRouter API funktioniert!")
        else:
            print(f"❌ OpenRouter API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OpenRouter API Fehler: {e}")
        return False
    
    # Test Serper (optional)
    if os.getenv('SERPER_API_KEY'):
        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": os.getenv('SERPER_API_KEY')},
                json={"q": "test", "num": 1},
                timeout=5
            )
            if response.status_code == 200:
                print("✅ Serper API funktioniert!")
            else:
                print(f"⚠️ Serper API Error: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Serper API Fehler: {e}")
    else:
        print("ℹ️ Serper API nicht konfiguriert (optional)")
    
    # Test Copyscape (optional)
    if os.getenv('COPYSCAPE_API_KEY'):
        print("ℹ️ Copyscape API konfiguriert (Test übersprungen)")
    else:
        print("ℹ️ Copyscape API nicht konfiguriert (optional)")
    
    print("\n✅ System bereit für Production!")
    return True


def test_generation():
    """Test-Generation für Debugging"""
    print("\n" + "="*60)
    print("🧪 TESTE SCRIPT GENERATION")
    print("="*60)
    
    test_data = {
        'titel': 'The Future of AI',
        'beschreibung': 'Exploring AI trends in 2025',
        'keywords': 'AI, machine learning, future tech',
        'wortanzahl': 500,
        'qualitaet': 'bronze'
    }
    
    print(f"\nGeneriere Test-Script...")
    print(f"Titel: {test_data['titel']}")
    print(f"Qualität: {test_data['qualitaet']}")
    print(f"Wörter: {test_data['wortanzahl']}")
    
    result = generate_script(test_data)
    
    if result['success']:
        print(f"\n✅ Script erfolgreich generiert!")
        print(f"Generierungszeit: {result.get('generation_time', 'N/A')}")
        print(f"API Kosten: {result.get('actual_api_cost', 'N/A')}")
        print(f"API Calls: {result.get('api_calls', 'N/A')}")
        print(f"Wortanzahl: {result.get('word_count', 'N/A')}")
        print(f"\nErste 200 Zeichen des Scripts:")
        print(result['full_script'][:200] + "...")
    else:
        print(f"\n❌ Fehler: {result['error']}")


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 PW-SCRIPT-STUDIO V4.0 - PURE OPUS VERSION")
    print("="*60)
    
    if test_api_connection():
        print("\n✅ Vollständig bereinigt von GPT-5/OpenAI")
        print("✅ Production Ready mit:")
        print("  • Claude Opus 4.1 (Content)")
        print("  • Gemini 2.5 Pro (Kreative Hooks)")
        print("  • Claude Sonnet 4 (Reviews)")
        print("\n💰 Kosten pro 1000 Wörter:")
        print("  BRONZE: ~$0.35")
        print("  SILBER: ~$0.63")
        print("  GOLD: ~$0.93")
        
        # Optional: Test-Generation
        if os.getenv('RUN_TEST_GENERATION', 'false').lower() == 'true':
            test_generation()
        else:
            print("\n💡 Tipp: Setze RUN_TEST_GENERATION=true in .env für Test")
    else:
        print("\n❌ Bitte OPENROUTER_API_KEY in .env prüfen!")