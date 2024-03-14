import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import keyboard

def record_with_space_stop(filename, fs=44100, channels=2):
    """
    Starts recording audio and stops when the space bar is pressed.
    
    :param filename: Filename where the recording will be saved.
    :param fs: Sampling frequency.
    :param channels: Number of audio channels.
    """
    global stop_recording
    stop_recording = False
    recorded_data = []  # List to hold recorded audio frames

    def check_space_press():
        global stop_recording
        keyboard.wait('space')  # Wait until space bar is pressed
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
            np_data = np.concatenate(recorded_data, axis=0)  # Concatenate all recorded audio frames
            write(filename, fs, np_data)  # Save the recording as a WAV file
            print(f"Recording finished. File saved as {filename}")

# Example usage
filename = "C:\\Users\\user\\Desktop\\Absolut Person\\recording.wav"
record_with_space_stop(filename)
