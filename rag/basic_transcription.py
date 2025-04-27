import os
from openai import OpenAI
from upsert_to_pinecone import upsert_to_pinecone
# from chunk_texts import chunk_gpt_tokens


# Create an api client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# Load audio file
audio_file = open("videos/roast.mp4", "rb")

# Transcribe
transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file,
  language='en'
)

print(transcription.text)
# gpt_chunks = chunk_gpt_tokens(transcription.text, chunk_size=50, overlap=25)

# for chunk in gpt_chunks:
#   upsert_to_pinecone(chunk['cleaned_text'], metadata={'content': chunk['raw_text'], 'video_id': 'videos/roast.mp4', 'category': 'Memes'})

upsert_to_pinecone(transcription.text, metadata={'video_id':'videos/roast.mp4','category':'Memes'})