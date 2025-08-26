import requests
import os
import re
import sys
import json
sys.path.append('Backend/apps/kachel1_jobanalysis')
from category_detector import CategoryDetector
from dotenv import load_dotenv
load_dotenv(override=True)  # WICHTIG: override=True!

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

def call_opus_41(prompt):
    """Call Claude Opus 4.1 via OpenRouter API"""
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-opus-4.1",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"OpenRouter Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"API Error: {e}")
        return None

def call_sonnet_4(prompt):
    """Call Claude Sonnet 4 for reviews via OpenRouter"""
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 500
            }
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return None
    except Exception as e:
        print(f"Sonnet API Error: {e}")
        return None

def serper_search(query):
    """Search Google via Serper API"""
    if not SERPER_API_KEY:
        return []
    
    try:
        response = requests.post(
            url="https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "q": query,
                "num": 5
            }
        )
        
        if response.status_code == 200:
            results = response.json()
            return results.get('organic', [])
        else:
            print(f"Serper Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Serper Error: {e}")
        return []

def extract_job_details(job_text):
    """Extract budget, hours, duration from job text"""
    details = {
        'budget': 'Nicht angegeben',
        'hours': 'Nicht angegeben', 
        'duration': 'Nicht angegeben'
    }
    
    # Budget extrahieren ($X-$Y oder $X.00 - $Y.00)
    budget_patterns = [
        r'\$(\d+(?:\.\d{2})?)\s*[-â€“]\s*\$(\d+(?:\.\d{2})?)',
        r'\$(\d+)\s*to\s*\$(\d+)',
        r'\$(\d+)/hr',
        r'\$(\d+)\s*hourly'
    ]
    for pattern in budget_patterns:
        if match := re.search(pattern, job_text, re.IGNORECASE):
            if len(match.groups()) == 2:
                details['budget'] = f"${match.group(1)}-${match.group(2)}"
            else:
                details['budget'] = f"${match.group(1)}/Stunde"
            break
    
    # Stunden extrahieren
    hours_patterns = [
        r'(\d+)\+?\s*hrs?/week',
        r'(\d+)\+?\s*hours?\s*per\s*week',
        r'More than\s*(\d+)\s*hrs?/week',
        r'(\d+)-(\d+)\s*hrs?/week'
    ]
    for pattern in hours_patterns:
        if match := re.search(pattern, job_text, re.IGNORECASE):
            if len(match.groups()) == 2:
                details['hours'] = f"{match.group(1)}-{match.group(2)} Stunden/Woche"
            else:
                details['hours'] = f"{match.group(1)}+ Stunden/Woche"
            break
    
    # Dauer extrahieren
    duration_patterns = [
        r'(\d+)\s*to\s*(\d+)\s*months?',
        r'(\d+)-(\d+)\s*months?',
        r'(\d+)\s*months?',
        r'(\d+)\s*weeks?'
    ]
    for pattern in duration_patterns:
        if match := re.search(pattern, job_text, re.IGNORECASE):
            if len(match.groups()) == 2:
                details['duration'] = f"{match.group(1)}-{match.group(2)} Monate"
            elif 'week' in pattern:
                details['duration'] = f"{match.group(1)} Wochen"
            else:
                details['duration'] = f"{match.group(1)} Monate"
            break
    
    return details

def needs_review(job_text, confidence):
    """Determine if review is needed"""
    # Review bei wichtigen Jobs oder unsicherer Kategorie
    if "$100" in job_text or "$200" in job_text or "$300" in job_text:
        return True
    if confidence < 80:
        return True
    if "expert" in job_text.lower() or "top-tier" in job_text.lower():
        return True
    return False

def review_and_improve(title, description, keywords, job_text):
    """
    Sonnet reviews SCRIPT TITLE and BRIEFING for work sample quality
    NICHT für Bewerbungen!
    """
    review_prompt = f"""
    Review this YOUTUBE SCRIPT TITLE and BRIEFING for a work sample:

    JOB CONTEXT: {job_text[:300]}

    GENERATED SCRIPT TITLE: {title}
    SCRIPT BRIEFING: {description[:300]}
    KEYWORDS: {keywords}

    Evaluate as SCRIPT WORK SAMPLE (not application):
    1. Is the title clickbait-worthy for YouTube? (1-10)
    2. Does title show expertise in the niche? (1-10)
    3. Is briefing clear for script creation? (1-10)
    4. Are keywords relevant? (1-10)

    IMPORTANT: This is a SCRIPT TITLE for a work sample, NOT an application title!

    Return format:
    SCORE: X/10
    IMPROVEMENTS: [suggestions for better YouTube title]
    KEEP_AS: SCRIPT_TITLE (never change to application)
    """

    review = call_sonnet_4(review_prompt)

    # Parse score from review
    score = 7  # Default
    if review and "SCORE:" in review:
        try:
            score_text = review.split("SCORE:")[1].split("/")[0].strip()
            score = int(score_text)
        except:
            score = 7

    # If score < 8, improve with Opus - aber als SCRIPT TITEL!
    if score < 8 and review:
        improve_prompt = f"""
        Improve this YOUTUBE SCRIPT TITLE based on feedback:

        ORIGINAL SCRIPT TITLE: {title}
        ORIGINAL BRIEFING: {description}

        REVIEW FEEDBACK: {review}

        Generate an IMPROVED YOUTUBE SCRIPT TITLE that:
        1. Is more clickbait-worthy
        2. Shows expertise better
        3. Fits the job niche
        4. Maximum 60 characters

        CRITICAL: Return a YOUTUBE VIDEO TITLE, not an application title!
        No "Experienced", "Available", "Hire me" etc.

        Examples of good script titles:
        - "The Hidden Truth About [Topic]"
        - "Why [Thing] Changes Everything"
        - "[Number] Secrets That [Result]"

        Return format:
        Title: [YouTube script title]
        Description: [Updated briefing if needed]
        """

        improved_response = call_opus_41(improve_prompt)
        if improved_response:
            # Extract improved parts - aber validiere dass es Script-Titel sind!
            if "Title:" in improved_response:
                new_title = improved_response.split("Title:")[1].split("\n")[0].strip()

                # VALIDIERUNG: Ist es wirklich ein Script-Titel?
                forbidden_words = ['experienced', 'available', 'hire', 'freelancer', 'writer', 'ready to']
                if not any(word in new_title.lower() for word in forbidden_words):
                    title = new_title
                else:
                    # Behalte Original wenn "Verbesserung" eine Bewerbung ist
                    print(f"⚠️ Review tried to create application title, keeping original")

            if "Description:" in improved_response:
                new_description = improved_response.split("Description:")[1].strip()
                # Nur übernehmen wenn es kein Bewerbungstext ist
                if not any(word in new_description.lower() for word in ["i'm", "i am", "my experience", "hire me"]):
                    description = new_description

    return title, description, keywords, score

def analyze_job(data):
    """Main function for job analysis workflow"""
    job_text = data.get('text', '')
    
    # SCHRITT 1: Category Detection (lokal)
    detector = CategoryDetector()
    category_result = detector.detect_category(job_text)
    
    # SCHRITT 2: Script-Titel fÃ¼r Arbeitsprobe generieren (GEÃ„NDERT!)
    title_prompt = f"""
    Create a YOUTUBE SCRIPT TITLE for a work sample that demonstrates expertise for this job:
    
    Job: {job_text[:500]}
    Category: {category_result.category}
    
    WICHTIG: Dies ist ein SCRIPT-TITEL fÃ¼r eine Arbeitsprobe, KEINE Bewerbung!
    
    Der Titel soll:
    1. Ein echter YouTube-Video-Titel sein (clickbait-wÃ¼rdig)
    2. Zum Job-Thema passen und Kompetenz zeigen
    3. Neugier wecken (Zahlen, Versprechen, Geheimnisse)
    4. Maximum 60 Zeichen
    5. Das Format zeigen das der Client sucht
    
    Beispiele nach Kategorie:
    - AI/Tech: "7 ChatGPT Tricks That Broke The Algorithm"
    - War History: "The 10 Minutes That Decided D-Day"
    - True Crime: "She Googled This Before Disappearing"
    - How-To: "From $0 to $10K in 30 Days (Proof Inside)"
    - Screenwriting: "The Call - Episode 1 (60 Seconds)"
    
    Generiere einen viralen Script-Titel der zeigt, dass ich die Nische verstehe.
    
    Return ONLY the script title, nothing else.
    """
    
    generated_title = call_opus_41(title_prompt)
    if not generated_title:
        generated_title = f"Expert {category_result.category.replace('_', ' ').title()} Specialist Available"
    
    # SCHRITT 3: Serper Recherche mit dem Titel
    search_results = []
    if SERPER_API_KEY:
        search_query = f"{generated_title} freelance rates expertise"
        search_results = serper_search(search_query)
    
    # Job Details extrahieren
    job_details = extract_job_details(job_text)

    # SCHRITT 4: Titel-Analyse fÃ¼r Script-Briefing (GEÃ„NDERT!)
    description_prompt = f"""
    Analysiere diesen generierten Titel fÃ¼r Script-Erstellung:
    "{generated_title.strip()}"

    Job-Kategorie: {category_result.category}
    Keywords gefunden: {', '.join(category_result.keywords_found[:5])}

    Erstelle ein BRIEFING fÃ¼r den Script-Writer in Spalte 3:

    === TITEL-INTERPRETATION ===
    [Was verspricht dieser Titel konkret? Welches Problem lÃ¶st er?]

    === ZIELGRUPPE ===
    [Wer ist der ideale Kunde basierend auf diesem Titel?]

    === KERN-BOTSCHAFTEN FÃœR SCRIPT ===
    â€¢ [Hauptversprechen 1 aus dem Titel]
    â€¢ [Hauptversprechen 2 aus dem Titel]  
    â€¢ [Hauptversprechen 3 aus dem Titel]

    === SCRIPT-ANFORDERUNGEN ===
    â€¢ [Welche konkreten Elemente muss das Script haben?]
    â€¢ [Welche Beweise/Beispiele sollten rein?]
    â€¢ [Welche Resultate versprechen wir?]

    === EMPFOHLENE TONALITÃ„T ===
    [Basierend auf Titel: Professionell/Casual/Technisch/Enthusiastisch?]

    === KONKRETE INHALTE FÃœR SCRIPT ===
    â€¢ [Tools/Methoden die zum Titel passen]
    â€¢ [Zahlen/Metriken die Ã¼berzeugen]
    â€¢ [Beispiele die den Titel unterstÃ¼tzen]

    WICHTIG: Dies ist ein BRIEFING fÃ¼r Script-Erstellung basierend auf dem TITEL.
    KEINE Bewerbung! KEINE Job-Analyse! 
    Fokus: Was muss ins Script um den Titel-Versprechen gerecht zu werden?
    """
    
    generated_description = call_opus_41(description_prompt)
    
    # OPTIONAL: Validierung ob wirklich Briefing (nicht Bewerbung)
    if generated_description and any(word in generated_description.lower() for word in ['hi there', "i'm excited", 'best regards', 'let me help']):
        # Nochmal versuchen mit stÃ¤rkerem Prompt
        retry_prompt = description_prompt + "\n\nKEINE BEWERBUNG! NUR TECHNISCHES BRIEFING! Keine Ich-Form!"
        generated_description = call_opus_41(retry_prompt)
    
    if not generated_description:
        generated_description = "Script-Briefing konnte nicht generiert werden."
    
    # SCHRITT 5: Keywords extrahieren
    keywords_prompt = f"""
    Extract 8 highly relevant keywords for an Upwork proposal from this job:
    {job_text[:300]}

    Focus on:
    - Technical skills mentioned
    - Tools and platforms
    - Deliverables
    - Industry terms
    - Experience requirements

    Format: keyword1, keyword2, keyword3...
    Return ONLY comma-separated keywords.
    """
    
    keywords = call_opus_41(keywords_prompt)
    if not keywords:
        keywords = ", ".join(category_result.keywords_found[:8])

    # NEUE SECTION: Second Opinion Review
    # TEMPORÄRER FIX - Review deaktivieren falls weiter Probleme
    review_needed = needs_review(job_text, category_result.confidence)  # Normal
    # review_needed = False  # Uncomment to disable review completely
    review_score = 0
    
    if review_needed:
        # Sonnet 4 Review + Potential Improvement
        generated_title, generated_description, keywords, review_score = review_and_improve(
            generated_title.strip(),
            generated_description.strip(),
            keywords.strip(),
            job_text[:1000]
        )
    
    # Django-kompatibel: Return dict statt jsonify
    return {
        'category': category_result.category,
        'confidence': category_result.confidence,
        'title': generated_title.strip(),
        'description': generated_description.strip(),
        'keywords': keywords.strip(),
        'research_count': len(search_results),
        'review_score': review_score,
        'reviewed': review_needed
    }