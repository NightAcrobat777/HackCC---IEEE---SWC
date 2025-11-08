import requests
from bs4 import BeautifulSoup
import json
from playwright.sync_api import sync_playwright
import time

def scrape_assist_org_with_javascript(url="https://www.assist.org"):
    """
    Scrape assist.org using Playwright to handle JavaScript rendering
    
    Args:
        url: The URL to scrape (default: assist.org homepage)
    
    Returns:
        Dictionary containing scraped data
    """
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            time.sleep(2)
            
            html = page.content()
            browser.close()
        
        return scrape_from_html(html)
    
    except Exception as e:
        return {'error': f'Failed to scrape {url}: {str(e)}'}

def scrape_assist_org_with_selenium(url="https://www.assist.org"):
    """
    Alias for scrape_assist_org_with_javascript
    """
    return scrape_assist_org_with_javascript(url)

def get_institutions_list(url="https://www.assist.org"):
    """
    Get the list of academic institutions from assist.org dropdowns
    
    Args:
        url: The URL to scrape (default: assist.org homepage)
    
    Returns:
        Dictionary containing institution lists for different categories
    """
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            time.sleep(2)
            
            institutions = {
                'from_institution': [],
                'transfer_institution': []
            }
            
            try:
                page.click('#None-governing-institution-select')
                time.sleep(1.5)
                options = page.query_selector_all('ul[role="listbox"] li, .ng-option, [role="option"]')
                for option in options:
                    text = option.inner_text().strip()
                    if text and len(text) > 0 and not text.startswith('link') and not 'Don\'t see' in text:
                        institutions['from_institution'].append(text)
            except Exception as e:
                pass
            
            try:
                page.keyboard.press('Escape')
                time.sleep(1)
                page.reload(wait_until='networkidle')
                time.sleep(2)
                page.click('#institution')
                time.sleep(2)
                options = page.query_selector_all('ul[role="listbox"] li, .ng-option, [role="option"]')
                for option in options:
                    text = option.inner_text().strip()
                    if text and len(text) > 0 and not text.startswith('link') and not 'Don\'t see' in text:
                        institutions['transfer_institution'].append(text)
            except Exception as e:
                pass
            
            browser.close()
        
        institutions['from_institution'] = list(dict.fromkeys(institutions['from_institution']))
        institutions['transfer_institution'] = list(dict.fromkeys(institutions['transfer_institution']))
        
        return institutions
    
    except Exception as e:
        return {'error': f'Failed to get institutions: {str(e)}'}

def scrape_assist_org(url="https://www.assist.org"):
    """
    Simple webscraper for assist.org (static content)
    
    Args:
        url: The URL to scrape (default: assist.org homepage)
    
    Returns:
        Dictionary containing scraped data
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {
            'url': url,
            'title': soup.title.string if soup.title else 'No title found',
            'headings': [],
            'links': [],
            'paragraphs': [],
            'form_labels': [],
            'form_fields': []
        }
        
        for h in soup.find_all(['h1', 'h2', 'h3'], limit=10):
            text = h.get_text(strip=True)
            if text:
                data['headings'].append(text)
        
        for link in soup.find_all('a', limit=20):
            href = link.get('href')
            text = link.get_text(strip=True)
            if href and text:
                data['links'].append({'text': text, 'url': href})
        
        for p in soup.find_all('p', limit=10):
            text = p.get_text(strip=True)
            if text:
                data['paragraphs'].append(text)
        
        for label in soup.find_all('label', limit=20):
            text = label.get_text(strip=True)
            if text:
                data['form_labels'].append(text)
        
        for field in soup.find_all(['input', 'select', 'textarea'], limit=20):
            field_type = field.get('type', field.name)
            field_id = field.get('id', 'no-id')
            field_name = field.get('name', 'no-name')
            data['form_fields'].append({
                'type': field_type,
                'id': field_id,
                'name': field_name
            })
        
        return data
    
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to fetch {url}: {str(e)}'}

def scrape_from_html(html_content):
    """
    Scrape data from raw HTML content
    
    Args:
        html_content: Raw HTML string to parse
    
    Returns:
        Dictionary containing scraped data
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    data = {
        'headings': [],
        'descriptions': [],
        'form_labels': [],
        'form_fields': [],
        'text_content': []
    }
    
    for h in soup.find_all(['h1', 'h2', 'h3']):
        text = h.get_text(strip=True)
        if text:
            data['headings'].append(text)
    
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if text:
            data['descriptions'].append(text)
    
    for label in soup.find_all('label'):
        text = label.get_text(strip=True)
        if text:
            data['form_labels'].append(text)
    
    for field in soup.find_all(['input', 'select', 'textarea']):
        field_type = field.get('type', field.name)
        field_id = field.get('id', 'no-id')
        field_name = field.get('name', 'no-name')
        aria_label = field.get('aria-label', '')
        data['form_fields'].append({
            'type': field_type,
            'id': field_id,
            'name': field_name,
            'aria-label': aria_label
        })
    
    all_text = soup.get_text(strip=True)
    if all_text:
        data['raw_text'] = all_text[:500]
    
    return data

if __name__ == "__main__":
    result = get_institutions_list()
    print(json.dumps(result, indent=2))
