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
st.subheader("Web Scraper for all Web Scraping Functionalites")

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

    # If the Website has www in the start instead of domain name
    if domain_name == 'www':
        domain_name = domain_name = parsed_url.netloc.split('.')[1]

    st.write("Domain Name:", domain_name.capitalize())

except:
    st.write("Please Give Valid URL")


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

    except:
        # If utitlity is embedded links or main website data we will notify the user about the failure
        if utility == "Embedded Links" or utility == 'Main Website Text Data' :
            st.write(f"Connection to {link} cannot be established. Try with another Website")

        # Else we will just pass or do nothing as we will use this function later in recursion and we do not need to
        # Notify user about each embedded website failure
        else:
            pass

# Scraping Text data from Website and rendering in a text file
def save_to_file(text, fname):

    if text is not None:
        st.download_button(
        label="Download Text File",
        data='\n'.join(text),
        file_name=fname,
        key="download_button",
        )
    else:
        st.write("Website has No Data!!")

# Function for Printing Data Scraped
def button_Print(text,statement):

    if text is not None:
        # Button for user to see data scraped without downloading
        # Create a button, that when clicked, shows a text
        if (st.button(statement)):
            st.write(text)

# Defining Functions of Web Scraping

# Function 1
# Gettting Embedded Links from a Website
def embedded_links(link):
    try:

        # For Pdf Link
        if link.endswith('pdf'):
            st.write("This is a PDF File.")

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith('svg') or link.endswith(
            'webp'):
            st.write("This is an Image File.")

        else:
            # Establishing COnnection
            soup = establish_Connection(link)

            # Find all the links on the webpage
            links = soup.find_all('a')

            if links is not None:
                # To Store Embedded link
                embed_link = []

                # Iterating through the links
                for link in links:
                    # Creating an object and storing links
                    href = link.get('href')

                    # To ensure we are scraping the link
                    if href is not None and not href.startswith("#"):
                        # Writing links to text file
                        embed_link.append(href)

                # Option to download the text file
                if embed_link is not None and embed_link != []:
                    if utility == 'Embedded Links':
                        fname = domain_name.capitalize() + "_Embedded_links_Website.txt"
                        save_to_file(embed_link, fname)

                        # Button for the user to see data scraped without downloading
                        # Create a button, that when clicked, shows text
                        button_Print(embed_link, "See Embedded Links")
                    else:
                        return embed_link

                else:
                    if utility == 'Embedded Links':
                        st.write("Website Has No Embedded Links!!")
                    return ""
            else:
                if utility == 'Embedded Links':
                    st.write("Website Has No Embedded Links!!")

    except:
        st.write("Website Has No Embedded Links!!")


# Adding Variables for Visited Links so that we do not visit them again while scraping
visited_links = []

# Function 2
# Gettting Main Website Text Data
def main_website_text_Data(link):

    global visited_links

    try:

        # For Pdf Link
        if link.endswith('pdf'):
            st.write("This is a PDF File.")

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        else:
            if link not in visited_links:
                soup = establish_Connection(link)

                # Extract all the text from the webpage
                text = soup.get_text()

                # Option to download the text file
                if text is not None:

                    if utility == 'Main Website Text Data':
                        fname = domain_name.capitalize() + "_Main_Website_Data.txt"
                        save_to_file(text, fname)

                        button_Print(text, "See Scraped Data")

                    else:
                        return text

                elif utility == 'Main Website Text Data':
                    st.write("Website Has No Data!!")
                    return ""

                else:
                    return ""

                visited_links.append(link)
            else:
                return ""

    except:
        visited_links.append(link)
        if utility == 'Main Website Text Data':
            st.write("Website does not have any Text Data!!")
        return ""


# Function 3
# Function for Getting Main Website Data along with Embedded Links Data
def main_website_text_embedded_link_text_Data(link):
    global visited_links
    web_text = []

    try:
        # For Pdf Link
        if link.endswith('pdf'):
            st.write("This is a PDF File.")

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        else:
            if link not in visited_links:
                # Adding Main website data
                web_text += main_website_text_Data(link)

                # Here we will directly use our functions instead of rewriting codes
                link = embedded_links(link)

                if link is not None:
                    for l in link:
                        web_text.append(main_website_text_Data(l))

                if web_text is not None and web_text != [""]:
                    if utility == 'Main Website Text Data along with Embedded Links Text Data':
                        fname = domain_name.capitalize() + "_Main_Website_Text_Data_Embedded_Links_Text_Data.txt"
                        save_to_file(web_text, fname)

                        # Button for the user to see data scraped without downloading
                        # Create a button that, when clicked, shows text
                        button_Print(web_text, "See Scraped Data")
                    else:
                        return web_text
                else:
                    st.write("Website has no Data!!")
                    return ""
            else:
                return ""

    except:
        visited_links.append(link)
        return ""


# Function 4
# Function for Getting Complete Website Data along with Embedded Links Data
# This also Fetches Data of Links embedded within the embedded links
def complete_text_data(link):
    try:
        # For Pdf Link
        if link.endswith('pdf'):
            st.write("This is a PDF File.")

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        else:
            complete_text = []

            main_website_text_Data(link)
            visited_links.append(link)

            links = embedded_links(link)

            if links is not None:
                for l in links:
                    complete_text.append(main_website_text_embedded_link_text_Data(l))

            if complete_text is not None:
                if utility == 'Complete Website Text Data':
                    fname = domain_name.capitalize() + "_Complete_Website_Text_Data.txt"
                    save_to_file(complete_text, fname)
                    button_Print(complete_text, "See Scraped Data")
                else:
                    return ""

            else:
                st.write("Website has no Text Data!!")
                return ""

    except:
        st.write("An error occurred or the website has no data!!")
        return ""

# Function for Extracting Text from PDF File
# It will only extract english text not able to extract hindi text
def extract_text_from_pdf(url):

    global visited_links

    try:
        if url not in visited_links:

            if url.startswith("../../"):
                url = url.replace("../../", 'https://csvtu.ac.in/ew/')
            url = url.replace(' ', '%20')
            response = requests.get(url, stream=True)

            pdf_content = BytesIO(response.content)

            text = ""
            pdf_reader = PyPDF2.PdfReader(pdf_content)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            if text is not None:
                return text

        visited_links.append(url)
        return ""

    except:
        visited_links.append(url)
        return ""


# Function 5
# For Gettting Main Website PDF File Data
def main_website_PDF_data(link):

    try:

        pdf_Data = []

        if link.endswith('pdf'):
            pdf_Data.append(extract_text_from_pdf(link))

            if pdf_Data is not None and pdf_Data != [""]:
                fname = domain_name.capitalize() + "_Main_Website_PDF_Data.txt"
                save_to_file(pdf_Data, fname)
                button_Print(pdf_Data, "See Scraped Data")

            else:
                st.write("PDF File has no Data or it is Unreadable.")

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                    'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        else:
            st.write("Website has No PDF File.")

    except:
        st.write("Website has no PDF Files Data.")



# Function 6
# For Gettting Main Website PDF File Data along with embedded PDF File Data
def main_website_PDF_embedded_link_PDF_Data(link):

    global visited_links
    pdf_Data = []

    try:
        if link.endswith('pdf'):
            pdf_Data.append(extract_text_from_pdf(link))
            visited_links.append(link)

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        else:
            links = embedded_links(link)

            if links is not None:

                for l in links:
                    pdf_Data.append(extract_text_from_pdf(l))

        if pdf_Data is not None and pdf_Data != [""]:

            if utility == "Main Website PDF Data along with Embedded Links PDF Data":

                fname = domain_name.capitalize() + "_Main_Website_PDF_Data_Embedded_Links_PDF_Data.txt"
                save_to_file(pdf_Data,fname)

                button_Print(pdf_Data, "See Scraped Data")

            else:
                return pdf_Data

        else:
            if utility == "Main Website PDF Data along with Embedded Links PDF Data":
                st.write("PDF File has no Data or it is Unreadable.")
            return ""


    except:
        st.write("Website has no PDF Files Data.")

# Function 7
# Function for Getting Complete Website PDF Data along with Embedded Links Data
# This also Fetches Data of Links embedded within the embedded links
def complete_PDF_data(link):
    try:
        complete_text = []

        if link.endswith('pdf'):
            extract_text_from_pdf(link)
            visited_links.append(link)

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        else:
            links = embedded_links(link)

            if links is not None:
                for l in links:
                    complete_text.append(main_website_PDF_embedded_link_PDF_Data(l))

        if complete_text is not None and complete_text != ['']:

            if utility == 'Complete Website PDF Data':
                fname = domain_name.capitalize() + "_Complete_Website_PDF_Data.txt"
                save_to_file(complete_text, fname)
                button_Print(complete_text, "See Scraped Data")
            else:
                return complete_text

        else:
            st.write("PDF File has no Data or it is Unreadable.")
            return ""

    except:
        st.write("An error occurred or the website has no data!!")
        return ""

# Function 8
# Function for Getting Complete Website Text and PDF Data along with Embedded Links Data
# This also Fetches Text and PDF Data of Links embedded within the embedded links
def complete_text_pdf_Data(link):

    try:
        complete_text = []

        if link.endswith('pdf'):
            extract_text_from_pdf(link)
            visited_links.append(link)

            # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        else:
            complete_text.append(complete_text_data(link))
            complete_text.append(complete_PDF_data(link))

        if complete_text is not None:
            fname = domain_name.capitalize() + "_Complete_Website_Text_PDF_Data.txt"
            save_to_file(complete_text, fname)
            button_Print(complete_text, "See Scraped Data")

        else:
            st.write("Website has no Text and PDF Data!!")

    except:
        st.write("An error occurred or the website has no data!!")

# Function for downloading PDF
def download_PDF(link, name):

    try:
        response = requests.get(link)

        temp = name

        with open(temp, 'wb') as f:
            f.write(response.content)

        with zipfile.ZipFile('Zip_File_PDF.zip', 'a') as zipf:
            zipf.write(temp)
    except:
        pass

# Button to Download Zip File which contains PDF Downloaded
def download_button_PDF():

    try:
        with open('Zip_File_PDF.zip', 'rb') as f:
            st.download_button('Download ZIP', f,
                               file_name=domain_name.capitalize() + '_Zip_File_PDF.zip',
                               mime='application/zip')


    except:
        st.write("Website has no PDF Files.")

# Function 9
# Function for Getting Main Website PDF Data along with Embedded Links PDF Data
def main_download_PDF_Files(link):

    try:
        if link.endswith('pdf'):
            if link.startswith("../../"):
                link = link.replace("../../", 'https://csvtu.ac.in/ew/')
            name = link.split('/')[-1]
            name = name.replace(" ", "_")
            link = link.replace(' ', '%20')
            download_PDF(link, name)

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        else:
            embed_link = []
            embed_link = embedded_links(link)
            if embed_link is not None and embed_link != []:
                for l in embed_link:
                    if l.endswith('pdf'):
                        if l.startswith("../../"):
                            l = l.replace("../../", 'https://csvtu.ac.in/ew/')
                        l = l.replace(' ', '%20')
                        name = l.split('/')[-1]
                        download_PDF(l, name)

    except:
        st.write("An Error Occured or Website has no PDF Files.")

# Function 10
# Function for Downloading Complete Website PDF Data along with Embedded Links Data
# This also Fetches PDF Data of Links embedded within the embedded links
def complete_download_PDF_Files(link):

    try:
        global visited_links

        if link.endswith('pdf') and link not in visited_links:
            if link.startswith("../../"):
                link = link.replace("../../", 'https://csvtu.ac.in/ew/')
            name = link.split('/')[-1]
            name = name.replace(" ", "_")
            link = link.replace(' ', '%20')
            download_PDF(link, name)
            visited_links.append(link)

        # For Image Link
        elif link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp'):
            st.write("This is an Image File.")

        elif link not in visited_links and not link.endswith('pdf'):
            embed_link = embedded_links(link)

            if embed_link is not None:
                for l in embed_link:
                    if l.endswith('pdf'):
                        if l.startswith("../../"):
                            l = l.replace("../../", 'https://csvtu.ac.in/ew/')
                        l = l.replace(' ', '%20')
                        name = l.split('/')[-1]
                        name = name.replace(" ", "_")
                        download_PDF(l, name)
                        visited_links.append(l)
                    else:
                        download_PDF_Files(l)

        else:
            pass

    except:
        st.write("An Error Occured or Website has no PDF Files.")

# Function for downloading Image
def download_Image(link, name):

    try:
        response = requests.get(link)

        with open(name , 'wb') as f:
            f.write(response.content)

        with zipfile.ZipFile('Zip_File_Image.zip', 'a') as zipf:
            zipf.write(name)


    except:
        pass

# Button to Download Zip File which contains Images Downloaded
def download_button_Image():

    try:
        with open('Zip_File_Image.zip', 'rb') as f:
            st.download_button('Download ZIP', f,
                               file_name=domain_name.capitalize() + '_Zip_File_Image.zip',
                               mime='application/zip')

    except:
        st.write("Website has No Image Files.")

# Function 11
# Function for Getting Main Website Image Data along with Embedded Links Image Data
def main_download_Image_Files(link):

    try:
        if link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith(
                'webp'):
            name = link.split('/')[-1]
            name = name.replace(" ", "_")
            link = link.replace(' ', '%20')
            download_Image(link, name)

        # For Pdf Link
        elif link.endswith('pdf'):
            st.write("This is a PDF File.")

        else:

            soup = establish_Connection(link)

            if soup is not None:
                # Find all the links on the webpage
                links = soup.find_all('img')

                # To Store Embedded link
                embed_link = []

                if links is not None:
                    # Iterating through the links
                    for link in links:
                        # Creating an object and storing links
                        src = link.get('src')

                        # To ensure we are scraping the link
                        if src is not None and not src.startswith("#"):
                            # Writing links to text file
                            embed_link.append(src)

                    if embed_link is not None and embed_link != []:
                        for l in embed_link:
                            if l.endswith('jpeg') or l.endswith('jpg') or l.endswith('png') or l.endswith(
                                    'svg') or l.endswith(
                                'webp'):
                                name = l.split('/')[-1]
                                name = name.replace(" ", "_")
                                l = l.replace(' ', '%20')
                                download_Image(l, name)
    except:
        st.write("An Error Occured or Website has no Image Files.")

# Function 12
# Function for Downloading Complete Website Image Data along with Embedded Links Data
# This also Fetches Image Data of Links embedded within the embedded links
def complete_download_Image_Files(link):

    try:
        global visited_links

        if (link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp')) and link not in visited_links:
            name = link.split('/')[-1]
            name = name.replace(" ", "_")
            link = link.replace(' ', '%20')
            download_Image(link, name)

        # For Pdf Link
        elif link.endswith('pdf'):
            st.write("This is a PDF File.")

        elif link not in visited_links and not (
                link.endswith('jpeg') or link.endswith('jpg') or link.endswith('png') or link.endswith(
                'svg') or link.endswith('webp')):

            soup = establish_Connection(link)

            if soup is not None:
                # Find all the links on the webpage
                links = soup.find_all('img')

                if links is not None:
                    # To Store Embedded link
                    embed_link = []

                    # Iterating through the links
                    for link in links:
                        # Creating an object and storing links
                        src = link.get('src')

                        # To ensure we are scraping the link
                        if src is not None and not src.startswith("#"):
                            # Writing links to text file
                            embed_link.append(src)

                if embed_link is not None and embed_link != [""]:
                    for l in embed_link:
                        if l.endswith('jpeg') or l.endswith('jpg') or l.endswith('png') or l.endswith(
                                'svg') or l.endswith('webp'):

                            name = l.split('/')[-1]
                            name = name.replace(" ", "_")
                            l = l.replace(' ', '%20')
                            download_Image(l, name)
                        else:
                            download_Image_Files(l)
        else:
            pass
    except:
        st.write("An Error Occured or Website has No Image Files.")


# First argument takes the title of the Selection Box
# Second argument takes options
utility = st.selectbox("Utility: ",
                     ['Embedded Links', 'Main Website Text Data',
                      'Main Website Text Data along with Embedded Links Text Data',
                      'Complete Website Text Data', 'Main Website PDF Files Data',
                      'Main Website PDF Data along with Embedded Links PDF Data',
                      'Complete Website PDF Data', 'Complete Website Text and PDF Data',
                      'Download PDF Files From Main Website','Download All PDF Files From Website',
                      'Download Image Files From Main Website','Download All Image Files From Website'])

# Selecting Function according to utility
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
