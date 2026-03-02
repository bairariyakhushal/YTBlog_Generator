from crewai import Task

def create_tasks(blog_researcher, blog_writer, yt_tool):
    
    research_task  = Task(
        description=(
            "Use the YouTube search tool to find video content about '{topic}'. "
            "After getting the transcript, summarize the key points into 3 detailed paragraphs. "
            "Do NOT repeat the raw transcript. Provide a clean summary only."
        ),
        expected_output="A 3-paragraph detailed summary of the video content about the topic.",
        tools=[yt_tool],
        agent=blog_researcher
    )
    
    write_task = Task(
        description=(
            "Using the research summary provided, write a complete blog post about '{topic}'. "
            "Include a catchy title, introduction, detailed body with subheadings, and a conclusion. "
            "Write in an engaging and informative tone."
        ),
        expected_output="A complete, well-formatted blog post in markdown with title, introduction, body sections, and conclusion.",
        tools=[],
        agent=blog_writer,
        output_file="blog.md"
    )
    
    return research_task, write_task
    