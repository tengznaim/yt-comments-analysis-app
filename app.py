import streamlit as st
import pandas as pd
import re
# from transformers import pipeline
import matplotlib.pyplot as plt

from utils import get_video_comments, generate_worldcloud, analyse_comments_huggingface, analyse_comments_textblob, highlight_rows

st.set_page_config(page_title="YouTube Video Comments Analysis App")
st.title("YouTube Video Comments Analysis App")

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
            sentiment_columns = analyse_comments_textblob(
                comments_list)
            df["sentiment"] = sentiment_columns["sentiment"]
            df["polarity"] = sentiment_columns["polarity"]
            df["subjectivity"] = sentiment_columns["subjectivity"]

            filtered_df = df[["textDisplay", "authorDisplayName",
                              "likeCount", "publishedAt", "updatedAt", "sentiment", "polarity", "subjectivity"]]
            filtered_df = filtered_df.sort_values(
                by="likeCount", ascending=False).reset_index(drop=True)
            video_wordcloud = generate_worldcloud(comments_list)

        # Comments dataframe
        st.subheader("Video Comments:")
        st.info(
            "🟩 - Positive predicted sentiment  \n  🟥 - Negative predicted sentiment  \n  Scroll to the right of the DataFrame below to view the scores")
        filtered_df = filtered_df.style.apply(highlight_rows, axis=1)
        st.dataframe(filtered_df)

        # Stats
        st.subheader("Analysis:")
        st.info("**Polarity**  \n  More than 0 = Leans towards a positive sentiment  \n  0 = Neutral sentiment  \n  Less than 0 = Leans towards a negative sentiment  \n  **Subjectivity**  \n  A value closer to 1 indicates a more subjective comment (potentially based on opinion)")

        px = 1 / plt.rcParams['figure.dpi']
        fig, axes = plt.subplots(1, 2, figsize=(1280*px, 720*px))

        plt.subplot(1, 2, 1)
        labels = list(df["sentiment"].value_counts().keys())
        values = df["sentiment"].value_counts().values
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Sentiment Breakdown")

        plt.subplot(1, 2, 2)
        polarity_values = df["polarity"]
        subjectivity_values = df["subjectivity"]
        plt.scatter(polarity_values, subjectivity_values)
        plt.xlabel("Polarity")
        plt.xlim([-1, 1])
        plt.ylabel("Subjectivity")
        plt.ylim([0, 1])
        plt.title("Polarity Against Subjectivity")
        plt.grid()

        st.pyplot(fig)

        # Average Scores
        col_1, col_2 = st.columns(2)
        col_1.metric("Average Polarity", df["polarity"].mean())
        col_2.metric("Average Subjectivity", df["subjectivity"].mean())

        # Word Cloud
        st.subheader("Word Cloud:")
        st.write("These are words that are commonly found in the comments.")
        st.image(video_wordcloud)

    else:
        st.error("Please enter a valid video URL")
