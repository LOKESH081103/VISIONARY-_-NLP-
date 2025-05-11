import PyPDF2
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Step 1: Extract text from PDFs
def extract_text_from_pdf(file_path):
    text_lines = []
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            lines = page.extract_text().split('\n')
            text_lines.extend(lines)
    return text_lines

# Load Braille and English PDFs
braille_lines = extract_text_from_pdf("C:\Users\gloke\OneDrive\Desktop\DL_MAIN\braille.pdf")
english_lines = extract_text_from_pdf("C:\Users\gloke\OneDrive\Desktop\DL_MAIN\english.pdf")

# Step 2: Basic preprocessing (strip empty lines and align)
braille_lines = [line.strip() for line in braille_lines if line.strip()]
english_lines = [line.strip() for line in english_lines if line.strip()]

# Ensure they have same number of lines
min_len = min(len(braille_lines), len(english_lines))
braille_lines = braille_lines[:min_len]
english_lines = english_lines[:min_len]

# Step 3: Simulate features for SVM
# In reality you'd extract real embeddings. Here we use dummy vectors.
def text_to_dummy_vector(text):
    return np.random.rand(13)  # Simulate MFCC-like feature vector

# Create dataset
X = np.array([text_to_dummy_vector(b) for b in braille_lines])
y = np.array(english_lines)  # We'll use this for classification demo

# Encode English outputs to numeric labels (simulate classification)
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Step 4: Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Step 5: Train SVM
clf = svm.SVC()
clf.fit(X_train, y_train)

# Step 6: Predict and Decode
y_pred = clf.predict(X_test)
y_pred_labels = encoder.inverse_transform(y_pred)

# Step 7: Evaluation
acc = accuracy_score(y_test, y_pred)
print(f" SVM Mapping Accuracy: {acc * 100:.2f}%")

# Step 8: Display a few  mappings
print("\nSample Mappings:")
for i in range(5):
    braille_sample = braille_lines[i]
    english_sample = english_lines[i]
    print(f"BRAILLE: {braille_sample}\n→ ENGLISH: {english_sample}\n")
