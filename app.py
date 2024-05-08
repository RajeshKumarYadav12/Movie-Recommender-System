import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()

    # Check if 'poster_path' exists in the response
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return None  # Return None if poster_path is not found


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:13]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from Api
        recommended_movies.append((movies.iloc[i[0]].title))
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters


movies_dict = pickle.load(open('movie_dict1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity1.pkl', 'rb'))

st.title('Movie Recommended System')

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Define the number of columns to display posters
    num_columns = 4
    num_rows = len(posters) // num_columns

    # Create placeholders for displaying posters
    for i in range(num_rows):
        row = st.columns(num_columns)
        for j in range(num_columns):
            with row[j]:
                index = i * num_columns + j
                if index < len(posters):
                    st.text(names[index])
                    st.image(posters[index])


