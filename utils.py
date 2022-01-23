import googleapiclient.discovery
from dotenv import load_dotenv
import os
import requests
import json
import re
from wordcloud import WordCloud
from textblob import TextBlob
# from transformers import pipeline

# Use for local testing
load_dotenv()


def get_video_comments(video_id: str):
    """Gets a list of relevant comments on a YouTube video.

    Args:
        video_id (str): YouTube video ID found at the end of the video URL.

    Returns:
        comment_list (list): List of dictionaries of comment information.
    """

    API_KEY = os.environ.get("YT_API_KEY")
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

    youtube = googleapiclient.discovery.build(API_SERVICE_NAME,
                                              API_VERSION,
                                              developerKey=API_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=20,
        order="relevance",
        textFormat="plainText",
        videoId=video_id)
    response = request.execute()

    comments_list = []
    for result in response["items"]:
        comment_info = result["snippet"]["topLevelComment"]["snippet"]
        comments_list.append(comment_info)

    return comments_list


def highlight_rows(s):
    if s["sentiment"] == "POSITIVE":
        return ['background-color: #04aa6d']*len(s)
    elif s["sentiment"] == "NEGATIVE":
        return ['background-color: #f44336']*len(s)


def analyse_comments_huggingface(classifier, comments_list: list):
    """Computes sentiment analysis on a list of comments using HuggingFace's Transformers.

    Args:
        classifier (transformers.pipeline): A transformers pipeline for sentiment analysis.
        comments_list (list): List of items properties from the commentThreads response.

    Returns:
        sentiment_columns (dict): A dict of two lists with "sentiment" and "polarity" as keys.

    Note: This is currently an unused method.
    """

    comments_text = [comment["textDisplay"] for comment in comments_list]

    predictions = classifier(comments_text)
    polarity = [comment_pred["score"] for comment_pred in predictions]
    sentiment = [comment_pred["label"] for comment_pred in predictions]

    sentiment_columns = {"sentiment": sentiment, "polarity": polarity}

    return sentiment_columns


def analyse_comments_textblob(comments_list: list):
    """Computes sentiment analysis on a list of comments using TextBlob.

    Args:
        comments_list (list): List of items properties from the commentThreads response.

    Returns:
        sentiment_columns (dict): A dict of 3 lists with "sentiment", "polarity" and "subjectivity" as keys.
    """

    comments_text = [comment["textDisplay"] for comment in comments_list]
    processed_comments = [preprocess_text(
        comment) for comment in comments_text]

    polarity = []
    sentiment = []
    subjectivity = []

    for comment in processed_comments:
        comment_blob = TextBlob(comment)
        comment_polarity = comment_blob.sentiment.polarity
        comment_subjectivity = comment_blob.sentiment.subjectivity

        if comment_polarity > 0:
            sentiment.append("POSITIVE")
        elif comment_polarity < 0:
            sentiment.append("NEGATIVE")
        else:
            sentiment.append("NEUTRAL")

        polarity.append(comment_polarity)
        subjectivity.append(comment_subjectivity)

    sentiment_columns = {"sentiment": sentiment,
                         "polarity": polarity, "subjectivity": subjectivity}

    return sentiment_columns


def preprocess_text(comment: str):
    """Preprocesses a string to remove punctuation, convert to lowercase.

    Args:
        comment (str): The original comment string.

    Returns:
        processed (str): The preprocessed comment string.
    """

    processed_comment = comment.lower()
    processed_comment = re.sub(r"[^a-zA-Z0-9 ]", "", processed_comment)

    return processed_comment


def generate_worldcloud(comments_list: list):
    """Generates a wordcloud from the API response.

    Args:
        comments_list (list): List of items properties from the commentThreads response.

    Returns:
        video_wordcloud (np.array): Wordcloud in the form of a numpy array for use in the Streamlit app.

    Note: This assumes that the input list is the filtered list of items from the API response.
    """

    comments_text = [comment["textDisplay"] for comment in comments_list]
    processed_comments = [preprocess_text(
        comment) for comment in comments_text]
    all_comments = " ".join(processed_comments)

    video_wordcloud = WordCloud(
        background_color="white", width=1280, height=720).generate(all_comments)

    return video_wordcloud.to_array()
