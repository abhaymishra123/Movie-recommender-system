import pickle
import streamlit as st

import numpy as np
import pandas as pd
import requests

st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

st.header('Movie Recommender System')
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox("Select The Movie To Find Similar Movie", movies['title'])

def recommend(movie):
    given_movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[given_movie_index]
    sorted_indices = np.argsort(distances)[::-1]
    top_similar_indices = [idx for idx in sorted_indices if idx != given_movie_index][:5]
    
    recommendations = []
    recommended_movie_posters = []
    for i in top_similar_indices:
        movie_id = movies.iloc[i].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommendations.append(movies.iloc[i].title)

    return recommendations,recommended_movie_posters


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])