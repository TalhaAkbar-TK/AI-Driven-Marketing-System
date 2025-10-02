"""
Data models for the Lucidya Marketing System
"""

from typing import List, Dict
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Company:
    """Represents a target company"""
    id: str
    name: str
    domain: str
    industry: str
    size: str
    location: str
    description: str
    challenges: List[str]
    fit_score: int
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Contact:
    """Represents a decision-maker at a company"""
    id: str
    company_id: str
    name: str
    title: str
    email: str
    linkedin_url: str
    seniority: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class OutreachEmail:
    """Represents a personalized outreach email"""
    contact_id: str
    subject: str
    body: str
    generated_at: str
    personalization_factors: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)