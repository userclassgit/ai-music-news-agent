# AI Music News Audio Generator

[Listen to Audio Demo](https://file.notion.so/f/f/02686ad4-1e38-4b1d-a1c7-c3057724c60e/bc6f3de5-1e7a-41d7-b920-ae5e6ad2680b/Spotify_is_expanding_its_AI_audiobook_narration_ca.mp3?table=block&id=1a2c218c-cd18-806c-b54b-df3e1cc4e18d&spaceId=02686ad4-1e38-4b1d-a1c7-c3057724c60e&expirationTimestamp=1740261600000&signature=D1hvsJjeHbmtW0kUKmG82bY2uXcKs6ft2mK3fJ4xWhw)

## What it Does

This AI agent autonomously
1. gets links to news articles published in the past 2 days that are relevant to both AI and music through NewsAPI.
2. scrapes the news content from each link.
3. gives Gemini the scraped news content for summarization with additional instructions (professional tone, one paragraph per article, etc).
4. uses ElevenLabs API to convert the summary into a single audio file that is ready to be edited and used in a YouTube video.

## Technology Stack

- **NewsAPI**: Fetches recent news articles about AI and music
- **BeautifulSoup4**: Scrapes the full content from each news article
- **Gemini 2.0 Flash Thinking Experimental 01-21 API**: Summarizes articles with a professional tone and consistent format
- **ElevenLabs API**: Converts text summaries into natural-sounding audio narration.

## Learn More

I have documented the entire process of building this AI agent on this Notion page:
https://mj-project-journal.notion.site/AI-Content-Creator-184c218ccd1880c7b608ceccc4f2cddc