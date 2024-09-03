import streamlit as st
import os
from src.video_info import GetVideo
from src.model import Model
from src.prompt import Prompt
from src.misc import Misc
from src.timestamp_formatter import TimestampFormatter
from dotenv import load_dotenv
from st_copy_to_clipboard import st_copy_to_clipboard

class AIVideoSummarizer:
    def __init__(self):
        self.youtube_url = None
        self.video_id = None
        self.video_title = None
        self.video_transcript = None
        self.video_transcript_time = None
        self.summary = None
        self.time_stamps = None
        self.transcript = None
        self.model_name = None
        self.col1 = None
        self.col2 = None
        self.col3 = None
        self.model_env_checker = []
        load_dotenv()

    def get_youtube_info(self):
        self.youtube_url = st.text_input("Enter YouTube Video Link")

        # Check for API keys
        if os.getenv("GOOGLE_GEMINI_API_KEY"):
            self.model_env_checker.append("Gemini")
        if os.getenv("OPENAI_CHATGPT_API_KEY"):
            self.model_env_checker.append("ChatGPT")
        
        if not self.model_env_checker:
            st.error('No API keys found. Please set up at least one API key to use this application.', icon="🚫")
            st.stop()

        with self.col2:
            with st.container():
                self.model_name = st.selectbox(
                    'Select the model',
                    self.model_env_checker)

                def switch(model_name):
                    if model_name == "Gemini":
                        st.columns(3)[1].image("https://i.imgur.com/w9izNH5.png", use_column_width=True)
                    elif model_name == "ChatGPT":
                        st.columns(3)[1].image("https://i.imgur.com/Sr9e9ZC.png", use_column_width=True)

                switch(self.model_name)

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
        if st.button(":rainbow[**Get Summary**]"):
            with st.spinner("Generating summary..."):
                self.video_transcript = GetVideo.transcript(self.youtube_url)
                if self.model_name == "Gemini":
                    self.summary = Model.google_gemini(transcript=self.video_transcript, prompt=Prompt.prompt1())
                elif self.model_name == "ChatGPT":
                    self.summary = Model.openai_chatgpt(transcript=self.video_transcript, prompt=Prompt.prompt1())
                st.markdown("## Summary:")
                st.write(self.summary)
                st_copy_to_clipboard(self.summary)

    def generate_time_stamps(self):
        if st.button(":rainbow[**Get Timestamps**]"):
            with st.spinner("Generating timestamps..."):
                self.video_transcript_time = GetVideo.transcript_time(self.youtube_url)
                youtube_url_full = f"https://youtube.com/watch?v={self.video_id}"
                if self.model_name == "Gemini":
                    self.time_stamps = Model.google_gemini(self.video_transcript_time, Prompt.prompt1(ID='timestamp'), extra=youtube_url_full)
                elif self.model_name == "ChatGPT":
                    self.time_stamps = Model.openai_chatgpt(self.video_transcript_time, Prompt.prompt1(ID='timestamp'), extra=youtube_url_full)
                st.markdown("## Timestamps:")
                st.markdown(self.time_stamps)
                cp_text = TimestampFormatter.format(self.time_stamps)
                st_copy_to_clipboard(cp_text)

    def generate_transcript(self):
        if st.button("Get Transcript"):
            with st.spinner("Fetching transcript..."):
                self.video_transcript = GetVideo.transcript(self.youtube_url)
                self.transcript = self.video_transcript
                st.markdown("## Transcript:") 
                st.download_button(label="Download as text file", data=self.transcript, file_name=f"Transcript - {self.video_title}.txt")
                st.write(self.transcript)
                st_copy_to_clipboard(self.transcript)

    def run(self):
        st.set_page_config(page_title="AI Video Summarizer", page_icon="chart_with_upwards_trend", layout="wide")
        st.title("AI Video Summarizer")
        
        self.col1, self.col2, self.col3 = st.columns(3)

        with self.col1:
            self.get_youtube_info()

        ran_loader = Misc.loaderx() 
        n, loader = ran_loader[0], ran_loader[1]

        with self.col3:
            mode = st.radio(
                "What do you want to generate for this video?",
                [":rainbow[**AI Summary**]", ":rainbow[**AI Timestamps**]", "**Transcript**"],
                index=0)
            if mode == ":rainbow[**AI Summary**]":
                self.generate_summary()
            elif mode == ":rainbow[**AI Timestamps**]":
                self.generate_time_stamps()
            else:
                self.generate_transcript()

        st.write(Misc.footer(), unsafe_allow_html=True)

if __name__ == "__main__":
    app = AIVideoSummarizer()
    app.run()