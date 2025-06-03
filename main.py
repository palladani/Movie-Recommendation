import streamlit as st
import pickle
import pandas as pd
import requests
st.set_page_config(layout="wide")

#8265bd1679663a7ea12ac168da84d2e8
new_title = '<p style="font-family:serif; color:White; font-size: 60px;">Cine sathi - Movie Recommendation System</p>'
quarry = '<p style="font-family:serif; color:Black; font-size:35px; ">Which movie you liked ??</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.markdown(quarry, unsafe_allow_html=True)

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US',
            timeout=5
        )
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommended_movie_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))
    return recommended_movie, recommended_movie_poster



selected_movie = st.selectbox("",movies['title'].values)
st.text("")

if st.button('Recommend'):
    st.text("")
    names, poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(poster[0])
        st.subheader(names[0])
        st.text("")
    with col2:
        st.image(poster[1])
        st.subheader(names[1])
        st.text("")
    with col3:
        st.image(poster[2])
        st.subheader(names[2])
        st.text("")
    with col4:
        st.image(poster[3])
        st.subheader(names[3])
        st.text("")
    with col5:
        st.image(poster[4])
        st.subheader(names[4])
        st.text("")
