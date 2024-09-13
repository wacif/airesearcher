import os
import streamlit as st
from groq import Groq
from scholarly import scholarly
from prompts import get_research_prompt, get_guidance_prompt, invalid_question_prompt

# Set up Groq client

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit UI Enhancements
st.set_page_config(page_title="AI Researcher Bot", layout="centered")

st.title("AI Researcher Bot 🤖")
st.write("Get guidance and papers on your research topic")

# Adding a tooltip to help users
st.markdown("""
    <small style='color:gray;'>Tip: Ask specific research questions like "What are the latest trends in AI?" or "How to improve model accuracy in NLP?"</small>
    """, unsafe_allow_html=True)

# Field selection
fields = ["Artificial Intelligence", "Machine Learning", "Data Science", "Computer Vision", "Natural Language Processing"]
selected_field = st.selectbox("Select Research Field", fields)

# User input
research_question = st.text_input("Research Question", "", help="Enter a clear research-related question")

# Function to get research papers from Google Scholar
def get_research_papers_from_scholar(topic, field):
    search_query = scholarly.search_pubs(f"{topic} {field}")
    papers = []
    for i in range(5):  # Get top 5 results
        try:
            paper = next(search_query)
            title = paper['bib']['title']
            abstract = paper.get('bib', {}).get('abstract', "No abstract available")
            url = paper.get('pub_url', "No URL available")
            papers.append({
                "title": title,
                "abstract": abstract,
                "url": url
            })
        except StopIteration:
            break
    return papers

# Function to simulate AI researcher's response
def get_researcher_response(question, field):
    # Use the imported prompt for generating the AI researcher's response
    chat_completion = client.chat.completions.create(
        messages=[get_research_prompt(question, field)],
        model="llama3-groq-70b-8192-tool-use-preview",
    )
    answer = chat_completion.choices[0].message.content

    # Model identifies if the question is research-related by response or flag
    if "non-research" in answer.lower():
        return invalid_question_prompt(), None  # Use the improved invalid question prompt

    # Get the guidance prompt for the research process
    guidance = get_guidance_prompt(question, field)
    
    return answer, guidance

# Show response when the user submits a question
if st.button("Submit"):
    if research_question:
        with st.spinner(f"Researching your question in {selected_field}..."):
            answer, guidance = get_researcher_response(research_question, selected_field)
            
            if guidance:
                # Use Tabs for better organization
                tab1, tab2 = st.tabs(["AI Response", "Suggested Papers"])
                
                with tab1:
                    st.write("### Researcher's Answer:")
                    st.write(answer)
                    st.write("### Researcher's Guidance:")
                    st.write(guidance)
                
                with tab2:
                    st.write("### Suggested Research Papers:")
                    scholar_papers = get_research_papers_from_scholar(research_question, selected_field)
                    if scholar_papers:
                        for i, paper in enumerate(scholar_papers):
                            with st.expander(f"Paper {i+1}: {paper['title']}"):
                                st.write(f"**Abstract**: {paper['abstract']}")
                                st.write(f"[Read Full Paper]({paper['url']})")
                    else:
                        st.info("No papers found, try a different query.")
            else:
                st.warning(answer)
    else:
        st.warning("Please enter a research question before submitting.")
