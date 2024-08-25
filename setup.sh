# Comment when deploying on Heroku 
# -------------------------------------------

# mkdir -p ~/.streamlit/
# mkdir -p ~/output/
# mkdir -p ~/output/gemini_out
# mkdir -p ~/ai_audio

# Uncomment for Deploying for Render 
# -------------------------------------------

# Creating the directors for the program outputs
#
echo "Creating the streamlit Directory "
mkdir -p .streamlit/
echo "Creating the output files directory for outputs"
mkdir -p output/
echo "Creating the Audio Output files "
mkdir -p output/gemini_out
echo "Creating the Ai_audio Files "
mkdir -p ai_audio

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\

[theme]\n\
base=\"dark\"\n\
primaryColor=\"#a5ecaa\"\n\
#backgroundColor=\"#1a1919\"\n\
#secondaryBackgroundColor=\"#5f6164\"\n\
textColor=\"#f9f9fb\"

" > .streamlit/config.toml

