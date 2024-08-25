#
#  Main File for Miah's AI Assistance 
#
#  Purpose: This has all the code for the Application to Run. 
#  Developed by: SweetRushCoder(sRC) aka Suetena Faatuuala Loia 
#
#
# Definding Imported Libaries for the Program
# #################################################
from youtube_transcript_api import YouTubeTranscriptApi
from colorama import Fore, Style
# from streamlit_gsheets import GSheetsConnection 
from pypdf import PdfReader
from gtts import gTTS
# from nltk.tokenize import word_tokenize

# From Streamlit Extra Components
from streamlit_extras.bottom_container import bottom

import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

import google.generativeai as genai
import speech_recognition as sr
import streamlit as st
import pandas as pd
import configparser
import PIL.Image
import requests
import logging
import datetime
import os
import re
import hashlib
import time


# Uncomment to Use them
# from io import BytesIO
# import numpy as np
# import pyperclip
# import time
# import nltk
# Definding the Current working version
# of the Miah AI assistance
# #################################################

version = "2.9.4"
develper = "SRCoder"

###################################################

# AccessCode for Testing
# accesscode_miah = "sodiuldfoiousdfj2o34lkj0o2134jollk;345ljk345]"
accesscode_miah = "1"

# Definding Emoji's
# #################################################

emj_tophat = " 🎩 "
emj_billcap = " 🧢 "
emj_gradcap = " 🎓 "
emj_clamper = " 🗜 "
emj_aaudio = " 🔊 "
emj_assistance = " 👾 "
emj_filebox = " 🗃 "
emj_gear = " ⚙ "
emj_safety = " 🩺 "
emj_pencil = " ✏ "
emj_stats = " 📊 "
emj_down = " ⬇ "
emj_help = " 📗 "
emj_help_ico = "📗"
emj_door = " 🚪 "

devmode = 0
apptile = ""
debprint = 0

# This Defines how many Agents can be loaded from the 
# Agent list
numagentload = 100


if devmode == 1:
    st.set_page_config(
        page_title="Miah AI (Devmode)",
        page_icon=":tada:", 
        layout="wide"
        )
else:
    st.set_page_config(
        page_title="Miah AI ",
        page_icon=":tada:",
        layout="wide"
        )

# Defining Arrays:
listofAssistance = []

# Generated Data Output Directors
dataOPD = "output/gemini_out"
audioOD = "ai_audio"

# Defining the Configuration Settings
# ##################################################

config = configparser.ConfigParser()
config.read("config.mcf")
apivalue = config.get("APIKEYS", "api")
api11labs = config.get("APIKEYS", "api_11labs")
epcolor_val = config.get("THEMEING", "ep_color")
ekks = config.get("EKS", "eeks")

# Defind Date Tags for Filenaming
# ##################################################

now = datetime.datetime.now()
ynm = f"{now.year}.{now.month}.{now.day}"  # shortdata
hms = f"{now.hour}{now.minute}{now.second}"  # Hour-Min-Sec
datetag_string = f"{ynm}_{hms}"

# Definding other Configuration support
ai_dont_lie = "Tell me only factual Information and not to lie"


#######################################################
# SETTING THE SESSION VARABLES                       ##
#######################################################

if "accesscode" not in st.session_state:
    st.session_state.accesscode = ""

if "authstatus" not in st.session_state:
    st.session_state.authstatus = True


# #########################################################################################
# Start of Function Definitions
# #########################################################################################

# #####################################################
# #  01         REPLACE CHAR FUNCTION                ##
# #####################################################
def replace_chars(text, chars_to_replace, replacement):
    # Uncomment for debugging or monitoring process
    #
    # colorful_print("[FX-R] replace chars (F01)", "magenta")

    pattern = f"[{chars_to_replace}]"  # Create a character class pattern
    return re.sub(pattern, replacement, text)


# #####################################################
# #  02         EXTRACT PDF TO TEXT FUNCTION         ##
# #####################################################
@st.cache_data
def openpdf_exttext(pdffile):
    """Extracts text from a PDF file with improved error
    handling and potential optimization."""

    colorful_print("[FX-R] openpdf (F02)", "magenta")
    try:
        pdf_reader = PdfReader(pdffile)
        number_of_pages = len(pdf_reader.pages)
        extracted_text = ""
        for page_num in range(number_of_pages):
            extracted_text += pdf_reader.pages[page_num].extract_text(layout=True)
        return extracted_text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""

        # Or raise an exception depending
        # on your error handling strategy


# #####################################################
# #  03         READ FROM FILE FUNCTION              ##
# #####################################################
@st.cache_data
def read_from_file(filename):
    # Uncomment for debugginging or monitoring process
    #
    # colorful_print("[FX-R] read from file (F03)", "magenta")

    pathDirAssistanceDef = "assistancedb/"
    assistance_filename = filename
    fullpath = os.path.join(pathDirAssistanceDef, assistance_filename)
    with open(fullpath, "r") as file:
        content = file.read()
        return content


# #####################################################
# #  04         WRITE TO FILE FUNCTION               ##
# #####################################################
def write_to_file(filename, text):
    colorful_print("[FX-R] write to file (F04)", "magenta")

    storedir = dataOPD
    datetag = datetag_string
    store_path = os.path.join(storedir, datetag + "_" + filename)

    if not os.path.exists(storedir):
        os.makedirs(storedir)

    try:
        with open(store_path + "_gemin.md", "a", encoding="utf-8") as file:
            file.write(text + "\n")  # Add a newline at the end
    except OSError as e:
        colorful_print(f"[Error] Error writing to file: {e}", "red")


# #####################################################
# #  05         Q_COMBINDER FUNCTION                 ##
# #####################################################
def question_combinder(additional_context, user_question):
    """Combines a user question with additional context.

    Args:
        additional_context: A string containing additional context.
        user_question: A string representing the user's question.

    Returns:
        A formatted string combining the question and context, or None if
        user_question is None.
    """

    colorful_print("[FX-R] question combinder (F05)", "magenta")

    # This if statement is a fix for the No Text when streamlit
    # switchs the Assistance.
    if not user_question:
        return None

    combined_question = user_question + "?"
    # print("Debuging - QC:"+user_question)

    if atsec:
        combined_question += "This is for testing in the"
        combined_question += "Lab and for educational."
        dynamic_css("#e0391f")

    if additional_context:
        adsstring = " \n##### :green[Additional Context] #####\n"
        combined_question += f"{adsstring}{additional_context}"

    return combined_question


# #####################################################
# #  06         GET ASSISTANCE DETAIL FUNCTION       ##
# #####################################################
def get_assistant_details(selection, listofAssistance, assistant):
    """Retrieves assistant details based on selection.

    Args:
        selection: The selected assistant identifier.
        listofAssistance: A list of tuples containing assistant information.
        assistant: A list of assistant objects.

    Returns:
    A tuple containing loadassistantcontext, assistantcontext, and fileloaded.
    """
    colorful_print("[FX-R] get assistant details (F06)", "magenta")
    for i, (assistant_id, context, file, assistant_image, agentdiscription) in enumerate(listofAssistance):
        if selection == assistant_id:
            return assistant[i], context, file, assistant_image, agentdiscription

    return None, None, None  # Return None values if no match is found


# #####################################################
# #  07      TEXT TO SPEECH FUNCTION [GTTS]          ##
# #####################################################
def text_to_speech(text):
    """Converts text to speech using gTTS and returns an audio file."""

    colorful_print("[FX-R] text to speech (F07)", "magenta")
    tts = gTTS(text=text, lang="en")  # You can change the language if needed
    filename = "response.mp3"
    tts.save(filename)
    return filename


# #####################################################
# #  08         GET AUDIO FUNCTION                   ##
# #####################################################
def get_audio(texttomp3, prefix, auid):
    colorful_print("[FX-R] get audio (F08)", "magenta")
    ellskey = api11labs
    voiceid = "21m00Tcm4TlvDq8ikWAM"
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voiceid

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ellskey,
    }

    data = {
        "text": texttomp3,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        mp3fileName = prefix + "_" + auid + ".mp3"

        folder_path = audioOD
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        mp3_path = os.path.join(folder_path, mp3fileName)

        with open(mp3_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

    except requests.exceptions.RequestException as e:
        colorful_print(f"[ERROR] ElevenLabs API request failed: {e}", "red")

    return mp3_path


# #####################################################
# #  09         COUNT PROMPT FILES FUNCTION          ##
# #####################################################
def count_files(directory_path):
    """Counts the number of files in a directory.

    Args:
        directory_path (str): The path to the directory.

    Returns:
        int: The number of files in the directory.
    """
    colorful_print("[FX-R] count_files (F09)", "magenta")
    file_count = 0
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            file_count += 1
    return file_count


# Function loads the Agent list from agent list files

# #####################################################
# #  10         LOAD AGENTS FROM DB/FILE FUNCTION    ##
# #####################################################
def loadagents():
    colorful_print("[FX-R] loadagents (F10)", "magenta")

    pathDirAssistanceConfig = "agentlist/"
    assistance_filename = "agentlisting.als"

    fullpath = os.path.join(pathDirAssistanceConfig, assistance_filename)
    file_path = fullpath

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if "@@" not in line and line:  # Check for "@@" and empty lines
                    emjtag, name, label, file, aimage, adps = line.strip().split(",")

                    if emjtag == "1":
                        listofAssistance.append(
                            [
                                emj_billcap + str(name),
                                str(label),
                                replace_chars(str(file), " ", ""),
                                aimage,
                                adps,
                            ]
                        )

                    elif emjtag == "2":
                        listofAssistance.append(
                            [
                                emj_tophat + str(name),
                                str(label),
                                replace_chars(str(file), " ", ""),
                                aimage,
                                adps,
                            ]
                        )

                    elif emjtag == "3":
                        listofAssistance.append(
                            [
                                emj_gradcap + str(name),
                                str(label),
                                replace_chars(str(file), " ", ""),
                                aimage,
                                adps,
                            ]
                        )

                    elif emjtag == "4":
                        listofAssistance.append(
                            [
                                emj_assistance + str(name),
                                str(label),
                                replace_chars(str(file), " ", ""),
                                aimage,
                                adps,
                            ]
                        )

                    else:
                        listofAssistance.append(
                            [
                                emj_billcap + str(name),
                                str(label),
                                replace_chars(str(file), " ", ""),
                                aimage,
                                adps,
                            ]
                        )
    except FileNotFoundError:
        colorful_print(
            f"[ERROR] Agent list file not found: {file_path}",
            "red"
            )
            
        # Handle the error gracefully, e.g., create a default agent list
    except IOError as e:
        colorful_print(f"[ERROR] Error reading agent list: {e}", "red")


# #####################################################
# #  11         HORIZONTAL LINE FUNCTION             ##
# #####################################################
def horizontal_line():
    colorful_print("[FX-R] horizontal line (F011)", "yellow")
    st.markdown("---", unsafe_allow_html=True)


# #####################################################
# #  12         DISPLAY DEV INFO FUNCTION            ##
# #####################################################
@st.experimental_dialog("About the Developer")
def display_about_dev():
    colorful_print("[FX-R] display about dev (F12)", "yellow")
    st.title("About the Developer")
    st.write("Name: SweetRushCoder")
    st.write("Project: Miah's AI Assistance")
    st.write("DevYear: 2024")


# #####################################################
# #  13         LISTAIN TO MICROPHONE FUNCTION       ##
# #####################################################
def listain_to_Microphone():
    colorful_print("[FX-R] listain to Microphone (F13)", "magenta")
    lm = sr.Recognizer()
    st.toast("Mic-Listing", icon=None)
    with sr.Microphone() as source:
        mic_audio = lm.listen(source)
        spoken = ""

        try:
            spoken = lm.recognize_google(mic_audio)
            st.toast(spoken, icon=None)
            colorful_print(spoken, "white")
        except Exception as e:
            colorful_print("Audio Exception:" + str(e), "red")

        st.toast("Mic-Not Listaining", icon=None)
        return spoken


# #####################################################
# #  14         YOUTUBE VIDEO TRANSCRIPT FUNCTION    ##
# #####################################################
@st.cache_data
def get_video_transcript(video_id):
    colorful_print("[FX-R] get video transcript (F14)", "magenta")

    try:
        # Get the transcript for the video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ""
        # Concatenate the text from each transcript segment
        for segment in transcript:
            text += segment["text"] + " "

        return text.strip()

    except Exception as e:
        colorful_print(f"[Error] Youtube API Request Failed: {str(e)}", "red")

    return None


# #####################################################
# #  15         GET YOUTUBE VIDEO ID FUNCTION        ##
# #####################################################
def get_video_id(url):
    colorful_print("[FX-R] get video id (F15)", "magenta")
    # Extract the video id from the YouTube URL
    video_id = re.findall(
        r"(?:v=|v\/|embed\/|youtu\.be\/|\/v\/|\/e\/|watch\?v=|"
        r"youtube\.com\/user\/[^#]*#([^\/]*\/)*\w+\/|"
        r"youtube\.com\/v\/|youtube\.com\/embed\/|"
        r"youtube\.com\/watch\?v=)([^#\&\?]*[^#\&\?\n]*)",
        # This is a Continues Line
        url,
    )

    # Return the video id
    return video_id[0] if video_id else None


# #####################################################
# #  16         ABOUT THE DEVELOPER FUNCTION         ##
# #####################################################
def about_the_developer():
    colorful_print("[FX-R] about_the_developer (F16)", "yellow")

    st.write("##### Version:   :orange[" + version + "]")
    st.write("##### Developer:   :green[" + develper + "]")


# #####################################################
# #  17         DYNAMIC CSS LOADER FUNCTION          ##
# #####################################################
def dynamic_css(color):
    colorful_print("[FX-R] dynamic css (F17)", "yellow")
    ubuntu = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">
    """
    pathcss = os.path.join("appstyle", "app0_style.css")
    with open(pathcss) as styleconfig:
        # expanderable_bordercolor = "rgba(82, 153, 127, 0.35)"
        expanderable_bordercolor = color
        # Replacing the Codec Mapping with new Value
        newtextcss = styleconfig.read().replace(
            "ST_CSS_CODE001", expanderable_bordercolor
        )
        st.markdown(f"<style>{ubuntu}{newtextcss}</style>",
                    unsafe_allow_html=True)


# #####################################################
# #  18         CHECK LOGIN CONDITION                ##
# #####################################################
def get_AccessCondition():
    grant = None
    colorful_print("[FX-R] get AccessCondition (F18)", "magenta")

    # userdata = load_user_data("appuac/uacdb_list.uacl")
    userdata = "appuac/uacdb_list.uacl"

    access = st.text_input(
        "Provide your access Code:",
        value=st.session_state.accesscode,
        type="password",
        max_chars=None,
    )

    st.session_state.accesscode = access

    # if devmode == 1:    # Allows Devloper user to bypass the login screen
    #     grant = True
    #     st.session_state.authstatus = True
    #     if access != "":
    #         st.sidebar.success("Authenticated & Active", icon="📡")
    
    if access == "":
        st.error("Access Code is Empty", icon="🚨")
        st.session_state.authstatus = False

    elif authenticate_user2(access, userdata):
        grant = True
        st.session_state.authstatus = True

        if access != "":
            st.success(
                "Authenticated & Active",
                icon="📡"
            )
            # logout = st.button("Logout")

    elif access == accesscode_miah:
        grant = True
        st.session_state.authstatus = True
        if access != "":
            st.success(
                "Authenticated & Active",
                icon="📡"
                )

    else:
        grant = False
        st.session_state.authstatus = False
        if access != "":
            st.warning(
                "Authentication Error: Please check your again!",
                icon="⛑️"
            )

    return grant


# #####################################################
# #  19         SHOWING THIS ON SIDEBAR  FX          ##
# #####################################################
def mapFileUploadOnSideBar():
    colorful_print("[FX-R] mapFileUpload On SideBar (F19)", "magenta")

    with st.expander(emj_tophat + "File Upload", expanded=False):
        uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")
        if uploaded_file is not None:
            pdftext = openpdf_exttext(uploaded_file)
        else:
            pdftext = ""
            uploaded_csv = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_csv is not None:
            df = pd.read_csv(uploaded_csv)
            json_data = df.to_json(orient="records")
        else:
            json_data = ""
            uploaded_img = st.file_uploader(
                "Choose an image...", type=["jpg", "png", "jpeg"]
            )

        return pdftext, json_data, uploaded_img


# #####################################################
# #  20         CHECHING INPUT FUNCTION FOR REG FORM ##
# #####################################################
def checkinput(input, name): 
    colorful_print("[FX-R] check input (F20)", "magenta")
    if input != "":
        return True
    else:
        st.error(name+"Field has a problem, check if not empty")
    return False


# #####################################################
# #  21         STRING COMPARE FX                    ##
# #####################################################
def compare_is_same(string1, string2):
    colorful_print("[FX-R] compare is same string (F22)", "magenta")
    if string1 == "":
        string1 = "er1"

    if string2 == "":
        string2 = "er2"

    compare = string1 == string2
    # if compare: 
    #    st.write("Password is the Same")
    # else:
    #   st.write("Password not the Same please check")
    return compare


# #####################################################
# #  22         GENERATE KEYHASH FX                  ##
# #####################################################
def calculate_string_hash(input_string, algorithm='sha256'):
    
    """
    Calculates the hash of a string using the specified algorithm.
    Args:
        input_string (str): The string to hash.
        algorithm (str, optional): The hash algorithm to use. 
                                    Defaults to 'sha256'.
    Returns:
        str: The hexadecimal representation of the hash value.
    """

    colorful_print("[FX-R] Calculate string hash (F22)", "magenta")
    # Encode the string to bytes if necessary
    if isinstance(input_string, str):
        input_string = input_string.encode('utf-8')

    # Create a hash object based on the chosen algorithm
    hash_object = hashlib.new(algorithm)

    # Update the hash object with the input string
    hash_object.update(input_string)

    # Get the hexadecimal representation of the hash
    hash_value = hash_object.hexdigest()

    return hash_value


# #####################################################
# #  23         WRITE TO GOOGLE SHEET FOR REG        ##
# #####################################################
def write_registration_to_sheet():
    colorful_print("[FX-R] write registration to sheet (F23)", "magenta")

    with st.form(key="regForm01", clear_on_submit=False):
        fullname = st.text_input("Full Name", value="", max_chars=None)
        country = st.text_input("Country")
        email = st.text_input("Email")
        password1 = st.text_input("Password one", key="33", type="password")
        password2 = st.text_input("Password two (retype)", key="34", type="password")
        specialCode = st.text_input("SpecialCode", type="password")

        st.markdown("##### :red[Required *]")
            
        submit = st.form_submit_button(label="Apply Registration")

        keyhash = calculate_string_hash(email+fullname+specialCode)

        registaDataFrame = pd.DataFrame(
                [
                    {
                        "fullname": fullname, 
                        "country": country,
                        "email": email,
                        "password": password1,
                        "specialcode": specialCode,
                        "keyhash": keyhash,
                    }
                ]
                )

        if submit:
            chkName = checkinput(fullname, "Full Name Field")
            chkCountry = checkinput(country, "Country Field")
            chkEmail = checkinput(email, "Email")
            chkPwd1 = checkinput(password1, "Password one")
            chkPwd2 = checkinput(password2, "Password two (retype)")
            chkSCode = checkinput(specialCode, "password")
            chkpwdeq = compare_is_same(password1, password2)

            # THIS CODE NEEDS TO BE CHECHED FOR CONTINUIED USE.
            #
            if chkpwdeq:
                if chkName and chkCountry and chkEmail and chkPwd1 and chkPwd2 and chkSCode:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    conn.update(data=registaDataFrame)
                    # data = conn.read(spreadsheet=url, usecols=list(range(2)), ttl=5, worksheet=SheetID)
                    # st.dataframe(data)
                    st.success("Thank you for Registering")
            else:
                st.error("Please the passwords are not the Same")


# #####################################################
# #  24         COLOR PRINTER FOR TEXT               ##
# #####################################################
def colorful_print(text, color):

    textcombind = ""

    if color == "red":
        textcombind = " * "+Fore.RED+Style.BRIGHT+text+Style.RESET_ALL

    if color == "green":
        textcombind = " * "+Fore.GREEN+Style.BRIGHT+text+Style.RESET_ALL

    if color == "yellow":
        textcombind = " * "+Fore.YELLOW+Style.BRIGHT+text+Style.RESET_ALL

    if color == "white":
        textcombind = " * "+Fore.WHITE+Style.BRIGHT+text+Style.RESET_ALL

    if color == "blue":
        textcombind = " * "+Fore.BLUE+Style.BRIGHT+text+Style.RESET_ALL

    if color == "magenta":
        textcombind = " * "+Fore.MAGENTA+Style.BRIGHT+text+Style.RESET_ALL

    if color == "cyan":
        textcombind = " * "+Fore.MAGENTA+Style.BRIGHT+text+Style.RESET_ALL
    
    print(textcombind)


# #####################################################
# #  25         TOKENIZER COUNTER                    ##
# #####################################################
# Check this function for removal 
# 
def tokencounter(text):
    nltk.download('punkt')
    return len(word_tokenize(text))


# #####################################################
# #  26         STREAM TEXT FX                       ##
# #####################################################
def stream_text(text, delay=0.003):
    """Streams text with a specified delay between characters."""
    for char in text:
        yield char
        time.sleep(delay)    

# #####################################################
# #  27         LOAD USER DATA FX                  ##
# #####################################################
def load_user_data(file_path):
    """Loads user data from a file, ignoring lines starting with '@'."""
    colorful_print("[FX-R] User access List Loading (F27)", "magenta")

    user_datac = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitesp
            # if "@" not in line and line:
            if line.startswith('@') or not line.strip():
                uuudata = line.split(',')
                user_datac.append(uuudata)
                colorful_print(str(user_datac)+"\n", "red")
    return user_datac


# #####################################################
# #  28         AUTHENTICATION USER FX               ##
# #####################################################
def authenticate_user(access_code, user_data):
    
    """Checks if the provided access code matches any user in the data."""
    colorful_print("[FX-R] User access Checking (F28)", "magenta")
    colorful_print(str(user_data), "white")
    for user in user_data:
        colorful_print("user:", "green")
        colorful_print("Data:"+user)
        if user[2000] == access_code:   # note 2000 is the target users
            return True
            
    return False

# #####################################################
# #  29         AUTHENTICATE USER FX 2               ##
# #####################################################
def authenticate_user2(access_code, file_path):
    """
    Checks if the provided access code exists in the user data file.

    Args:
        access_code (str): The access code to validate.
        file_path (str): The path to the user data file.

    Returns:
        bool: True if the access code is found, False otherwise.
    """

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('@'):  # Ignore comment lines
                continue
            user_id, _, _, stored_access_code = line.strip().split(', ')
            # print(stored_access_code)
            if access_code == stored_access_code:
                colorful_print("[Auth-OK] "+access_code+" => "+stored_access_code, "green")
                return True
            # Uncomment to show the Faled Auths
            # else:
            #     colorful_print("[Auth-FL] "+access_code+" => "+stored_access_code, "red")

    return False  # Access code not found in the file

# #####################################################
# #  30         Email Notifcation FX 30              ##
# #####################################################
def email_notification(SubjectString, MessageString):
    sender_email = "miahaisupport@bytewatchers.com"
    sender_password = ekks

    # Recipient's Email
    receiver_email = "suetena.loia@gmail.com"

    # Email Content
    message = MIMEText(MessageString)
    message["Subject"] = SubjectString
    message["From"] = sender_email
    message["To"] = receiver_email

    # Sending the Email
    try:
        with smtplib.SMTP_SSL('mail.bytewatchers.com', 465) as server:
            server.login(sender_email, sender_password)
            colorful_print("[FX-R] Emaillogin-A (F29)", "magenta")
            server.sendmail(sender_email, receiver_email, message.as_string())
            colorful_print("[FX-R] EmailSending-B (F29)", "magenta")
    except Exception as e:
        print(f"Error sending email: {e}")

#########################################################################
#########################################################################
#########################################################################
#########################################################################
#
#
#                  END OF FUNCTION DEFINTIONS
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################

# Defining more Variables
# ##############################################################


fileInStore = count_files(dataOPD)
audioInStore = count_files(audioOD)

model_tokens = "8024"

models = [
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro-exp-0801",
    "gemini-1.5-flash-latest",
    "Model Slot Empty",
]

# OLD Definition
# safety_options = [
#                   "BLOCK_NONE",
#                   "BLOCK_FEW",
#                   "BLOCK_SOME",
#                   "BLOCK_MOST"
#                  ]

# NEW Option Selector
safety_options = [
    "BLOCK_NONE",
    "BLOCK_LOW_AND_ABOVE",
    "BLOCK_MEDIUM_AND_ABOVE",
    "BLOCK_ONLY_HIGH",
]

# Loading in the Agents from File 
loadagents()
assistant = []
for i in range(len(listofAssistance)):
    assistant.append(read_from_file(listofAssistance[i][2]))

##############################################################################
# ############################################################################
#  SIDE BAR CODE FOR THE PROGRAM
#    - This is the start of the Side bar and with all elements
# ############################################################################
##############################################################################


##############################################################################
##############################################################################
# #                                                                         ##
# #             START OF THE MAIN CONTENT BODY                              ##
# #                                                                         ##
##############################################################################
##############################################################################

if devmode == 1:
    st.sidebar.title(emj_clamper + "Miah's AI (DevMode)")
else:
    st.sidebar.title(emj_clamper + "Miah's AI")

dynamic_css(epcolor_val)

# Getting the Condition of the Access
with st.sidebar:
    with st.expander(emj_door+" Auth Panel "):
        get_AccessCondition()

# Initiating the Logout State:
logout = restdata = None

# Checking Authentication State
if st.session_state.authstatus and st.session_state.accesscode != "":
    with st.sidebar:

        global tempture_val, fileloaded, opt1_safe, opt2_safe
        global opt3_safe, opt4_safe, pdftext, getResponsetext
        global loadassistantcontext, assistantcontext, adcn
        global agentimagelement, agdiscription

        # horizontal_line() # Uncomment to show the Line
        btt1, btt2 = st.columns(2, gap="small") 

        logout = btt1.button(" 🕡 "+"Logout")
        restdata = btt2.button(" ♻ "+"Datarest")
        # Uncomment this to reflect the file Upload Feature on the Side Bar
        # mapFileUploadOnSideBar()
        
        with st.expander(emj_gear + "Prompt Config", expanded=False):
            
            l1_tl1, l1_tl2 = st.tabs([emj_gear + "Main", emj_safety + "Safety"])
            
            with l1_tl1:
                # st.write(emj_gear + "Settings Config")
                popup_notifications = st.toggle("Popup Notification", value=False)
                GeminiAPIkey = st.text_input(
                    "Gemini-key:", type="password", value="", max_chars=None
                )
                tempture_val = st.slider(
                    "Prompt temperature",  # Label for the slider
                    min_value=0.0,  # Minimum value
                    max_value=1.0,  # Maximum value
                    value=0.07,  # Default value
                    step=0.01,  # Increment step
                )

                # topp = st.text_input("Set Top P", value="1", max_chars=None)
                topp = st.slider(
                    "Set Top-P",    # Label for the slider
                    min_value=0.0,  # Minimum value
                    max_value=1.0,  # Maximum value
                    value=0.07,     # Default value
                    step=0.05,      # Increment step
                )

                topk = st.number_input(
                    "Set Top-K",
                    min_value=None,
                    max_value=None,
                    value=10,
                    step=1
                )

                if not isinstance(topk, int) or topk < 1 or topk > 100:
                    st.error("Invalid Top-K value. Please enter an integer between 1 and 100.")

                mot = st.text_input("Max Output Tokens", value=model_tokens, max_chars=None)

                convert_tpv = float(tempture_val)

        # with st.expander(emj_safety + "Safety Config", expanded=False):
            with l1_tl2:
                # st.write(emj_safety + "Safety Config")
                opt1_safe = st.selectbox(
                    "Harassment",
                    (
                        safety_options[0],
                        safety_options[1],
                        safety_options[2],
                        safety_options[3],
                    ),
                    index=0,
                )

                opt2_safe = st.selectbox(
                    "Hate",
                    (
                        safety_options[0],
                        safety_options[1],
                        safety_options[2],
                        safety_options[3],
                    ),
                    index=0,
                )

                opt3_safe = st.selectbox(
                    "Sexually Explicit",
                    (
                        safety_options[0],
                        safety_options[1],
                        safety_options[2],
                        safety_options[3],
                    ),
                    index=0,
                )

                opt4_safe = st.selectbox(
                    "Dangerous Content",
                    (
                        safety_options[0],
                        safety_options[1],
                        safety_options[2],
                        safety_options[3],
                    ),
                    index=0,
                )

        #
        # Setting the Module Selection for the Assistance
        # ###############################################
        with st.expander(emj_assistance + "Model & Assistance", expanded=True):
            model_select = st.selectbox(
                emj_clamper + "Choose Model", (
                    models[0],
                    models[1],
                    models[2],
                    models[3]
                    ), index=0

            )

            # Setting the selected Active Assistance
            # ################################################

            selection = st.selectbox(
                emj_assistance + "Active Assistance:",
                [
                    item[0]
                    for item in listofAssistance[: min(
                        numagentload, 
                        len(listofAssistance))]
                ],
                index=0,
            )

        # Checking and setting the Selected Assistance
        # ##############################################

        loadassistantcontext, assistantcontext, fileloaded, agentimagelement, agdiscription = get_assistant_details(
            selection, listofAssistance, assistant
        )

        #
        # END OF the selected Assistance
        # ############################################################

        if popup_notifications:
            st.toast("**:blue[Using AI:]**\n :red[" + assistantcontext + "]")
            st.toast(":green[File:]" + fileloaded)
            st.toast(":green[Model:]" + model_select)
            st.toast(":green[Image:]" + agentimagelement)
            st.toast(":green[Discription:]" + agdiscription)

        with st.expander(emj_safety + "Special Features", expanded=False):

            spclm1, spclm2 = st.tabs([emj_safety + "UI", emj_aaudio + "Audio"])
            with spclm1:
                st.write(emj_safety + "UI Config")
                attsm = st.toggle("TSM", value=False, help="Activate Text Stream Reponses")
                atpts = st.toggle("PTS", value=False, help="Activate Prompt Token Status")
                if attsm:
                    writespeed = st.text_input("Text-Speed:", value="0.007", max_chars=None)
                atsec = st.toggle("ALT", value=False, help="Activate Lab Testing")
                bexpanderColor = st.color_picker("Theme:", epcolor_val)

                # save new color to Config
                config["THEMEING"]["ep_color"] = bexpanderColor
                with open("config.ini", "w") as configfile:
                    config.write(configfile)

                # set the session color
                st.session_state.exbclor = bexpanderColor
                dynamic_css(bexpanderColor)

        # with st.expander(emj_aaudio + "Audio Config", expanded=False):
            with spclm2:
                st.write(emj_aaudio + "Audio Config")
                e11labkey = st.text_input(
                    "e11labkey:",
                    value="",
                    max_chars=None,
                    type="password",
                    help="You to place your e11lab key to use Audio (1)",
                )

                if e11labkey:
                    activate_audio_output = st.toggle(
                        emj_aaudio + "Audio(1):", value=False, help="Active Audio E11L"
                    )
                # Access Code for "SCH"
                elif e11labkey == "sch2024-code":
                    activate_audio_output = st.toggle(
                        emj_aaudio + "Audio(1):", value=False, help="Active Audio E11L"
                    )
                elif devmode == 1:   # IF ONE this will show the audio in dev Enviroment
                    activate_audio_output = st.toggle(
                        emj_aaudio + "Audio(1):", value=False, help="Active Audio E11L"
                    )
                else:
                    activate_audio_output = False

                activate_audio_output002 = st.toggle(
                    emj_aaudio + "Audio(2):", value=False, help="Active Audio GTTs"
                )

        with st.expander(emj_stats + "Status", expanded=False):
            st.write("##### Number of SAR: " + str(fileInStore))
            st.write("##### Number of SAF: " + str(audioInStore))
            st.write("##### Number of AN: " + str(len(listofAssistance)))


        # #####################################################################
        # #####################################################################
        #             PAGE MENU ON THE SIDE BAR FOR OTHER FEATURES
        # 
        # #####################################################################
        horizontal_line()
        st.page_link(
            "pages/help.py", label="Help Guide", icon=emj_help_ico, disabled=False
        )
        st.page_link(
            "pages/aboutdev.py", label="About Dev", icon=emj_help_ico, disabled=False
        )
        # st.page_link(
        #     "pages/agentdev.py", label="Edit Agents", icon=emj_help_ico, disabled=False
        # )
        horizontal_line()
        about_the_developer()

    if "exbclor" not in st.session_state:
        st.session_state.exbclor = ""

    # #########################################################################
    # ##  END OF: Sidebar  ####################################################
    #
    # #########################################################################
    # #########################################################################

    # ####################################################################
    # ####################################################################
    #   Content Just Above the Chatline input field
    # ####################################################################
    # ####################################################################

    codewrap = ""  # initating the var for the code wrap here{adc
    with bottom():
        with st.expander(emj_pencil + "Extention Context", expanded=False):

            tb1, tb2, tb3, tb4, tb5 = st.tabs(["ATC", "ACC", "AYC", "FU", "AB"])

            with tb1:
                adcn = st.text_area(
                    label="Additional Context", height=100, key="KK09923"
                )

            with tb2:
                code = st.selectbox(
                    "Select Code Type",
                    (
                        "no-code",
                        "bash",
                        "c++",
                        "powershell",
                        "python",
                        "go",
                        "c",
                        "r",
                        "sh",
                        "batch",
                        "php",
                        "perl",
                        "javascript",
                    ),
                    index=0,
                )

                codearea = st.text_area(
                    "Code Area Context",
                    value="",
                    help="Activates the Code Context",
                    height=None,
                    max_chars=None,
                )

                if code == "no-code":
                    codewrap = codearea
                else:
                    codewrap = "```" + code + "\n " + codearea + " \n```"

            with tb3:
                yytab1, yytab2 = st.tabs(["URL", "WV"])

                with yytab1:
                    youtubeURL = st.text_input(
                        "Youtube Video URL", value="", max_chars=None
                    )

                    ac_youtubesc = st.toggle(
                        "AYS", value=False, help="Activate Transcript"
                    )
                    youtubesac = st.toggle(
                        "LV", value=False, help="LoadVideo Transcript"
                    )

                with yytab2:
                    if youtubesac:
                        st.video(youtubeURL)  # #

            with tb4:
                ytb1, ytb2, ytb3 = st.tabs(["PDF", "CSV", "IMG"])

                with ytb1:
                    uploaded_file = st.file_uploader(
                        "Choose your .pdf file", type="pdf"
                    )
                    if uploaded_file is not None:
                        try:
                            pdftext = openpdf_exttext(uploaded_file)
                        except Exception as e:
                            st.error(f"Error processing PDF: {e}")
                            pdftext = ""  # Ensure pdftext is initialized
                    else:
                        pdftext = ""

                with ytb2:
                    uploaded_csv = st.file_uploader("Choose a CSV file", type="csv")
                    if uploaded_csv is not None:
                        df = pd.read_csv(uploaded_csv)
                        json_data = df.to_json(orient="records")
                    else:
                        json_data = ""

                with ytb3:
                    uploaded_img = st.file_uploader(
                        "Choose an image...", type=["jpg", "png", "jpeg"]
                    )
            # Other related Buttons
            #
            with tb5:
                (
                    col1,
                    col2,
                ) = st.columns(2, gap="small")
                # copyresponsetoClip = col1.button("cc", help="Copy Clipboard")
                get_mictext = col1.button("GM", help="Listain to Microphone")

                # dialogpop = col2.button(
                #                    "AD",
                #                    on_click=display_about_dev(),
                #                    help="pops a dialog box")

    # ####################################################################
    # ####################################################################
    # ###################### END OF ABOVE CHAT AREA   ####################
    # ####################################################################
    # ####################################################################


    # ####################################################################
    # ####################################################################
    # ########### IMPLEMENTING SETTINGS FOR THE MODEL  ###################
    # ####################################################################
    # ####################################################################

    if GeminiAPIkey:
        # API from the UI interface 
        genai.configure(api_key=GeminiAPIkey)
    else:
        # API from file when holded 
        genai.configure(api_key=apivalue)

    # Set up the model
    generation_config = {
        "temperature": convert_tpv,
        "top_p": float(topp),
        "top_k": int(topk),
        "max_output_tokens": int(mot),
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": opt1_safe},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": opt2_safe},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": opt3_safe},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": opt4_safe},
    ]

    chatdata = []
    model_name = model_select

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    # ##################################################################
    # ##################################################################
    # #####  For Session Storing Information [ Caching ]     ###########
    # ##################################################################
    # ##################################################################

    if "chathistory" not in st.session_state:
        st.session_state.chathistory = []

    if "chathistoryprompt" not in st.session_state:
        st.session_state.chathistoryprompt = ""

    if "lastchatoutput" not in st.session_state:
        st.session_state.lastchatoutput = ""

    # Looping through the session stored Information
    for message in st.session_state.chathistory:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # END OF: Session Storing Information ###############################
    # ###################################################################

    # ###################################################################
    # ###################################################################
    # ###################################################################
    # Getting the User Prompt Information
    # ###################################################################

    # For the Youtube Context Prompt
    # Gets the Transcript for a Youtube Video
    #####################################################################

    ranscriptdata = ""
    videoTranscript = ""
    if ac_youtubesc:
        video_idd = str(get_video_id(youtubeURL)[1])
        videoTranscript = get_video_transcript(video_idd)
        transcriptdata = f'[Video Transcript]: "{videoTranscript}'
        # print("Video Id: "+video_idd)
        # print(transcriptdata)

    inputquestion = st.chat_input("Provide your Question / Prompt / Reqest")
    usermessage = question_combinder(f"{adcn}{codewrap}", inputquestion)

    if get_mictext:
        listain_to_Microphone()

    # if dialogpop:
    #     display_about_dev()
    
    # Runs What the User has input
    if usermessage:
        with st.chat_message("User"):
            st.write(usermessage)

            if uploaded_img:
                st.image(uploaded_img, caption=None, width=None)

            # Storing User Information to the Session Variable
            st.session_state.chathistory.append(
                {"role": "User", "content": usermessage}
            )

        chars_tobe_replaced = " ,."
        chars_swap = ""  # Noted that this will make the space as the char swap

        filename = replace_chars(str(inputquestion), chars_tobe_replaced, chars_swap)

        filename = filename[:20]
        colorful_print("[info] FileName is: " + filename + "", "white")

        convo = model.start_chat(history=chatdata)

        with st.status("Processing Request ...."):
            dynamic_css("#D0A112")
            # Combinding the Context Information
            # ############################################################################

            # Checking for PDF Context if Any
            if pdftext == "":
                grpcontext = ""
            else:
                grpcontext = pdftext

            # Cheching for Json Data Context
            if json_data == "":
                grpcontext += ""
            else:
                grpcontext += json_data

            # Checking for video Context as Text
            if videoTranscript == "":
                grpcontext += ""
            else:
                grpcontext += transcriptdata

            # End of Context Commincation Checks and Binding
            # #############################################################################
            # #############################################################################
            # print("[Debuging]:[0] "+groupcontext+usermessage)  #Debugging Perpose

            cache_history_now = st.session_state.chathistoryprompt
            cxt_n_usermsg = loadassistantcontext + usermessage + ai_dont_lie

            # Debugging calls 
            # Comment to use for Debugging
            # 
            # colorful_print(loadassistantcontext, "red")

            # This Combinds all prompt strings ready for loading to the chat.
            finalpromptstring = cxt_n_usermsg + grpcontext + ", " + cache_history_now 

            # ######## AREA FOR SEND PROMPT INFOR TO AI
            #

            try:
                if uploaded_img:
                    img = PIL.Image.open(uploaded_img)
                    colorful_print("[INCAL] Sending Prompt with Text and Image", "green")
                    convo.send_message([finalpromptstring, img])
                else:
                    convo.send_message(finalpromptstring)
                    colorful_print("[INCAL] Sending Prompt with Text only", "green")

                # Uncomment for Debugging for purpose.
                #
                # print("[Debuging]:[1] "+groupcontext+usermessage)

            except Exception as e:
                st.toast(":red[Error:] Problem sending Prompt on call", icon=None)
                st.error(e, icon=None)

            ca = usermessage + cache_history_now
            st.session_state.chathistoryprompt = ca
            # print(f"\n\n Current CACHE BP:{cache_history_now}") # Debuging Perpose
            # Uncomment to View ChathistroyPrompt data in terminal
            # print(st.session_state.chathistoryprompt)

            # systempromptadd = "Your name is Miah, You are named after my son"
            res04data = {
                            "role": "user", 
                            "parts": "What is 2"
            }

            res05data = {
                         "role": "model", 
                         "parts": "1"
            }

            res06data = {
                         "role": "user", 
                         "parts": "What is 3"
            }
            res07data = {
                         "role": "model", 
                         "parts": "5"
            }

            res08data = {
                         "role": "user", 
                         "parts": "What is 2"
            }

            res09data = {
                         "role": "model", 
                         "parts": "1"
            }

            res10data = {
                         "role": "user", 
                         "parts": "What is 3"
            }
            res11data = {
                         "role": "model", 
                         "parts": "5"
            }


            res12data = {
                         "role": "user", 
                         "parts": "What is 2"
            }

            res13data = {
                         "role": "model", 
                         "parts": "1"
            }

            res14data = {
                         "role": "user", 
                         "parts": "What is 3"
            }
            res15data = {
                         "role": "model", 
                         "parts": "5"
            }

            res16data = {
                         "role": "user", 
                         "parts": "What is 2"
            }

            res17data = {
                         "role": "model", 
                         "parts": "1"
            }

            res18data = {
                         "role": "user", 
                         "parts": "What is 3"
            }
            res19data = {
                         "role": "model", 
                         "parts": "5"
            }




            res00data = {
                         "role": "user", 
                         "parts": [ca]
            }

            res01data = {
                         "role": "model", 
                         "parts": [convo.last.text]
            }

            # res03data = {"role": "model", "parts": [systempromptadd]}
            res02data = {
                "role": "user",
                "parts": [loadassistantcontext],
            }

            chatdata.append(res02data)
            chatdata.append(res01data)
            chatdata.append(res00data)

            chatdata.append(res19data)
            chatdata.append(res18data)
            chatdata.append(res17data)
            chatdata.append(res16data)
            chatdata.append(res15data)
            chatdata.append(res14data)
            chatdata.append(res13data)
            chatdata.append(res12data)
            chatdata.append(res11data)
            chatdata.append(res10data)
            chatdata.append(res09data)
            chatdata.append(res08data)
            chatdata.append(res07data)
            chatdata.append(res06data)
            chatdata.append(res05data)
            chatdata.append(res04data)

            st.write(chatdata)
            # print(f'\n\n Chatdata: {chatdata}\n\n') # Uncomment for Deginfo
        
        if atsec:
            dynamic_css("#e0391f")    # Activate the Red Broaders000000000000..
        else:
            dynamic_css(st.session_state.exbclor)
        
        successtext = "Generated Response Completed"

        # Comment to Use the Toast as the Alert element
        st.success(successtext)

        # Uncomment to use the toast as the Alert element
        # st.toast(":green["+successtext+"]", icon=None)

        write_to_file(filename, convo.last.text)
        st.session_state.lastchatoutput = convo.last.text

        # This Gets the Number of Tokens needed.
        tokencount = model.count_tokens(convo.last.text)
        tokencountsent = model.count_tokens(finalpromptstring)
        tokensndrecd = model.count_tokens(convo.last.text+finalpromptstring)

        email_notification(
            "Miah AI Notification: "+st.session_state.accesscode+"  activity",
            "Activity Information \n\n Prompt Sent:"+ca+""
            "\n\n\n"+convo.last.text+"\n\n"
            )

        with st.chat_message("assistant"):
            botmessage = convo.last.text

            #
            # @@ Note to implement streaming of Returned information.
            #

            #  checks if the special feature for text Stream is active
            #  if yes then it will output the responses in a text Stream way 
            #  else it will just show all the text at Once. 
            if attsm:
                # st.status("Assistance Typing ..")
                st.write_stream(stream_text(botmessage, float(writespeed)))
            else:
                st.write(botmessage)

            if activate_audio_output:
                acol1, acol2 = st.columns(2, gap="small")
                with st.status("Processing Audio request"):
                    audiofilename = datetag_string + "_" + filename
                    audiopath = get_audio(botmessage, "el11_au", audiofilename)
                    audiofile = open(audiopath, "rb")
                    audiobytes = audiofile.read()

                acol1.audio(audiobytes, format="audio/mp3")
                acol2.download_button(
                    emj_down + "Download Audio",
                    audiobytes,
                    file_name=datetag_string + ".mp3",
                    mime=None,
                )

                if popup_notifications:
                    st.toast(":blue[Audio 01] :green[activated]")
                st.write("Audio Generation Completed")

            if activate_audio_output002:
                acol1, acol2 = st.columns(2, gap="small")
                with st.status("Processing Audio request"):
                    audiofilename = datetag_string + "_" + filename
                    audiopath = text_to_speech(botmessage)
                    audiofile = open(audiopath, "rb")
                    audiobytes = audiofile.read()

                acol1.audio(audiobytes, format="audio/mp3")
                acol2.download_button(
                    emj_down + "Download Audio",
                    audiobytes,
                    file_name=datetag_string + ".mp3",
                    mime=None,
                )

                if popup_notifications:
                    st.toast(":blue[Audio 02] :green[activated]")
                st.markdown(
                    "##### Audio Generation :green[Completed]", unsafe_allow_html=False
                )

            status_string = (
                "**:red[Using "
                "" + assistantcontext + "] "
                "" + ":white[Reponse ("+str(tokencount) + ")]"
                " :blue[Sent ("+str(tokencountsent)+")] :cyan[Overall Tokens ("+str(tokensndrecd)+")]**"
                ""
            )

            status_cache = (
                "**:red[Using: " + assistantcontext + ""
                " ( " + "Reponse "+str(tokencount) + "Sent"
                ""+str(tokencountsent) + " )]**"
            )

            if atpts:
                st.markdown(status_string, unsafe_allow_html=True)

                st.session_state.chathistory.append(
                    {"role": "status", "content": status_cache}
                        )

            st.session_state.chathistory.append(
                {"role": "assistant", "content": botmessage}
            )

    # if activate_audio_output:
    #     st.toast(":blue[Audio] :green[activated]")
    # else:
    #     st.toast(":blue[Audio] :red[deactivated]")
if logout:
    colorful_print("[Info] User is loging out", "blue")
    st.session_state.accesscode = ""
    st.session_state.authstatus = False
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()


if restdata:
    colorful_print("[Info] User is resting Prompt", "blue")
    st.toast(":blue[Data Rest] :green[resting Session prompt]")
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.chathistoryprompt = ""
    st.session_state.chathistory = []
    st.session_state.lastchatoutput = ""
    st.warning("Prompt Memory has been reset", icon='⚠')

if not st.session_state.authstatus or st.session_state.authstatus == "":
    colorful_print("[Info] User waiting to login", "blue")

    bodyc1 = (
        """
        Great to have you on broad, If you have not registred for an 
        account, quickly do it now and get your **ACCESS CODE** now. 
        Currently Access is open at the moment for this 
        beta Release """+version+""". 

        Or get in contact with the team now for your chance to be 
        a head of your friends and colleges at work with this 
        very helpful tool.



        """
    )

    ltnewsapp = (
                """
                ##### :white[Lastest Update: New Models Now available]
                - :green[New Model from Google : Gemini 1.5 Pro Experiment 0801]
                """
            )

    f1 = (
        """
        ##### :red[Custom] Prompt Configuration

        allows you to customize the prompt configuration 
        in terms of the Prompt Temperature , Top-P, Top-K
        the max output tokens.It also allows you change 
        the safety options to: Harassment , Hate, Sexually
        and dangerous content.


        ##### :blue[Special] Features

        allows you to control the out of the response 
        in terms of the typing speed , the theming of 
        UI to fit your mood by changing the color. 


        ##### :red[File Context] Features

        allows you to upload PDF, CSV to chat to or 
        ask question to the PDF or CSV in terms of the 
        data it has. In other words chat with PDF and CSV.


        ##### :blue[Image Context] Features

        allows you to upload an Image to chat to or 
        ask question to the JPG, PNG, JPEG in terms of the 
        what is in the image. In other words chat with an Image.


        ##### :red[Youtube] Context Features

        allows you to Youtube Video as a URL Link to chat to or 
        ask question to the video in terms of the what is in the 
        video. In other words chat with youtube. This is especially
        useful if you want to get a summary of the video that you 
        have time to watch.


        """
    )

    f2 = (
        """

        ##### :blue[Model Options] and Assistances 

        allows you to select the Gemini Models to use. 
        also it give users the ability to use many many 
        different assistance to help with there productivity


        ##### :green[Text-To-Speech / Response-to-mp3] 

        allows you to generate the response output to audio
        or downloadable audio , also supports Elevenlabs Voices
        with your own API key. 


        ##### :blue[Additional] Custom Context

        allows you explain the problem or senerio and then
        provide detail of how the assistance can aid you to 
        solve that problem. with chating of providing questions 
        for it.  


        ##### :green[Code Context] Feature

        allows you to provide code from the most common programming 
        languages and then use this context to chat with the code you 
        have provided, either to check for problems in your code or to 
        let the assistance improve your code based on the questions and 
        comments you provide to the assistance. 

        """
    )
    
    st.header("Welcome to Miah's AI Assistance")
    # st.write("Number of test token:"+str(tokencounter(bodyc1)))

    st.markdown(bodyc1, unsafe_allow_html=True)

    st.markdown(ltnewsapp, unsafe_allow_html=False)
    st.markdown("---", unsafe_allow_html=False)

    btncl1, btncl2 = st.columns(2, gap="small")

    btncl1.markdown(
                    " ### Apply now and Get in to the Fun.",
                    unsafe_allow_html=False
                    )

    btncl1.link_button(
                        emj_down+"Register now",
                        "https://forms.gle/EMozLZeLbbuP4Tvr9"
                        )

    btncl2.markdown(" ### Share your feed and make Miah AI Great.",
                    unsafe_allow_html=False)
    btncl2.link_button(
                        emj_down+"Share your feedback",
                        "https://forms.gle/WmX8LEvwhVEvRCAPA"
                        )
    
    st.markdown("---", unsafe_allow_html=False)
    
    st.markdown(" ### Features of the Application", unsafe_allow_html=False)
    st.markdown("    ", unsafe_allow_html=False)

    mbcl1, mbcl2, mbcl3 = st.columns([1, 7, 1], gap="small")
    mmbcl1, mmbcl2 = st.columns([6, 6], gap="small")

    mmbcl1.markdown(f1, unsafe_allow_html=False)
    mmbcl2.markdown(f2, unsafe_allow_html=False)
    st.markdown("---", unsafe_allow_html=False)
    about_the_developer()

###########################
# Endof the Line
###########################
