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

st.header("Miah's AI Assistance - Help and Guidance")