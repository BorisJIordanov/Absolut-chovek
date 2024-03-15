# import openai
# from whisper import load_model

# def transcribe_audio(audio_path):
#     model = load_model("base")  # Load a Whisper model; you can choose another model based on your needs.
#     result = model.transcribe(audio_path)
#     print(result["text"])
#     return result["text"]



# # Example usage
# audio_path = "file.wav"
# transcribed_text = transcribe_audio(audio_path)
# chatgpt_response = chat_with_chatgpt(transcribed_text)
# print(chatgpt_response)
#Import the openai Library
from openai import OpenAI
import openai

# Create an api client
client = OpenAI(api_key="your_api_key_here")

# Load audio file
audio_file= open("C:\\Users\\user\\Desktop\\hacktues_10_2.0\\Recording.wav", "rb")

# Transcribe
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
# Print the transcribed text
print(transcription.text)

def chat_with_chatgpt(transcribed_text):
    openai.api_key = "your_api_key_here"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "system", "content": "Your main purpose is to answer to 4-8 year old kids in a playful and understandable way.p"},{"role": "user", "content": transcribed_text}]
    )
    return response.choices[0].message.content

print(chat_with_chatgpt(transcription.text))