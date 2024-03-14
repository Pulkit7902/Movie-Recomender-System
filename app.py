import streamlit as st 
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
     data = requests.get(url)
     data = data.json()
     poster_path = data['poster_path']
     full_path =  "https://image.tmdb.org/t/p/w500/" + poster_path
     return full_path
def recomend(movie):
    movie_index = movies[movies['title'] == movie ].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)) ,reverse=True , key = lambda x:x[1])[1:6]

    recomend_movie_poster = []
    recomend_movie = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recomend_movie_poster.append(fetch_poster(movie_id))
        recomend_movie.append(movies.iloc[i[0]].title)
    return recomend_movie , recomend_movie_poster
movie_list = pickle.load(open('movie_dict.pkl' ,'rb'))
similarity = pickle.load(open('similarity.pkl' , 'rb'))

movies = pd.DataFrame(movie_list)
st.title("Movie Recomender System")
selected_movie = st.selectbox(
    'Enter the name of movie',
    movies['title'].values)
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recomend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
    
   