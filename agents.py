from crewai import Agent

def create_agents(yt_tool, llm):
    
    blog_researcher = Agent(
        role="Blog Researcher",
        goal="Get transcription for topic {topic}",
        backstory="Expert YouTube content researcher who finds and extracts relevant video transcripts on any given topic.",
        verbose=True,
        memory=False,
        tools=[yt_tool],
        llm=llm,
        allow_delegation=True
    )
    
    blog_writer = Agent(
        role="Blog Writer",
        goal="Write blog on {topic}",
        backstory="Skilled technical blog writer who transforms video transcripts and research into engaging, well-structured blog posts.",
        verbose=True,
        memory=False,
        tools=[yt_tool],
        llm=llm,
        allow_delegation=False
    )
    
    return blog_researcher,blog_writer