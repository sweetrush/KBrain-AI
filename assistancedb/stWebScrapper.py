import requests
from bs4 import BeautifulSoup
import streamlit as st

def extract_text_from_url(url):
    """Fetches content from a URL and extracts text.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The extracted text content, or an error message if unsuccessful.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text while removing script and style tags
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(strip=True)
        return text
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"

# Streamlit UI
st.title("Web Page Text Extractor")
url = st.text_input("Enter the URL to scrape:")

if url:
    extracted_text = extract_text_from_url(url)
    st.text("Extracted Text:")
    st.write(extracted_text)