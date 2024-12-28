# <｜placeholder_replace_marker｜>
from pathlib import Path
from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(api_key='your-api-key-here')

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!",
)
response.stream_to_file(speech_file_path)