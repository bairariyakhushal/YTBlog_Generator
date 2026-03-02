import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class YoutubeSearchInput(BaseModel):
    search_query: str = Field(..., description="The search query to find relevant content in the YouTube channel.")


class YoutubeChannelSearchTool(BaseTool):
    """Search a YouTube channel's video transcripts for relevant content."""

    name: str = "Search YouTube Channel Content"
    description: str = "Searches a YouTube channel's videos and returns transcript content relevant to the query."
    args_schema: type[BaseModel] = YoutubeSearchInput
    channel_handle: str = ""
    max_videos: int = 10

    def _run(self, search_query: str) -> str:
        handle = self.channel_handle.strip().lstrip("@")

        videos = scrapetube.get_channel(channel_username=handle, limit=self.max_videos)
        video_list = list(videos)

        if not video_list:
            return f"No videos found for channel @{handle}"

        # Score videos by keyword relevance
        query_words = [w.lower() for w in search_query.split() if len(w) > 2]
        scored_results = []
        api = YouTubeTranscriptApi()

        for video in video_list:
            video_id = video["videoId"]
            title = video.get("title", {}).get("runs", [{}])[0].get("text", video_id)

            try:
                transcript = api.fetch(video_id, languages=["en"])
                text = " ".join(snippet.text for snippet in transcript)

                # Score by how many query words appear in title + transcript
                combined = (title + " " + text).lower()
                score = sum(1 for word in query_words if word in combined)

                if score > 0:
                    scored_results.append((score, title, text))
            except Exception:
                continue

        if not scored_results:
            # Fallback: return first available transcripts regardless of keywords
            fallback = []
            for video in video_list[:3]:
                video_id = video["videoId"]
                title = video.get("title", {}).get("runs", [{}])[0].get("text", video_id)
                try:
                    transcript = api.fetch(video_id, languages=["en"])
                    text = " ".join(snippet.text for snippet in transcript)
                    fallback.append(f"**{title}**\n{text[:1500]}")
                except Exception:
                    continue
            if fallback:
                output = "\n\n---\n\n".join(fallback)
                return output[:3000]
            return f"No transcript content found in channel @{handle}"

        # Sort by relevance score (highest first) and return top results
        scored_results.sort(key=lambda x: x[0], reverse=True)
        results = [f"**{title}**\n{text[:800]}" for score, title, text in scored_results[:3]]
        output = "\n\n---\n\n".join(results)
        # Truncate total output to avoid overwhelming the LLM during tool-use
        return output[:3000]


def create_yt_tool(channel_handle: str) -> YoutubeChannelSearchTool:
    handle = channel_handle.strip()
    # Extract handle from full URL if provided
    if "youtube.com/@" in handle:
        handle = handle.split("youtube.com/@")[-1].split("/")[0]
    elif handle.startswith("@"):
        handle = handle[1:]

    return YoutubeChannelSearchTool(
        channel_handle=handle,
        description=f"Searches the @{handle} YouTube channel's videos and returns transcript content relevant to the query.",
    )