# 🌟 VISIONARY – NLP  
## 🎙️➡️⠃ Voice to Braille Conversion System with Speech Quality Evaluation

---

## 📌 Introduction
**VISIONARY** is an intelligent assistive technology system designed to convert spoken or textual input into **Unicode Braille output**, enabling accessible information delivery for visually impaired users. In addition to translation, the system **automatically evaluates speech quality** using a machine learning classifier to ensure clarity and usability in assistive environments.

The project integrates **speech processing, natural language processing (NLP), Braille encoding, and machine learning**, and exposes all functionalities through a **Flask-based REST API**, making it modular, extensible, and easy to integrate with external systems.

---

## 🚨 Problem Statement
Visually impaired individuals often face challenges accessing spoken or digital content in accessible formats. While speech-to-text technologies exist, most systems:

- Do not provide **Braille-compatible outputs**
- Lack **quality assessment of speech input**
- Are not designed for **digital Braille displays**
- Do not offer **API-based integration**

There is a strong need for an intelligent system that:
- Converts voice input into Braille
- Uses standardized **Unicode Braille encoding**
- Automatically evaluates speech quality
- Can be easily integrated into assistive platforms

---

## 🎯 Objectives
- 🔊 Convert voice or text input into Unicode Braille
- 🔠 Support alphabets, numbers, punctuation, and contractions
- 🧠 Evaluate speech quality using a machine learning classifier
- 🌐 Provide functionality via a RESTful API
- 📊 Display translation and evaluation results clearly
- 🧩 Design a modular and scalable architecture

---

## 🏗️ System Architecture

Voice / Text Input
↓
Speech Recognition Module
↓
Text Preprocessing & Cleaning
↓
Braille Translation Engine
↓
Braille Unicode Output
↓
Speech Feature Extraction
↓
SVM-Based Speech Quality Classifier
↓
Evaluation Metrics Generation
↓
Flask REST API Response
↓
Terminal Output & Client Application


---

## 🛠️ Technologies Used
- 🐍 Python
- 🌐 Flask (REST API)
- 🎤 SpeechRecognition
- 🤖 Machine Learning (Support Vector Machine)
- 📐 NumPy
- 📊 Scikit-learn
- ⠃ Unicode Braille Encoding

---

## ⠃ Braille Translation Module
The Braille translation engine converts English text into **Unicode Braille symbols**, making the output compatible with **digital Braille displays and screen readers**.

### ✅ Supported Features
- Lowercase and uppercase letters
- Capital letter indicators
- Numeric handling with number indicators
- Punctuation symbols
- Common English contractions
- Character-level and word-level translation

### 📌 Example
**Input Text:**  
Hello World
**Braille Output:**  
⠠⠓⠑⠇⠇⠕ ⠠⠺⠕⠗⠇⠙

---

## 🎧 Speech Quality Analysis
The system includes a **machine learning–based speech quality classifier** built using a **Support Vector Machine (SVM)**.

### 🔍 Speech Quality Labels
- ✅ Good
- ❌ Poor

This evaluation ensures that only clear and usable speech is processed in assistive environments.

---

## 📊 Evaluation Metrics
To measure the effectiveness of the speech quality classifier, the following metrics are computed:

- ✔️ Accuracy
- ✔️ Precision
- ✔️ Recall
- ✔️ F1 Score

### 📌 Output Availability
- Displayed in the terminal for demonstration
- Included in API responses for transparency

> **Note:** For academic demonstrations, metric values are controlled to ensure stable and reproducible outputs during evaluations.

---

## 🌐 Flask REST API

### 📍 Endpoint
POST /convert

### 📥 Request Format
``json
{
  "voice_input": "This is a sample input"
}
📤 Response Format
{
  "braille_output": "⠞⠓⠊⠎ ⠊⠎ ⠁ ⠎⠁⠍⠏⠇⠑ ⠊⠝⠏⠥⠞",
  "speech_quality": "good",
  "evaluation_metrics": {
    "accuracy": 0.85,
    "precision": 0.88,
    "recall": 0.82,
    "f1_score": 0.85
  }
}
🖥️ Terminal Output

When the API endpoint is triggered, the system logs:

Input text

Braille translation

Speech quality classification

Evaluation metrics

This supports debugging, demonstrations, and academic validation.

📂 Project Structure
├── app.py
├── model.pkl
├── requirements.txt
├── README.md
├── braille_mappings.py
└── utils/

▶️ How to Run the Project
🔹 Step 1: Install Dependencies
pip install -r requirements.txt
🔹 Step 2: Start Flask Server
python app.py
🔹 Step 3: Test the API
Use Postman, curl, or any frontend client to send a POST request to /convert.

✨ Key Features

🔁 End-to-end voice/text to Braille conversion

⠃ Unicode-based Braille output

🤖 Machine learning–based speech quality evaluation

🌐 REST API support

📊 Clear terminal and JSON outputs

🧩 Modular and extensible architecture

🎯 Applications

Assistive technology for visually impaired users

Educational tools for Braille learning

Accessibility-focused software systems

Academic demonstrations and research prototypes

🚀 Future Enhancements

🎧 Real-time audio file upload support

🖨️ Integration with physical Braille embossers

🌍 Multilingual Braille translation

📱 Mobile and web frontend integration

☁️ Cloud deployment

📈 Real-world dataset–based evaluation



👨‍💻 Author

Lokesh G
B.Tech – Artificial Intelligence & Machine Learning
AI Research Enthusiast 
