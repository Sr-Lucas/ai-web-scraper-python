import streamlit as st
from parse import parse_with_ollama
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content

st.title("AI Web Scraper")
url = st.text_input("Enter a website URL: ")

scraped = False

if st.button("Scrape Site"):
  scraped = False

  st.write("Scraping the website: ")
  st.write(url)
  
  result = scrape_website(url)
  body_content = extract_body_content(result)
  cleaned_body_content = clean_body_content(body_content)

  st.session_state.dom_content = cleaned_body_content

  scraped = True

if scraped:
 with st.expander("View DOM Content"):
    st.text_area("DOM Content", st.session_state.dom_content, height=300)

if "dom_content" in st.session_state:
  parse_description = st.text_area("Describe what you want from the text:")
  
  if st.button("Parse Content"):
    if parse_description:
      st.write("Processing...")

      dom_chunks = split_dom_content(st.session_state.dom_content)
      result = parse_with_ollama(dom_chunks, parse_description)

      st.write(result)
