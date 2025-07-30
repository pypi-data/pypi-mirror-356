"""Web scraping functionality for Azure pricing pages."""

import logging
import re
from typing import Any, Dict, List, Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

AZURE_PRICING_BASE = "https://azure.microsoft.com/en-us/pricing/"
SERVICE_URLS = {
    'virtual-machines': 'details/virtual-machines/',
    'storage': 'details/storage/',
    'sql-database': 'details/sql-database/',
    'app-service': 'details/app-service/',
    'functions': 'details/functions/'
}

async def scrape_azure_pricing(service_name: str) -> Dict[str, Any]:
    """Scrape Azure pricing page for a service."""
    logger.info(f"Scraping pricing for {service_name}")
    
    service_key = service_name.lower().replace(' ', '-').replace('_', '-')
    if service_key not in SERVICE_URLS:
        return {
            'status': 'error',
            'message': f'Service not supported: {service_name}',
            'supported_services': list(SERVICE_URLS.keys())
        }
    
    url = AZURE_PRICING_BASE + SERVICE_URLS[service_key]
    
    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; Azure-Pricing-Bot/1.0)'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            pricing_info = {
                'service': service_name,
                'url': url,
                'pricing_summary': _extract_pricing_summary(soup),
                'free_tier': _extract_free_tier(soup),
                'special_offers': _extract_offers(soup)
            }
            
            return {'status': 'success', 'data': pricing_info}
            
    except Exception as e:
        logger.error(f"Error scraping {service_name}: {e}")
        return {'status': 'error', 'message': f'Failed to scrape: {str(e)}'}

def _extract_pricing_summary(soup: BeautifulSoup) -> List[str]:
    """Extract pricing summary."""
    summaries = []
    price_elements = soup.find_all(text=re.compile(r'\$\d+', re.I))
    for element in price_elements[:5]:
        parent_text = element.parent.get_text(strip=True) if element.parent else str(element)
        if len(parent_text) < 200:
            summaries.append(parent_text)
    return summaries

def _extract_free_tier(soup: BeautifulSoup) -> Optional[str]:
    """Extract free tier info."""
    free_elements = soup.find_all(text=re.compile(r'free', re.I))
    for element in free_elements:
        parent_text = element.parent.get_text(strip=True) if element.parent else str(element)
        if 'free' in parent_text.lower() and len(parent_text) > 20:
            return parent_text[:300]
    return None

def _extract_offers(soup: BeautifulSoup) -> List[str]:
    """Extract special offers."""
    offers = []
    offer_keywords = ['discount', 'promotion', 'offer', 'deal', 'save']
    
    for keyword in offer_keywords:
        elements = soup.find_all(text=re.compile(keyword, re.I))
        for element in elements[:2]:
            parent_text = element.parent.get_text(strip=True) if element.parent else str(element)
            if len(parent_text) > 20 and len(parent_text) < 200:
                offers.append(parent_text)
    
    return offers[:3]
