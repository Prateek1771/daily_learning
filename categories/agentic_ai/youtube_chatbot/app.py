"""Streamlit UI: paste a YouTube URL, get an analysis, chat about the video."""

import streamlit as st
from langchain_core.messages import HumanMessage

from graph import fetch_video_details, graph

st.set_page_config(page_title="YouTube Chatbot", page_icon="📺", layout="wide")
st.title("📺 YouTube Video Analyzer & Chatbot")

with st.sidebar:
    st.header("Video")
    url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)

if analyze_clicked and url:
    try:
        with st.spinner("Fetching video details & transcript..."):
            video = fetch_video_details(url)
        with st.spinner("Analyzing with LLM..."):
            config = {"configurable": {"thread_id": video.video_id}}
            result = graph.invoke({"video": video, "messages": []}, config)
        st.session_state.video = video
        st.session_state.analysis = result["analysis"]
        st.session_state.chat_history = []
    except Exception as e:
        st.error(str(e))

if "video" not in st.session_state:
    st.info("Paste a YouTube URL in the sidebar and click **Analyze** to get started.")
    st.stop()

video = st.session_state.video
analysis = st.session_state.analysis

col_video, col_chat = st.columns([2, 3])

with col_video:
    st.image(video.thumbnail_url, use_container_width=True)
    st.subheader(video.title)
    st.caption(f"by {video.author} · transcript language: {video.transcript_language}")

    st.markdown("#### Summary")
    st.write(analysis.summary)

    st.markdown("#### Topics")
    st.write(" ".join(f"`{t}`" for t in analysis.topics))

    st.markdown("#### Key points")
    for point in analysis.key_points:
        st.markdown(f"- {point}")

    st.caption(f"**Tone:** {analysis.sentiment} · **Audience:** {analysis.target_audience}")

with col_chat:
    st.markdown("#### Chat about this video")
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    if question := st.chat_input("Ask anything about the video..."):
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"), st.spinner("Thinking..."):
            config = {"configurable": {"thread_id": video.video_id}}
            out = graph.invoke(
                {"video": video, "messages": [HumanMessage(question)]}, config
            )
            answer = out["messages"][-1].content
            st.write(answer)
        st.session_state.chat_history += [("user", question), ("assistant", answer)]
