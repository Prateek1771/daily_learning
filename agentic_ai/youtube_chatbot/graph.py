"""Video fetching + the LangGraph analyze->chat workflow."""

import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import CouldNotRetrieveTranscript

from models import VideoAnalysis, VideoDetails, extract_video_id

# reuse the key already configured for the langgraph notebooks
load_dotenv(Path(__file__).parent.parent / "langgraph_code" / ".env")

# .env enables LangSmith with a placeholder key -> 403 spam; turn it off here
import os
os.environ["LANGSMITH_TRACING"] = "false"

llm = ChatOpenRouter(model="tencent/hy3:free", temperature=0.5)


# ---------- extraction ----------

def fetch_video_details(url: str) -> VideoDetails:
    video_id = extract_video_id(url)

    # metadata: oEmbed needs no API key
    oembed_url = "https://www.youtube.com/oembed?" + urllib.parse.urlencode(
        {"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"}
    )
    with urllib.request.urlopen(oembed_url, timeout=10) as resp:
        meta = json.load(resp)

    try:
        fetched = YouTubeTranscriptApi().fetch(video_id, languages=["en", "hi"])
    except CouldNotRetrieveTranscript as e:
        raise ValueError(
            "No transcript available for this video (captions may be disabled)."
        ) from e

    return VideoDetails(
        video_id=video_id,
        url=url,
        title=meta["title"],
        author=meta["author_name"],
        thumbnail_url=meta["thumbnail_url"],
        transcript=" ".join(snippet.text for snippet in fetched),
        transcript_language=fetched.language_code,
    )


# ---------- graph ----------

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    video: VideoDetails
    analysis: VideoAnalysis | None


def analyze(state: ChatState) -> dict:
    if state.get("analysis"):  # only analyze once per thread
        return {}
    video = state["video"]
    # ponytail: json_schema because this free model ignores tool-calling (returns None)
    analysis = llm.with_structured_output(VideoAnalysis, method="json_schema").invoke(
        f"Analyze this YouTube video.\n\nTitle: {video.title}\n"
        f"Channel: {video.author}\n\nTranscript:\n{video.transcript}"
    )
    return {"analysis": analysis}


def chat(state: ChatState) -> dict:
    if not state["messages"]:  # analysis-only run, nothing to answer yet
        return {}
    video = state["video"]
    system = SystemMessage(
        f"You answer questions about the YouTube video '{video.title}' by {video.author}. "
        f"Ground every answer in the transcript below; say so if it doesn't cover the question.\n\n"
        f"Analysis: {state['analysis'].model_dump_json() if state.get('analysis') else 'n/a'}\n\n"
        f"Transcript:\n{video.transcript}"
    )
    response = llm.invoke([system, *state["messages"]])
    return {"messages": [response]}


builder = StateGraph(ChatState)
builder.add_node("analyze", analyze)
builder.add_node("chat", chat)
builder.add_edge(START, "analyze")
builder.add_edge("analyze", "chat")
builder.add_edge("chat", END)
# ponytail: MemorySaver = in-process memory only; swap for SqliteSaver if history must survive restarts
graph = builder.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    from langchain_core.messages import HumanMessage

    details = fetch_video_details("https://www.youtube.com/watch?v=aircAruvnKk")  # 3Blue1Brown NN video
    assert details.title and len(details.transcript) > 1000, details
    print(f"Fetched: {details.title} ({len(details.transcript)} chars)")

    config = {"configurable": {"thread_id": details.video_id}}
    out = graph.invoke(
        {"video": details, "messages": [HumanMessage("In one sentence, what is this video about?")]},
        config,
    )
    assert out["analysis"].summary and out["messages"][-1].content
    print("Analysis:", out["analysis"].summary[:200])
    print("Chat:", out["messages"][-1].content[:200])
    print("graph.py self-check OK")
