"""
Claude Sonnet Service über OpenRouter API
Ausgewogene Content-Generierung zwischen Qualität und Geschwindigkeit
"""
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class SonnetService:
    """
    Service für Claude Sonnet über OpenRouter
    """
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "anthropic/claude-3.5-sonnet"
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY nicht konfiguriert!")
    
    def generate_content(self, prompt: str, max_tokens: int = 3500, temperature: float = 0.7) -> dict:
        """
        Generiert Content mit Claude Sonnet
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://pw-script-studio.com',
            'X-Title': 'PW Script Studio'
        }
        
        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': 0.9
        }
        
        try:
            logger.info(f"Sonnet API Aufruf - Tokens: {max_tokens}")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=90
            )
            response.raise_for_status()
            
            data = response.json()
            content = data['choices'][0]['message']['content']
            tokens_used = data.get('usage', {}).get('total_tokens', max_tokens)
            
            logger.info(f"Sonnet erfolgreich - Tokens: {tokens_used}")
            
            return {
                'success': True,
                'content': content,
                'tokens_used': tokens_used,
                'model': self.model,
                'cost': self._calculate_cost(tokens_used)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Sonnet API Fehler: {e}")
            return {
                'success': False,
                'error': str(e),
                'cost': 0.00
            }
    
    def _calculate_cost(self, tokens: int) -> float:
        """
        Berechnet geschätzte Kosten für Sonnet
        """
        # Sonnet Kosten: ca. $0.003 per 1K tokens (Input) + $0.015 per 1K tokens (Output)
        # Vereinfachte Schätzung: $0.009 per 1K tokens (Durchschnitt)
        return (tokens / 1000) * 0.009
