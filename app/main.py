import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from PyPDF2 import PdfReader  # Import for PDF text extraction
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # Step 3: Add URL input for the job posting
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")

    # Step 4: Upload PDF for the resume
    uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"])

    if uploaded_file is not None:
        resume_content = extract_text_from_pdf(uploaded_file)  # Extract the text from the PDF
        st.success("PDF file has been uploaded and processed!")
    else:
        st.warning("Please upload a PDF resume.")

    # Step 5: Submit button to trigger the process
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load and clean the job description from the provided URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Load portfolio
            portfolio.load_portfolio()

            # Extract jobs from the scraped content
            jobs = llm.extract_jobs(data)

            for job in jobs:
                # Step 6: Match resume content with job description
                matched_resume = llm.match_resume(job['description'], resume_content)

                # Query portfolio for relevant links based on job skills
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)

                # Generate the cold email based on the job and matched resume
                email = llm.write_mail(job, links, matched_resume)
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
