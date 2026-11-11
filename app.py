import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(book_id):
    return f'https://covers.openlibrary.org/b/isbn/{book_id}-M.jpg'


def recommend(book):
    book_index = books[books['Title']==book].index[0]
    minAge = books.loc[books['Title']==book, 'MinAge'].iloc[0]
    maxAge = books.loc[books['Title']==book, 'MaxAge'].iloc[0]
    distances = similarity[book_index]
    book_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:500]
    recommended_books = []
    recommended_book_posters = []
    counter = 0
    for i in book_list:
        if ((books.iloc[i[0]]['MinAge']>=minAge) and (books.iloc[i[0]]['MaxAge']<=maxAge)):
            book_id = books.iloc[i[0]]['ISBN']
            recommended_books.append(books.iloc[i[0]]['Title'])
            recommended_book_posters.append(fetch_poster(book_id))
            counter +=1
        if(counter==5):
            return recommended_books, recommended_book_posters
    return recommended_books, recommended_book_posters

st.title('Book Recommendation System')
books = pickle.load(open('C:\\Users\\Vishwanath\\Documents\\MachineLearningProjects\\Book Recommondation System\\book-recommender-system\\books.pkl', 'rb'))
similarity = pickle.load(open('C:\\Users\\Vishwanath\\Documents\\MachineLearningProjects\\Book Recommondation System\\book-recommender-system\\similarity.pkl', 'rb'))
books = pd.DataFrame(books)
book = st.selectbox('Select a book : ', books['Title'].values)
if st.button('Recommend'):
    names, posters = recommend(book)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])