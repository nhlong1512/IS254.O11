import pickle
import streamlit as st


st.header('Recommendation System')

with open('book_recommend_list.pkl','rb') as file:
    book_recommend_list = pickle.load(file)

with open('link_recommend_list.pkl','rb') as file:
    link_recommend_list = pickle.load(file)

def find_similar_items(selected_item, recommend_list):
    for name, similar_items in recommend_list:
        if selected_item == name:
            cols = st.columns(len(similar_items))
            for col, item in zip(cols, similar_items):
                col.write(item)
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