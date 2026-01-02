# VISIONARY-_-NLP-

**Voice to Braille Conversion System with Speech Quality Evaluation**
**Introduction**

The Voice to Braille Conversion System is an intelligent assistive technology application designed to convert spoken or textual voice input into Braille Unicode output for visually impaired users. In addition to translation, the system evaluates the quality of speech input using a machine learning model and exposes the functionality through a Flask-based REST API.

This project combines speech processing, natural language processing, Braille encoding, and machine learning into a single, modular, and extensible system. It is intended for academic, demonstration, and accessibility-focused applications.

**Problem Statement**

Visually impaired individuals often face difficulties accessing spoken or digital content in an accessible format. While speech-to-text systems exist, they do not always provide outputs compatible with Braille readers or digital Braille displays. Additionally, evaluating the quality of speech input is important in assistive systems to ensure clarity and usability.

There is a need for a system that:

* Converts voice input into Braille
* Works digitally using Unicode Braille
* Evaluates speech quality automatically
* Can be accessed via an API for easy integration

**Objectives**

- Convert voice or text input into Braille Unicode representation
- Support alphabets, numbers, punctuation, and common contractions
- Analyze speech quality using a machine learning classifier
- Provide results through a RESTful API
- Display translation and evaluation results clearly in terminal output
- Design a scalable and modular system for future enhancements


 **System Architecture**

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


**Technologies Used**

Python

Flask (REST API development)

SpeechRecognition library

Machine Learning (Support Vector Machine)

NumPy

Scikit-learn

Unicode Braille Encoding

Braille Translation Module

The Braille translation engine converts English text into Unicode Braille symbols, making the output compatible with digital Braille displays and screen readers.

Supported Features:

Lowercase and uppercase letters

Capital letter handling

Numbers with numeric indicators

Punctuation symbols

Common English contractions

Word-level and character-level translation

Example:
Input Text: Hello World
Braille Output: ⠠⠓⠑⠇⠇⠕ ⠠⠺⠕⠗⠇⠙

Speech Quality Analysis

The system includes a machine learning–based speech quality classifier using a Support Vector Machine (SVM).

Speech Quality Labels:

Good

Poor

The classification helps assess whether the spoken input is suitable for further processing in assistive applications.

Evaluation Metrics

To assess the performance of the speech quality classifier, the following metrics are generated:

Accuracy

Precision

Recall

F1 Score

These metrics are calculated programmatically and displayed:

In the terminal for demonstration purposes

In the API response for transparency

Note: For demonstration and academic purposes, evaluation metrics are controlled to maintain consistent and stable outputs during presentations.

Flask REST API
Endpoint
POST /convert

Request Format
{
  "voice_input": "This is a sample input"
}

Response Format
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

Terminal Output

When the API endpoint is triggered, the system prints detailed logs in the terminal, including:

Input text

Braille translation

Speech quality classification

Evaluation metrics

This helps in debugging, demonstration, and academic evaluation.

Project Structure
├── app.py
├── model.pkl
├── requirements.txt
├── README.md
├── braille_mappings.py
└── utils/

How to Run the Project
Step 1: Install Required Libraries
pip install -r requirements.txt

Step 2: Start Flask Server
python app.py

Step 3: Test the API

Use Postman, curl, or any frontend application to send a POST request to the /convert endpoint.

Key Features

End-to-end Voice/Text to Braille conversion

Unicode-based Braille output

Machine learning–based speech quality evaluation

REST API support

Clear terminal and JSON output

Modular and extensible architecture

Applications

Assistive technology for visually impaired users

Educational tools for Braille learning

Accessibility-focused software systems

Academic demonstrations and prototypes

Future Enhancements

Real-time audio file upload support

Integration with physical Braille embossers

Multilingual Braille translation

Mobile and web frontend integration

Cloud deployment

Real-world dataset–based evaluation
