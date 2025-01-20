import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx
import phonenumbers
import validators
from datetime import datetime
import re
import datetime
import parsedatetime

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro Model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def process_uploaded_document(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        document_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        document_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        return None
    return document_text

#chatbot's response based on the document content
def get_answer_from_document(query, document_text):
    if query.lower() in document_text.lower():
        start_index = document_text.lower().find(query.lower())
        end_index = start_index + 500  
        return document_text[start_index:end_index] + "..."
    else:
        return "Sorry, I couldn't find any relevant information in the document."

# Validation functions
def validate_phone_number(phone):
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def validate_email(email):
    return validators.email(email)


def extract_date_from_string(date_string):
    cal = parsedatetime.Calendar()
    parsed_time, success = cal.parse(date_string)
    
    if success:
        date = datetime.datetime(*parsed_time[:6])
        return date.strftime("%Y-%m-%d")
    else:
        return None
    

def validate_time_string(time_string):
    try:
        time_object = datetime.strptime(time_string, "%I:%M %p") 
        return time_object.strftime("%H:%M")
    except ValueError:
        try:
            time_object = datetime.strptime(time_string, "%I %p")  # 12-hour format without minutes
            return time_object.strftime("%H:%M")
        except ValueError:
            try:
                # Handle 24-hour format like "14:00"
                time_object = datetime.strptime(time_string, "%H:%M")
                return time_object.strftime("%H:%M")
            except ValueError:
                return None

st.set_page_config(page_title="Document-Based Q&A Chatbot")
st.header("Chatbot with Document-Based QandA and Call Appointment")


uploaded_file = st.file_uploader("Upload a DOCX or PDF document", type=["docx", "pdf"])

# Initialize document_text to None
document_text = None


if uploaded_file is not None:
    document_text = process_uploaded_document(uploaded_file)
    if document_text:
        st.success("Document uploaded and processed successfully!")
    else:
        st.error("Error in processing the document.")


input_text = st.text_input("Ask a question:")

# Check if the user has asked a question
if input_text:
    if document_text and "document" not in input_text.lower():
        response = chat.send_message(f"Answer the following based on the document: {input_text}")
        st.subheader("Bot Response:")
        for chunk in response:
            st.write(chunk.text)
    
    # General query handling using Gemini if document is not uploaded
    else:
        response = chat.send_message(input_text)
        st.subheader("General Chatbot Response:")
        for chunk in response:
            st.write(chunk.text)


if "call me" in input_text.lower():
    # Call me functionality (form for collecting user info)
    with st.form("user_info_form", clear_on_submit=True):
        st.subheader("Please provide your information:")
        name = st.text_input("What is your name?")
        phone = st.text_input("What is your phone number?")
        email = st.text_input("What is your email address?")

        submitted = st.form_submit_button("Submit Information")

        if submitted:
            if not name or not phone or not email:
                st.warning("All fields are required.")
            elif not validate_phone_number(phone):
                st.error("Invalid phone number. Please enter a valid phone number.")
            elif not validate_email(email):
                st.error("Invalid email. Please enter a valid email address.")
            else:
                st.success("Your information has been submitted successfully!")
                st.write(f"Name: {name}")
                st.write(f"Phone: {phone}")
                st.write(f"Email: {email}")


# Collect appointment details if they ask to "Book Appointment"
if "book appointment" in input_text.lower():
    with st.form("appointment_form", clear_on_submit=True):
        st.subheader("Please provide appointment details:")
        date_input = st.text_input("What date would you like to schedule the appointment? (e.g., Next Monday)")
        time_input = st.text_input("What time would you like to book the appointment? (e.g., 10 am, 14:00)")

        submitted = st.form_submit_button("Book Appointment")

        if submitted:
            date = extract_date_from_string(date_input)
            time = extract_date_from_string(time_input) 

            if not date:
                st.error("Could not extract a valid date. Please enter a proper date format.")
            elif not time:
                st.error("Could not extract a valid time. Please enter a proper time format (e.g., '10 am', '14:00').")
            else:
                st.success(f"Your appointment has been booked for {date} at {time}.")
                st.write(f"Date: {date}")
                st.write(f"Time: {time}")

