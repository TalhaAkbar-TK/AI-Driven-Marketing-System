"""
Discovery Agent Node for LangGraph
"""

from typing import List, Dict
from models import Company
from data.mock_data import MOCK_COMPANIES
from config import MIN_FIT_SCORE


def discover_companies_node(state: Dict) -> Dict:
    """Node: Discover and filter companies"""
    print("🔍 Discovery Agent: Scanning for potential companies...")
    print(f"   Found {len(MOCK_COMPANIES)} companies matching ICP criteria\n")
    
    companies = MOCK_COMPANIES
    high_fit = [c for c in companies if c.fit_score >= MIN_FIT_SCORE]
    print(f"Filtered to {len(high_fit)} high-fit companies (score >= {MIN_FIT_SCORE})\n")
    
    return {
        "companies": companies,
        "high_fit_companies": high_fit,
        "processed_companies": [],
        "sent_emails": []
    }