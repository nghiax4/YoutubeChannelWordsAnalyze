from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable
from dotenv import load_dotenv
import os
import random

def fetch_video_ids(channel_id: str) -> list[str]:
    """
    Fetches all video IDs from a YouTube channel.

    Args:
        channel_id (str): The YouTube channel ID.

    Returns:
        list: A list of video IDs from the channel.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key not found. Ensure it is set in the .env file.")

    video_ids = []
    next_page_token = None

    with build("youtube", "v3", developerKey=api_key) as youtube:
        while True:
            request = youtube.search().list(
                part="id",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token,
                type="video"
            )
            response = request.execute()
            video_ids.extend(item["id"]["videoId"] for item in response.get("items", []))
            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

    print('(fetch_video_ids) Video ids retrieved:', len(video_ids))
    return video_ids

def fetch_random_video_transcripts(channel_id, sample_size=5):
    """
    Retrieves transcripts from a random sample of videos from a YouTube channel.

    Args:
        channel_id (str): The YouTube channel ID.
        sample_size (int): Number of random videos to retrieve transcripts from.

    Returns:
        list: A list of transcripts (or a message if transcripts are not available).

    Example Return Value:
        [
            [  # Transcript of video 1
                {"text": "Hello world!", "start": 0.0, "duration": 1.5},
                {"text": "Welcome to the channel.", "start": 1.5, "duration": 2.0},
                ...
            ],
            [  # Transcript of video 2
                {"text": "This is another video.", "start": 0.0, "duration": 1.2},
                {"text": "Stay tuned for more content.", "start": 1.2, "duration": 2.3},
                ...
            ],
            "Transcript not available.",  # Video 3 has no transcript
            ...
        ]
    """
    video_ids = fetch_video_ids(channel_id)
    if not video_ids:
        raise ValueError("No videos found for the given channel ID.")

    sample_video_ids = random.sample(video_ids, min(sample_size, len(video_ids)))
    transcripts = []

    for video_id in sample_video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcripts.append(transcript)  # Add the transcript directly
        except (TranscriptsDisabled, VideoUnavailable):
            transcripts.append("Transcript not available.")

    print('(fetch_random_video_transcripts) Transcripts retrieved:', len(transcripts))
    return transcripts
