import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

os.getenv("GROK_API_KEY")


class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROK_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def match_resume(self, job_description, resume_content):
        prompt_match = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### RESUME CONTENT:
            {resume_content}

            ### INSTRUCTION:
            Compare the job description to the resume content. Extract and highlight key matching experiences and skills that align with the job description.
            Return the comparison in a concise bullet point format.
            ### MATCHED SUMMARY (NO PREAMBLE):
            """
        )
        chain_match = prompt_match | self.llm
        res = chain_match.invoke({"job_description": job_description, "resume_content": resume_content})
        return res.content

    def write_mail(self, job, links, matched_resume):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### MATCHED RESUME SUMMARY:
            {matched_resume}

            ### INSTRUCTION:
            You are an individual looking to apply for the job mentioned above. 
            Write a personalized cold email to the employer describing how your skills and experience align with their job posting, 
            referencing the matched resume summary where appropriate. 
            Add any links or portfolio items from the following list to strengthen your application: {link_list}.
            Remember to be professional and concise. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links, "matched_resume": matched_resume})
        return res.content


if __name__ == "__main__":
    print(os.getenv("GROK_API_KEY"))
