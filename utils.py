"""
Utility functions
"""

import json
from typing import Dict, Any
from config import OUTPUT_FILE
from models import Company, Contact, OutreachEmail  

def to_serializable(obj: Any) -> Any:
    """Recursively convert dataclasses and non-serializable objects to dicts/lists."""
    if isinstance(obj, (Company, Contact, OutreachEmail)):
        return obj.to_dict()
    elif hasattr(obj, '__dict__'):
        return {k: to_serializable(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    else:
        return obj


def export_results(results: Dict):
    """Save results to JSON file (with serialization fix)"""
    serializable_results = to_serializable(results)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    print(f"Results exported to: {OUTPUT_FILE}")


def prepare_streamlit_data(state: Dict) -> Dict:
    """Prepare data for Streamlit display (ensure all dicts)"""
    processed = []
    for p in state.get("processed_companies", []):
        processed.append({
            "company": to_serializable(p["company"]),  
            "intelligence": to_serializable(p["intelligence"]),
            "contacts": [to_serializable(c) for c in p["contacts"]]
        })
    sent_emails = [{"contact": to_serializable(e["contact"]), 
                    "email": to_serializable(e["email"]), 
                    "company_intelligence": to_serializable(e["company_intelligence"])} 
                   for e in state.get("sent_emails", [])]
    return {
        "summary": {
            "companies_discovered": len(state.get("companies", [])),
            "companies_processed": len(processed),
            "emails_generated": len(sent_emails)
        },
        "processed_companies": processed,
        "sent_emails": sent_emails
    }