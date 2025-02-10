import streamlit as st 
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2 as pdf

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY')) # Giving the api key of gemini pro

# Getting the response respect to gemini-pro model
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Reading the pages of the pdf file 
def pdf_to_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text+= str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst,
Machine Learning, Artificial Intelligent, Generative AIand big data engineer. Your task 
is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on Job_description and the missing keywords with high accuracy. So find the all keywords in the 
job_description to compare with the uploaded_file(resume) and give all missing  keywords in the given resume with respect to the job description(job_description).
Also give me the accurate JD Match percentage.
resume:{text}
description:{job_description}

I want the response in three different lines of string having the structure of
{{"JD Match":"%",\n
"MissingKeywords:[]",\n
"Profile Summary":"",\n
"Recomendation":""}}
"""

st.header("ATS Tracking System")
st.title("Made By Tawshok")

job_description=st.text_area("Enter the Job Description Here: ")
uploaded_file=st.file_uploader('upload you pdf here',type='pdf')
submit = st.button('Generate Result')

if submit:
    if uploaded_file is not None:
        text=pdf_to_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.write(response)