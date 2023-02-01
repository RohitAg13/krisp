from plugins.youtube import get_transcript


class FakeYouTubeTranscriptApi:
    def get_transcript(video_id: str):
        return [{"text": "Hello, everyone"}, {"text": "Hello"}]


def test_get_transcript():
    url = "https://www.youtube.com/watch?v=6ZfuNTqbHE8"
    transcript = get_transcript(url, FakeYouTubeTranscriptApi)
    assert len(transcript) > 0
    assert isinstance(transcript, str)
    assert "Hello, everyone" in transcript
