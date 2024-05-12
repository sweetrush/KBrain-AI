
"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

# Definding Imported Libaries for the Program 
# #################################################

from pypdf import PdfReader
from gtts import gTTS
from io import BytesIO
import re
import requests
import logging
import configparser
import datetime
import pyperclip
import os
import google.generativeai as genai
import streamlit as st
import pandas as pd


# Definding the Current working version 
# of the Miah AI assistance 
# #################################################

version = "1.7"

####################

emj_tophat = ' 🎩 '
emj_billcap = ' 🧢 '
emj_gradcap = ' 🎓 '
emj_clamper = ' 🗜 '
emj_aaudio = ' 🔊 '

config = configparser.ConfigParser()
config.read('config.ini')
apivalue = config.get("APIKEYS", "api")
api11labs = config.get("APIKEYS", "api_11labs")

# Defind Date Tags for Filenaming
now = datetime.datetime.now()
datetag_string = f'{now.year}.{now.month}.{now.day}_{now.hour}{now.minute}{now.second}'

genai.configure(api_key=apivalue)
st.set_page_config(page_title="Miah GeminiAI", page_icon=":tada:", layout="wide")


# def openpdf_exttext(pdffile):
#     exttext = ''
#     preFile = PdfReader(pdffile)
#     numberofpages = len(preFile.pages)
#     for ps in range(numberofpages):
#         exttext += preFile.pages[ps].extract_text()
#     return exttext

def replace_chars(text, chars_to_replace, replacement):
    pattern = f"[{chars_to_replace}]"  # Create a character class pattern
    return re.sub(pattern, replacement, text)


@st.cache_data
def openpdf_exttext(pdffile):
    """Extracts text from a PDF file with improved error handling and potential optimization."""
    try:
        pdf_reader = PdfReader(pdffile)
        number_of_pages = len(pdf_reader.pages)
        extracted_text = ""
        for page_num in range(number_of_pages):
            extracted_text += pdf_reader.pages[page_num].extract_text(layout=True)
        return extracted_text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""  # Or raise an exception depending on your error handling strategy


@st.cache_data
def read_from_file(filename):
    pathDirAssistanceDef = "assistancedb/"
    assistance_filename = filename
    fullpath = os.path.join(pathDirAssistanceDef, assistance_filename)
    with open(fullpath, "r") as file:
        content = file.read()
        return content


def write_to_file(filename, text):
    storedir = "output/gemini_out"
    datetag = datetag_string
    store_path = os.path.join(storedir, datetag+'_'+filename)

    if not os.path.exists(storedir):
        os.makedirs(storedir)
    try:
        with open(store_path+"_gemin.md", "a", encoding="utf-8") as file:
            file.write(text + "\n")  # Add a newline at the end
    except OSError as e:
        print(f"Error writing to file: {e}")


def question_combinder(adcn_01, uquestions):
    if adcn_01 is not None and uquestions is not None:
        umessage = inputquestion+'?'+'\n##### [Additional Context] #####\n'+str(adcn_01)
        st.echo(str(adcn_01))
    else:
        umessage = inputquestion
    return umessage


def get_assistant_details(selection, listofAssistance, assistant):
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


def text_to_speech(text):
    """Converts text to speech using gTTS and returns an audio file."""
    tts = gTTS(text=text, lang='en')  # You can change the language if needed
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp


def get_audio(texttomp3, prefix, auid):
    ellskey = api11labs
    voiceid = "21m00Tcm4TlvDq8ikWAM"
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voiceid

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ellskey
    }

    data = {
        "text": texttomp3,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    mp3fileName = prefix + "_" + auid + '_output.mp3'
    
    folder_path = "ai_audio"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    mp3_path = os.path.join(folder_path, mp3fileName)

    with open(mp3_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    return mp3_path


model_tokens = "8024"

models = [
          "gemini-1.5-pro-latest",
          "gemini-1.0-pro",
          "gemini-pro-vision"
         ]


safety_options = [ 
                  "BLOCK_NONE", 
                  "BLOCK_FEW", 
                  "BLOCK_SOME", 
                  "BLOCK_MOST"
                 ]


listofAssistance = [
                   
                    # General Agents 
                    [emj_billcap+"GA_Default", "Default Assistance", "Default.atx"],
                    [emj_billcap+"GA_General", "General Assisance", "General.atx"],

                    # Technical Agents 
                    [emj_tophat+"TA_Linux", "Linux Assistance", "linux_assistance.atx"], 
                    [emj_tophat+"TA_Python", "Python Assistance", "Python_assistance.atx"],
                    [emj_tophat+"TA_Bash", "Bash Assistance", "bashexpert.atx"],
                    [emj_tophat+"TA_RedTeam", "RedTeam Assistance", "Red_Team_Expert.atx"],

                    # Assistive Professional Agents 
                    [emj_gradcap+"PA_2Ddotplan", "2D Plot Assistance", "dotplanner.atx"],
                    [emj_gradcap+"PA_Emailhelper", "EmailHelper Assistance", "emailhelper.atx"],
                    [emj_gradcap+"PA_BusniessExpert", "BE Assistance", "BusniessExpert.atx"]
                   
                   ]


assistant = []
for i in range(len(listofAssistance)):
    assistant.append(read_from_file(listofAssistance[i][2]))

# assistant = [
#              read_from_file(listofAssistance[0][2]),
#              read_from_file(listofAssistance[1][2]),
#              read_from_file(listofAssistance[2][2]),
#              read_from_file(listofAssistance[3][2]),
#              read_from_file(listofAssistance[4][2]),
#              read_from_file(listofAssistance[5][2]),
#              read_from_file(listofAssistance[6][2]),
#              read_from_file(listofAssistance[7][2]),
#              read_from_file(listofAssistance[8][2])
#             ]

# ###################################################################################
#  SIDE BAR CODE FOR THE PROGRAM 
#    - This is the start of the Side bar and with all elements 
# ###################################################################################


with st.sidebar:
    global tempture_val, fileloaded, opt1_safe, opt2_safe, opt3_safe, opt4_safe
    global loadassistantcontext, assistantcontext, adcn, pdftext, getResponsetext

    st.title(emj_clamper+"Miah's AI Gemini Assistance")

    with st.expander("Files Upload", expanded=False):
        uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
        if uploaded_file is not None:
            pdftext = openpdf_exttext(uploaded_file)
        else:
            pdftext = ""

        uploaded_csv = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_csv is not None:
            df = pd.read_csv(uploaded_csv)
            json_data = df.to_json(orient='records')
        else: 
            json_data = ""

        uploaded_img = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    with st.expander("Prompt Config", expanded=False):
        tempture_val = st.text_input("Prompt Temperature", value="0.07", max_chars=None)
        topp = st.text_input("Set Top P", value="1", max_chars=None)
        topk = st.text_input("Set Top K", value="1", max_chars=None)
        mot = st.text_input("Max Output Tokens", value=model_tokens, max_chars=None)
        convert_tpv = float(tempture_val)

    with st.expander("Safety Config", expanded=False):
        opt1_safe = st.selectbox("Harassment", (
                              safety_options[0],
                              safety_options[1],
                              safety_options[2],
                              safety_options[3]
                              ), index=0)

        opt2_safe = st.selectbox("Hate", (
                              safety_options[0],
                              safety_options[1],
                              safety_options[2],
                              safety_options[3]
                              ), index=0)

        opt3_safe = st.selectbox("Sexually Explicit", (
                              safety_options[0],
                              safety_options[1],
                              safety_options[2],
                              safety_options[3]
                              ), index=0)

        opt4_safe = st.selectbox("Dangerous Content", (
                              safety_options[0],
                              safety_options[1],
                              safety_options[2],
                              safety_options[3]
                              ), index=0)

    #
    # Setting the Module Selection for the Assistance 
    # ################################################

    model_select = st.selectbox("Choose Model", (
                               models[0],
                               models[1],
                               models[2]
                             ), index=0)

    # Setting the selected Active Assistance 
    # ################################################

    # selection = st.selectbox("Active Assistance:", 
    #                          (
    #                             listofAssistance[0][0],
    #                             listofAssistance[1][0],
    #                             listofAssistance[2][0],
    #                             listofAssistance[3][0],
    #                             listofAssistance[4][0],
    #                             listofAssistance[5][0],
    #                             listofAssistance[6][0],
    #                             listofAssistance[7][0],
    #                             listofAssistance[8][0]
    #                          ), index=0)

    selection = st.selectbox("Active Assistance:", 
                             [item[0] for item in listofAssistance[:min(9,
                              len(listofAssistance))]], index=0
                             )

    # Checking and setting the Selected Assistance 
    # ##############################################

    # if selection == listofAssistance[0][0]:
    #     loadassistantcontext = assistant[0]
    #     assistantcontext = listofAssistance[0][1]
    #     fileloaded = listofAssistance[0][2]

    # elif selection == listofAssistance[1][0]:
    #     loadassistantcontext = assistant[1]
    #     assistantcontext = listofAssistance[1][1]
    #     fileloaded = listofAssistance[1][2]

    # elif selection == listofAssistance[2][0]:
    #     loadassistantcontext = assistant[2]
    #     assistantcontext = listofAssistance[2][1]
    #     fileloaded = listofAssistance[2][2]

    # elif selection == listofAssistance[3][0]:
    #     loadassistantcontext = assistant[3]
    #     assistantcontext = listofAssistance[3][1]
    #     fileloaded = listofAssistance[3][2]

    # elif selection == listofAssistance[4][0]:
    #     loadassistantcontext = assistant[4]
    #     assistantcontext = listofAssistance[4][1]
    #     fileloaded = listofAssistance[4][2]

    # elif selection == listofAssistance[5][0]:
    #     loadassistantcontext = assistant[5]
    #     assistantcontext = listofAssistance[5][1]
    #     fileloaded = listofAssistance[5][2]

    # elif selection == listofAssistance[6][0]:
    #     loadassistantcontext = assistant[6]
    #     assistantcontext = listofAssistance[6][1]
    #     fileloaded = listofAssistance[6][2]

    # elif selection == listofAssistance[7][0]:
    #     loadassistantcontext = assistant[7]
    #     assistantcontext = listofAssistance[7][1]
    #     fileloaded = listofAssistance[7][2]

    # elif selection == listofAssistance[8][0]:
    #     loadassistantcontext = assistant[8]
    #     assistantcontext = listofAssistance[8][1]
    #     fileloaded = listofAssistance[8][2]

    loadassistantcontext, assistantcontext, fileloaded = get_assistant_details(
        selection, listofAssistance, assistant
    )

    # 
    # END OF the selected Assistance 
    # ############################################################

    st.toast("**:blue[Using AI:]**\n :red["+assistantcontext+"]")
    st.toast(":green[File:]"+fileloaded)
    st.toast(":green[Model:]"+model_select)

    adcn = st.text_area(label="Additional Context", key="KK09923")
    activate_audio_output = st.checkbox(emj_aaudio+"Activate Audio:", value=False)
    st.write("version: "+version)
    copyresponsetoClip = st.button("CC")


# #########################################################################
# END OF: Sidebar  ######################################################## 
#
###########################################################################

# Set up the model
generation_config = {
  "temperature": convert_tpv,
  "top_p": float(topp),
  "top_k": int(topk),
  "max_output_tokens": int(mot),
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": opt1_safe
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": opt2_safe
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": opt3_safe
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": opt4_safe
  },
]

chatdata = []
model_name = model_select

model = genai.GenerativeModel(model_name=model_name,
                              generation_config=generation_config,
                              safety_settings=safety_settings)


# For Session Storing Information  
# ##################################################################
# ##################################################################

if "chathistory" not in st.session_state:
    st.session_state.chathistory = []

if "chathistoryprompt" not in st.session_state:
    st.session_state.chathistoryprompt = ''

if "lastchatoutput" not in st.session_state:
    st.session_state.lastchatoutput = ''


# Looping through the session stored Information  
for message in st.session_state.chathistory:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# END OF: Session Storing Information ################
# ####################################################


# Getting the User Prompt Information 
# 
inputquestion = st.chat_input("Provide your Prompt")

usermessage = question_combinder(adcn, inputquestion)

# Runs What the User has input
if usermessage:
    with st.chat_message("User"):
        st.write(usermessage)

        # Storing User Information to the Session Variable
        st.session_state.chathistory.append({"role": "User", "content": usermessage})  # noqa: E501

    chars_tobe_replaced = ' ,.'
    chars_swap = ""  # Noted that this will make the space as the char swap
    filename = replace_chars(inputquestion, chars_tobe_replaced, chars_swap)
    filename = filename[:20]
    print("[info] FileName is: "+filename+"")

    convo = model.start_chat(history=chatdata) 

    with st.status("Processing Request ...."):
        if pdftext == "":
            groupcontext = loadassistantcontext
        else:
            groupcontext = loadassistantcontext+pdftext

        if json_data == "":
            groupcontext += ""
        else:
            groupcontext += json_data

        try: 
            convo.send_message(groupcontext+usermessage)

        except Exception as e:
            st.toast(":red[Error:] on call", icon=None)
            st.error(e, icon=None)

        ca = st.session_state.chathistoryprompt = st.session_state.chathistoryprompt+convo.last.text+usermessage

        # Uncomment to View ChathistroyPrompt data in terminal 
        # print(st.session_state.chathistoryprompt)

        res00data = {"role": "user", "parts": [ca]}
        res01data = {"role": "model", "parts": [convo.last.text]}
        res02data = {"role": "user", "parts": [groupcontext+usermessage]}
        chatdata.append(res02data)
        chatdata.append(res00data)
        chatdata.append(res01data)
        st.write(chatdata)

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
        st.write(botmessage)

        if activate_audio_output:
            audiofilename = datetag_string+"_"+filename
            audiopath = get_audio(botmessage, "el11_au", audiofilename)
            audiofile = open(audiopath, "rb")
            audiobytes = audiofile.read()
            st.audio(audiobytes, format='audio/mp3')
            st.toast(":blue[Audio] :green[activated]")

        status_string = "<strong style='color:red'>Using: "+assistantcontext+" [ "+str(tokencount)+" ]</strong>"  # noqa: E501
        status_cache = "**:red[Using: "+assistantcontext+" ( "+str(tokencount)+" )]**"  # noqa: E501
        st.markdown(status_string, unsafe_allow_html=True)
        st.session_state.chathistory.append({"role": "assistant", "content": botmessage})  #noqa: E501
        st.session_state.chathistory.append({"role": "status", "content": status_cache})
        # 

if activate_audio_output:
    st.toast(":blue[Audio] :green[activated]")
else:
    st.toast(":blue[Audio] :red[deactivated]")


if copyresponsetoClip:
    pyperclip.copy(st.session_state.lastchatoutput)
    st.success("Text copied to clipboard!")