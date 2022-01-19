import streamlit as st
import pandas as pd
import re

from utils import get_video_comments, generate_worldcloud, analyse_comments_huggingface, highlight_rows

st.set_page_config(page_title="YouTube Video Comments Sentiment Analysis App")
st.title("YouTube Video Comments Sentiment Analysis App")
st.write("This is an application that performs sentiment analysis on desired videos.")

video_url = st.text_input(
    label="Enter a video URL:", placeholder="Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
submit_button = st.button("Submit")

if submit_button:
    valid_url = re.match(
        "^(http(s)?:\/\/(www.)?)?youtube.com\/watch\?v=.+", video_url)

    if valid_url:
        video_id = video_url[video_url.index("=") + 1:]
        with st.spinner("Analysing comments..."):
            comments_list = get_video_comments(video_id)

            df = pd.DataFrame(comments_list)
            sentiment_columns = analyse_comments_huggingface(comments_list)
            df["sentiment"] = sentiment_columns["sentiment"]
            df["polarity"] = sentiment_columns["polarity"]

            filtered_df = df[["textDisplay", "authorDisplayName",
                              "likeCount", "publishedAt", "updatedAt", "sentiment", "polarity"]]
            filtered_df = filtered_df.sort_values(
                by="likeCount", ascending=False).reset_index(drop=True)
            video_wordcloud = generate_worldcloud(comments_list)

        st.subheader("Video Comments:")
        filtered_df = filtered_df.style.apply(highlight_rows, axis=1)
        st.dataframe(filtered_df)
        st.subheader("Word Cloud:")
        st.image(video_wordcloud)

    else:
        st.error("Please enter a valid video URL")
