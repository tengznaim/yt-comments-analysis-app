# YouTube Video Comment Analysis App

This is a web application that enables users to enter their desired video link and obtain analysis of the most relevant comments on the video.

The motivation behind this app is to better understand the quality of a video prior to watching it, especially after YouTube's removal of the dislike count. Without this count, I personally look through the comments to see what people are saying about it.

![Screenshot 2022-01-23 121919](https://user-images.githubusercontent.com/63803360/150664693-04652580-4220-434d-928a-c858b5920647.jpg)
![Screenshot 2022-01-23 122000](https://user-images.githubusercontent.com/63803360/150664697-dae54136-e194-4abf-9dc0-27269ac335fb.jpg)
![Screenshot 2022-01-23 122021](https://user-images.githubusercontent.com/63803360/150664708-b967f4ab-3750-4045-a37c-f9255bf680ef.jpg)

### Setting Up the YouTube Data API

1. Create a Google Cloud project.
2. Go to the [API Console](https://console.developers.google.com/apis/dashboard), visit the Enabled APIs page and enable the YouTube Data API v3.
3. Obtain authorization credentials.
   - There are two suggested ways of doing this (OAuth 2.0 and API keys) as described in the documentation [here](https://developers.google.com/youtube/registering_an_application)
   - For this app, I used an API key as it didn't need any personal access.
4. To work with the API, I used the `google-api-python-client` in the function written in the `utils.py` file. Alternatively, manual requests can also be made to the specific endpoint as documented [here](https://developers.google.com/youtube/v3/docs). If the latter is used, the API key can be used in the `key` parameter in the request, eg.

   ```python
   import requests

   api_key = ""
   # Also include the other parameters here.
   params = {"key":api_key}
   api_url = "ENDPOINT_URL"

   response = requests.get(api_url, params=params)
   ```

### Working on this App Locally

1. Get an API key for the YouTube Data API as described in the earlier section.
2. Create a .env file with the following:
   ```
   YT_API_KEY=<YOUR_API_KEY>
   ```
3. Install the requirements with `pip install -r requirements.txt`
4. Run `streamlit run app.py`. The app should start at `localhost:8501`

### WIP

1. Try the HuggingFace Transformers module for sentiment analysis.
   - At the moment, I chose TextBlob over this due to speed and the information provided by TextBlob.
2. Scrape data and either fine tune transformers or train a custom classifier?
3. Compare method performance on labeled data through metrics.

### References

1. [Google API Client Discovery](https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html)

   - What is important here is the `build` function which creates the resource to interact with the APIs.
   - Note that I used the `developerKey` parameter as I authenticated with an API key.

2. [YouTube Data API Docs](https://developers.google.com/youtube/v3/docs)

3. [Generating a WordCloud](https://www.datacamp.com/community/tutorials/wordcloud-python)
4. [HuggingFace Transformers Quick Start](https://huggingface.co/docs/transformers/quicktour)
5. TextBlob
   - [TextBlob Calculations](https://planspace.org/20150607-textblob_sentiment/)
6. Docker Deployment Related
   - [Using and setting environment variables in Docker](https://stackoverflow.com/questions/39597925/how-do-i-set-environment-variables-during-the-build-in-docker)
   - [Handling secrets in Docker apps](https://techbeacon.com/app-dev-testing/how-keep-your-container-secrets-secure)
