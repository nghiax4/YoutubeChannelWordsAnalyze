from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable
from dotenv import load_dotenv
import os
from datetime import datetime

def calculate_statistics(data):
    # Helper to extract year from ISO date
    def get_year(iso_date):
        return datetime.fromisoformat(iso_date.replace("Z", "")).year
    
    year_and_wpm_and_views = []
    total_words = 0
    unique_words = set()

    for video in data:
        all_text = ' '.join(entry['text'] for entry in video['transcript'])
        words = all_text.split(' ')
        total_words += len(all_text.split())
        unique_words |= set(all_text.split())

        year = get_year(video['date'])
        wpm = round(len(words) / (video['transcript'][-1]["start"] + video['transcript'][-1]["duration"]) * 60)
        views = int(video["views"])

        year_and_wpm_and_views.append((year, wpm, views))

    return {
        'numDistinctWords': len(unique_words),
        'totalWords': total_words,
        'yearAndWpmAndViews': year_and_wpm_and_views
    }
        

    # return sample data
    return {
        'numDistinctWords': 58,
        'totalWords': 100,
        'yearAndWpmAndViews': [(2021, 5, 100), (2022, 6, 60), (2023, 7, 78), (2024, 8, 45)]
    }


def fetch_video_data(channel_id):
    print('(DEBUG) Fetching video data...')

    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    from googleapiclient.discovery import build
    import json

    videos_data = []

    with build('youtube', 'v3', developerKey=api_key) as youtube:
        next_page_token = None

        while True:
            request = youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token,
                type="video"
            )
            
            response = request.execute()
            videos_data.extend(response['items'])

            if not next_page_token:
                break

        videos_ids = [video['id']['videoId'] for video in videos_data]

        videos_views = {}

        with build('youtube', 'v3', developerKey=api_key) as youtube:
            next_page_token = None

            while True:
                request = youtube.videos().list(
                    part='statistics',
                    id=','.join(videos_ids),
                    pageToken=next_page_token,
                )

                response = request.execute()
                
                for video in response['items']:
                    videos_views[video['id']] = video['statistics']['viewCount']

                if not next_page_token:
                    break

        from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable

        final_video_data = []

        for video in videos_data:
            transcript = YouTubeTranscriptApi.get_transcript(video['id']['videoId'])
            
            this_data = {
                'videoId': video['id']['videoId'],
                'date': video['snippet']['publishedAt'],
                'thumbnail': video['snippet']['thumbnails']['default']['url'],
                'views': videos_views[video['id']['videoId']],
                'transcript': transcript
            }

            final_video_data.append(this_data)


        print('(DEBUG) DONE FETCHING DATA')
        return final_video_data