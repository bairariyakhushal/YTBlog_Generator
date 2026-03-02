from crewai import Agent

def create_agents(yt_tool, llm):
    
    blog_researcher = Agent(
        role="Blog Researcher",
        goal="Search the YouTube channel and retrieve transcript content about {topic}. Summarize the key points from the transcript.",
        backstory="Expert YouTube content researcher who finds and extracts relevant video transcripts on any given topic. You always summarize your findings in clear paragraphs.",
        verbose=True,
        memory=False,
        tools=[yt_tool],
        llm=llm,
        allow_delegation=False,
        max_iter=3
    )
    
    blog_writer = Agent(
        role="Blog Writer",
        goal="Write a well-structured, engaging blog post about {topic} using the research provided.",
        backstory="Skilled blog writer who transforms research summaries into engaging, well-structured blog posts with clear headings, introduction, body, and conclusion.",
        verbose=True,
        memory=False,
        tools=[],
        llm=llm,
        allow_delegation=False,
        max_iter=3
    )
    
    return blog_researcher,blog_writer