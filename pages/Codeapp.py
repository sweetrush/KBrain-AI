

from streamlit_extras.bottom_container import bottom
import streamlit as st
import google.generativeai as genai
# import os
import configparser
import streamlit.components.v1 as components
from PIL import Image
import PyPDF2
import io

config = configparser.ConfigParser()
config.read("config.mcf")
apivalue00 = config.get("APIKEYS", "api_mathGemini")


st.markdown(
    '''
    <style>
    /* Hide Streamlit's default components */
    /* Consider keeping header and footer and use custom styles if needed */
    .MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Styling for the header, if kept */
    header {
        background-color: rgba(0, 0, 0, 0.8); /* Semi-transparent background */
        color: #ffffff; /* White text for contrast */
        padding: 10px; /* Add some padding */
    }

    /* Body styling */
    body {
        font-family: "Ubuntu", sans-serif;
        background-color: #2c2c2e; /* Dark background for better contrast */
        color: rgb(249, 249, 251); /* Light text color */
        line-height: 1.6;
    }

    p, li {
        font-weight: 300;
    }

    /* Hide unnecessary Streamlit elements */
    .st-emotion-cache-10rjk4g,
    .st-emotion-cache-79elbk {
        display: none;
    }

    .st-emotion-cache-juxevh {
        padding-top: 0rem;
    }

    /* Additional styling for better visual appeal */
    h1, h2, h3 {
        color: #ffffff; /* Ensures headers are visible */
    }

    /* Button styles */
    .stButton, .stButton > button {
        background-color: #6200ea; /* Purple background for buttons */
        color: white; /* White text for buttons */
        border: none;
        border-radius: 5px; /* Rounded buttons */
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .stButton > button:hover {
        background-color: #3700b3; /* Darker purple on hover */
    }
    </style>
    ''', unsafe_allow_html=True)


# Assuming the necessary imports and prior initializations are done

def send_GeminiMessage_NoImage(user_message, model):
    genai.configure(api_key=apivalue00)
    modeltouse = model
    model = genai.GenerativeModel(modeltouse)

    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]
    )

    # Send a message from the user
    with st.chat_message("assistant"):
        response = chat.send_message([user_message])
        st.write(response.text)


def send_GeminiMessage_WImage(user_message, image, model):
    genai.configure(api_key=apivalue00)
    modeltouse = model
    model = genai.GenerativeModel(modeltouse)

    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]
    )

    # Send a message from the user
    with st.chat_message("assistant"):
        response = chat.send_message([user_message, image])
        st.write(response.text)


emj_tool_box = '🧰'
emj_upload_file = '📁'
emj_camera = '📷'
emj_image = '🖼️'
emj_tool = '🛠️'

emj_help = ' 📗 '
emj_help_ico = '📗'

pmpteng_string = "Provide output as MD format , also Layout the Output in details"


# Function to read PDF files
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# List of available models


models = [
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro-002",
    "gemini-1.5-pro-exp-0827",
    "gemini-1.5-flash-latest",
]

# Sidebar
with st.sidebar:
    st.page_link("Main.py", label="Back toMain", icon=emj_help_ico, disabled=False)
    st.title("Code App")
    st.subheader("Code Platform")
    modelselect = st.selectbox("Select a Model", models)


with bottom():
    with st.expander(emj_tool_box+"Context Engine:"):
        global image
        global run_button
        # Create tabs
        tab0, tab1, tab2, tab3 = st.tabs([
                                        emj_tool+"Main", 
                                        emj_upload_file+"Upload PDF", 
                                        emj_image+" Upload Image", 
                                        emj_camera+" Camera"
                                        ])

        with tab0:
            st.write("Welcome to the Code App!")
            st.write("This app is designed to help you with basic Coding Elements")

        with tab1:
            pdf_file = st.file_uploader("Choose a PDF file", type='pdf')
            
        if pdf_file:
            try:
                pdf_text = read_pdf(pdf_file)
                st.write("Extracted Text from PDF:")
                st.text_area("PDF Text", pdf_text, height=200)
            except Exception as e:
                st.error(f"An error occurred while reading the PDF: {e}")

        with tab2:
            image_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])
            if image_file:
                image = Image.open(image_file)
                st.image(image, caption='Uploaded Image', use_column_width=True)

        with tab3:
            t2A, t2B = st.tabs([emj_camera+" Camera Input", emj_image+" Camera Output"])
            with t2A:
                camera_photo = st.camera_input("Capture a photo")

            with t2B:
                if camera_photo:
                    image = Image.open(camera_photo)
                    st.image(image, caption='Captured Photo', use_column_width=True)

        # Columns For the Input and Run Button
        cl0, cl1 = st.columns([1, 6])
        user_input = cl1.text_area("💬 Enter your message here:")
        run_button = cl0.button("🚀 Run     ", key="run_button", type="primary")


if run_button and user_input:
    if pdf_file:
        st.write("Running context with PDF text...")
        # Process the PDF text and the input prompt here
        send_GeminiMessage_NoImage(pmpteng_string+user_input+pdf_text, modelselect)       
    if image_file:
        st.write("Running context with uploaded image...")
        # Process the uploaded image
        send_GeminiMessage_WImage(pmpteng_string+user_input, image, modelselect)
    if camera_photo:
        st.write("Running context with captured photo...")
        # Process the captured photo
        send_GeminiMessage_WImage(pmpteng_string+user_input, image, modelselect)
