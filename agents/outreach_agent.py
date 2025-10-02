"""
Outreach Agent: LangChain chain for email generation
"""

from typing import Dict, List
from datetime import datetime
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from config import llm, EmailOutput
from models import Contact, OutreachEmail, Company
import json
import re


class OutreachChain:
    def __init__(self):
        pydantic_parser = PydanticOutputParser(pydantic_object=EmailOutput)
        json_parser = JsonOutputParser(pydantic_object=EmailOutput) 
        
        prompt = PromptTemplate(
            template="""
            Generate a personalized cold outreach email for Lucidya (AI customer intelligence for MENA).
            
            Recipient: {contact_name}, {title} at {company_name}
            Company: {company_name}, {industry}, {size}, {location}
            Description: {description}
            Key Insights: {insights}
            Challenges: {challenges}
            Opportunities: {opportunities}
            Use Case: {use_case_description} (Results: {metrics})
            
            IMPORTANT: Respond ONLY with valid JSON matching this exact schema. No extra text, explanations, or markdown. Do not output the schema itself—only the data. Ensure proper commas and quotes in JSON.
            Example JSON output:
            {{
                "subject": "Helping {company_name} Unlock Insights",
                "body": "Hi [Name],\\n\\n[Full body here with CTA]\\n\\nBest,\\nSales Team"
            }}
            
            Email Structure:
            - subject: Engaging, personalized (under 60 chars).
            - body: Professional, concise (200-300 words). Hi [First Name], impress with company, address challenge, highlight 2-3 opportunities, use case, CTA for 20-min call [Calendar Link], sign Sales Team, Lucidya. P.S. Arabic support. Unsubscribe footer.
            
            {format_instructions}
            """,
            input_variables=["contact_name", "title", "company_name", "industry", "size", "location", "description", "insights", "challenges", "opportunities", "use_case_description", "metrics"],
            partial_variables={"format_instructions": pydantic_parser.get_format_instructions()},
        )
        self.chain = prompt | llm
        self.pydantic_parser = pydantic_parser
        self.json_parser = json_parser
        self.use_cases = {
            "E-Commerce": {
                "title": "Cart Abandonment Recovery",
                "description": "A leading fashion retailer reduced cart abandonment by 23% by analyzing customer sentiment during checkout and proactively addressing concerns.",
                "metrics": "23% reduction in cart abandonment, $2.1M additional revenue"
            },
            "Retail Technology": {
                "title": "Omnichannel Experience Optimization",
                "description": "A major retail chain unified customer feedback from online and in-store channels, identifying and resolving pain points 3x faster.",
                "metrics": "3x faster issue resolution, 18-point NPS increase"
            },
            "Healthcare Technology": {
                "title": "Patient Satisfaction Monitoring",
                "description": "A telehealth platform automated patient feedback analysis across all touchpoints, improving response time to concerns by 65%.",
                "metrics": "65% faster response time, 94% patient satisfaction score"
            }
        }
    
    def generate_email(self, contact: Dict, intelligence: Dict) -> OutreachEmail:
        company_dict = intelligence['company']
        company = Company(**company_dict)
        opportunities = intelligence['opportunity_areas']
        insights = intelligence['key_insights']
        use_case = self.use_cases.get(company.industry, self.use_cases["E-Commerce"])
        
        print(f"Outreach Agent: Crafting personalized email for {contact['name']}...")
        try:
            raw_output = self.chain.invoke({
                "contact_name": contact['name'],
                "title": contact['title'],
                "company_name": company.name,
                "industry": company.industry,
                "size": company.size,
                "location": company.location,
                "description": company.description,
                "insights": ", ".join(insights),
                "challenges": ", ".join(company.challenges),
                "opportunities": ", ".join(opportunities),
                "use_case_description": use_case['description'],
                "metrics": use_case['metrics']
            })
            raw_text = str(raw_output).strip()
            
            if not raw_text or raw_text == 'null':
                raise ValueError("Empty output")

            raw_text = raw_text.replace('", "', '","') 
            raw_text = re.sub(r'(\w+):(\s*)(\{)', r'\1: \3', raw_text)  

            try:
                email_out = self.pydantic_parser.parse(raw_text)
            except Exception:
                match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    try:
                        parsed = json.loads(json_str)
                    except json.JSONDecodeError as je:
                        fixed_str = re.sub(r'([}\]])\s*([{\[])', r'\1, \2', json_str)
                        parsed = json.loads(fixed_str)
                    if "value" in parsed:
                        parsed = parsed["value"]
                    email_out = EmailOutput(**parsed)
                else:
                    email_out = self.json_parser.parse(raw_text)
            
            subject = email_out.subject
            body = email_out.body
            print("LLM-generated email successful")
        except Exception as e:
            print(f"LangChain error: {e}. Fallback to template.")
            subject = f"Helping {company.name} unlock customer intelligence"
            body = f"""Hi {contact['name'].split()[0]},

I hope this email finds you well. I came across {company.name} and was impressed by your work in the {company.industry.lower()} space, particularly your focus on serving the {company.location.split(',')[0]} market.

I noticed that {company.name} is likely facing challenges around {company.challenges[0].lower()}. This is a common pain point we see with companies at your scale, and it's exactly what Lucidya was built to solve.

Lucidya is an AI-powered customer intelligence platform specifically designed for the MENA region. We help companies like yours:
• {opportunities[0] if opportunities else 'Social Listening & Sentiment Analysis'}
• {opportunities[1] if len(opportunities) > 1 else 'Omnichannel Analytics'}

One of our clients in the {company.industry.lower()} space had similar challenges. {use_case['description']}

The results: {use_case['metrics']}.

Given {company.name}'s focus on innovation and your role as {contact['title']}, I thought this might be relevant. Would you be open to a brief 20-minute conversation to explore how Lucidya could help {company.name} achieve similar results?

I'm happy to work around your schedule. You can book a time directly here: [Calendar Link]

Best regards,
Sales Team
Lucidya
www.lucidya.com

P.S. - We offer native Arabic language support and dialect detection, which I understand is particularly important for your market.

---
If you'd prefer not to receive emails from us, you can unsubscribe here: [Unsubscribe Link]"""
        
        personalization_factors = [
            f"Industry: {company.industry}",
            f"Title: {contact['title']}",
            f"Company size: {company.size}",
            f"Key challenges: {len(company.challenges)} identified",
            f"Opportunities: {', '.join(opportunities[:2])}"
        ]
        
        return OutreachEmail(
            contact_id=contact['id'],
            subject=subject,
            body=body,
            generated_at=datetime.now().isoformat(),
            personalization_factors=personalization_factors
        )


def outreach_node(state: Dict) -> Dict:
    """Node: Generate emails for each processed company"""
    chain = OutreachChain()
    sent_emails = []
    for processed in state["processed_companies"]:
        for contact in processed["contacts"]:
            email = chain.generate_email(contact, processed["intelligence"])
            sent_emails.append({
                "contact": contact,
                "email": email.to_dict(), 
                "company_intelligence": processed["intelligence"]
            })
    return {"sent_emails": sent_emails}