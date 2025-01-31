from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable
from dotenv import load_dotenv
import os
import random

def fetch_video_ids_with_dates(channel_id: str) -> list[dict]:
    """
    Fetches all video IDs and their publication dates from a YouTube channel.

    Args:
        channel_id (str): The YouTube channel ID.

    Returns:
        list: A list of dictionaries with video IDs and their publication years.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key not found. Ensure it is set in the .env file.")

    video_data = []
    next_page_token = None

    with build("youtube", "v3", developerKey=api_key) as youtube:
        while True:
            request = youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token,
                type="video"
            )
            response = request.execute()
            for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                published_at = item["snippet"]["publishedAt"]
                publication_year = published_at[:4]  # Extract the year from the timestamp
                video_data.append({"video_id": video_id, "year": publication_year})
            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

    print('(fetch_video_ids_with_dates) Video data retrieved:', len(video_data))
    return video_data

def fetch_random_video_transcripts_with_years(channel_id, sample_size=5):
    """
    Retrieves transcripts and years from a random sample of videos from a YouTube channel.

    Args:
        channel_id (str): The YouTube channel ID.
        sample_size (int): Number of random videos to retrieve transcripts from.

    Returns:
        list: A list of dictionaries containing transcripts and years.

    Example Return Value:
        [
            {
                "year": "2023",
                "transcript": [
                    {"text": "Hello world!", "start": 0.0, "duration": 1.5},
                    {"text": "Welcome to the channel.", "start": 1.5, "duration": 2.0},
                    ...
                ]
            },
            {
                "year": "2022",
                "transcript": "Transcript not available."
            },
            ...
        ]
    """
    video_data = fetch_video_ids_with_dates(channel_id)
    if not video_data:
        raise ValueError("No videos found for the given channel ID.")

    sample_video_data = random.sample(video_data, min(sample_size, len(video_data)))
    transcripts = []

    for video in sample_video_data:
        video_id = video["video_id"]
        year = video["year"]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcripts.append({"year": year, "transcript": transcript})
        except (TranscriptsDisabled, VideoUnavailable):
            transcripts.append({"year": year, "transcript": "Transcript not available."})

    print('(fetch_random_video_transcripts_with_years) Transcripts retrieved:', len(transcripts))
    return transcripts

def calculate_statistics(transcripts_with_years):
    """
    Calculates various statistics from the transcripts.

    Args:
        transcripts_with_years (list): A list of dictionaries containing transcripts and years.
        Example:
        [
            {
                "year": "2023",
                "transcript": [
                    {"text": "Hello world!", "start": 0.0, "duration": 1.5},
                    {"text": "Welcome to the channel.", "start": 1.5, "duration": 2.0},
                    ...
                ]
            },
            {
                "year": "2022",
                "transcript": "Transcript not available."
            },
            ...
        ]

    Returns:
        dict: A dictionary containing the calculated statistics.
        Example:
        {
            "numDifferentWords": 1000,
            "totalWordsSpoken": 50000,
            "wpmOverYear": [{"year": 2020, "wpm": 120}, {"year": 2021, "wpm": 130}],
            "wpmVsViews": [{"year": 2020, "wpm": 120, "views": 1000}, {"year": 2021, "wpm": 130, "views": 1500}],
            "sentimentOverYear": [{"year": 2020, "sentiment": 0.5}, {"year": 2021, "sentiment": 0.6}]
        }
    """
    # Placeholder implementation
    num_different_words = 0
    total_words_spoken = 0
    wpm_over_year = []
    wpm_vs_views = []
    sentiment_over_year = []

    # TODO: Implement the actual calculations

    return {
        "numDifferentWords": num_different_words,
        "totalWordsSpoken": total_words_spoken,
        "wpmOverYear": wpm_over_year,
        "wpmVsViews": wpm_vs_views,
        "sentimentOverYear": sentiment_over_year
    }