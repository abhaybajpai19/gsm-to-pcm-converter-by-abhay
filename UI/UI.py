import streamlit as st
import requests
from pydub import AudioSegment
import io

st.title("GSM WAV to PCM WAV Converter & Player")

url = st.text_input(" Paste GSM WAV File URL", "")

if url:
    try:
        st.info(" Downloading audio file...")
        response = requests.get(url)
        audio_data = io.BytesIO(response.content)

        st.success("✅ File downloaded! Converting now...")

        # Convert GSM WAV to PCM WAV using ffmpeg
        audio = AudioSegment.from_file(audio_data, format="wav")
        pcm_wav = io.BytesIO()
        audio.export(pcm_wav, format="wav", codec="pcm_s16le")
        pcm_wav.seek(0)

        st.success("✅ Conversion complete!")

        st.audio(pcm_wav, format="audio/wav")

        # Optional: Allow download
        st.download_button(label="⬇️ Download PCM WAV", data=pcm_wav, file_name="converted_output.wav", mime="audio/wav")

    except Exception as e:
        st.error(f"Error: {str(e)}")
