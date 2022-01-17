import googleapiclient.discovery
from dotenv import load_dotenv
import os
import requests
import json
from wordcloud import WordCloud

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


def generate_worldcloud(comments_list: list):
    """Generates a wordcloud from the API response.

    Args:
        comments_list (list): List of items properties from the commentThreads response.

    Returns:
        video_world (np.array): Wordcloud in the form of a numpy array for use in the Streamlit app.
    """

    comments_text = [comment["textDisplay"] for comment in comments_list]
    all_comments = " ".join(comments_text)

    video_wordcloud = WordCloud(
        background_color="white", width=1280, height=720).generate(all_comments)

    return video_wordcloud.to_array()
