"""
Configuration for the Lucidya Marketing App
"""

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser  
from pydantic import BaseModel, Field
from typing import List

OLLAMA_MODEL = 'llama3:latest'
OLLAMA_BASE_URL = 'http://localhost:11434'

llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.0)

MIN_FIT_SCORE = 85
OUTPUT_FILE = 'lucidya_marketing_system_output.json'

class CompanyIntelligence(BaseModel):
    key_insights: List[str] = Field(description="Key insights about the company")
    opportunity_areas: List[str] = Field(description="Opportunity areas for Lucidya")
    competitive_context: dict = Field(description="Competitive analysis dict")

class EmailOutput(BaseModel):
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body")