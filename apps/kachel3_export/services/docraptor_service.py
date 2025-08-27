import docraptor
import logging
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class DocRaptorService:
    """
    DocRaptor API Service für professionelle PDF-Generierung
    """
    
    def __init__(self):
        # DocRaptor API-Key aus Settings
        api_key = getattr(settings, 'DOCRAPTOR_API_KEY', 'YOUR_API_KEY_HERE')
        docraptor.configuration.username = api_key
        self.client = docraptor.DocApi()
    
    def generate_pdf(self, script_data):
        """
        Generiert professionelles PDF mit DocRaptor
        
        Args:
            script_data (dict): Daten für PDF-Generierung
            
        Returns:
            bytes: PDF-Daten
        """
        try:
            html = self._create_html_template(script_data)
            
            # DocRaptor API-Call
            response = self.client.create_doc({
                "test": getattr(settings, 'DEBUG', True),  # Test-Mode in Development
                "document_type": "pdf",
                "document_content": html,
                "name": f"{script_data.get('id', 'script')}.pdf",
                "prince_options": {
                    "media": "print",
                    "baseurl": "https://docraptor.com/",
                }
            })
            
            logger.info(f"PDF erfolgreich generiert für: {script_data.get('id', 'unknown')}")
            return response
            
        except Exception as e:
            logger.error(f"DocRaptor Fehler: {e}")
            raise Exception(f"PDF-Generierung fehlgeschlagen: {str(e)}")
    
    def _create_html_template(self, data):
        """
        Erstellt professionelles HTML-Template für PDF
        
        Args:
            data (dict): Script/Arbeitsprobe-Daten
            
        Returns:
            str: HTML-Template
        """
        # Qualitäts-Badge-Klasse bestimmen
        quality = data.get('quality', 'bronze').lower()
        quality_class = f"quality-{quality}"
        
        # Datum formatieren
        date_str = data.get('date', datetime.now().strftime('%d.%m.%Y'))
        
        return f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{data.get('titel', 'Script')}</title>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                    @bottom-center {{
                        content: "Seite " counter(page) " von " counter(pages);
                        font-size: 10px;
                        color: #666;
                    }}
                }}
                
                body {{
                    font-family: 'Georgia', 'Times New Roman', serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                
                .header {{
                    border-bottom: 3px solid #2196F3;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                
                .title {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #1976D2;
                    margin: 0 0 15px 0;
                    text-align: center;
                }}
                
                .subtitle {{
                    font-size: 16px;
                    color: #666;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                
                .metadata {{
                    background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                    border-left: 5px solid #2196F3;
                }}
                
                .metadata-row {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 10px;
                }}
                
                .metadata-label {{
                    font-weight: bold;
                    color: #1976D2;
                }}
                
                .content {{
                    white-space: pre-wrap;
                    text-align: justify;
                    font-size: 14px;
                    line-height: 1.8;
                    margin-top: 30px;
                }}
                
                .quality-badge {{
                    padding: 8px 16px;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 12px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .quality-gold {{
                    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                    color: #8B4513;
                    box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
                }}
                
                .quality-silber {{
                    background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
                    color: #333;
                    box-shadow: 0 2px 4px rgba(192, 192, 192, 0.3);
                }}
                
                .quality-bronze {{
                    background: linear-gradient(135deg, #CD7F32 0%, #A0522D 100%);
                    color: white;
                    box-shadow: 0 2px 4px rgba(205, 127, 50, 0.3);
                }}
                
                .quality-premium {{
                    background: linear-gradient(135deg, #8A2BE2 0%, #4B0082 100%);
                    color: white;
                    box-shadow: 0 2px 4px rgba(138, 43, 226, 0.3);
                }}
                
                .footer {{
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                    text-align: center;
                }}
                
                .logo {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #2196F3;
                    margin-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">🚀 PW-Script-Studio</div>
                <h1 class="title">{data.get('titel', 'Script')}</h1>
                <div class="subtitle">Professionell generierter Content</div>
                
                <div class="metadata">
                    <div class="metadata-row">
                        <span class="metadata-label">Auftrag-ID:</span>
                        <span>{data.get('id', 'N/A')}</span>
                    </div>
                    <div class="metadata-row">
                        <span class="metadata-label">Typ:</span>
                        <span>{data.get('type', 'Script')}</span>
                    </div>
                    <div class="metadata-row">
                        <span class="metadata-label">Qualität:</span>
                        <span class="quality-badge {quality_class}">
                            {quality.upper()}
                        </span>
                    </div>
                    <div class="metadata-row">
                        <span class="metadata-label">Erstellt am:</span>
                        <span>{date_str}</span>
                    </div>
                    <div class="metadata-row">
                        <span class="metadata-label">Status:</span>
                        <span>Fertiggestellt</span>
                    </div>
                </div>
            </div>
            
            <div class="content">{data.get('content', 'Kein Inhalt verfügbar.')}</div>
            
            <div class="footer">
                <div class="logo">PW-Script-Studio</div>
                <div>Professionelle Script-Erstellung & Content-Management</div>
                <div>Generiert am: {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')}</div>
            </div>
        </body>
        </html>
        """
