import streamlit as st
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import random

# Function to scrape text data from a website
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

# Function to preprocess text data
def preprocess_text(text):
    sentences = sent_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    preprocessed_sentences = []
    for sentence in sentences:
        sentence = re.sub(r'[^a-zA-Z]', ' ', sentence).lower()
        words = sentence.split()
        words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words('english')]
        preprocessed_sentence = ' '.join(words)
        preprocessed_sentences.append(preprocessed_sentence)
    return preprocessed_sentences

# Function to generate response based on user input
def generate_response(question):
    # List of URLs to scrape
    urls = [
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Artificial_intelligence',
        'https://en.wikipedia.org/wiki/Machine_learning'
    ]

    # Dictionary to store scraped data
    scraped_data = {}

    # Scrape data from each website
    for url in urls:
        try:
            text = scrape_website(url)
            scraped_data[url] = text
            print(f"Scraped data from {url}")
        except Exception as e:
            print(f"Error scraping data from {url}: {str(e)}")

    # Combine scraped text data from all websites
    combined_text = ' '.join(scraped_data.values())

    # Preprocess the combined text
    preprocessed_sentences = preprocess_text(combined_text)

    # Generate response based on user input
    for sentence in preprocessed_sentences:
        if question in sentence:
            return sentence

    # If no matching sentence found, provide a generic response
    return "I'm sorry, I don't have an answer to that question at the moment."

# Streamlit web application
def main():
    st.title("Chatbot")
    st.write("Ask me anything!")

    # User input text box
    user_input = st.text_input("You:", "")

    if st.button("Ask"):
        # Generate response based on user input
        response = generate_response(user_input)
        # Display response
        st.text_area("Chatbot:", response)

if __name__ == "__main__":
    main()
