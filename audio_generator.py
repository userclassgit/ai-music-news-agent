import os
from pathlib import Path
from elevenlabs import generate, save, set_api_key
import logging
from config import AUDIO_DIR, ELEVENLABS_API_KEY

class AudioGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        set_api_key(ELEVENLABS_API_KEY)
    
    def process_article(self, summary: str) -> str:
        """Generate audio for the article summary."""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(AUDIO_DIR, exist_ok=True)
            
            # Create a clean filename from the first 50 chars of summary
            filename = "".join(c if c.isalnum() else "_" for c in summary[:50])
            filename = f"{filename}.mp3"
            output_path = os.path.join(AUDIO_DIR, filename)
            
            # Generate and save audio
            audio = generate(
                text=summary,
                voice="Josh",  # Professional male voice
                model="eleven_monolingual_v1"
            )
            save(audio, output_path)
            
            self.logger.info(f"Audio saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating audio: {str(e)}")
            raise
