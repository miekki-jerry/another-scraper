import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Set page title and icon
st.set_page_config(page_title="GPT-based Web Scraper", page_icon="🔍")

# Function to perform web scraping
def scrape_website(url, css_class):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all(class_=css_class)
            results = "\n".join([element.text.strip() for element in elements])
            if results:
                st.session_state['scraped_data'] = results
                return results
        else:
            return f"Failed to fetch the website, status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to query GPT with the scraped data
def ask_gpt(scraped_data, user_query):
    client = OpenAI(api_key=st.session_state['api_key'])
    system_message = f"You are a helpful assistant. Given the following scraped data, answer the user's question: {user_query}"
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": scraped_data}
    ]
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response_message = completion.choices[0].message.content
        return response_message
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Initialize session state for storing API key if not already present
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

st.title("Website Scraper and GPT-based Interaction")

# Web scraping UI
url = st.text_input("Enter the URL to scrape:", key="url")
css_class = st.text_input("Enter the CSS class:", key="css_class")
if st.button("Scrape", key="scrape"):
    if url and css_class:
        results = scrape_website(url, css_class)
        if results:
            st.success("Scraping successful!")

# Display scraped data
if 'scraped_data' in st.session_state and st.session_state['scraped_data']:
    st.write("Scraped Data:")
    st.text_area("", value=st.session_state['scraped_data'], height=300, key="scraped_results")

# GPT interaction UI, displayed conditionally
if 'scraped_data' in st.session_state and st.session_state['scraped_data']:
    st.markdown("## And now... ask GPT")
    st.text_input("Enter your OpenAI API key (optional):", type="password", key="api_key")
    question = st.text_area("Ask GPT about the scraped data:", key="question")
    if st.button("Ask GPT"):
        if st.session_state['api_key']:
            answer = ask_gpt(st.session_state['scraped_data'], question)
            if answer:
                # Enhanced text area with copyable output
                st.text_area("GPT's response:", value=answer, height=300, key="gpt_response")
        else:
            st.error("Please provide an OpenAI API key to ask GPT.")
