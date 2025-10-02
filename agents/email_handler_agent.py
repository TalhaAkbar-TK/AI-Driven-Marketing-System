"""
Email Handler Agent
"""

from typing import Optional, List, Dict
from datetime import datetime


def classify_response(email_content: str) -> str:
    """
    Classify incoming email response
    In production: Use NLP model or LLM for classification
    """
    content_lower = email_content.lower()
    
    if any(word in content_lower for word in ["interested", "yes", "call", "meeting", "discuss"]):
        return "POSITIVE_INTEREST"
    elif any(word in content_lower for word in ["pricing", "cost", "how much", "features", "demo"]):
        return "QUESTIONS"
    elif any(word in content_lower for word in ["not interested", "no thank", "remove", "unsubscribe"]):
        return "NEGATIVE"
    elif any(word in content_lower for word in ["out of office", "away", "vacation"]):
        return "OUT_OF_OFFICE"
    else:
        return "NEEDS_HUMAN_REVIEW"


def generate_auto_response(classification: str, original_email: str) -> Optional[str]:
    """
    Generate automated response based on classification
    Returns None if human escalation needed
    """
    
    if classification == "POSITIVE_INTEREST":
        return """Thank you for your interest! I'm excited to discuss how Lucidya can help your organization.

You can book a convenient time for our conversation using this link: [Calendar Link]

Or feel free to reply with your preferred dates/times and I'll send over an invite.

Looking forward to connecting!"""
    
    elif classification == "QUESTIONS":
        if "pricing" in original_email.lower():
            return """Thank you for your interest in Lucidya's pricing!

Our pricing is customized based on your specific needs, data volume, and use cases. I'd love to understand your requirements better and provide you with a tailored proposal.

Would you be available for a brief 15-minute call? You can book directly: [Calendar Link]

In the meantime, you can explore our platform capabilities at: www.lucidya.com/products"""
        else:
            return """Thank you for reaching out! I'd be happy to answer your questions in detail.

For the most productive conversation, would you be available for a quick call? You can book a time here: [Calendar Link]

Alternatively, feel free to reply with specific questions and I'll address them right away."""
    
    elif classification == "OUT_OF_OFFICE":
        return None
    
    else:
        return None


def escalate_to_human(contact_id: str, company_intelligence: Dict, 
                       conversation_history: List[Dict]) -> Dict:
    """
    Prepare complete context for human handoff
    """
    return {
        "contact_id": contact_id,
        "escalation_reason": "High-value prospect requires human attention",
        "company_profile": company_intelligence,
        "conversation_history": conversation_history,
        "suggested_talking_points": [
            "Discuss specific use cases relevant to their industry",
            "Address any concerns about Arabic language capabilities",
            "Offer personalized demo focusing on their pain points"
        ],
        "priority": "HIGH",
        "escalated_at": datetime.now().isoformat()
    }