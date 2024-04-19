
"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""


import google.generativeai as genai
import configparser
import datetime
import os
import streamlit as st

version = "1.3"

####################

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

assistant0 = read_from_file("Default.atx")
assistant1 = read_from_file("linux_assistance.atx")
assistant2 = read_from_file("Python_assistance.atx")
assistant3 = read_from_file("General.atx")
assistant4 = read_from_file("bashexpert.atx")
assistant5 = read_from_file("dotplanner.atx")



# loadassistantcontext = ''
# assistantcontext = ''



with st.sidebar:
    global tempture_val
    tempture_val = st.text_input("Prompt Temperature", value="0.01", max_chars=None)
    convert_tpv = float(tempture_val)
    selection = st.selectbox("Active Assistance:", 
                            (
                                "Default",
                                "General",
                                "Linux",
                                "Python",
                                "2Ddotplan",
                                "Bash"
                            )
                            , index=0)

    global loadassistantcontext, assistantcontext
    if selection == "Default":
        loadassistantcontext = assistant0
        assistantcontext = "Default Assistance"
    elif selection == "Linux":
        loadassistantcontext = assistant1
        assistantcontext = "Linux Assistance"
    elif selection == "Python":
        loadassistantcontext = assistant2
        assistantcontext = "Python Assistance"
    elif selection == "General":
        loadassistantcontext = assistant3
        assistantcontext = "General Assistance"
    elif selection == "Bash":
        loadassistantcontext = assistant4
        assistantcontext = "Bash Assistance"
    elif selection == "2Ddotplan":
        loadassistantcontext = assistant5
        assistantcontext = "2D Dot planner Assistance"

    st.write("version: "+version)


# Set up the model
generation_config = {
  "temperature": convert_tpv,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model_name = "gemini-1.0-pro-latest"
chatdata = []
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

# Getting the User Prompt Information 
# 

usermessage = st.chat_input("Provide your Prompt")


if usermessage:

    with st.chat_message("User"):
        st.write(usermessage)

        # Storing User Information to the Session Variable
        st.session_state.chathistory.append({"role": "User", "content": usermessage})  # noqa: E501

    filename = usermessage.replace(" ", "")
    filename = filename.replace(',', "")
    filename = filename.replace('.', "")
    filename = filename[:20]
    print("[info] FileName is: "+filename+"")

    convo = model.start_chat(history=chatdata) 

    with st.status("Processing Request ...."):

        convo.send_message(loadassistantcontext+usermessage)
        ca = st.session_state.chathistoryprompt = st.session_state.chathistoryprompt+convo.last.text+usermessage
        res00data = {"role": "user", "parts": [ca]}
        res01data = {"role": "model", "parts": [convo.last.text]}
        res02data = {"role": "user", "parts": [loadassistantcontext+usermessage]}
        chatdata.append(res02data)
        chatdata.append(res00data)
        chatdata.append(res01data)

        st.write(chatdata)

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
