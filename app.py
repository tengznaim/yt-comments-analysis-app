import streamlit as st
import pandas as pd
import re

from utils import get_video_comments

st.set_page_config(page_title="YouTube Video Comments Sentiment Analysis App")
st.title("YouTube Video Comments Sentiment Analysis App")
st.write("This is an application that performs sentiment analysis on desired videos.")

video_url = st.text_input(
    label="Enter a video URL:", placeholder="Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
submit_button = st.button("Submit")

if submit_button:
    valid_url = re.match(
        "^(http(s)?:\/\/(www)?)?youtube.com\/watch\?v=.+", video_url)
    if valid_url:
        video_id = video_url[video_url.index("=") + 1:]
        comments_list = get_video_comments(video_id)

        df = pd.DataFrame(comments_list)
        st.dataframe(df)
    else:
        st.error("Please enter a valid video URL")
