import streamlit as st
from pydub import AudioSegment
import requests
import os
import zipfile
import base64

st.title("🎧 WAV to PCM Converter by Abhay Bajpai")

# Make sure output folder exists
os.makedirs("converted", exist_ok=True)

option = st.radio("Choose Input Method:", ["🔗 Convert via URL", "📁 Upload .wav files"])

# Function to play audio in Streamlit
def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    audio.export("converted/temp.wav", format="wav")  # Save as temp WAV file
    st.audio("converted/temp.wav", format="audio/wav")

if option == "🔗 Convert via URL":
    url = st.text_input("Enter WAV Audio URL:")

    if st.button("Convert URL to PCM"):
        if url:
            try:
                file_name = "converted/input_url.wav"
                response = requests.get(url)
                with open(file_name, "wb") as f:
                    f.write(response.content)

                # Play audio directly from URL
                st.subheader("🎵 Playing the Original Audio:")
                play_audio(file_name)

                audio = AudioSegment.from_file(file_name, format="wav")
                output_path = "converted/output_url.pcm"
                audio.export(output_path, format="raw")

                st.success("✅ Converted successfully!")
                with open(output_path, "rb") as f:
                    st.download_button("⬇️ Download PCM File", f, file_name="output_url.pcm")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a valid URL.")

# Upload section
elif option == "📁 Upload .wav files":
    uploaded_files = st.file_uploader("Upload one or more WAV files", type=["wav"], accept_multiple_files=True)

    if st.button("Convert Uploaded Files to PCM"):
        if uploaded_files:
            zip_filename = "converted_pcm_files.zip"
            with zipfile.ZipFile(zip_filename, "w") as zipf:
                for uploaded_file in uploaded_files:
                    wav_data = uploaded_file.read()
                    temp_path = f"converted/{uploaded_file.name}"
                    pcm_path = temp_path.replace(".wav", ".pcm")

                    with open(temp_path, "wb") as f:
                        f.write(wav_data)

                    # Play the uploaded file
                    st.subheader(f"🎵 Playing {uploaded_file.name}:")
                    play_audio(temp_path)

                    audio = AudioSegment.from_wav(temp_path)
                    audio.export(pcm_path, format="raw")

                    zipf.write(pcm_path, arcname=os.path.basename(pcm_path))

            st.success("✅ All files converted and zipped!")
            with open(zip_filename, "rb") as f:
                st.download_button("⬇️ Download All PCM Files (ZIP)", f, file_name=zip_filename)
        else:
            st.warning("⚠️ Please upload at least one .wav file.")
