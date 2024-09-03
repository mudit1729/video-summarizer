import streamlit as st
import os
from src.video_info import GetVideo
from src.model import Model
from src.prompt import Prompt
from dotenv import load_dotenv
from st_copy_to_clipboard import st_copy_to_clipboard

class AIVideoSummarizer:
    def __init__(self):
        self.youtube_url = None
        self.video_id = None
        self.video_title = None
        self.video_transcript = None
        self.summary = None
        load_dotenv()

    def get_youtube_info(self):
        self.youtube_url = st.text_input("Enter YouTube Video Link")
        
        if self.youtube_url:
            self.video_id = GetVideo.Id(self.youtube_url)
            if self.video_id is None:
                st.error("Invalid YouTube URL. Please check and try again.")
                st.image("https://i.imgur.com/KWFtgxB.png", use_column_width=True)
                st.stop()
            self.video_title = GetVideo.title(self.youtube_url)
            st.write(f"**{self.video_title}**")
            st.image(f"http://img.youtube.com/vi/{self.video_id}/0.jpg", use_column_width=True)

    def generate_summary(self):
        if st.button("Get Summary"):
            with st.spinner("Generating summary..."):
                self.video_transcript = GetVideo.transcript(self.youtube_url)
                # Using Gemini by default, but you can change this to ChatGPT if preferred
                self.summary = Model.google_gemini(transcript=self.video_transcript, prompt=Prompt.prompt1())
                st.markdown("## Summary:")
                st.write(self.summary)
                st_copy_to_clipboard(self.summary)

    def run(self):
        st.set_page_config(page_title="AI Video Summarizer", page_icon="chart_with_upwards_trend", layout="wide")
        st.title("AI Video Summarizer")
        
        self.get_youtube_info()
        self.generate_summary()

if __name__ == "__main__":
    app = AIVideoSummarizer()
    app.run()