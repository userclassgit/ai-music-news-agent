# AI Music News Audio Generator

An AI agent that automatically generates audio news content about AI and music. The agent:
1. Scrapes news about AI and music from various sources
2. Generates professional audio narration using ElevenLabs
3. Outputs ready-to-use audio files for video production

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```
NEWSAPI_KEY=your_news_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

## Project Structure

- `news_scraper.py`: Handles news collection and filtering
- `audio_generator.py`: Creates audio narration from news articles
- `config.py`: Configuration settings
- `main.py`: Orchestrates the entire process

## Features

- Multi-source news scraping (NewsAPI, RSS feeds)
- Natural-sounding voice narration using ElevenLabs
- Automatic content summarization
- Error handling and logging
- Configurable news sources and filters

## Usage

Run the agent:
```bash
python main.py
```

The agent will:
1. Find relevant AI music news
2. Generate audio narration
3. Save audio files in the `temp` directory

You can then use these audio files as narration for your video content creation.

## Configuration

Edit `config.py` to customize:
- News sources and filters
- Audio quality settings
- Output directories
- Search period for news
