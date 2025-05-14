from pydub import AudioSegment
import requests

# Step 1: Audio file download karo
url = "http://203.145.42.91:8807//monitor/Growupnext_2/20250513/OUT-6045-7037216556-20250513-131914-1747122554.1562088.WAV"
response = requests.get(url)

with open("input.wavgsm.wav", "wb") as f:
    f.write(response.content)

# Step 2: Load the GSM-encoded WAV file (FFmpeg will handle it)
audio = AudioSegment.from_file("input.wavgsm.wav", format="wav")

# Step 3: Export as standard PCM WAV
audio.export("output_pcm.wav", format="wav", codec="pcm_s16le")

# Print message with proper encoding
print("Conversion complete! ✅ File saved as output_pcm.wav".encode('utf-8'))
