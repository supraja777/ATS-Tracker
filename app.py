import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{job_description}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

def get_gemini_response(input):
    
    # models = genai.list_models()

    # for model in models:
    #     print(model.name)

    # print("In get_gemini_response")

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page1 = reader.pages[page]
        text += str(page1.extract_text())
    return text

st.title("Smart ATS")
st.text("Improve your resume ATS score")

job_description = st.text_area("Paste job description")
uploaded_file = st.file_uploader("Upload your resume", type = "pdf", help = "Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = input_prompt.format(job_description = job_description, text = text)
        response = get_gemini_response(prompt)
        st.subheader(response)
