import pickle
import pyaudio
import wave
import os
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer

# Braille translation mappings (same as before)
letters = {'a': chr(10241), 'b': chr(10243), 'c': chr(10249), 'd': chr(10265), 'e': chr(10257),
           'f': chr(10251), 'g': chr(10267), 'h': chr(10259), 'i': chr(10250), 'j': chr(10266),
           'k': chr(10245), 'l': chr(10247), 'm': chr(10253), 'n': chr(10269), 'o': chr(10261),
           'p': chr(10255), 'q': chr(10271), 'r': chr(10263), 's': chr(10254), 't': chr(10270),
           'u': chr(10277), 'v': chr(10279), 'w': chr(10298), 'x': chr(10285), 'y': chr(10301),
           'z': chr(10293)}

contractions = {'but': chr(10243), 'can': chr(10249), 'do': chr(10265), 'every': chr(10257),
                'from': chr(10251), 'go': chr(10267), 'have': chr(10259), 'just': chr(10266),
                'knowledge': chr(10280), 'like': chr(10296), 'more': chr(10253), 'not': chr(10269),
                'people': chr(10255), 'quite': chr(10271), 'rather': chr(10263), 'so': chr(10254),
                'that': chr(10270), 'us': chr(10277), 'very': chr(10279), 'it': chr(10285),
                'you': chr(10301), 'as': chr(10293), 'and': chr(10287), 'for': chr(10303),
                'of': chr(10295), 'the': chr(10286), 'with': chr(10302), 'will': chr(10298),
                'his': chr(10278), 'in': chr(10260), 'was': chr(10292), 'to': chr(10262)}

punctuation = {',': chr(10242), ';': chr(10246), ':': chr(10258), '.': chr(10290), '!': chr(10262),
               '(': chr(10294), ')': chr(10294), '“': chr(10278), '”': chr(10292), '?': chr(10278),
               '/': chr(10252), '#': chr(10300), '\'': chr(10244), '…': chr(10290) + chr(10290) + chr(10290),
               '’': chr(10244), '­': chr(10276), '-': chr(10276), '‐': chr(10276), '‑': chr(10276),
               '‒': chr(10276), '–': chr(10276), '—': chr(10276), '―': chr(10276)}

numbers = {'1': chr(10241), '2': chr(10243), '3': chr(10249), '4': chr(10265), '5': chr(10257),
           '6': chr(10251), '7': chr(10267), '8': chr(10259), '9': chr(10250), '0': chr(10266)}

CAPITAL = chr(10272)  # ⠠
NUMBER = chr(10300)  # ⠼
UNRECOGNIZED = '?'
open_quotes = True

# --- Braille Translation Functions (same as before) ---
def extract_words(string):
    words = string.split(" ")
    result = []
    for word in words:
        temp = word.split("\n")
        for item in temp:
            result.append(item)
    return result

def trim(word):
    while len(word) != 0 and not word[0].isalnum():
        word = word[1:]
    while len(word) != 0 and not word[-1].isalnum():
        word = word[:-1]
    return word

def numbers_handler(word):
    if word == "":
        return word
    result = word[0]
    if word[0].isdigit():
        result = NUMBER + numbers.get(word[0])
    for i in range(1, len(word)):
        if word[i].isdigit() and word[i-1].isdigit():
            result += numbers.get(word[i])
        elif word[i].isdigit():
            result += NUMBER + numbers.get(word[i])
        else:
            result += word[i]
    return result

def capital_letters_handler(word):
    if word == "":
        return word
    result = ""
    for char in word:
        if char.isupper():
            result += CAPITAL + char.lower()
        else:
            result += char.lower()
    return result

def find_utf_code(char):
    if len(char) != 1:
        return -1
    for i in range(0, 55000):
        if char == chr(i):
            return i

def char_to_braille(char):
    if char == "\n":
        return "\n"
    elif char == "\"":
        global open_quotes
        if open_quotes:
            open_quotes = not open_quotes
            return punctuation.get("“")
        else:
            open_quotes = not open_quotes
            return punctuation.get("”")
    elif char in letters and char.isupper():
        return CAPITAL + letters.get(char.lower())
    elif char in letters:
        return letters.get(char)
    elif char in punctuation:
        return punctuation.get(char)
    else:
        print("Unrecognized Symbol:", char, "with UTF code:", find_utf_code(char))
        return UNRECOGNIZED

def word_to_braille(word):
    if word in contractions:
        return contractions.get(word)
    else:
        result = ""
        for char in word:
            result += char_to_braille(char)
        return result

def build_braille_word(trimmed_word, shavings, index, braille):
    if shavings == "":
        braille += word_to_braille(trimmed_word)
    else:
        for i in range(0, len(shavings)):
            if i == index and trimmed_word != "":
                braille += word_to_braille(trimmed_word)
            braille += word_to_braille(shavings[i])
        if index == len(shavings):
            braille += word_to_braille(trimmed_word)
    return braille

def translate(string):
    braille = ""
    words = extract_words(string)
    for word in words:
        word = numbers_handler(word)
        word = capital_letters_handler(word)
        trimmed_word = trim(word)
        untrimmed_word = word
        index = untrimmed_word.find(trimmed_word)
        shavings = untrimmed_word.replace(trimmed_word, "")
        braille = build_braille_word(trimmed_word, shavings, index, braille) + " "
    return braille[:-1]

# --- Audio Recording Functions (same as before) ---
# Define constants
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1  # Mono audio
RATE = 16000  # Sampling rate
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 5  # Duration of recording
OUTPUT_FILENAME = "speech.wav"  # Output file name

# Function to record audio from microphone
def record_audio():
    audio = pyaudio.PyAudio()

    print("🎤 Recording... Speak now!")
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("✅ Recording finished!")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save audio to a WAV file
    wf = wave.open(OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to process and convert audio (if needed)
def convert_audio():
    sound = AudioSegment.from_wav(OUTPUT_FILENAME)
    sound = sound.set_channels(1).set_frame_rate(16000)  # Ensure compatibility
    sound.export(OUTPUT_FILENAME, format="wav")

# --- Speech Recognition with Vosk ---
def recognize_speech_vosk():
    model_path = "vosk-model-small-en-us-0.15"  # Default English model path - ADJUST IF NEEDED
    try:
        if not os.path.exists(model_path):
            print(f"Error: Vosk model not found at {model_path}")
            print("Please download a Vosk model from https://alphacephei.com/vosk/models and place it in the current directory or provide the correct path.")
            return None

        model = Model(model_path)
        wf = wave.open(OUTPUT_FILENAME, "rb")
        if wf.getnchannels() != 1 or wf.getframerate() != 16000 or wf.getsampwidth() != 2:
            print("Warning: Audio file should be mono 16kHz 16-bit.")
            return None
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)  # Enable word-level timestamps (optional)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                print("Partial Result:", result)
            else:
                partial_result = rec.PartialResult()
                print("Partial Result:", partial_result)

        final_result = rec.FinalResult()
        print("📝 Recognized Text (Vosk):", final_result['text'])
        return final_result['text']

    except FileNotFoundError:
        print(f"Error: Vosk model not found at {model_path}")
        print("Please download a Vosk model and place it in the specified path.")
        return None
    except Exception as e:
        print(f"Error during Vosk recognition: {e}")
        return None

# --- Feature Extraction and SVM (Placeholder - Needs Actual Implementation) ---
def extract_features(audio_data, sample_rate):
    # This is a placeholder. Implementing robust audio feature extraction (e.g., MFCC)
    # requires signal processing knowledge and libraries like librosa or python_speech_features.
    # The quality of these features significantly impacts SVM performance.
    # For now, we'll return a dummy feature.
    return np.random.rand(1, 13)

# --- Main Execution ---
if __name__ == "__main__":
    record_audio()  # Step 1: Record from Mic
    convert_audio()  # Step 2: Ensure correct audio format

    recognized_text = recognize_speech_vosk()  # Step 3: Speech-to-Text with Vosk

    if recognized_text:
        # Load the audio file to get the sample rate for feature extraction
        wf = wave.open(OUTPUT_FILENAME, 'rb')
        sample_rate = wf.getframerate()
        audio_frames = wf.readframes(wf.getnframes())
        audio_array = np.frombuffer(audio_frames, np.int16)
        wf.close()

        # Placeholder for loading the pre-trained SVM model
        try:
            with open('model.pkl', 'rb') as model_file:
                svm_model = pickle.load(model_file)
        except FileNotFoundError:
            print("Error: 'model.pkl' not found. Please ensure the model file exists in the same directory.")
            svm_model = None
        except Exception as e:
            print(f"Error loading the model: {e}")
            svm_model = None

        if svm_model:
            # Extract features from the audio
            features = extract_features(audio_array, sample_rate)
            speech_quality = svm_model.predict(features.reshape(1, -1))[0] # Reshape for single sample
            quality_label = "good" if speech_quality == 1 else "poor"
            print("Speech Quality:", quality_label)

            # Translate the recognized text to Braille
            braille_output = translate(recognized_text)
            print("Braille Translation:", braille_output)
        else:
            print("Skipping speech quality assessment and Braille translation due to missing/loading model.")
    else:
        print("Could not recognize speech, skipping further processing.")