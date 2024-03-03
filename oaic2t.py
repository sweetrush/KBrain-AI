import os
import time
import random
import string
import datetime
import json
import subprocess
import curses
import colorama as clm
import pygments
from playsound           import playsound
from pathlib             import Path
from openai              import OpenAI
from pygments.lexers     import PhpLexer
from pygments.formatters import TerminalFormatter

#  Initiatizing OpenAI
#  Defining the New Code with New OpenAI changes 
client = OpenAI(api_key="")

#  Initializing Colorama
clm.init()
promptcx = "a"
promptFormat = """
               Provide response in Markdown format, And Well Structured Having
               each section in Bold.
               """
systemcontext = """
                As a seasoned Linux aficionado with a particular emphasis on 
                Ubuntu, I possess an encyclopedic knowledge of the Linux 
                operating system, covering every nook and cranny from its core 
                principles to its most intricate details. My expertise spans 
                all major distributions, with a deep specialization in Ubuntu, 
                alongside proficiency in Fedora, CentOS, and Arch Linux. I am 
                well-versed in system administration, adept at managing and 
                optimizing Ubuntu servers for peak performance, and proficient 
                in deploying and maintaining a wide array of network services 
                and protocols on this platform.

                My command over the Linux command line interface (CLI) is 
                second to none, allowing me to navigate the file system, 
                manage processes, and automate tasks with ease using shell 
                scripting, especially within the Ubuntu environment. Security 
                in Linux, with a focus on Ubuntu, is another area where my 
                proficiency shines, encompassing everything from setting up 
                firewalls and intrusion detection systems to implementing 
                access controls and encryption techniques.

                In addition to system-level expertise, I have a strong grasp 
                of software development on Linux platforms, particularly on 
                Ubuntu, including development tools, compilers, and debugging 
                techniques. My experience also extends to containerization and 
                virtualization technologies like Docker and KVM, enabling me to
                architect and manage scalable, isolated environments for 
                application deployment on Ubuntu systems.

                Furthermore, my knowledge is continually updated, as I 
                stay abreast of the latest advancements in the Linux ecosystem,
                including kernel updates, distribution releases, especially 
                Ubuntu updates, and emerging technologies. This comprehensive 
                mastery of Linux, with a deep dive into Ubuntu, empowers me to 
                tackle complex challenges, optimize systems for various needs, 
                and share insights with those eager to learn about the 
                intricacies of this powerful operating system and its most 
                popular distribution.

                """
tokens = 3000


def gpt3(ask):
    global promptcx
    global systemcontext
    promptcx += ask
    response = client.chat.completions.create(

    # Uncomment the Mode to Use.
    #######################################
    # model ="text-davinci-003",
    # model = "gpt-3.5-turbo-1106",
    model = "gpt-4",
    messages= [ 
               {"role": "system", "content": systemcontext},
               {"role": "user","content": promptcx }

               ],
    )

    # content = response.choices[0].text.split('.')   #OLD CODE
    content = response.choices[0].message.content             #New Code 
    # print(content)

    return content


def read_text_with_espeak(text, voice="en-us"):
    try:
        print(clm.Fore.YELLOW+'-----------------------------------------')
        print(clm.Fore.YELLOW+"*** Loading Audio Feed ***")
        print(clm.Fore.YELLOW+'-----------------------------------------')
        subprocess.call(['espeak', '-v', voice, text])
    except OSError:
        print("Error: espeak is not installed or accessible.")


def text_to_speech(text,filename):
    
    audiostore = "KBrain_Audio"
    filestring = "speech_" + filename + ".mp3"

    if not os.path.exists(audiostore):
        os.makedirs(audiostore)

    speech_file_path = Path("KBrain_Audio").parent/filestring
    
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
    print(clm.Fore.CYAN + "///////////////////////////////////////////////////")
    print(clm.Fore.CYAN + "//        Welcome to the K-Brain Prompt          //")
    print(clm.Fore.CYAN + "//            version 1.2                        //")
    print(clm.Fore.CYAN + "//         Developed by: Sw33tRu5h_C0d3r         //")
    print(clm.Fore.CYAN + "//                                               //")
    print(clm.Fore.CYAN + "///////////////////////////////////////////////////")


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
    file_name = f'{now.year}-{now.month}-{now.day}_{now.hour}_{now.minute}_{now.second}.okpt.md'
    audiofilename = gen_random_string(10)
    storedir = "output"
    store_path = os.path.join(storedir,file_name)
    charCount = str(len(promptcx))
    wordCount = str(len(promptcx.split()))

    if not os.path.exists(storedir):
        os.makedirs(storedir)

    reply = input(clm.Fore.RED + "\n Menu - (q) quite | (cx) Clear Context \n "
                                 "Set System Prompt - (sc) \n Status:("
                                 ""+charCount+"/"+str(tokens)+"CR - "
                                 ""+wordCount+" Word )\n\n "
                                 ""+clm.Fore.YELLOW+">>> ")

    print(clm.Fore.GREEN + "\n----> Request Sent\n")
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

      print(clm.Fore.BLUE + "<---- [Human(Question)]" )
      print(clm.Fore.GREEN + "")
      print(reply)
      print(clm.Fore.GREEN + "")

    # UNCOMMENT TO SEE THE FULL Responses
    #  - Debugging Perposes. 
      # print(answer)  
   
      # dataanswer = answer
      # choices = dataanswer["choices"]
      # choice = choices[0]
      # answertext = choice["text"]
      promptcx += answer
      
      phpcode = pygments.highlight(answer, PhpLexer(), TerminalFormatter())
      
      print(clm.Fore.MAGENTA + "----> [ (Reply) K-Brain ]" )
      print(clm.Back.BLACK+clm.Fore.WHITE + "")
   
    # This Loop Creates the Effect of Typing 
    # it will type the output from GPT3

      for char in phpcode:
        print(char, end="", flush=True)
        time.sleep(0.03876)
        # time.sleep(random.uniform(0.05,0.2))
      
      read_text_with_espeak(answer,"en-us")  
      print(clm.Fore.WHITE + "")
      with open(store_path,'w') as f:
        f.write(str("\n\n### QUESTION BY HUMAN ###\n\n"))
        f.write(str(reply))
        f.write(str("\n\n#### MIAH Assistance Reponse ####\n\n"))
        f.write(str(phpcode))

    # Converting the Output to Speech 
    # text_to_speech(answer,audiofilename)
