import requests
from bs4 import BeautifulSoup

def scrape_wikivoyage_dubai() -> str:
    """
    Scrapes the main Dubai wikivoyage page and extracts relevant sections 
    (See, Do, Buy, Eat, Drink, Sleep, Get around, Budget) as baseline data.
    """
    url = "https://en.wikivoyage.org/wiki/Dubai"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Failed to retrieve data from {url}. Status code: {response.status_code}"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # We want to extract text from certain headers
    target_headers = ['Get_around', 'See', 'Do', 'Buy', 'Eat', 'Drink', 'Sleep', 'Budget']
    extracted_text = "### Dubai Baseline Data ###\n\n"
    
    for header_id in target_headers:
        header_span = soup.find('span', id=header_id)
        if not header_span:
            continue
            
        header_element = header_span.parent
        extracted_text += f"==== {header_id} ====\n"
        
        # Extract content until the next header of the same level
        sibling = header_element.find_next_sibling()
        while sibling and sibling.name not in ['h2', 'h3']:
            if sibling.name in ['p', 'ul', 'ol', 'div']:
                text = sibling.get_text(strip=True)
                if text:
                    # Basic truncation to avoid passing too much context in one go if it's huge, 
                    # but typically wikivoyage sections are manageable.
                    extracted_text += text + "\n"
            sibling = sibling.find_next_sibling()
            
        extracted_text += "\n"
        
    return extracted_text

def get_baseline_data() -> str:
    """Helper to get and cache the baseline data for all agents."""
    return scrape_wikivoyage_dubai()
