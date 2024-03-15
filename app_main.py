import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import keyboard
from openai import OpenAI
import openai
from pathlib import Path 
from playsound import playsound 

client = OpenAI(api_key="")

def record_voice(fs=44100, channels=2):
    global stop_recording
    stop_recording = False
    recorded_data = [] 

    def check_space_press():
        global stop_recording
        keyboard.wait('space')  
        stop_recording = True
        print("Stopping recording...")

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        recorded_data.append(indata.copy())  # Append incoming audio data

    # Start checking for space press in a separate thread
    threading.Thread(target=check_space_press, daemon=True).start()

    try:
        # Record audio until "stop_recording" becomes True
        with sd.InputStream(callback=callback, channels=channels, samplerate=fs):
            print("Recording... Press space to stop.")
            while not stop_recording:
                sd.sleep(100)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if recorded_data:  # Check if there is anything to save
            np_data = np.concatenate(recorded_data, axis=0)  # Concatenate all recorded audio framese
            filename= "C:\\Users\\user\\Desktop\\hacktues_10_2.0\\Recording.wav"
            write(filename, fs, np_data)  # Save the recording as a WAV file
            print(f"Recording finished. File saved as {filename}")

def chat_with_chatgpt(transcribed_text):
    openai.api_key = ""
    response = client.chat.completions.create(
        model="gpt-4",  
        messages=[{"role": "system", "content": "Your main purpose is to answer to 4-8 year old kids in a playful and understandable way.p"},{"role": "user", "content": transcribed_text}]
    )
    return response.choices[0].message.content

def transcribe_text_to_audio(input_text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input= input_text
) 
    response.stream_to_file(speech_file_path) 

def transcribe_audio_to_text():
    audio_file= open("C:\\Users\\user\\Desktop\\hacktues_10_2.0\\Recording.wav", "rb")

    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )

    return transcription.text

def  play_audio_file(): 
    path  = Path(__file__).parent / "speech.mp3" 
    playsound(path)
 
while(True):
    record_voice(fs=44100, channels=2)
    transcribed_text = transcribe_audio_to_text()
    answer = chat_with_chatgpt(transcribed_text)
    print(f"Question: {transcribed_text}")
    transcribe_text_to_audio(answer) 
    print(f"Answer: {answer}")
    play_audio_file()
    command = input()
    if(command == "exit"):
        break
