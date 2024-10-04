import streamlit as st
from scrape import scrape_website, split_dom_content, clear_body_content, extract_body_content
from parse import parse_with_ollama

st.title("AI Web Scraper")

# Initialize session state for 'dom_content'
if 'dom_content' not in st.session_state:
    st.session_state['dom_content'] = None

# Input for website URL
url = st.text_input("Enter Website URL")

# Scrape website button
if st.button("Scrape Website"):
    st.write("Scraping the website...")
    result = scrape_website(url)

    if result:
        st.write("Scraping successful!")
        body_content = extract_body_content(result)
        cleaned_content = clear_body_content(body_content)
        st.session_state.dom_content = cleaned_content  # Save cleaned content in session state
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
    else:
        st.write("Failed to scrape the website.")

# Parsing section only if DOM content is available
if st.session_state['dom_content']:
    parse_description = st.text_area("Describe what you want to parse?", height=100)

    # Parse Content button
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Split DOM content into chunks
            dom_chunk = split_dom_content(st.session_state['dom_content'])

            # Call the parsing function with the Ollama model
            result = parse_with_ollama(dom_chunk, parse_description)

            # Check if the result is valid
            if result:
                st.write("Parsing successful! Here are the results:")
                st.write(result)
            else:
                st.write("No results found. Check your description.")
        else:
            st.write("Please provide a description for parsing.")
else:
    st.write("Please scrape a website first to enable parsing.")
