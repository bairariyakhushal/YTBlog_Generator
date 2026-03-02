from crewai import Task

def create_tasks(blog_researcher, blog_writer, yt_tool):
    
    research_task  = Task(
        description="Find video on {topic}",
        expected_output="3 paragraph detailed summary",
        tools=[yt_tool],
        agent=blog_researcher
    )
    
    write_task = Task(
        description="Write blog for {topic}",
        expected_output="Complete blog content",
        tools=[yt_tool],
        agent=blog_writer,
        output_file="blog.md"
    )
    
    return research_task, write_task
    