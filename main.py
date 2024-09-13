import os
import streamlit as st
from groq import Groq
from scholarly import scholarly

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
    # AI-generated response to the research question
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Explain the topic '{question}' in detail, focusing on the field of '{field}'. Provide guidance and suggest relevant research papers.",
            }
        ],
        model="llama3-groq-70b-8192-tool-use-preview",
    )
    answer = chat_completion.choices[0].message.content
    
    # Guidance: detailed steps for conducting research
    guidance = (f"To deepen your understanding of '{question}' within the field of '{field}', start by exploring foundational concepts related to the topic. "
                f"Next, identify specific subtopics or questions that you want to investigate further. Review existing research papers, conduct experiments if applicable, "
                "and formulate your own insights or hypotheses. Ensure that you organize your findings in a structured manner, potentially in a research paper format.")
    
    return answer, guidance

# Show response when the user submits a question
if st.button("Submit"):
    with st.spinner("Your researcher is working..."):
        # Get the researcher's response to the question
        answer, guidance = get_researcher_response(research_question, selected_field)
        
        # Display AI-generated answer
        st.write("### Researcher's Answer:")
        st.write(answer)
        
        # Display guidance
        st.write("### Researcher's Guidance:")
        st.write(guidance)
        
        # Display relevant research papers from Google Scholar
        st.write("### Suggested Research Papers:")
        scholar_papers = get_research_papers_from_scholar(research_question, selected_field)
        for i, paper in enumerate(scholar_papers):
            with st.expander(f"Paper {i+1}: {paper['title']}"):
                st.write(f"**Abstract**: {paper['abstract']}")
                st.write(f"[Read Full Paper]({paper['url']})")