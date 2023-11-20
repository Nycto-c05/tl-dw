from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import openai
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
)
def get_title(url:str) -> str:
    # test url
    # link = 'https://www.youtube.com/watch?v=jaRCENYBuYo'

    link = url
    page = requests.get(link)
    soup = BeautifulSoup(page.text,'html.parser')
    title = soup.title.text

    return title

def transcript(url:str) -> str:

    # test url
    # link = 'https://www.youtube.com/watch?v=jaRCENYBuYo'

    link = url

    id = link.replace('https://www.youtube.com/watch?v=', '')
    id = id.replace('https://youtu.be/', '')
    # print(id)

    transcr = YouTubeTranscriptApi.get_transcript(id)

    formatd_transcr = ''
    for i in transcr:
        subs = i['text']
        formatd_transcr = f'{formatd_transcr} {subs}'
    
    return formatd_transcr

def init():
    st.set_page_config(
        page_title="TL;DW",
        page_icon='▶️'
    )
    st.header("Too long; didn't watch(TL;DW)")

def summary(transcr:str) -> str:
    chat = ChatOpenAI(temperature=0.6, max_tokens=300, openai_api_key='YOUR_KEY')

    prompt = [SystemMessage(content='You are to summarize a youtube video from the given transcipt below.use 10 bullet points'), HumanMessage(content=transcr)]
    with st.spinner("Summarizing..."):
        response = chat(prompt)
    summary = response.content
    # response = chat(messages=prompt)


    return summary

def gen_ai():
    chat = ChatOpenAI(temperature=0.6, max_tokens=70, openai_api_key='_')

    url_input = st.text_input('Enter YouTube URL: ')
    button = st.button(key='send_url', label='Summarize')
    if button:
        if(url_input):
            st.write(f'<h4>{get_title(url_input)}</h4>',unsafe_allow_html=1)
            st.write(f"Link: {url_input}")
            transcript_ = transcript(url=url_input) 
            # st.write(transcript_)

            vid_summary = summary(transcript_)
            st.write(vid_summary)
            
        else:
            st.write('<strong style="color: red">Enter a valid YouTube link!</strong>',unsafe_allow_html=1)
        
def main():
    init()
    gen_ai()
    

main()
