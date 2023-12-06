# Importing Required Libraries

# For Frontend(Provides Interface) and Deployment
import streamlit as st

# requests is used to get access to the website or in other words connect to the website
import requests

# Beautiful Soup 4 is a Python library that makes it easy to scrape information from web pages.
# It provides Pythonic idioms for iterating, searching, and modifying the parse tree.
# The library sits atop an HTML or XML parser.
from bs4 import BeautifulSoup

# For Reading PDF Files and Manipulation in PDF Files
import PyPDF2

# For Reading PDF Files Bytes by Bytes Instead of Downloading them
from io import BytesIO

# For Rendering in Zip File
import zipfile

# Adding Title
st.title("Web Scraper")

# Adding Subheader
st.subheader("Web Scraper for all Web Scraping Functionalities")

# For writing Text we use text function
st.text("Enter Website Link and Get all Web Scraping Functions for it.")

# Getting Input from User
try:
    link = st.text_input("Enter Website Link")
    from urllib.parse import urlparse

    # Parse the URL
    parsed_url = urlparse(link)

    # Split the domain by dots and get the first part
    # For name after https
    domain_name = parsed_url.netloc.split('.')[0]

    # If the Website has www in the start instead of the domain name
    if domain_name == 'www':
        domain_name = domain_name = parsed_url.netloc.split('.')[1]

    st.write("Domain Name:", domain_name.capitalize())

except:
    st.write("Please Give a Valid URL")

# Send an HTTP request to the URL of the webpage we want to access
# Defining Function for Requesting Access to link/Establishing Connection
def establish_Connection(link):
    try:
        # Connecting to Website
        r = requests.get(link)
        # Create a BeautifulSoup object and parse the HTML content
        # lxml is capable of parsing both HTML and XML Content
        soup = BeautifulSoup(r.content, 'lxml')
        # Returning Soup object to use it later
        return soup

    except Exception as e:
        st.error(f"An error occurred in 'establish_Connection': {e}")

# Scraping Text data from Website and rendering in a text file
def save_to_file(text, fname):
    try:
        if text is not None:
            st.download_button(
            label="Download Text File",
            data='\n'.join(text),
            file_name=fname,
            key="download_button",
            )
        else:
            st.write("Website has No Data!!")

    except Exception as e:
        st.error(f"An error occurred in 'save_to_file': {e}")

# Function for Printing Data Scraped
def button_Print(text, statement):
    try:
        if text is not None:
            # Button for user to see data scraped without downloading
            # Create a button, that when clicked, shows a text
            if (st.button(statement)):
                st.write(text)

    except Exception as e:
        st.error(f"An error occurred in 'button_Print': {e}")

# Defining Functions for Web Scraping

# Function 1
# Getting Embedded Links from a Website
def embedded_links(link):
    try:
        # Existing code

    except Exception as e:
        st.error(f"An error occurred in 'embedded_links': {e}")

# Adding Variables for Visited Links so that we do not visit them again while scraping
visited_links = []

# Function 2
# Getting Main Website Text Data
def main_website_text_Data(link):
    try:
        # Existing code

    except Exception as e:
        st.error(f"An error occurred in 'main_website_text_Data': {e}")

# Function 3
# Function for Getting Main Website Data along with Embedded Links Data
def main_website_text_embedded_link_text_Data(link):
    try:
        # Existing code

    except Exception as e:
        st.error(f"An error occurred in 'main_website_text_embedded_link_text_Data': {e}")

# Function 4
# Function for Getting Complete Website Data along with Embedded Links Data
def complete_text_data(link):
    try:
        # Existing code

    except Exception as e:
        st.error(f"An error occurred in 'complete_text_data': {e}")

# Function 5
# Function for Extracting Text from PDF File
def extract_text_from_pdf(url):
    try:
        # Existing code

    except Exception as e:
        st.error(f"An error occurred in 'extract_text_from_pdf': {e}")

# Function 6
# For Getting Main Website PDF File Data
def main_website_PDF_data(link):
    try:
        # Existing code

    except Exception as e:
        st.error(f"An error occurred in 'main_website_PDF_data': {e}")

# Function 7
# Function for Getting Main Website PDF File Data along with embedded PDF File Data
def main_website_PDF_embedded_link_PDF_Data(link):
    try:
        # Existing code

    except Exception as e:
        st.error(f"An error occurred in 'main_website_PDF_embedded_link_PDF_Data': {e}")

# ... (Rest of the functions)

# Selecting Function according to utility
try:
    if utility == 'Embedded Links':
        embedded_links(link)

    elif utility == 'Main Website Text Data':
        main_website_text_Data(link)

    elif utility == 'Complete Website Text Data':
        complete_text_data(link)

    elif utility == 'Main Website Text Data along with Embedded Links Text Data':
        main_website_text_embedded_link_text_Data(link)

    elif utility == 'Main Website PDF Files Data':
        main_website_PDF_data(link)

    elif utility == 'Main Website PDF Data along with Embedded Links PDF Data':
        main_website_PDF_embedded_link_PDF_Data(link)

    elif utility == 'Complete Website PDF Data':
        complete_PDF_data(link)

    elif utility == 'Complete Website Text and PDF Data':
        complete_text_pdf_Data(link)

    elif utility == 'Download PDF Files From Main Website':
        main_download_PDF_Files(link)
        download_button_PDF()

    elif utility == 'Download All PDF Files From Website':
        complete_download_PDF_Files(link)
        download_button_PDF()

    elif utility == 'Download Image Files From Main Website':
        main_download_Image_Files(link)
        download_button_Image()

    else:
        complete_download_Image_Files(link)
        download_button_Image()

except Exception as e:
    st.error(f"An error occurred in the main execution: {e}")
