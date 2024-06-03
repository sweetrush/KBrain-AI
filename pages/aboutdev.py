import streamlit as st
import os

st.markdown(
	        '''
	        <style>
	        MainMenu {
	           visibility : hidden;
	        }
            footer   {
            visibility: hidden;
            }
            header   { visibility: hidden;
            }

            p, li {
		    font-family: "Ubuntu", sans-serif;
			  font-weight: 300;
			  line-height: 1.6;
			  color: rgb(249, 249, 251);
			}
			/*These are the Page Menu Inserted by Streamlit*/
			.st-emotion-cache-10rjk4g{
			  display: none;

			}

			.st-emotion-cache-79elbk{
			  display: none;
			}

			.st-emotion-cache-juxevh{
			  padding-top: 0rem;
			}
	        </style>
	        ''', unsafe_allow_html=True)

emj_help = ' 📗 '
emj_help_ico = '📗'

with st.sidebar:
	st.page_link("Main.py", label="Main", icon=emj_help_ico, disabled=False)
	st.page_link("pages/help.py", label="Help Guide", icon=emj_help_ico, disabled=False)
	st.page_link("pages/aboutdev.py", label="About Dev", icon=emj_help_ico, disabled=False)

# FX Definitions 
def strdp(string, colselect):
	if colselect == "1":
         cl1.markdown(string, unsafe_allow_html=False)
	elif colselect == "2":
	 	 cl2.markdown(string, unsafe_allow_html=False)
	elif colselect == "3":
	 	 cl3.markdown(string, unsafe_allow_html=False)

# 

st.header("Miah's AI Assistance - About the Developer")

cl1, cl2, cl3 = st.columns([1, 4, 1], gap="small")

strdp("**SweetRushCoder(sRC)** is the Developer of this AI assistance", "2")
strdp("**Github:** [Github: https://github.com/sweetrush](https://github.com/sweetrush)", "2")
strdp("**Youtube:** [Check out his Youtube](https://youtube.com/@phontric?si=3XPBeam0WfPxL4pY)", "2")
strdp("**Website:** [Check out his Website](https://suetenaloia.net/)", "2")

devLogo = os.path.join("appImages", "devlogo.png")

cl1.image(devLogo, caption=None, width=None)

clx1, clx2 = st.columns([4, 4], gap="small")

clx1.markdown("#### Dev Technology", unsafe_allow_html=False)
clx1.markdown("- Streamlit : [https://streamlit.io/](https://streamlit.io/)")
clx1.markdown("- Google AI : [https://ai.google.dev/](https://ai.google.dev/)")
clx1.markdown("- Python    : [https://www.python.org/](https://www.python.org/)")
clx1.markdown("- CSS       : [https://developer.mozilla.org/en-US/docs/Web/CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)")
clx1.markdown("- HTML      : [https://html.com/](https://html.com/)")
clx1.markdown("- React-JS  : [https://react.dev/](https://react.dev/)")


clx2.markdown("#### Dev Systems", unsafe_allow_html=False)
clx2.markdown("- LocalDev - Linux         : [https://ubuntu.com/](https://ubuntu.com/)")
clx2.markdown("- Beta Deployment - heroku : [https://www.heroku.com/home](https://www.heroku.com/home)")

clx1.markdown("#### Dev Editor", unsafe_allow_html=False)
clx1.markdown("- Google-Colab   : [https://colab.research.google.com/](https://colab.research.google.com/)")
clx1.markdown("- Sublime Text 4 : [https://www.sublimetext.com/](https://www.sublimetext.com/)")


clx2.markdown("#### Dev Mapper and Designer Editor", unsafe_allow_html=False)
clx2.markdown("- Miro        : [https://miro.com/](https://miro.com/)")
clx2.markdown("- Google Draw : [https://www.heroku.com/home](https://www.heroku.com/home)")


