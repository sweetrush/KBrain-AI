import streamlit as st

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

strdp("**SweetRush Coder** is the Developer of this AI assistance", "2")
strdp("**Github:** [Check out his Github](https://github.com/sweetrush)", "2")
strdp("**Youtube:** [Check out his Youtube](https://youtube.com/@phontric?si=3XPBeam0WfPxL4pY)", "2")
cl1.image("https://yt3.ggpht.com/ytc/AIdro_lKLTe_g4SRSW8drvCTx5ychkb_vXDRWdMr-4ic7ML6A6s=s600-c-k-c0x00ffffff-no-rj-rp-mo", caption=None, width=None)

