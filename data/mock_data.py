"""
Mock data for the Lucidya Marketing System Prototype
"""

from models import Company, Contact

MOCK_COMPANIES = [
    Company(
        id="comp_001",
        name="Gulf E-Commerce Hub",
        domain="gulfecohub.com",
        industry="E-Commerce",
        size="500-1000 employees",
        location="Dubai, UAE",
        description="Leading online marketplace in the GCC region specializing in fashion and electronics with 2M+ monthly active users.",
        challenges=[
            "Managing customer feedback across 5 social media platforms",
            "High cart abandonment rate (68%)",
            "Difficulty understanding customer sentiment in Arabic dialects",
            "Limited visibility into customer journey across channels"
        ],
        fit_score=92
    ),
    Company(
        id="comp_002",
        name="SmartRetail Solutions",
        domain="smartretail.sa",
        industry="Retail Technology",
        size="200-500 employees",
        location="Riyadh, Saudi Arabia",
        description="SaaS platform providing omnichannel retail solutions to 150+ stores across Saudi Arabia.",
        challenges=[
            "Inconsistent customer experience across online and offline channels",
            "Unable to track customer sentiment from in-store interactions",
            "Need for real-time analytics to optimize inventory",
            "Growing volume of customer inquiries overwhelming support team"
        ],
        fit_score=88
    ),
    Company(
        id="comp_003",
        name="HealthConnect Telehealth",
        domain="healthconnect.ae",
        industry="Healthcare Technology",
        size="100-200 employees",
        location="Abu Dhabi, UAE",
        description="Telemedicine platform connecting patients with doctors across the Middle East, serving 50k+ patients monthly.",
        challenges=[
            "Patient satisfaction measurement is manual and time-consuming",
            "No unified view of patient feedback across app, calls, and chat",
            "Compliance requirements for handling sensitive feedback",
            "Need to identify service quality issues proactively"
        ],
        fit_score=85
    )
]

MOCK_CONTACTS = [
    Contact(
        id="cont_001",
        company_id="comp_001",
        name="Fatima Al-Rashid",
        title="Chief Marketing Officer",
        email="fatima.alrashid@gulfecohub.com",
        linkedin_url="linkedin.com/in/fatima-alrashid",
        seniority="C-Level"
    ),
    Contact(
        id="cont_002",
        company_id="comp_002",
        name="Mohammed Hassan",
        title="VP of Customer Experience",
        email="m.hassan@smartretail.sa",
        linkedin_url="linkedin.com/in/mohammed-hassan-cx",
        seniority="VP"
    ),
    Contact(
        id="cont_003",
        company_id="comp_003",
        name="Sarah Thompson",
        title="Head of Digital Strategy",
        email="sarah.thompson@healthconnect.ae",
        linkedin_url="linkedin.com/in/sarah-thompson-digital",
        seniority="Director"
    )
]