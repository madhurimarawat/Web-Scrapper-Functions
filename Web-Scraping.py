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

# For Parsing and Joining Links
from urllib.parse import urlparse, urljoin

# For Rendering in Zip File
import zipfile

# Importing os module to get size of zip file and limit it so that it stops after a certain limit is reached
import os

# Consistent Zipfile Naming
ZIP_PDF_FILENAME = "Zip_File_PDF.zip"
ZIP_IMAGE_FILENAME = "Zip_File_Image.zip"

# Adding Variables for Visited Links so that we do not visit them again while scraping
# Initialize visited_links in session state
visited_links = []

# Set a maximum size for the zip file in bytes
MAX_ZIP_FILE_SIZE = 1024 * 1024 * 100  # 100 MB


# Send an HTTP request to the URL of the webpage we want to access
# Defining Function for Requesting Access to link/Establishing Connection
def establish_Connection(link):
    try:
        # Connecting to Website
        r = requests.get(link)
        # Create a BeautifulSoup object and parse the HTML content
        # lxml is capable of parsing both HTML and XML Content
        soup = BeautifulSoup(r.content, "lxml")
        # Returning Soup object to use it later
        return soup

    except:
        # If utitlity is embedded links or main website data we will notify the user about the failure
        if utility == "Embedded Links" or utility == "Main Website Text Data":
            st.write(
                f"Connection to {link} cannot be established. Try with another Website"
            )

        # Else we will just pass or do nothing as we will use this function later in recursion and we do not need to
        # Notify user about each embedded website failure
        else:
            pass


# Scraping Text data from Website and rendering in a text file
def save_to_file(text, fname):
    if text:
        if isinstance(text, list):
            data = "\n".join(text)
        else:
            data = text
        st.download_button(
            label="Download Text File",
            data=data,
            file_name=fname,
            key=f"download_button_{fname}",  # Unique key for each download button
        )
    else:
        st.write("Website has No Data!!")


# Function for Printing Data Scraped
def button_Print(text, statement):
    if text is not None:
        # Button for user to see data scraped without downloading
        # Create a button, that when clicked, shows a text
        if st.button(statement):
            st.write(text)


# Function for Link Checking
def link_Check(link):
    link_lower = (
        link.lower().split("?")[0].split("#")[0]
    )  # Remove query params and fragments

    # For Pdf Link
    if link_lower.endswith(".pdf"):
        st.write("This is a PDF File.")
        return "pdf"

    # For Image Link
    elif any(
        link_lower.endswith(ext) for ext in [".jpeg", ".jpg", ".png", ".svg", ".webp"]
    ):
        st.write("This is an Image File.")
        return "img"

    # For Normal Link
    else:
        return 1


# Defining Functions of Web Scraping


# Function 1
# Getting Embedded Links from a Website
def embedded_links(link):
    try:
        if link_Check(link) == 1:
            soup = establish_Connection(link)
            if not soup:
                return []
            links = soup.find_all("a")

            if links:
                embed_link = set()
                for link_tag in links:
                    href = link_tag.get("href")
                    if href and not href.startswith("#"):
                        absolute_link = urljoin(link, href)
                        embed_link.add(absolute_link)

                if embed_link:
                    embed_link = list(embed_link)
                    if utility == "Embedded Links":
                        fname = f"{domain_name.capitalize()}_Embedded_links_Website.txt"
                        save_to_file(embed_link, fname)
                        button_Print(embed_link, "See Embedded Links")
                    else:
                        return embed_link
                else:
                    if utility == "Embedded Links":
                        st.write("Website Has No Embedded Links!!")
                    return []
            else:
                if utility == "Embedded Links":
                    st.write("Website Has No Embedded Links!!")
                return []
        else:
            if utility == "Embedded Links":
                st.write("Provided link is not a normal webpage link.")
            return []
    except Exception as e:
        st.write(f"Error in embedded_links: {e}")
        return []


# Function 2
# Getting Main Website Text Data
def main_website_text_Data(link):
    global visited_links

    try:

        # For Pdf and Image Link Checking
        if link_Check(link) == 1:

            if link not in visited_links:
                soup = establish_Connection(link)

                # Extract all the text from the webpage
                web_text = soup.get_text()

                # Option to download the text file
                if web_text is not None:

                    if utility == "Main Website Text Data":
                        fname = domain_name.capitalize() + "_Main_Website_Data.txt"
                        save_to_file(web_text, fname)

                        button_Print(web_text, "See Scraped Data")

                    else:
                        return web_text

                elif utility == "Main Website Text Data":
                    st.write("Website Has No Data!!")
                    return ""

                else:
                    return ""

                visited_links.append(link)
            else:
                return ""

    except:
        visited_links.append(link)
        if utility == "Main Website Text Data":
            st.write("Website does not have any Text Data!!")
        return ""


# Function 3
# Function for Getting Main Website Data along with Embedded Links Data
def main_website_text_embedded_link_text_Data(link):
    global visited_links
    web_text = []

    try:

        # For Pdf and Image Link Checking
        if link_Check(link) == 1:

            if link not in visited_links:
                # Adding Main website data
                web_text += main_website_text_Data(link)

                # Here we will directly use our functions instead of rewriting codes
                link = embedded_links(link)

                if link is not None:
                    for l in link:
                        web_text.append(main_website_text_Data(l))

                if web_text is not None and web_text != [""]:
                    if (
                        utility
                        == "Main Website Text Data along with Embedded Links Text Data"
                    ):
                        fname = (
                            domain_name.capitalize()
                            + "_Main_Website_Text_Data_Embedded_Links_Text_Data.txt"
                        )
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

        # For Pdf and Image Link Checking
        if link_Check(link) == 1:

            complete_text = []

            main_website_text_Data(link)
            visited_links.append(link)

            links = embedded_links(link)

            if links is not None:
                for l in links:
                    complete_text.append(main_website_text_embedded_link_text_Data(l))

            if complete_text is not None:
                if utility == "Complete Website Text Data":
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
    try:
        if url not in visited_links:
            absolute_url = urljoin(link, url)
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(absolute_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Validate PDF by checking Content-Type
            if (
                "application/pdf"
                not in response.headers.get("Content-Type", "").lower()
            ):
                st.write(f"URL does not point to a PDF file: {absolute_url}")
                visited_links.append(url)
                return ""

            pdf_content = BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_content)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            visited_links.append(url)
            return text

    except Exception as e:
        st.write(f"Error extracting text from PDF ({url}): {e}")
        visited_links.append(url)
        return ""


# Function 5
# For Gettting Text From PDF Link
def PDF_link_data(link):
    try:

        pdf_Data = []

        # Storing Type of link
        link_type = link_Check(link)

        # For Pdf and Image Link Checking
        if link_type == "pdf":

            pdf_Data.append(extract_text_from_pdf(link))

            if pdf_Data is not None and pdf_Data != [""]:
                fname = domain_name.capitalize() + "_Link_PDF_Data.txt"
                save_to_file(pdf_Data, fname)
                button_Print(pdf_Data, "See Scraped Data")

            else:
                st.write("PDF File has no Data or it is Unreadable.")

        # For Image Link we will not do anything as it will already print that it is a image file
        elif link_type == "img":
            pass

        else:
            st.write("PDF is Unreadable or Link has no PDF File..")

    except:
        st.write("PDF is Unreadable or Link has no PDF File.")


# Function 6
# For Gettting Main Website PDF File Data along with embedded PDF File Data
def main_website_PDF_embedded_link_PDF_Data(link):
    global visited_links
    pdf_Data = []

    try:
        # For Pdf and Image Link Checking
        if link_Check(link) == 1:

            links = embedded_links(link)

            if links is not None:

                for l in links:
                    pdf_Data.append(extract_text_from_pdf(l))

        if pdf_Data is not None and pdf_Data != [""]:

            if utility == "Main Website PDF Data along with Embedded Links PDF Data":

                fname = (
                    domain_name.capitalize()
                    + "_Main_Website_PDF_Data_Embedded_Links_PDF_Data.txt"
                )
                save_to_file(pdf_Data, fname)

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

        # For Pdf and Image Link Checking
        if link_Check(link) == 1:

            links = embedded_links(link)

            if links is not None:
                for l in links:
                    complete_text.append(main_website_PDF_embedded_link_PDF_Data(l))

        if complete_text is not None and complete_text != [""]:

            if utility == "Complete Website PDF Data":
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

        # For Pdf and Image Link Checking
        if link_Check(link) == 1:
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
def download_PDF(link, name, zip_filename):
    try:
        st.write(f"Attempting to download PDF: {link}")
        response = requests.get(link)
        temp = name

        # Save the PDF temporarily
        with open(temp, "wb") as f:
            f.write(response.content)

        # Check if the ZIP file exists; if not, create it
        if not os.path.exists(zip_filename):
            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                pass  # Create an empty ZIP file

        # Get the current size of the ZIP file
        current_zip_size = os.path.getsize(zip_filename)

        # Check if adding the new PDF exceeds the maximum size
        if current_zip_size + os.path.getsize(temp) <= MAX_ZIP_FILE_SIZE:
            with zipfile.ZipFile(zip_filename, "a") as zip_file:
                zip_file.write(temp, arcname=name)
            st.write(f"Added {name} to {zip_filename}")
        else:
            st.write("Download limit reached. ZIP file is too large.")

        # Optionally, remove the temporary PDF file after adding to ZIP
        os.remove(temp)

    except Exception as e:
        st.write(f"Failed to download PDF: {e}")


# Button to Download Zip File which contains PDF Downloaded
def download_button_PDF():
    try:
        if os.path.exists(ZIP_PDF_FILENAME):
            with open(ZIP_PDF_FILENAME, "rb") as f:
                st.download_button(
                    "Download PDF ZIP",
                    f,
                    file_name=f"{domain_name.capitalize()}_Zip_File_PDF.zip",
                    mime="application/zip",
                )
        else:
            st.write("No PDF files available for download.")
    except Exception as e:
        st.write(f"An error occurred while preparing the ZIP file: {e}")


# Function 9
# Function for Getting Main Website PDF Data along with Embedded Links PDF Data
def main_download_PDF_Files(link):
    try:
        link_type = link_Check(link)

        if link_type == "pdf":
            name = link.split("/")[-1].replace(" ", "_")
            download_PDF(link, name, ZIP_PDF_FILENAME)

        elif link_type == "img":
            pass

        else:
            embed_links = embedded_links(link)
            if embed_links:
                for l in embed_links:
                    if l.lower().endswith(".pdf"):
                        name = l.split("/")[-1].replace(" ", "_")
                        download_PDF(l, name, ZIP_PDF_FILENAME)
    except Exception as e:
        st.write(f"An error occurred while downloading PDFs: {e}")


# Function 10
# Function for Downloading Complete Website PDF Data along with Embedded Links Data
# This also Fetches PDF Data of Links embedded within the embedded links
def complete_download_PDF_Files(link):
    try:
        global visited_links
        link_type = link_Check(link)

        if link_type == "pdf" and link not in visited_links:
            if link.startswith("../../"):
                link = link.replace("../../", "https://")
            name = link.split("/")[-1].replace(" ", "_")
            link = link.replace(" ", "%20")
            download_PDF(link, name, ZIP_PDF_FILENAME)
            visited_links.append(link)

        elif link_type == "img":
            pass

        elif link not in visited_links and not link.endswith("pdf"):
            embed_links = embedded_links(link)
            if embed_links:
                for l in embed_links:
                    if l.endswith("pdf"):
                        if l.startswith("../../"):
                            l = l.replace("../../", "https://")
                        l = l.replace(" ", "%20")
                        name = l.split("/")[-1].replace(" ", "_")
                        download_PDF(l, name, ZIP_PDF_FILENAME)
                        visited_links.append(l)
                    else:
                        main_download_PDF_Files(l)

    except Exception as e:
        st.write(f"An error occurred while downloading all PDFs: {e}")


# Function for downloading Image
def download_Image(link, name):
    try:
        response = requests.get(link)

        # Save image locally first
        with open(name, "wb") as f:
            f.write(response.content)

        # Check the size of the zip file before adding a new image
        if os.path.exists(ZIP_IMAGE_FILENAME):
            current_size = os.path.getsize(ZIP_IMAGE_FILENAME)
        else:
            current_size = 0

        # Only add image if the zip file size is under the limit
        if current_size + os.path.getsize(name) <= MAX_ZIP_FILE_SIZE:
            with zipfile.ZipFile(ZIP_IMAGE_FILENAME, "a") as zip_file:
                zip_file.write(name)

            # Optionally delete the image file after adding it to the zip file
            os.remove(name)
        else:
            print(f"Zip file size limit exceeded ({MAX_ZIP_FILE_SIZE} bytes).")
    except Exception as e:
        print(f"Error downloading image: {e}")


# Button to Download Zip File which contains Images Downloaded
def download_button_Image():
    try:
        with open("Zip_File_Image.zip", "rb") as f:
            st.download_button(
                "Download ZIP",
                f,
                file_name=domain_name.capitalize() + "_Zip_File_Image.zip",
                mime="application/zip",
            )

    except:
        st.write("Website has No Image Files.")


# Function 11
# Function for Getting Main Website Image Data along with Embedded Links Image Data
def main_download_Image_Files(link):
    try:

        link_type = link_Check(link)
        if link_type == "img":
            name = link.split("/")[-1]
            name = name.replace(" ", "_")
            link = link.replace(" ", "%20")
            download_Image(link, name)

        # For Pdf Link it will print message
        elif link_type == "pdf":
            pass

        else:

            soup = establish_Connection(link)

            if soup is not None:
                # Find all the links on the webpage
                links = soup.find_all("img")

                # To Store Embedded link
                embed_link = []

                if links is not None:
                    # Iterating through the links
                    for link in links:
                        # Creating an object and storing links
                        src = link.get("src")

                        # To ensure we are scraping the link
                        if src is not None and not src.startswith("#"):
                            # Writing links to text file
                            embed_link.append(src)

                    if embed_link is not None and embed_link != []:
                        for l in embed_link:
                            if (
                                l.endswith("jpeg")
                                or l.endswith("jpg")
                                or l.endswith("png")
                                or l.endswith("svg")
                                or l.endswith("webp")
                            ):
                                name = l.split("/")[-1]
                                name = name.replace(" ", "_")
                                l = l.replace(" ", "%20")
                                download_Image(l, name)
    except:
        st.write("An Error Occured or Website has no Image Files.")


# Function 12
# Function for Downloading Complete Website Image Data along with Embedded Links Data
# This also Fetches Image Data of Links embedded within the embedded links
def complete_download_Image_Files(link):
    try:
        global visited_links

        link_type = link_Check(link)

        if link_type == "img" and link not in visited_links:
            name = link.split("/")[-1]
            name = name.replace(" ", "_")
            link = link.replace(" ", "%20")
            download_Image(link, name)

        # For Pdf Link it will print message
        elif link_type == "pdf":
            pass

        elif link not in visited_links and not link_type == "img":

            soup = establish_Connection(link)

            if soup is not None:
                # Find all the links on the webpage
                links = soup.find_all("img")

                if links is not None:
                    # To Store Embedded link
                    embed_link = []

                    # Iterating through the links
                    for link in links:
                        # Creating an object and storing links
                        src = link.get("src")

                        # To ensure we are scraping the link
                        if src is not None and not src.startswith("#"):
                            # Writing links to text file
                            embed_link.append(src)

                if embed_link is not None and embed_link != [""]:
                    for l in embed_link:
                        if link_Check(l) == "img":

                            name = l.split("/")[-1]
                            name = name.replace(" ", "_")
                            l = l.replace(" ", "%20")
                            download_Image(l, name)
                        else:
                            main_download_Image_Files(l)
        else:
            pass
    except:
        st.write("An Error Occured or Website has No Image Files.")


# Function to remove files after download button is clicked
def remove_files(fname):
    try:
        os.remove(fname)

    except:
        pass


def user_input():

    # Getting Input from User
    try:
        link = st.text_input("Enter Website Link")

        # Parse the URL
        parsed_url = urlparse(link)

        # Split the domain by dots and get the first part
        # For name after https
        domain_name = parsed_url.netloc.split(".")[0]

        # If the Website has www in the start instead of domain name
        if domain_name == "www":
            domain_name = domain_name = parsed_url.netloc.split(".")[1]

        st.write("Domain Name:", domain_name.capitalize())

        return link

    except:
        st.write("Please Give Valid URL")


# Main Function for Code execution
def main(utility, link):

    # Selecting Function according to utility
    if utility == "Embedded Links":
        embedded_links(link)

    elif utility == "Main Website Text Data":
        main_website_text_Data(link)

    elif utility == "Complete Website Text Data":
        complete_text_data(link)

    elif utility == "Main Website Text Data along with Embedded Links Text Data":
        main_website_text_embedded_link_text_Data(link)

    elif utility == "Extract Text from PDF Link":
        PDF_link_data(link)

    elif utility == "Main Website PDF Data along with Embedded Links PDF Data":
        main_website_PDF_embedded_link_PDF_Data(link)

    elif utility == "Complete Website PDF Data":
        complete_PDF_data(link)

    elif utility == "Complete Website Text and PDF Data":
        complete_text_pdf_Data(link)

    elif utility == "Download PDF Files From Main Website":
        main_download_PDF_Files(link)
        download_button_PDF()
        fname = "Zip_File_PDF.zip"
        remove_files(fname)

    elif utility == "Download All PDF Files From Website":
        complete_download_PDF_Files(link)
        download_button_PDF()
        fname = "Zip_File_PDF.zip"
        remove_files(fname)

    elif utility == "Download Image Files From Main Website":
        main_download_Image_Files(link)
        download_button_Image()
        fname = "Zip_File_Image.zip"
        remove_files(fname)

    else:
        complete_download_Image_Files(link)
        download_button_Image()
        fname = "Zip_File_Image.zip"
        remove_files(fname)

    # For Closing Button
    # Function to handle app closure and file removal
    # Check a condition to close the app

    try:

        if st.button("Close App"):
            st.experimental_clear_cache()

            # Close the app
            st.stop()

    except:
        pass


# Function to include background image and opacity
def display_background_image(url, opacity):
    """
    Displays a background image with a specified opacity on the web app using CSS.

    Args:
    - url (str): URL of the background image.
    - opacity (float): Opacity level of the background image.
    """
    # Set background image using HTML and CSS
    st.markdown(
        f"""
        <style>
            body {{
                background: url('{url}') no-repeat center center fixed;
                background-size: cover;
                opacity: {opacity};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Running the main function
if __name__ == "__main__":

    # Setting the page title
    # This title will only be visible when running the app locally.
    # In the deployed app, the title will be displayed as "Title - Streamlit," where "Title" is the one we provide.
    # If we don't set the title, it will default to "Streamlit"
    st.set_page_config(page_title="Web Scraper")

    # Call function to display the background image with opacity
    display_background_image(
        "https://analyticsdrift.com/wp-content/uploads/2022/12/web-scraping-tools.jpg",
        0.8,
    )

    # Adding Title
    st.title("Web Scraper")

    # Adding Subheader
    st.subheader("Web Scraper for all Web Scraping Functionalities")

    # For writing Text we use text function
    st.text("Enter Website Link and Get all Web Scraping Functions for it.")

    link = user_input()

    # First argument takes the title of the Selection Box
    # Second argument takes options
    utility = st.selectbox(
        "Utility: ",
        [
            "Embedded Links",
            "Main Website Text Data",
            "Main Website Text Data along with Embedded Links Text Data",
            "Complete Website Text Data",
            "Extract Text from PDF Link",
            "Main Website PDF Data along with Embedded Links PDF Data",
            "Complete Website PDF Data",
            "Complete Website Text and PDF Data",
            "Download PDF Files From Main Website",
            "Download All PDF Files From Website",
            "Download Image Files From Main Website",
            "Download All Image Files From Website",
        ],
    )

    # Call main function to run the app
    main(utility, link)
