import pickle
import requests
from bs4 import BeautifulSoup
import streamlit as st

st.header('Recommendation System')

def get_wikipedia_image_url(book_title):
    formatted_title = book_title.replace(" ", "_")
    wikipedia_url = f'https://en.wikipedia.org/wiki/{formatted_title}'

    try:
        response = requests.get(wikipedia_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        meta_image_tag = soup.find('meta', {'property': 'og:image'})
        if meta_image_tag:
            image_url = meta_image_tag.get('content')
            return image_url

        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

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

def find_similar_items(selected_item, recommend_list):
    for name, similar_items in recommend_list:
        if selected_item == name:
            cols = st.columns(len(similar_items))
            for col, item in zip(cols, similar_items):
                col.write(item)
                image_url = get_wikipedia_image_url(item)
                if image_url:
                    col.image(image_url)
                else:
                    col.image('./default.jpeg')
            break
    else:
        st.write(f"No similar items found for {selected_item}")

book_names = [item[0] for item in book_recommend_list]
link_names = [item[0] for item in link_recommend_list]

selected_category = st.radio("Select Category", ["Book", "Page"])

selected_item = st.selectbox(f"Type or select a {selected_category.lower()} from the dropdown",
                             book_names if selected_category == "Book" else link_names)
recommend_list = book_recommend_list if selected_category == "Book" else link_recommend_list

if st.button('Show Recommendation'):
    find_similar_items(selected_item, recommend_list)
