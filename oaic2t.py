import os
import time
import random
import datetime
import json
import curses
import openai
import colorama
import pygments
from pygments.lexers import PhpLexer
from pygments.formatters import TerminalFormatter

# Initializing Colorama
colorama.init()
promptcx = "a"
tokens = 2000

def gpt3(ask):
    openai.api_key = ""
    global promptcx
    promptcx += ask
    response = openai.Completion.create(

    # Uncomment the Mode to Use.
    #######################################
    model ="text-davinci-003",
    #model = "gpt-3.5-turbo",
    prompt= promptcx,
    temperature=0.4,
    max_tokens=tokens,
    top_p=1,
    best_of=2,
    frequency_penalty=0,
    presence_penalty=0
    )

    content = response.choices[0].text.split('.')
    #print(content)

    return response

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


displaybanner()
while True:
    #key = input(colorama.Fore.RED + 'Continue(C) / Quit(Q) $ ')
    #curses.wrapper(main)
    #if key.lower() == 'q':
    #   break
    
    now = datetime.datetime.now()
    file_name = f'{now.year}-{now.month}-{now.day}_{now.hour}{now.minute}{now.second}.okpt'
    storedir = '/home/esu/myscripts/okpt_outputs/'
    store_path = os.path.join(storedir,file_name)
    charCount = str(len(promptcx))
    wordCount = str(len(promptcx.split()))


    reply = input(colorama.Fore.RED + "\n Menu - (q) quite | (cx) Clear Context \n Status:("+charCount+"/"+str(tokens)+"CR - "+wordCount+" Word )\n\n "+colorama.Fore.YELLOW+"Ask K-Brain : $ ")
     
    if len(promptcx) > 3500:
       promptcx = " "   
   
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
   # print(answer)
      dataanswer = answer
      choices = dataanswer["choices"]
      choice = choices[0]
      answertext = choice["text"]
      promptcx += answertext
      phpcode = pygments.highlight(answertext, PhpLexer(), TerminalFormatter())
      print(colorama.Fore.MAGENTA + "____________________________________________________: [ (Reply) K-Brain ]" )
      print(colorama.Fore.WHITE + "")
   
   # This Loop Creates the Effect of Typing 
   # it will type the output from GPT3
      for char in  phpcode:
        print(char, end="", flush=True)
        time.sleep(0.04876)
        #time.sleep(random.uniform(0.05,0.2))

      print(colorama.Fore.WHITE + "")
      with open(store_path,'w') as f:
        f.write(str(phpcode))


#curses.wrapper(main)
