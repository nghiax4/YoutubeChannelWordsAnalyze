from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable
from dotenv import load_dotenv
import os
import random

def calculate_statistics(data):
    # return sample data
    return {
        'numDistinctWords': 58,
        'totalWords': 100,
        'yearAndWpmAndViews': [(2021, 5, 100), (2022, 6, 60), (2023, 7, 78), (2024, 8, 45)]
    }