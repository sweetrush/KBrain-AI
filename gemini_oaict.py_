
"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""


import google.generativeai as genai
import datetime
import os
import colorama
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
apivalue = config.get("APIKEYS", "api")


genai.configure(api_key=apivalue)


Banner = '\n\nWelcome to the Gemini Miah AI\n'
Banner = Banner+'by SweetRushC0d3r\n'
Banner = Banner+'v.1.0.1 @ 2024\n\n'


txtRED = colorama.Fore.RED
txtBLACK = colorama.Fore.BLACK
txtGREEN = colorama.Fore.GREEN
txtYELLOW = colorama.Fore.YELLOW
txtBLUE = colorama.Fore.BLUE
txtMAGENTA = colorama.Fore.MAGENTA
txtCYAN = colorama.Fore.CYAN
txtWHITE = colorama.Fore.WHITE
txtRESET = colorama.Fore.RESET


userprompttag = "\n\nMe : ************************************** \n\n"
aiprompttag = "\n\nAI : ************************************** \n\n"


# Set up the model
generation_config = {
  "temperature": 0.03,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4048,
}

safety_settings = [
  # {
  #   "category": "HARM_CATEGORY_HARASSMENT",
  #   "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  # },
  # {
  #   "category": "HARM_CATEGORY_HATE_SPEECH",
  #   "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  # },
  # {
  #   "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
  #   "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  # },
  # {
  #   "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
  #   "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  # },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
chatdata = []


def write_to_file(filename, text):
    now = datetime.datetime.now()
    storedir = "output/gemini_out"
    datetag = f"""{now.year}{now.month}{now.day}{now.hour}
                {now.minute}{now.second}"""
    store_path = os.path.join(storedir, datetag+'_'+filename)

    if not os.path.exists(storedir):
        os.makedirs(storedir)

    try:
        with open(store_path+"_gemin.md", "a", encoding="utf-8") as file:
            file.write(text + "\n")  # Add a newline at the end
    except OSError as e:
        print(f"Error writing to file: {e}")


# Displaying the Program Banner
print(txtBLUE+Banner)

while True:
    usermessage = input(txtGREEN+userprompttag+txtRESET)
    filename = usermessage.replace(" ", "")
    filename = filename.replace(',', "")
    filename = filename.replace('.', "")

    if usermessage.lower() == "exit":
        print(txtYELLOW+"\n\n\n\n\n"
              "Thank you for using Miah Gemini AI\n\n"
              ""+txtRESET)
    else:
        convo = model.start_chat(history=chatdata)
        convo.send_message(usermessage)
        res01data = {
                "role": "model",
                "parts": [convo.last.text]
                }
        res02data = {
                "role": "user",
                "parts": [usermessage]
                }

    chatdata.append(res02data)
    chatdata.append(res01data)
    write_to_file(filename, convo.last.text)
    tokencount = txtRED+str(model.count_tokens(convo.last.text))+txtRESET
    rtext = convo.last.text
    rtext = rtext.replace(":**", "#####")
    rtext = rtext.replace("**", txtMAGENTA+"**")
    rtext = rtext.replace("#####", ":**"+txtRESET+txtYELLOW)

    print(txtRED+aiprompttag+txtRESET+rtext+'\n\n'+tokencount)
