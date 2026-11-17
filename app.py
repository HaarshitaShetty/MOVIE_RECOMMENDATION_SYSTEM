import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="CineMatch | Movie Discovery",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #10091D, #211333);
    color: white;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label {
    color: #FFFFFF !important;
}

.hero-box {
    background: linear-gradient(120deg, #39205B, #69429A);
    padding: 35px;
    border-radius: 20px;
    border: 1px solid #9166C4;
    margin-bottom: 30px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #26183A;
    border: 1px solid #68468E;
    border-radius: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #7545B5, #A879E8);
    color: white;
    border: none;
    border-radius: 12px;
    height: 48px;
    font-weight: bold;
    font-size: 16px;
}

.stButton > button:hover {
    background: #B18AE6;
    color: white;
    border: none;
}

div[data-baseweb="select"] > div {
    background-color: #281B3D;
    border: 1px solid #9166C4;
    border-radius: 10px;
}

.footer {
    color: #BBA8D5;
    text-align: center;
    padding: 30px;
}

</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_data():

    with open("Movie_data.pkl", "rb") as file:
        movies = pickle.load(file)

    with open("Movie_similarity.pkl", "rb") as file:
        similarity = pickle.load(file)

    movies = pd.DataFrame(movies)

    return movies, similarity


movies, similarity = load_data()


def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []

    for i in movie_list:
        recommended_movies.append(
            movies.iloc[i[0]].title
        )

    return recommended_movies

with st.container(border=True):

    st.caption("✦ YOUR PERSONAL MOVIE DISCOVERY PLATFORM")

    st.title("Discover Your Next Favourite Movie.")

    st.write(
        "Find movies that match your taste. "
        "Select a movie you love and let CineMatch "
        "discover your next watch."
    )

st.markdown("## 🎬 Find Your Next Watch")

st.write("Choose a movie from our collection to get started.")

selected_movie = st.selectbox(
    "Select your favourite movie",
    movies["title"].values
)

st.write("")


if st.button("✨ Recommend Movies", use_container_width=True):

    with st.spinner("Finding movies you'll love..."):

        recommendations = recommend(selected_movie)

    st.markdown("---")

    st.markdown("## ✨ Your Recommendations")

    st.write(
        f"Because you liked *{selected_movie}*, "
        "here are five movies you might enjoy."
    )

    for index, movie in enumerate(recommendations, 1):

        with st.container(border=True):

            col1, col2 = st.columns([1, 8])

            with col1:
                st.markdown(f"### {index:02d}")

            with col2:
                st.markdown(f"### {movie}")

                st.caption("Recommended for you ✦")


st.markdown("---")

st.markdown(
    "<div class='footer'>"
    "CINEMATCH | MOVIE RECOMMENDATION SYSTEM"
    "<br><br>"
    "Powered by Machine Learning | TF-IDF + Cosine Similarity"
    "</div>",
    unsafe_allow_html=True
)