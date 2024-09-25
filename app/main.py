# app.py or main.py
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from PyPDF2 import PdfReader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text, extract_text_from_pdf

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_streamlit_app(chain, portfolio, clean_text):
    st.title("📄 Tailored Resume & ATS Optimizer")

    # URL input for the job posting
    url_input = st.text_input("Enter a job posting URL:")

    # Upload PDF resume
    uploaded_file = st.file_uploader("Upload your resume (PDF):", type=["pdf"])

    # Submit button
    submit_button = st.button("Submit")

    if submit_button:
        if url_input and uploaded_file is not None:
            # Extract resume content
            resume_content = extract_text_from_pdf(uploaded_file)
            st.success("Resume uploaded and extracted successfully!")

            # Load and clean job description from the provided URL
            loader = WebBaseLoader([url_input])
            data = loader.load()
            if data:
                job_description_raw = data[0].page_content
                job_description = clean_text(job_description_raw)

                # Extract jobs from the scraped content
                jobs = chain.extract_jobs(job_description)

                if jobs:
                    # Assuming only one job for simplicity
                    job = jobs[0]
                    st.success("Job description loaded successfully!")

                    # Store variables in st.session_state
                    st.session_state.resume_content = resume_content
                    st.session_state.job_description = job['description']
                    st.session_state.job = job

                else:
                    st.error("No job postings found in the provided URL.")
                    return
            else:
                st.error("Failed to load job description from the URL.")
                return
        else:
            st.error("Please provide both a job posting URL and upload your resume.")
            return

    # Proceed if resume_content and job_description are available
    if 'resume_content' in st.session_state and 'job_description' in st.session_state:
        # Display job description
        st.subheader("Job Description")
        st.write(st.session_state.job_description)

        # Editable resume content
        st.subheader("Edit Your Resume Content:")
        resume_content = st.text_area("Resume Content", value=st.session_state.resume_content, height=300)

        # Real-Time ATS Score
        ats_score, job_keywords = chain.calculate_ats_score(resume_content, st.session_state.job_description)
        st.subheader(f"ATS Match Score: {ats_score}%")

        # Display keywords
        st.write("**Job Keywords:**", ', '.join(job_keywords))

        # Generate real-time suggestions
        suggestions = chain.get_real_time_suggestions(resume_content, st.session_state.job_description)

        st.subheader("Actionable Suggestions")
        if suggestions:
            for suggestion in suggestions:
                st.markdown(f"- **Original Text:** {suggestion['Original Text']}")
                st.markdown(f"  **Suggested Improvement:** {suggestion['Suggested Improvement']}")
                st.markdown(f"  **Reason:** {suggestion['Reason']}")
        else:
            st.write("No suggestions at this time.")

        # Option to generate the tailored resume
        if st.button("Generate Tailored Resume"):
            tailored_resume = chain.generate_tuned_resume(resume_content, st.session_state.job_description)
            st.subheader("Tailored Resume")
            st.text_area("Updated Resume Content", tailored_resume, height=300)

        # Option to generate the cold email
        if st.button("Generate Cold Email"):
            matched_resume = chain.match_resume(st.session_state.job_description, resume_content)
            skills = st.session_state.job.get('skills', [])
            links = portfolio.query_links(skills)
            email = chain.write_mail(st.session_state.job, links, matched_resume)
            st.subheader("Generated Cold Email")
            st.code(email, language='markdown')

    else:
        st.info("Please provide both a job posting URL and upload your resume, then click Submit.")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    portfolio.load_portfolio()
    st.set_page_config(layout="wide", page_title="Resume Optimizer", page_icon="📄")
    create_streamlit_app(chain, portfolio, clean_text)
