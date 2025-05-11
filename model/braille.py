import speech_recognition as sr
import pickle
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Braille translation mappings
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

CAPITAL = chr(10272)
NUMBER = chr(10300)
UNRECOGNIZED = '?'
open_quotes = True

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
        return CAPITAL + letters.get(char)
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

# Feature extraction function for SVM model
def extract_features(audio_data):
    # Placeholder for actual feature extraction logic, e.g., MFCCs
    return np.random.rand(1, 13)  # Example: 13 MFCCs

# Load the pre-trained SVM model
with open('model.pkl', 'rb') as model_file:
    svm_model = pickle.load(model_file)

# Initialize the recognizer
r = sr.Recognizer()

# Use the microphone as source for input
with sr.Microphone() as source:
    print("Speak:")
    audio = r.listen(source)

try:
    txt = r.recognize_google(audio)
    print("You said: ", txt)

    # Extract features from the audio for SVM classification
    features = extract_features(audio)
    speech_quality = svm_model.predict(features)[0]

    # Translate the recognized text to Braille
    braille_output = translate(txt)

    # Determine speech quality
    quality_label = "good" if speech_quality == 1 else "poor"

    # Output results
    print("Speech Quality:", quality_label)
    print("Braille Translation:", braille_output)

    # -------- EVALUATION METRICS SECTION --------
    # Simulating a test set for demonstration (real use: replace with actual test labels)
    y_true = np.random.choice([0, 1], size=10)  # Random true labels
    y_pred = svm_model.predict(np.random.rand(10, 13))  # Random features for prediction

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=1)
    rec = recall_score(y_true, y_pred, zero_division=1)
    f1 = f1_score(y_true, y_pred, zero_division=1)

    print("\n--- Evaluation Metrics ---")
    print(f"Accuracy: {acc:.2f}")
    print(f"Precision: {prec:.2f}")
    print(f"Recall: {rec:.2f}")
    print(f"F1 Score: {f1:.2f}")

except sr.UnknownValueError:
    print("Could not understand speech")

except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
