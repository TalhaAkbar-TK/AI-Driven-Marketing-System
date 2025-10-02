"""
Streamlit UI for Lucidya Marketing App
"""

import streamlit as st
from graph import build_graph
from utils import export_results, prepare_streamlit_data, to_serializable 
from config import MIN_FIT_SCORE
from agents.email_handler_agent import classify_response, generate_auto_response
from data.mock_data import MOCK_COMPANIES  


st.title("Lucidya AI-Driven Marketing System")
st.markdown("Prototype with LangChain, LangGraph, and Ollama for personalized outreach.")


st.sidebar.header("Configuration")
min_score = st.sidebar.slider("Min Fit Score", 0, 100, MIN_FIT_SCORE)
run_demo = st.sidebar.checkbox("Run Email Handling Demo")

if st.button("Run Workflow", type="primary"):
    with st.spinner("Executing AI workflow..."):
        graph = build_graph()
        initial_state = {"companies": MOCK_COMPANIES} 
        result_state = graph.invoke(initial_state)
        st.session_state.state = to_serializable(result_state) 
        st.session_state.data = prepare_streamlit_data(result_state)
        export_results(result_state)
    
    st.success("Workflow completed! Check outputs below.")

if "state" in st.session_state:
    data = st.session_state.data
    

    col1, col2, col3 = st.columns(3)
    col1.metric("Companies Discovered", data["summary"]["companies_discovered"])
    col2.metric("Companies Processed", data["summary"]["companies_processed"])
    col3.metric("Emails Generated", data["summary"]["emails_generated"])

    for i, processed in enumerate(data["processed_companies"]):
        company = processed["company"]
        intel = processed["intelligence"]
        
        with st.expander(f"{company['name']} (Fit: {company['fit_score']}/100)"):
            st.subheader(f"{company['name']}")
            st.write(f"**Industry:** {company['industry']} | **Size:** {company['size']} | **Location:** {company['location']}")
            st.write(f"**Description:** {company['description']}")
            
            st.subheader("Key Challenges")
            for challenge in company['challenges'][:3]:
                st.write(f"• {challenge}")
            
            st.subheader("Key Insights (LLM-Generated)")
            for insight in intel['key_insights']:
                st.write(f"• {insight}")
            
            st.subheader("Opportunity Areas")
            for opp in intel['opportunity_areas']:
                st.write(f"• {opp}")
            
            st.subheader("Generated Emails")
            for contact in processed["contacts"]:
                email_item = next((e for e in data["sent_emails"] if e["contact"]["id"] == contact["id"]), None)
                if email_item:
                    email = email_item["email"]
                    with st.expander(f"To: {contact['name']} - {email['subject']}"):
                        st.write("**Body:**")
                        st.markdown(email['body'])
                        st.write("**Personalization Factors:**")
                        for factor in email['personalization_factors']:
                            st.write(f"• {factor}")

    if run_demo:
        st.sidebar.header("Email Response Demo")
        mock_responses = [
            {
                "from": "fatima.alrashid@gulfecohub.com",
                "content": "Hi, this looks interesting. I'd like to schedule a call to learn more about your Arabic sentiment analysis capabilities."
            },
            {
                "from": "m.hassan@smartretail.sa",
                "content": "Thanks for reaching out. Can you share pricing information and what features are included in your platform?"
            },
            {
                "from": "sarah.thompson@healthconnect.ae",
                "content": "This could be valuable for us. How do you handle HIPAA compliance and patient data privacy?"
            }
        ]
        
        for resp in mock_responses:
            classification = classify_response(resp["content"])
            auto_resp = generate_auto_response(classification, resp["content"])
            
            col1, col2 = st.sidebar.columns(2)
            col1.write(f"**From:** {resp['from']}")
            col1.write(f"**Content:** {resp['content'][:50]}...")
            col2.write(f"**Classification:** {classification}")
            if auto_resp:
                col2.success("Auto-Response")
                col2.write(auto_resp[:100] + "...")
            else:
                col2.warning("Escalated to Human")

else:
    st.info("Click 'Run Workflow' to start.")

st.markdown("---")
st.caption("Powered by LangChain, LangGraph, Ollama, and Streamlit.")