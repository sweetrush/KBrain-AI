import os
import time
import random
import string
import datetime
import json
import curses
import colorama
import pygments
from playsound           import playsound
from pathlib             import Path
from openai              import OpenAI
from pygments.lexers     import PhpLexer
from pygments.formatters import TerminalFormatter

#Initiatizing OpenAI
# Defining the New Code with New OpenAI changes 
client = OpenAI(api_key="  ")

# Initializing Colorama
colorama.init()
promptcx = "a"
systemcontext = "You are a helpful assistance that know everything"
tokens = 3000

def gpt3(ask):
    global promptcx
    global systemcontext
    promptcx += ask
    response = client.chat.completions.create(

    # Uncomment the Mode to Use.
    #######################################
    #model ="text-davinci-003",
    model = "gpt-3.5-turbo-1106",
    messages= [ 
               {"role": "system", "content": systemcontext},
               {"role": "user","content": promptcx }

               ],
    )


    # content = response.choices[0].text.split('.')   #OLD CODE
    content = response.choices[0].message.content             #New Code 
    #print(content)

    return content


def text_to_speech(text,filename):
    
    filestring = "speech_" + filename + ".mp3"
    speech_file_path = Path("G:\\KBrain_Audio").parent/filestring
    
    response = client.audio.speech.create(
        
        model="tts-1",
        voice="alloy",
        input=text 
        
        )


    response.stream_to_file(speech_file_path)
    playsound(speech_file_path)
    pass

def gen_random_string(length):

    characters = string.ascii_letters + string.digits 
    genstring = ''.join(random.choice(characters) for i in range(length))


    return genstring


def displaybanner():
    print(colorama.Fore.CYAN + "///////////////////////////////////////////////////")
    print(colorama.Fore.CYAN + "//        Welcome to the K-Brain Prompt          //")
    print(colorama.Fore.CYAN + "//            version 1.0                        //")
    print(colorama.Fore.CYAN + "//         Developed by: Sw33tRu5h_C0d3r         //")
    print(colorama.Fore.CYAN + "//                                               //")
    print(colorama.Fore.CYAN + "///////////////////////////////////////////////////")




def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    menu_height = 3
    menu_window = curses.newwin(menu_height, curses.COLS, curses.LINES - menu_height,0)
    menu_window.border()
    
    menu_window.addstr(1, 2, "Ctrl + q: Quit")
    menu_window.addstr(1, 12, "Ctrl + C: Clear Context")
    menu_window.refresh()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_CTRL_Q:
            break
        elif c == curses.KEY_CTRL_C:
           promptcx = " "
           pass



####################################################################################
#                 AREA OF CODE START : 
####################################################################################


displaybanner()
while True:
    
    
    now = datetime.datetime.now()
    file_name = f'{now.year}-{now.month}-{now.day}_{now.hour}{now.minute}{now.second}.okpt'
    audiofilename = gen_random_string(10)
    storedir = "G:/"
    store_path = os.path.join(storedir,file_name)
    charCount = str(len(promptcx))
    wordCount = str(len(promptcx.split()))


    reply = input(colorama.Fore.RED + "\n Menu - (q) quite | (cx) Clear Context \n Set System Prompt - (sc) \n Status:("+charCount+"/"+str(tokens)+"CR - "+wordCount+" Word )\n\n "+colorama.Fore.YELLOW+"Ask K-Brain : $ ")
     
    if len(promptcx) > 3500:
       promptcx = " "   

    if reply.lower() == 'sc':
        print("Set System Prompt Context:")
        systemcontext = input("Type Here:")
   
    if reply.lower() == 'q':
       print("Exiting Thanks for Using K-Brain")
       break

    if reply.lower() == 'cx':
      promptcx = " "
      print("Context Area Cleared << ")

    else: 
      answer = gpt3(promptcx+reply)

      print(colorama.Fore.BLUE + "[Human(Question)] :____________________________________________ " )
      print(colorama.Fore.GREEN + "")
      print(reply)
      print(colorama.Fore.GREEN + "")


   # UNCOMMENT TO SEE THE FULL Responses
   #  - Debugging Perposes. 
      # print(answer)  
   
      # dataanswer = answer
      # choices = dataanswer["choices"]
      # choice = choices[0]
      # answertext = choice["text"]
      promptcx += answer
      
      phpcode = pygments.highlight(answer, PhpLexer(), TerminalFormatter())
      
      print(colorama.Fore.MAGENTA + "____________________________________________________: [ (Reply) K-Brain ]" )
      print(colorama.Fore.WHITE + "")
   
   # This Loop Creates the Effect of Typing 
   # it will type the output from GPT3
      for char in  phpcode:
        print(char, end="", flush=True)
        time.sleep(0.07276)
        #time.sleep(random.uniform(0.05,0.2))

      print(colorama.Fore.WHITE + "")
      with open(store_path,'w') as f:
        f.write(str(phpcode))


   #Converting the Output to Speech 
      text_to_speech(answer,audiofilename)



#curses.wrapper(main)
