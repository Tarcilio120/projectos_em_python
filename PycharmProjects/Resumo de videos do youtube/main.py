import sys
from pytubefix import YouTube
import ffmpeg
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='YOUR_API_KEY')

# Check if a URL is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python main.py <YouTube_URL>")
    sys.exit(1)

# Get the URL from command line arguments
url = sys.argv[1]
filename = "audio.wav"

# Download audio from YouTube
yt = YouTube(url)
stream = yt.streams.filter(only_audio=True).first()
ffmpeg.input(stream.url).output(filename, format='wav', loglevel="error").run()

# Create the transcription
with open(filename, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file).text

# Request a summary of the transcription
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Você é um assistente que resume vídeos e responde em formato Markdown."},
        {"role": "user", "content": f"Descreva o seguinte vídeo: {transcription}"}
    ]
)

# Write the summary to a Markdown file
with open("resume.md", "w") as md_file:
    md_file.write(completion.choices[0].message.content)
