import os
from pathlib import Path
import requests
import logging
from config import AUDIO_DIR, ELEVENLABS_API_KEY

class AudioGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "Accept": "audio/mpeg",
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
    
    def generate_audio(self, summary: str) -> str:
        """Generate audio for the article summary."""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(AUDIO_DIR, exist_ok=True)
            
            # Create a clean filename from the first 50 chars of summary
            filename = "".join(c if c.isalnum() else "_" for c in summary[:50])
            filename = f"{filename}.mp3"
            output_path = os.path.join(AUDIO_DIR, filename)
            
            # Generate audio using ElevenLabs API
            url = "https://api.elevenlabs.io/v1/text-to-speech/wViXBPUzp2ZZixB1xQuM"  # Bill Oxley voice ID
            
            data = {
                "text": summary,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            # Save the audio file
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            self.logger.info(f"Audio saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating audio: {str(e)}")
            raise
