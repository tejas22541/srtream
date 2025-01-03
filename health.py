import streamlit as st
import speech_recognition as sr
from langchain_groq import ChatGroq
import os

# Step 1: Transcribe audio to text
def transcribe_audio(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

# Step 2: Get health guidance using ChatGroq
def get_health_guidance_from_groq(symptoms_text):
    prompt = f"Identify symptoms in this audio input and suggest possible health guidance: {symptoms_text}"
    llm = ChatGroq(
        temperature=0,
        groq_api_key='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',
        model_name="llama-3.1-8b-instant"
    )
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App
def main():
    st.title("Health Assistant Tool")
    st.write("Upload an audio file describing symptoms to receive health guidance.")

    # Audio file uploader
    audio_file = st.file_uploader("Upload an audio file (WAV format recommended):", type=["wav", "mp3"])

    if audio_file is not None:
        # Save the audio file temporarily
        temp_audio_path = "temp_audio.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_file.read())

        # Play the uploaded audio
        st.audio(temp_audio_path, format="audio/wav")

        st.info("Processing audio file...")
        
        try:
            # Transcribe audio
            symptoms_text = transcribe_audio(temp_audio_path)
            st.success(f"Transcription: {symptoms_text}")
            
            # Get health guidance
            health_guidance = get_health_guidance_from_groq(symptoms_text)
            st.header("Health Guidance")
            st.write(health_guidance)
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
        
        # Clean up temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    main()
