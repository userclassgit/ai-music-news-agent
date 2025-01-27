import os
from pathlib import Path
from elevenlabs import generate, save, set_api_key
import logging
from news_scraper import NewsArticle
from config import TEMP_DIR, ELEVENLABS_API_KEY

class AudioGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        set_api_key(ELEVENLABS_API_KEY)
        
    def create_script(self, article: NewsArticle) -> str:
        """Create a natural-sounding script from the article."""
        script = [
            "Welcome to AI Music News Update.",
            f"Today's story: {article.title}",
            "",
            article.content,
            "",
            f"This story comes from {article.source}.",
            "Thanks for listening to AI Music News Update."
        ]
        return "\n".join(script)
    
    def generate_audio(self, script: str, output_path: str) -> str:
        """Generate audio using ElevenLabs API for more natural voice."""
        try:
            audio = generate(
                text=script,
                voice="Josh",  # Professional male voice
                model="eleven_monolingual_v1"
            )
            
            save(audio, output_path)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating audio: {str(e)}")
            raise

    def process_article(self, article: NewsArticle) -> str:
        """Process an article into audio news update."""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(TEMP_DIR, exist_ok=True)
            
            # Generate script
            script = self.create_script(article)
            
            # Generate audio file
            output_path = os.path.join(TEMP_DIR, f"news_update_{article.title[:30]}.mp3")
            self.generate_audio(script, output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error processing article: {str(e)}")
            raise
