# AI Music News Audio Generator

[Listen to the Audio Demo](https://file.notion.so/f/f/02686ad4-1e38-4b1d-a1c7-c3057724c60e/bc6f3de5-1e7a-41d7-b920-ae5e6ad2680b/Spotify_is_expanding_its_AI_audiobook_narration_ca.mp3?table=block&id=1a2c218c-cd18-806c-b54b-df3e1cc4e18d&spaceId=02686ad4-1e38-4b1d-a1c7-c3057724c60e&expirationTimestamp=1740470400000&signature=VViUrofYv4c5jgqEjBtaj6Ha3NjN3fPZfdyjYw5LfRo)

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

## How I Built This Agent

I have documented the entire process of building this AI agent on this Notion page:
https://mj-project-journal.notion.site/AI-Content-Creator-184c218ccd1880c7b608ceccc4f2cddc

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/userclassgit/ai-music-news-agent.git
   cd ai-music-news-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get API keys:
   - NewsAPI key from [newsapi.org](https://newsapi.org)
   - Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - ElevenLabs API key from [elevenlabs.io](https://elevenlabs.io)

4. Create a `.env` file with your API keys:
   ```
   NEWS_API_KEY=your_news_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```

5. Set up audio output:
   - Either create the default directory:
     ```bash
     # On Mac/Linux:
     mkdir -p "$HOME/Desktop/AI music news audio"
     # On Windows (in Command Prompt):
     mkdir "%USERPROFILE%\Desktop\AI music news audio"
     ```
   - Or modify this line in `config.py` with your preferred path:
     ```python
     AUDIO_DIR = "/Users/bruh/Desktop/AI music news audio"  # Change this path
     ```

6. Run the agent:
   ```bash
   python main.py
   ```

The agent will fetch recent AI music news, generate a summary, and create an audio file in your specified directory.