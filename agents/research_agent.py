"""
Research Agent: LangChain chain for company intelligence
"""

from typing import Dict, List
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from config import llm, CompanyIntelligence
from models import Company
from data.mock_data import MOCK_CONTACTS
import json
import re


class ResearchChain:
    def __init__(self):
        pydantic_parser = PydanticOutputParser(pydantic_object=CompanyIntelligence)
        json_parser = JsonOutputParser(pydantic_object=CompanyIntelligence)  
        
        prompt = PromptTemplate(
            template="""
            Analyze this company for Lucidya (AI-powered customer intelligence platform for MENA region).
            
            Company: {company_name}
            Industry: {industry}
            Size: {size}
            Location: {location}
            Description: {description}
            Challenges: {challenges}
            
            CRITICAL: IGNORE THE SCHEMA BELOW. Output ONLY the JSON DATA that FILLS the schema. Do NOT output the schema description, properties, or required fields. No explanations, markdown, or extra text—just the raw JSON object with sample data based on the analysis.
            
            Example of REQUIRED OUTPUT FORMAT (data only, no schema):
            {{"key_insights": ["High e-commerce traffic implies need for sentiment monitoring", "Arabic dialects challenge require localized NLP"], "opportunity_areas": ["Social Listening & Sentiment Analysis", "Arabic NLP & Dialect Detection"], "competitive_context": {{"likely_using": ["Sprinklr", "Hootsuite"], "gaps": ["Limited MENA focus"], "lucidya_advantages": ["Regional Arabic support", "Unified analytics"]}}}}
            
            Now generate the data:
            1. key_insights: 3-5 business implications (list of strings).
            2. opportunity_areas: 3-5 Lucidya features (e.g., Social Listening) (list of strings).
            3. competitive_context: {{"likely_using": [list], "gaps": [list], "lucidya_advantages": [list]}}.
            
            {format_instructions}
            """,
            input_variables=["company_name", "industry", "size", "location", "description", "challenges"],
            partial_variables={"format_instructions": pydantic_parser.get_format_instructions()},
        )
        self.chain = prompt | llm
        self.pydantic_parser = pydantic_parser
        self.json_parser = json_parser
    
    def research_company(self, company: Company) -> Dict:
        """Generate intelligence for a company"""
        print(f"Research Agent: Analyzing {company.name}...")
        try:
            raw_output = self.chain.invoke({
                "company_name": company.name,
                "industry": company.industry,
                "size": company.size,
                "location": company.location,
                "description": company.description,
                "challenges": ", ".join(company.challenges)
            })
            raw_text = str(raw_output).strip()  
            if not raw_text or raw_text == 'null' or 'properties' in raw_text and 'required' in raw_text:
                raise ValueError("Schema echo or empty output—rejecting")
            
            try:
                intel = self.pydantic_parser.parse(raw_text)
            except Exception:
                match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    parsed = json.loads(json_str)
                    if "value" in parsed:
                        parsed = parsed["value"]
                    intel = CompanyIntelligence(**parsed)
                else:
                    intel = self.json_parser.parse(raw_text)
            
            print(f"   ✓ Identified {len(intel.opportunity_areas)} opportunity areas\n")
            return {
                "company": company.to_dict(),
                "key_insights": intel.key_insights,
                "pain_points": company.challenges,
                "opportunity_areas": intel.opportunity_areas,
                "competitive_context": intel.competitive_context
            }
        except Exception as e:
            print(f"LangChain error: {e}. Fallback to mock.")
            if "E-Commerce" in company.industry:
                mock_insights = ["High volume of customer interactions across multiple channels", "Need for real-time sentiment analysis during peak seasons"]
                mock_opps = ["Social Listening & Sentiment Analysis", "Arabic NLP & Dialect Detection"]
            elif "Retail" in company.industry:
                mock_insights = ["Omnichannel presence requires unified analytics", "Customer feedback directly impacts inventory decisions"]
                mock_opps = ["Omnichannel Analytics", "Real-Time Alerting & Monitoring"]
            elif "Healthcare" in company.industry:
                mock_insights = ["Patient satisfaction is critical for retention and compliance", "Sensitive to privacy and regulatory requirements"]
                mock_opps = ["Conversational Intelligence", "Real-Time Alerting & Monitoring"]
            else:
                mock_insights = ["Scale requires automated analytics solutions", "Local language support is essential"]
                mock_opps = ["Social Listening & Sentiment Analysis", "Omnichannel Analytics"]
            return {
                "company": company.to_dict(),
                "key_insights": mock_insights,
                "pain_points": company.challenges,
                "opportunity_areas": mock_opps,
                "competitive_context": {"likely_using": ["Sprinklr", "Hootsuite"], "gaps": ["Limited Arabic language support"], "lucidya_advantages": ["Purpose-built for MENA region", "Advanced Arabic NLP"]}
            }
    
    def find_contacts(self, company_id: str) -> List[Dict]:
        contacts = [c.to_dict() for c in MOCK_CONTACTS if c.company_id == company_id]
        print(f"👤 Found {len(contacts)} decision-maker(s) at company\n")
        return contacts


def research_node(state: Dict) -> Dict:
    """Node: Research each high-fit company"""
    research_chain = ResearchChain()
    processed = []
    for company in state["high_fit_companies"]:
        intelligence = research_chain.research_company(company)
        contacts = research_chain.find_contacts(company.id)
        processed.append({
            "company": company.to_dict(), 
            "intelligence": intelligence,
            "contacts": contacts
        })
    return {"processed_companies": processed}