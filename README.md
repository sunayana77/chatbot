# Document-Based Q&A Chatbot with Appointment Scheduling

This is a Streamlit-based chatbot that can answer user queries from uploaded PDF or DOCX documents and also allow users to schedule appointments or provide their contact information through conversational forms.

## Features
- **Document Upload**: Upload a PDF or DOCX document for the chatbot to reference.
- **Document-Based Q&A**: Ask questions related to the uploaded document, and the chatbot will provide answers based on the document's content.
- **General Chatbot**: The chatbot also provides general responses to user queries.
- **Call Me**: Users can provide their contact information (name, phone number, and email) when they request a "Call me".
- **Book Appointment**: Users can schedule an appointment by providing a date and time in natural language.

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/sunayana77/chatbot.git
   cd chatbot
2. Create an env and install the requirements:
 ```bash
   pip install -r requirements.txt
```
4. GOOGLE_API_KEY=your_api_key_here(replace it with your api key) which will be stored `.env` file securely
5. ```bash
   streamlit run chatbot.py
