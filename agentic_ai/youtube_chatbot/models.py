"""Pydantic models: input validation (VideoDetails) and LLM structured output (VideoAnalysis)."""

import re

from pydantic import BaseModel, Field

# matches watch?v=ID, youtu.be/ID, shorts/ID, embed/ID
_VIDEO_ID_RE = re.compile(
    r"(?:youtu\.be/|youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|embed/))([A-Za-z0-9_-]{11})"
)


def extract_video_id(url: str) -> str:
    match = _VIDEO_ID_RE.search(url.strip())
    if not match:
        raise ValueError(f"Could not find a YouTube video ID in: {url!r}")
    return match.group(1)


class VideoDetails(BaseModel):
    video_id: str = Field(min_length=11, max_length=11)
    url: str
    title: str
    author: str
    thumbnail_url: str
    transcript: str
    transcript_language: str


class VideoAnalysis(BaseModel):
    """Schema the LLM must fill via with_structured_output()."""

    summary: str = Field(description="3-5 sentence summary of the video")
    topics: list[str] = Field(description="Main topics covered, short phrases")
    key_points: list[str] = Field(description="Most important takeaways")
    sentiment: str = Field(description="Overall tone: e.g. educational, promotional, critical")
    target_audience: str = Field(description="Who this video is for")


if __name__ == "__main__":
    for u in (
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ?t=5",
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",
        "https://www.youtube.com/watch?list=PL123&v=dQw4w9WgXcQ",
    ):
        assert extract_video_id(u) == "dQw4w9WgXcQ", u
    try:
        extract_video_id("https://example.com/notavideo")
        raise AssertionError("should have raised")
    except ValueError:
        pass
    print("models.py self-check OK")
