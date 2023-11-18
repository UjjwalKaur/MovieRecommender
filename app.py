import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import io

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    #will hit the api using library, requests
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fac07bb7c8387add311821e1fd0a7a46&language=en-US'.format(movie_id))
    data = response.json()

    return 'https://image.tmdb.org/t/p/originaldata' + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # posterurl = requests.get(fetch_poster(movie_id), verify=False, stream=True)
        # poster = Image.open(io.BytesIO(posterurl.content))
        # poster.resize(200,300)
        # recommended_movies_posters.append(poster)
        recommended_movies_posters.append(fetch_poster(movie_id))
        # fetch poster from api
    return(recommended_movies, recommended_movies_posters)


movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
'Choose a movie from the dropdown and we will recommend an underrated movie similar to the one you liked', movies['title'].values)

if st.button('Recommend'):
    import time
    with st.spinner('Hold on while our not-so-sophisticated AI makes relevant connections...'):
        names, posters = recommend(selected_movie_name)
    st.success('Here you go!')


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

    st.text('')
    st.text('')
    st.text('')
    # values = st.slider(
    #     'Rate your recommendations',
    #     0, 10, 5)
    #
    # if st.button('Submit'):
    #     st.write('Thank you')
    #     st.snow()

primaryColor = '#7792E3'
backgroundColor = '#273346'
secondaryBackgroundColor = '#B9F1C0'
textColor = '#FFFFFF'


