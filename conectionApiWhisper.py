import requests
import os

def transcribe_audio_whisper(audio_file_path, api_key):
    """
    Transcribes an audio file using OpenAI's Whisper API.

    Parameters:
    - audio_file_path: The path to the audio file to transcribe.
    - api_key: Your OpenAI API key.

    Returns:
    - The transcribed text if successful, None otherwise.
    """
    url = "https://api.openai.com/v1/whisper"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    try:
        with open(audio_file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(url, headers=headers, files=files)
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        return None

    try:
        if response.status_code == 200:
            print("Transcription successful!")
            data = response.json()
            if 'text' in data:
                return data['text']
            else:
                print("Transcription was successful but no text was returned.")
                return None
        else:
            print(f"Error during transcription: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while processing the response: {e}")
        return None

# Example usage
def main():
    api_key = os.getenv("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")  # It's safer to use an environment variable for the API key
    audio_file_path = 'C:\\Users\\user\\Desktop\\Absolut Person\\recording.wav'
    transcription = transcribe_audio_whisper(audio_file_path, api_key)
    if transcription:
        print("Transcription:", transcription)

if __name__ == "__main__":
    main()
