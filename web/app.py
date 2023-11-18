import pickle
import streamlit as st
from selenium import webdriver
from ctypes.wintypes import SERVICE_STATUS_HANDLE
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import os

options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)

st.header('Recommendation System')

#CSS Card
css = """
    <style>
    div[data-testid="stHorizontalBlock"] div[role="img"] img {
        width: 300px !important;
        object-fit: contain !important;
    }
    </style>
"""

#CSS title: 
css_title = """
    <style>
    .title-class {
        height: 280px;
        width: 300px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    </style>
"""

st.markdown(css, unsafe_allow_html=True)

def find_similar_items(selected_item, recommend_list):
    i = 0
    for name, similar_items in recommend_list:
        if selected_item == name:
            i += 1
            cols = st.columns(len(similar_items))
            for col, item in zip(cols, similar_items):
                col.markdown(f'<div class="title-class"><strong>Title: </strong>{item}</div>', unsafe_allow_html=True)
                url_item = f"https://en.wikipedia.org/wiki/{item}"
                driver.get(url_item)

                #Get image book
                try: 
                    image_element = driver.find_element(By.CSS_SELECTOR, ".mw-file-element").get_attribute("src")
                    image_html = f'<a href="{url_item}" target="_blank"><img src="{image_element}" style="width:100px;height:200px;"></a>'
                    col.markdown(image_html, unsafe_allow_html=True)
                except NoSuchElementException:
                    image_element = 'Not Found'
                
                #Get author Book
                try: 
                    author_element = driver.find_element("xpath", "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table/tbody/tr[2]/td/a").text
                    col.markdown(f'**Author:** {author_element}')
                except NoSuchElementException:
                    col.markdown('**Author:** Not Found')

                #Get genre Book
                try:
                    genre_label = driver.find_element("xpath","//th[@class='infobox-label' and text()='Genre']")
                    if genre_label:
                        genre_info = genre_label.find_element("xpath","following-sibling::td").text
                        col.markdown(f'**Genre:** {genre_info}')
                    else:
                        col.markdown('**Genre:** Not Found')
                except NoSuchElementException:
                    col.markdown('**Genre:** Not Found')

                #Get publisher Book    
                try:
                    publisher_label = driver.find_element("xpath","//th[@class='infobox-label' and text()='Publisher']")
                    if publisher_label:
                        publisher_info = publisher_label.find_element("xpath","following-sibling::td").text
                        col.markdown(f'**Publisher:** {publisher_info}')
                    else:
                        col.write('Publisher: ' + 'Not Found')
                        col.markdown('**Publisher:** Not Found')
                except NoSuchElementException:
                    col.markdown('**Publisher:** Not Found')
                if(i>=4): break

selected_model_type = st.radio("Select Model Type", ["Regression", "Classification"])

if selected_model_type == "Regression":
    with open('regression_book_recommend_list.pkl','rb') as file:
        book_recommend_list = pickle.load(file)
    with open('regression_link_recommend_list.pkl','rb') as file:
        link_recommend_list = pickle.load(file)
else:
    with open('classification_book_recommend_list.pkl','rb') as file:
        book_recommend_list = pickle.load(file)
    with open('classification_link_recommend_list.pkl','rb') as file:
        link_recommend_list = pickle.load(file)

book_names = [item[0] for item in book_recommend_list]
link_names = [item[0] for item in link_recommend_list]

selected_category = st.radio("Select Category", ["Book", "Page"])

selected_item = st.selectbox(f"Type or select a {selected_category.lower()} from the dropdown",
                             book_names if selected_category == "Book" else link_names)
recommend_list = book_recommend_list if selected_category == "Book" else link_recommend_list

if st.button('Show Recommendation'):
    find_similar_items(selected_item, recommend_list)
