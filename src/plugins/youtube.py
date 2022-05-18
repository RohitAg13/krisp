from logger import create_logger
from youtube_transcript_api import YouTubeTranscriptApi

logging = create_logger(__name__)


def get_transcript(url: str) -> str:
    logging.info(f"fetching transcript for Youtube video: {url}")
    try:
        video_id = url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        final_transcript = " ".join([i["text"] for i in transcript])
    except Exception as e:
        logging.error(e)
        final_transcript = ""
    logging.info(f"Length of the transcript: {len(final_transcript)}")
    return final_transcript
