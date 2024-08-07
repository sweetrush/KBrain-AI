# Comment when deploying on Heroku 
# -------------------------------------------

# mkdir -p ~/.streamlit/
# mkdir -p ~/output/
# mkdir -p ~/output/gemini_out
# mkdir -p ~/ai_audio

# Uncomment for Deploying for Render 
# -------------------------------------------

mkdir -p ~/.streamlit/
mkdir -p output/
mkdir -p output/gemini_out
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

" > ~/.streamlit/config.toml