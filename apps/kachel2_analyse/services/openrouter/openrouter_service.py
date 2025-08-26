"""
OpenRouter API Service für beide Workflows

Dieser Service wird sowohl für OFFENE als auch AKTIVE Aufträge verwendet.
Unterschiedliche Modelle basierend auf Qualitätsstufe.
"""
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class OpenRouterService:
    """
    Service für OpenRouter API - für beide Workflows
    """
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY nicht konfiguriert!")
        
        # Modell-Mapping basierend auf Qualitätsstufe
        self.models = {
            'bronze': {
                'model': 'meta-llama/llama-3.1-8b-instruct:free',
                'cost_per_token': 0.0000001,
                'max_tokens': 2000
            },
            'silber': {
                'model': 'meta-llama/llama-3.1-70b-instruct',
                'cost_per_token': 0.0000005,
                'max_tokens': 3000
            },
            'gold': {
                'model': 'anthropic/claude-3.5-sonnet',
                'cost_per_token': 0.000001,
                'max_tokens': 4000
            }
        }
    
    def generate_content(self, prompt, model_quality='bronze', max_tokens=None):
        """
        Generiert Content über OpenRouter API
        
        Args:
            prompt: Text-Prompt für die Generierung
            model_quality: bronze/silber/gold
            max_tokens: Maximale Token-Anzahl (optional)
        
        Returns:
            dict mit generiertem Content und Kosten
        """
        if model_quality not in self.models:
            raise ValueError(f"Unbekannte Qualitätsstufe: {model_quality}")
        
        model_config = self.models[model_quality]
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://pw-script-studio.com',
            'X-Title': 'PW Script Studio'
        }
        
        payload = {
            'model': model_config['model'],
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': max_tokens or model_config['max_tokens'],
            'temperature': 0.7,
            'top_p': 0.9
        }
        
        try:
            logger.info(f"OpenRouter API Aufruf - Modell: {model_config['model']}")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Content extrahieren
            content = data['choices'][0]['message']['content']
            
            # Kosten berechnen (geschätzt)
            tokens_used = data.get('usage', {}).get('total_tokens', 1000)
            estimated_cost = tokens_used * model_config['cost_per_token']
            
            logger.info(f"OpenRouter erfolgreich - Tokens: {tokens_used}, Kosten: ${estimated_cost:.4f}")
            
            return {
                'success': True,
                'content': content,
                'cost': estimated_cost,
                'tokens_used': tokens_used,
                'model': model_config['model'],
                'quality': model_quality
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API Fehler: {e}")
            return {
                'success': False,
                'error': str(e),
                'cost': 0.00
            }
        except KeyError as e:
            logger.error(f"OpenRouter Response Format Fehler: {e}")
            return {
                'success': False,
                'error': f"Unerwartetes Response Format: {e}",
                'cost': 0.00
            }
    
    def get_model_info(self, quality_level):
        """
        Gibt Informationen über das Modell für eine Qualitätsstufe zurück
        """
        if quality_level not in self.models:
            return None
        
        return self.models[quality_level]
    
    def estimate_cost(self, prompt_length, quality_level='bronze'):
        """
        Schätzt die Kosten für einen Prompt
        """
        if quality_level not in self.models:
            return 0.00
        
        # Grobe Schätzung: 1 Zeichen ≈ 0.25 Token
        estimated_tokens = prompt_length * 0.25 * 2  # Input + Output
        cost_per_token = self.models[quality_level]['cost_per_token']
        
        return estimated_tokens * cost_per_token
