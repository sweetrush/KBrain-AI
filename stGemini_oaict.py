
"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""


import google.generativeai as genai
from pypdf import PdfReader
import re
import logging
import configparser
import datetime
import os
import streamlit as st
import pandas as pd

version = "1.6"

####################


# def openpdf_exttext(pdffile):
#     exttext = ''
#     preFile = PdfReader(pdffile)
#     numberofpages = len(preFile.pages)
#     for ps in range(numberofpages):
#         exttext += preFile.pages[ps].extract_text()
#     return exttext

def replace_chars(text, chars_to_replace, replacement):
   """Replaces specific characters in a string using regular expressions.

  Args:
    text: The input string.
    chars_to_replace: A string containing the characters to be replaced.
    replacement: The replacement character or string.

  Returns:
    The modified string with the specified characters replaced.
   """
   pattern = f"[{chars_to_replace}]"  # Create a character class pattern
   return re.sub(pattern, replacement, text)

# Example usage
# text = "This is a sample string with special characters like # and %."
# chars_to_replace = "#%"
# replacement = "*"
# result = replace_chars(text, chars_to_replace, replacement)
# print(result)  # Output: This is a sample string with special characters like * and *.


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
    now = datetime.datetime.now()
    storedir = "output/gemini_out"
    datetag = f'{now.year}.{now.month}.{now.day}_{now.hour}{now.minute}{now.second}'
    store_path = os.path.join(storedir, datetag+'_'+filename)

    if not os.path.exists(storedir):
        os.makedirs(storedir)
    try:
        with open(store_path+"_gemin.md", "a", encoding="utf-8") as file:
            file.write(text + "\n")  # Add a newline at the end
    except OSError as e:
        print(f"Error writing to file: {e}")


config = configparser.ConfigParser()
config.read('config.ini')
apivalue = config.get("APIKEYS", "api")


genai.configure(api_key=apivalue)
st.set_page_config(page_title="Miah GeminiAI", page_icon=":tada:", layout="wide")
st.title("Miah's AI Gemini Assistance")

models = [
          "gemini-1.5-pro-latest",
          "gemini-1.0-pro"
         ]


safety_options = [ 
                  "BLOCK_NONE", 
                  "BLOCK_FEW", 
                  "BLOCK_SOME", 
                  "BLOCK_MOST"
                 ]


listofAssistance = [
                   
                    ["Default", "Default Assistance", "Default.atx"],
                    ["General", "General Assisance", "General.atx"],
                    ["Linux", "Linux Assistance", "linux_assistance.atx"], 
                    ["Python", "Python Assistance", "Python_assistance.atx"],
                    ["2Ddotplan", "2D Plot Assistance", "dotplanner.atx"],
                    ["Emailhelper", "EmailHelper Assistance", "emailhelper.atx"],
                    ["Bash", "Bash Assistance", "bashexpert.atx"],
                    ["RedTeam", "RedTeam Assistance", "Red_Team_Expert.atx"]
                   
                   ]


assistant0 = read_from_file(listofAssistance[0][2])
assistant1 = read_from_file(listofAssistance[1][2])
assistant2 = read_from_file(listofAssistance[2][2])
assistant3 = read_from_file(listofAssistance[3][2])
assistant4 = read_from_file(listofAssistance[4][2])
assistant5 = read_from_file(listofAssistance[5][2])
assistant6 = read_from_file(listofAssistance[6][2])
assistant7 = read_from_file(listofAssistance[7][2])


# loadassistantcontext = ''
# assistantcontext = ''


with st.sidebar:
    global tempture_val, fileloaded, opt1_safe, opt2_safe, opt3_safe, opt4_safe
    global loadassistantcontext, assistantcontext, adcn, pdftext 

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

    with st.expander("Prompt Config", expanded=False):
        tempture_val = st.text_input("Prompt Temperature", value="0.07", max_chars=None)
        topp = st.text_input("Set Top P", value="1", max_chars=None)
        topk = st.text_input("Set Top K", value="1", max_chars=None)
        mot = st.text_input("Max Output Tokens", value="4024", max_chars=None)
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

    model_select = st.selectbox("Choose Model", (
                               models[0],
                               models[1]
                             ), index=0)

    selection = st.selectbox("Active Assistance:", 
                             (
                                listofAssistance[0][0],
                                listofAssistance[1][0],
                                listofAssistance[2][0],
                                listofAssistance[3][0],
                                listofAssistance[4][0],
                                listofAssistance[5][0],
                                listofAssistance[6][0],
                                listofAssistance[7][0]
                             ), index=0)

    if selection == listofAssistance[0][0]:
        loadassistantcontext = assistant0
        assistantcontext = listofAssistance[0][1]
        fileloaded = listofAssistance[0][2]
    elif selection == listofAssistance[1][0]:
        loadassistantcontext = assistant1
        assistantcontext = listofAssistance[1][1]
        fileloaded = listofAssistance[1][2]
    elif selection == listofAssistance[2][0]:
        loadassistantcontext = assistant2
        assistantcontext = listofAssistance[2][1]
        fileloaded = listofAssistance[2][2]
    elif selection == listofAssistance[3][0]:
        loadassistantcontext = assistant3
        assistantcontext = listofAssistance[3][1]
        fileloaded = listofAssistance[3][2]
    elif selection == listofAssistance[4][0]:
        loadassistantcontext = assistant4
        assistantcontext = listofAssistance[4][1]
        fileloaded = listofAssistance[4][2]
    elif selection == listofAssistance[5][0]:
        loadassistantcontext = assistant5
        assistantcontext = listofAssistance[5][1]
        fileloaded = listofAssistance[5][2]
    elif selection == listofAssistance[6][0]:
        loadassistantcontext = assistant6
        assistantcontext = listofAssistance[6][1]
        fileloaded = listofAssistance[6][2]
    elif selection == listofAssistance[7][0]:
        loadassistantcontext = assistant7
        assistantcontext = listofAssistance[7][1]
        fileloaded = listofAssistance[7][2]

    st.toast("**:blue[Using AI:]**\n :red["+assistantcontext+"]")
    st.toast(":green[File:]"+fileloaded)
    st.toast(":green[Model:]"+model_select)
    adcn = st.text_area(label="Additional Context")
    st.write("version: "+version)

# END OF: Sidebar  #################################################### 


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
# ####################################################
if "chathistory" not in st.session_state:
    st.session_state.chathistory = []
if "chathistoryprompt" not in st.session_state:
    st.session_state.chathistoryprompt = ''

# Looping through the session stored Information  
for message in st.session_state.chathistory:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# END OF: Session Storing Information ################

# Getting the User Prompt Information 
# 
aa = st.chat_input("Provide your Prompt")
if adcn is not None and aa is not None:
    usermessage = aa+'?'+'\n##### [Additional Context] #####\n'+str(adcn)
    st.echo(str(adcn))
else:
    usermessage = aa


# Runs What the User has input
if usermessage:
    with st.chat_message("User"):
        st.write(usermessage)

        # Storing User Information to the Session Variable
        st.session_state.chathistory.append({"role": "User", "content": usermessage})  # noqa: E501

    chars_tobe_replaced = " ,."
    chars_swap = ""  # Noted that this will make the space as the char swap
    # filename = usermessage.replace(" ", "")
    # filename = filename.replace(',', "")
    # filename = filename.replace('.', "")
    filename = replace_chars(usermessage, chars_tobe_replaced, chars_swap)
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

        convo.send_message(groupcontext+usermessage)
        ca = st.session_state.chathistoryprompt = st.session_state.chathistoryprompt+convo.last.text+usermessage
        res00data = {"role": "user", "parts": [ca]}
        res01data = {"role": "model", "parts": [convo.last.text]}
        res02data = {"role": "user", "parts": [groupcontext+usermessage]}
        chatdata.append(res02data)
        chatdata.append(res00data)
        chatdata.append(res01data)
        st.write(chatdata)
        st.toast("Generated Response Completed", icon=None)

    write_to_file(filename, convo.last.text)
    
    # This Gets the Number of Tokens needed.  
    tokencount = model.count_tokens(convo.last.text)

    with st.chat_message("assistant"):
        botmessage = convo.last.text
        st.write(botmessage)
        status_string = "<strong style='color:red'>Using: "+assistantcontext+" [ "+str(tokencount)+" ]</strong>"  # noqa: E501
        status_cache = "**:red[Using: "+assistantcontext+" ( "+str(tokencount)+" )]**"  # noqa: E501
        st.markdown(status_string, unsafe_allow_html=True)
        st.session_state.chathistory.append({"role": "assistant", "content": botmessage})  #noqa: E501
        st.session_state.chathistory.append({"role": "status", "content": status_cache})
        # 
