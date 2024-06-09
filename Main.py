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

# From Streamlit Extra Components
from streamlit_extras.bottom_container import bottom

import google.generativeai as genai
import speech_recognition as sr
import streamlit as st
import pandas as pd
import configparser
import requests
import logging
import datetime
import os
import re
import hashlib


# Uncomment to Use them
# from io import BytesIO
# import numpy as np
# import pyperclip
# import time

# Definding the Current working version
# of the Miah AI assistance
# #################################################

version = "2.9.1"
develper = "SweetRushCoder"

###################################################

# AccessCode for Testing
accesscode_miah = "pWScyxQzvFN3rxjxi4aevEv3srgbJa56nvQcB6T7Yw"

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

devmode = 0
apptile = ""
debprint = 0

if devmode == 1:
    st.set_page_config(page_title="Miah's AI Assistance (Devmode)", page_icon=":tada:", layout="wide")
else:
    st.set_page_config(page_title="Miah's AI Assistance", page_icon=":tada:", layout="wide")

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
    colorful_print("[FX-R] replace chars (F01)", "magenta")

    pattern = f"[{chars_to_replace}]"  # Create a character class pattern
    return re.sub(pattern, replacement, text)


# #####################################################
# #  02         EXTRACT PDF TO TEXT FUNCTION         ##
# #####################################################
@st.cache_data
def openpdf_exttext(pdffile):
    colorful_print("[FX-R] openpdf (F02)", "magenta")

    """Extracts text from a PDF file with improved error
    handling and potential optimization."""

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
    colorful_print("[FX-R] read from file (F03)", "magenta")

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
        colorful_print(f"Error writing to file: {e}", "red")


# #####################################################
# #  05         Q_COMBINDER FUNCTION                 ##
# #####################################################
def question_combinder(additional_context, user_question):
    colorful_print("[FX-R] question combinder (F05)", "magenta")

    """Combines a user question with additional context.

    Args:
      additional_context: A string containing additional context.
      user_question: A string representing the user's question.

    Returns:
      A formatted string combining the question and context, or None if
      user_question is None.
    """

    # This if statement is a fix for the No Text when streamlit
    # switchs the Assistance.
    if not user_question:
        return None

    combined_question = user_question + "?"
    # print("Debuging - QC:"+user_question)

    if atsec:
        combined_question += " This is for testing in the Lab and " " for educational."
        dynamic_css("#e0391f")

    if additional_context:
        adsstring = " \n##### :green[Additional Context] #####\n"
        combined_question += f"{adsstring}{additional_context}"

    return combined_question


# #####################################################
# #  06         GET ASSISTANCE DETAIL FUNCTION       ##
# #####################################################
def get_assistant_details(selection, listofAssistance, assistant):
    colorful_print("[FX-R] get assistant details (F06)", "magenta")
    """Retrieves assistant details based on selection.

    Args:
       selection: The selected assistant identifier.
       listofAssistance: A list of tuples containing assistant information.
       assistant: A list of assistant objects.

    Returns:
    A tuple containing loadassistantcontext, assistantcontext, and fileloaded.
    """
    for i, (assistant_id, context, file) in enumerate(listofAssistance):
        if selection == assistant_id:
            return assistant[i], context, file

    return None, None, None  # Return None values if no match is found


# #####################################################
# #  07      TEXT TO SPEECH FUNCTION [GTTS]          ##
# #####################################################
def text_to_speech(text):
    colorful_print("[FX-R] text to speech (F07)", "magenta")
    """Converts text to speech using gTTS and returns an audio file."""
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

    return mp3_path


# #####################################################
# #  09         COUNT PROMPT FILES FUNCTION          ##
# #####################################################
def count_files(directory_path):
    colorful_print("[FX-R] count_files (F09)", "magenta")
    """Counts the number of files in a directory.

    Args:
        directory_path (str): The path to the directory.

    Returns:
        int: The number of files in the directory.
    """
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

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if "@@" not in line and line:  # Check for "@@" and empty lines
                emjtag, name, label, file = line.strip().split(",")

                if emjtag == "1":
                    listofAssistance.append(
                        [
                            emj_billcap + str(name),
                            str(label),
                            replace_chars(str(file), " ", ""),
                        ]
                    )

                elif emjtag == "2":
                    listofAssistance.append(
                        [
                            emj_tophat + str(name),
                            str(label),
                            replace_chars(str(file), " ", ""),
                        ]
                    )

                elif emjtag == "3":
                    listofAssistance.append(
                        [
                            emj_gradcap + str(name),
                            str(label),
                            replace_chars(str(file), " ", ""),
                        ]
                    )

                elif emjtag == "4":
                    listofAssistance.append(
                        [
                            emj_assistance + str(name),
                            str(label),
                            replace_chars(str(file), " ", ""),
                        ]
                    )

                else:
                    listofAssistance.append(
                        [
                            emj_billcap + str(name),
                            str(label),
                            replace_chars(str(file), " ", ""),
                        ]
                    )


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
        colorful_print(f"Error: {str(e)}","red")

    return None


# #####################################################
# #  15         GET YOUTUBE VIDEO ID FUNCTION        ##
# #####################################################
def get_video_id(url):
    colorful_print("[FX-R] get video id (F15)", "magenta")
    # Extract the video id from the YouTube URL
    video_id = re.findall(
        r"(?:v=|v\/|embed\/|youtu\.be\/|\/v\/|\/e\/|watch\?v=|youtube\.com\/user\/[^#]*#([^\/]*\/)*\w+\/|youtube\.com\/v\/|youtube\.com\/embed\/|youtube\.com\/watch\?v=)([^#\&\?]*[^#\&\?\n]*)",
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
        st.markdown(f"<style>{ubuntu}{newtextcss}</style>", unsafe_allow_html=True)


# #####################################################
# #  18         CHECK LOGIN CONDITION                ##
# #####################################################
def get_AccessCondition():
    colorful_print("[FX-R] get AccessCondition (F18)", "magenta")
    access = st.sidebar.text_input(
        "Provide your access Code:",
        value=st.session_state.accesscode,
        type="password",
        max_chars=None,
    )

    st.session_state.accesscode = access

    if access == "":
        st.sidebar.error("Access Code is Empty", icon="🚨")

    if access == accesscode_miah:
        grant = True
        st.session_state.authstatus = True
        if access != "":
            st.sidebar.success("Authenticated & Active", icon="📡")
    else:
        grant = False
        st.session_state.authstatus = False
        if access != "":
            st.sidebar.warning(
                "Authentication Error: Please check your again!", icon="⛑️"
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
    colorful_print("[FX-R] Calculate string hash (F22)", "magenta")
    """
    Calculates the hash of a string using the specified algorithm.
    Args:
        input_string (str): The string to hash.
        algorithm (str, optional): The hash algorithm to use. 
                                    Defaults to 'sha256'.
    Returns:
        str: The hexadecimal representation of the hash value.
    """
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
        textcombind = Fore.RED+Style.BRIGHT+text+Style.RESET_ALL

    if color == "green":
        textcombind = Fore.GREEN+Style.BRIGHT+text+Style.RESET_ALL

    if color == "yellow":
        textcombind = Fore.YELLOW+Style.BRIGHT+text+Style.RESET_ALL

    if color == "white":
        textcombind = Fore.WHITE+Style.BRIGHT+text+Style.RESET_ALL

    if color == "blue":
        textcombind = Fore.BLUE+Style.BRIGHT+text+Style.RESET_ALL

    if color == "magenta":
        textcombind = Fore.MAGENTA+Style.BRIGHT+text+Style.RESET_ALL

    if color == "cyan":
        textcombind = Fore.MAGENTA+Style.BRIGHT+text+Style.RESET_ALL
    
    print(textcombind)


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
    "gemini-1.5-flash-latest",
    "gemini-1.0-pro",
    "gemini-pro-vision",
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
    st.sidebar.title(emj_clamper + "Miah's AI Gemini Assistance (DevMode)")
else:
    st.sidebar.title(emj_clamper + "Miah's AI Gemini Assistance")

dynamic_css(epcolor_val)

# Getting the Condition of the Access
get_AccessCondition()

logout = None

if st.session_state.authstatus and st.session_state.accesscode != "":
    with st.sidebar:

        logout = st.button("Logout")

        global tempture_val, fileloaded, opt1_safe, opt2_safe
        global opt3_safe, opt4_safe, pdftext, getResponsetext
        global loadassistantcontext, assistantcontext, adcn

        # horizontal_line() # Uncomment to show the Line

        # Uncomment this to reflect the file Upload Feature on the Side Bar
        # mapFileUploadOnSideBar()

        with st.expander(emj_gear + "Prompt Config", expanded=False):
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
                "Set Top-P",  # Label for the slider
                min_value=0.0,  # Minimum value
                max_value=1.0,  # Maximum value
                value=0.07,  # Default value
                step=0.05,  # Increment step
            )

            topk = st.number_input(
                "Set Top-K", min_value=None, max_value=None, value=10, step=1
            )

            mot = st.text_input("Max Output Tokens", value=model_tokens, max_chars=None)

            convert_tpv = float(tempture_val)

        with st.expander(emj_safety + "Safety Config", expanded=False):

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
                emj_clamper + "Choose Model", (models[0], models[1], models[2]), index=0
            )

            # Setting the selected Active Assistance
            # ################################################

            selection = st.selectbox(
                emj_assistance + "Active Assistance:",
                [
                    item[0]
                    for item in listofAssistance[: min(20, len(listofAssistance))]
                ],
                index=0,
            )

        # Checking and setting the Selected Assistance
        # ##############################################

        loadassistantcontext, assistantcontext, fileloaded = get_assistant_details(
            selection, listofAssistance, assistant
        )

        #
        # END OF the selected Assistance
        # ############################################################

        if popup_notifications:
            st.toast("**:blue[Using AI:]**\n :red[" + assistantcontext + "]")
            st.toast(":green[File:]" + fileloaded)
            st.toast(":green[Model:]" + model_select)

        with st.expander(emj_safety + "Special Features", expanded=False):
            atsec = st.toggle("ALT", value=False, help="Active Lab Testing")
            bexpanderColor = st.color_picker("Theme:", epcolor_val)

            # save new color to Config
            config["THEMEING"]["ep_color"] = bexpanderColor
            with open("config.ini", "w") as configfile:
                config.write(configfile)

            # set the session color
            st.session_state.exbclor = bexpanderColor
            dynamic_css(bexpanderColor)

        with st.expander(emj_aaudio + "Audio Config", expanded=False):
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
            else:
                activate_audio_output = False

            activate_audio_output002 = st.toggle(
                emj_aaudio + "Audio(2):", value=False, help="Active Audio GTTs"
            )

        with st.expander(emj_stats + "Status", expanded=False):
            st.write("##### Number of SAR: " + str(fileInStore))
            st.write("##### Number of SAF: " + str(audioInStore))
            st.write("##### Number of AN: " + str(len(listofAssistance)))

        horizontal_line()
        st.page_link(
            "pages/help.py", label="Help Guide", icon=emj_help_ico, disabled=False
        )
        st.page_link(
            "pages/aboutdev.py", label="About Dev", icon=emj_help_ico, disabled=False
        )
        horizontal_line()
    # about_the_developer()

    if "exbclor" not in st.session_state:
        st.session_state.exbclor = ""

    # #########################################################################
    # ##  END OF: Sidebar  ####################################################
    #
    # #########################################################################
    # #########################################################################

    # ####################################################################
    # ####################################################################
    #   Content Below the Chatline input field

    codewrap = ""  # initating the var for the code wrap here
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
                        pdftext = openpdf_exttext(uploaded_file)
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

    if GeminiAPIkey:
        genai.configure(api_key=GeminiAPIkey)
    else:
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

    # For Session Storing Information [ Caching ]
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

            # ######## AREA FOR SEND PROMPT INFOR TO AI
            #

            try:
                convo.send_message(cache_history_now + grpcontext + cxt_n_usermsg)

                # Uncomment for Debugging for purpose.
                #
                # print("[Debuging]:[1] "+groupcontext+usermessage)

            except Exception as e:
                st.toast(":red[Error:] on call", icon=None)
                st.error(e, icon=None)

            ca = cache_history_now + usermessage
            st.session_state.chathistoryprompt = ca
            # print(f"\n\n Current CACHE BP:{cache_history_now}") # Debuging Perpose
            # Uncomment to View ChathistroyPrompt data in terminal
            # print(st.session_state.chathistoryprompt)

            # systempromptadd = "Your name is Miah, You are named after my son"

            res00data = {"role": "user", "parts": [ca]}
            res01data = {"role": "model", "parts": [convo.last.text]}
            # res03data = {"role": "model", "parts": [systempromptadd]}
            res02data = {
                "role": "user",
                "parts": [convo.last.text + grpcontext + usermessage],
            }

            chatdata.append(res00data)
            chatdata.append(res01data)
            # chatdata.append(res03data)
            chatdata.append(res02data)

            st.write(chatdata)
            # print(f'\n\n Chatdata: {chatdata}\n\n') # Uncomment for Deginfo
        
        if atsec:
            dynamic_css("#e0391f")
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

        with st.chat_message("assistant"):
            botmessage = convo.last.text

            #
            # @@ Note to implement streaming of Returned information.
            #

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
                "<strong style='color:red'>Using: "
                "" + assistantcontext + " [ "
                "" + str(tokencount) + " ]</strong>"
            )

            status_cache = (
                "**:red[Using: " + assistantcontext + ""
                " ( " + str(tokencount) + " )]**"
            )

            st.markdown(status_string, unsafe_allow_html=True)
            st.session_state.chathistory.append(
                {"role": "assistant", "content": botmessage}
            )
            st.session_state.chathistory.append(
                {"role": "status", "content": status_cache}
            )

    # if activate_audio_output:
    #     st.toast(":blue[Audio] :green[activated]")
    # else:
    #     st.toast(":blue[Audio] :red[deactivated]")
if logout:
    st.session_state.accesscode = ""
    st.session_state.authstatus = False
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()


if not st.session_state.authstatus:
    bodyc1 = (
        """
        Great to have you on the Application, If you have not registred for an 
        account to get you :white[accesscode] you should now. Currently Access 
        is open at the moment for this :yellow[Beta Release]. 

        Or get in contact with the team now for your chance to be a head of your 
        friends and colleges at work with this very helpful tool.

        ### Apply now and Get in to the Fun. 
        """
    )
    
    st.header("Welcome to Miah's AI Assistance")

    st.markdown(bodyc1, unsafe_allow_html=True)
    st.link_button(emj_down+"Register now", "https://forms.gle/EMozLZeLbbuP4Tvr9")

    # with st.expander("Get Access"):
    # # write_registration_to_sheet()
    # st.markdown(
    #             "<div><iframe src=\"https://docs.google.com/forms/d/e/1" 
    #             "FAIpQLSecGZXC1puJAd4VfNYEkh_ZeNmjDIDaThtCd-HQh2cg"
    #             "d-vQew/viewform?embedded=true\" width=\"400\" hei"
    #             "ght=\"1091\" frameborder=\"0\" marginheight=\"0\""
    #             "marginwidth=\"0\">Loading…</iframe></div>",
    #             unsafe_allow_html=True
    #             )
        
    # with bottom():
    # cl1, cl2 = st.columns(2, gap="small")
    # cl1.markdown("Using: :red["+model_select+"]")


# Endof the Line
