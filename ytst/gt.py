from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url):
    return url.split("?v=")[1]

video_url = "https://www.youtube.com/watch?v=ZCNgbg9zXUk"  # Replace with your YouTube video URL
video_id = get_video_id(video_url)

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    for entry in transcript:
        print(f"{entry['start']}s: {entry['text']}")

except Exception as e:
    print(f"Error retrieving transcript: {e}")
