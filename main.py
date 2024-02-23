# Import necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to perform web scraping
def scrape_website(url, css_class):
    try:
        # Fetch the content of the website
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find elements with the given CSS class
            elements = soup.find_all(class_=css_class)
            # Extract and return the text from each element
            return "\n".join([element.text.strip() for element in elements])
        else:
            return f"Failed to fetch the website, status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI components
st.title("Website Scraper")

# User input for URL
url = st.text_input("Enter the URL to scrape:")

# User input for CSS class
css_class = st.text_input("Enter the CSS class:")

# Button to start the scraping process
if st.button("Scrape"):
    if url and css_class:
        # Call the scrape_website function
        results = scrape_website(url, css_class)
        if results:
            # Display the results in a text area, making it easy to copy
            st.text_area("Scraped values:", value=results, height=300)
        else:
            st.write("No results found.")
    else:
        st.write("Please enter both URL and CSS class.")
