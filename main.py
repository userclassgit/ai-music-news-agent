import os
import logging
from datetime import datetime
import google.generativeai as genai
from audio_generator import AudioGenerator
from config import AUDIO_DIR, GEMINI_API_KEY

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AINewsBot:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
        self.audio_generator = AudioGenerator()
    
    def get_news_summary(self):
        """Get AI music news summary using Gemini API."""
        query = """
# Role

You are a highly skilled news curator who specializes in accurately finding news content about a given topic published within a given timeframe and summarizing news events.

# Task

Find news articles about music and AI published in the past 2 days and summarize them. Use this step-by-step process:
  1. Search "Music AI" on Google news to find articles published in the past 2 days that have to do with both AI and music. Do not read the articles yet. Only pay attention to the titles.
  2. If a title contains words related to music and AI (e.g., Taylor Swift bashes AI generated music, The UI passes bill that permits use of copyrighted songs in AI training) AND the meaning of the title does not match the title of an article you have already read before (meaning the article is not about the same news event as an article you saw before), read the entire article and summarize it.
  3. Keep doing this until you have summarized all the AI and music related articles that came out in the past 2 days that satisfy the 2 conditions in the previous step.
  4. Give me all the summaries in your response. If a news article is outside the 2-day timeframe, do not include it in your response. Do not even mention it.

# Specifics

-This task is vital to my career, so please carefully follow each step I listed above.
-If a news article is outside the 2-day timeframe, do not include it in your response. Do not even mention it.
-Always check when the article was published before you read it. If it was not published in the past 2 days, do not read or summarize it.
-If there are no news about both AI and music in the past 2 days, simply tell me there's no news about this topic.
-Include the publishing date for each summary.

# Context

I am a busy content creator who publishes videos about AI and music. Your role in finding AI and music related news articles and summarizing them is essential because it will save me a lot of time and help me create accurate and high quality content for my audience, therefore my audience and I greatly value your ability to accurately find and summarize relevant news articles.

# Examples
###Example 1
News article title: AI is being used to de-age singers. This is just the tip of an iceberg
Publishing date: 3 days ago
This news article is relevant to both AI and music but was published 3 days ago which is outside the 2-day timeframe, therefore you should NOT read or summarize it.

###Example 2
News article title: Marlon Wayans drops AI-generated country music diss track to taunt Soulja Boy amid feud
Publishing date: 23 hours ago
This news article is relevant to both AI and music and was published within the past 2 days, therefore you should read and summarize it.

###Example 3
News article title: Marlon Wayans releases AI-generated diss track on Soulja Boy
Publishing date: 18 hours ago
This news article is relevant to both AI and music and was published within the past 2 days, but it's about the same news event as the previous article, therefore you should NOT read or summarize it.

###Example 4
News article title: Taylor Swift releases diss track on Kanye West
Publishing date: 19 days ago
This news article is relevant to music but not to AI. It was published 19 days ago which is outside the 2-day timeframe, therefore you should NOT read or summarize it.

# Notes
-If a news article is outside the 2-day timeframe, do not include it in your response. Do not even mention it.
        """
        
        try:
            response = self.model.generate_content(query)
            logger.info("Successfully generated news summary using Gemini API")
            return response.text
        except Exception as e:
            logger.error(f"Error getting news summary: {str(e)}")
            return None

    def run(self):
        """Main bot execution loop."""
        try:
            logger.info("Starting AI News Bot")
            
            # Get news summary from Sonar
            summary = self.get_news_summary()
            if not summary:
                logger.info("No news summary generated")
                return
            
            # Generate audio file
            audio_path = self.audio_generator.process_article(summary)
            logger.info(f"Audio generated: {audio_path}")
            
        except Exception as e:
            logger.error(f"Bot execution error: {str(e)}")


    def test_prompt(self):
        """Test the Gemini prompt without audio conversion."""
        try:
            logger.info("Testing Gemini prompt...")
            summary = self.get_news_summary()
            if summary:
                print("\nGemini Response:\n")
                print(summary)
            else:
                print("No summary generated")
        except Exception as e:
            logger.error(f"Error in test: {str(e)}")

if __name__ == "__main__":
    bot = AINewsBot()
    # For testing, use test_prompt() instead of run()
    bot.test_prompt()
