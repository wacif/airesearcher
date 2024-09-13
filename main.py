import os
import streamlit as st
from groq import Groq
from scholarly import scholarly
from prompts import get_research_prompt, get_guidance_prompt, invalid_question_prompt

# Set up Groq client
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit UI
st.title("AI Researcher Bot")
st.write("Ask a research question, and your researcher will provide guidance and relevant papers:")

# Field selection
fields = ["Artificial Intelligence", "Machine Learning", "Data Science", "Computer Vision", "Natural Language Processing"]
selected_field = st.selectbox("Select Research Field", fields)

# User input
research_question = st.text_input("Research Question", "")

# Check if the question is related to research
def is_research_related(question):
    # Define keywords for non-research-related topics
    non_research_keywords = ["recipe", "cooking", "politics", "sports", "food", "celebrity"]
    
    # Check if the question contains any non-research keywords
    for keyword in non_research_keywords:
        if keyword.lower() in question.lower():
            return False
    return True

# Function to get research paper links from Google Scholar
def get_research_papers_from_scholar(topic, field):
    search_query = scholarly.search_pubs(f"{topic} {field}")
    papers = []
    for i in range(5):  # Get top 5 results
        paper = next(search_query)
        title = paper['bib']['title']
        abstract = paper.get('bib', {}).get('abstract', "No abstract available")
        url = paper.get('pub_url', "No URL available")
        papers.append({
            "title": title,
            "abstract": abstract,
            "url": url
        })
    return papers

# Function to simulate a proper researcher response
def get_researcher_response(question, field):
    # Check if the question is research-related
    if not is_research_related(question):
        # Return a nice message instead of the prompt content
        return "As an AI research assistant, I'm here to assist with research-related questions. Please feel free to ask something on a research topic, and I'll be happy to help!", None
    
    # Use the imported prompt for generating the AI researcher's response
    chat_completion = client.chat.completions.create(
        messages=[get_research_prompt(question, field)],  # Use prompt from prompts.py
        model="llama3-groq-70b-8192-tool-use-preview",
    )
    answer = chat_completion.choices[0].message.content
    
    # Get the guidance prompt for the research process
    guidance = get_guidance_prompt(question, field)
    
    return answer, guidance

# Show response when the user submits a question
if st.button("Submit"):
    if research_question:
        with st.spinner("Your researcher is working..."):
            # Get the researcher's response to the question
            answer, guidance = get_researcher_response(research_question, selected_field)
            
            if guidance:  # Means it's a valid research question
                # Display AI-generated answer
                st.write("### Researcher's Answer:")
                st.write(answer)
                
                # Display guidance
                st.write("### Researcher's Guidance:")
                st.write(guidance)
            
            else:
                # Show a polite message if the question is not research-related
                st.warning(answer)
            
            # Display relevant research papers from Google Scholar if it's a valid research question
            if guidance:
                st.write("### Suggested Research Papers:")
                scholar_papers = get_research_papers_from_scholar(research_question, selected_field)
                for i, paper in enumerate(scholar_papers):
                    with st.expander(f"Paper {i+1}: {paper['title']}"):
                        st.write(f"**Abstract**: {paper['abstract']}")
                        st.write(f"[Read Full Paper]({paper['url']})")
    else:
        st.warning("Please enter a research question before submitting.")
