import streamlit as st
import pandas as pd
from myIBCF import myIBCF

# Instructions to run:
# pip install streamlit
# run command: streamlit run app.py
# then, navigate to http://localhost:8501/

movie_data = pd.read_csv(
    "./ml-1m/movies.dat",
    delimiter="::",
    engine="python",
    encoding="latin-1",
    header=None,
    names=["MovieID", "Title", "Genres"],
)

movie_data_sampled = movie_data.iloc[:100]

st.header("Please rate movies to get recommendations")
submit_button = st.button("Get Recommendations")
reset_button = st.button("Reset")

image_host_path = "https://liangfgithub.github.io/MovieImages/"

if "ratings" not in st.session_state:
    st.session_state.ratings = {}

if not submit_button:
    for i in range(0, len(movie_data_sampled), 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(movie_data_sampled):
                movie = movie_data_sampled.iloc[idx]
                movie_key = movie["MovieID"]

                with col:
                    st.text(movie["Title"])
                    image_url = f"{image_host_path}{movie['MovieID']}.jpg"
                    st.image(image_url, use_container_width=True)

                    rating = st.feedback("stars", key=movie_key)
                    st.session_state.ratings[movie_key] = rating


if submit_button:
    newuser = pd.DataFrame(
        list(st.session_state.ratings.items()), columns=["MovieID", "Rating"]
    ).drop_duplicates(subset="MovieID")

    # Get recommended movies
    recommended_movies = pd.DataFrame(myIBCF(newuser), columns=["MovieID"])
    st.session_state.recommended_movies = recommended_movies
    st.header("You may enjoy:")
    # Display recommended movies in columns
    for i in range(0, len(st.session_state.recommended_movies), 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(st.session_state.recommended_movies):
                movie_id = int(
                    st.session_state.recommended_movies.iloc[idx]["MovieID"][1:]
                )
                new_movie = movie_data.loc[movie_data["MovieID"] == movie_id]
                with col:
                    st.text(new_movie["Title"].values[0])
                    image_url = f"{image_host_path}{str(movie_id)}.jpg"
                    st.image(image_url, use_container_width=True)
                    st.text(new_movie["Genres"].values[0])
if reset_button:
    st.session_state.clear()
    st.rerun()
