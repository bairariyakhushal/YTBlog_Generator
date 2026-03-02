import streamlit as st
from crewai import Crew, Process, LLM
from tools import create_yt_tool
from agents import create_agents
from tasks import create_tasks
import os
from dotenv import load_dotenv
load_dotenv()

st.title("YouTube Video Blog Generator")

channel=st.text_input("Enter YouTube Channel Handle")
topic=st.text_input("Enter Topic")

if st.button("Generate Blog"):
    if channel and topic:
    
        llm = LLM(
            model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
            api_key=os.getenv("GROQ_API_KEY")
        )
    
        yt_tool=create_yt_tool(channel)
        
        blog_researcher, blog_writer= create_agents(yt_tool, llm)
        
        research_task, write_task=create_tasks(blog_researcher,blog_writer,yt_tool)
        
        crew = Crew(
            agents=[blog_researcher,blog_writer],
            tasks=[research_task,write_task],
            process=Process.sequential,
            memory=False,
            verbose=True
        )
        
        result=crew.kickoff(inputs={'topic':topic})
        
        blog_text = str(result)
        
        st.success("Blog Generated")
        st.markdown(blog_text)
        
        st.download_button(
            "Download Blog",
            blog_text,
            file_name="blog.md"
        )
    
    else :
        st.warning("Please enter both channel and topic")
        
        
        
        