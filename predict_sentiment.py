# predict_sentiment.py
"""
Robust sentiment prediction script.

Behavior:
- Tries user-provided full paths (edit DEFAULT_PATHS if needed).
- Falls back to searching current directory and a couple of commonly used folders.
- If files are not found, prompts the user to enter the folder containing the 3 files.
- Prints helpful errors when something goes wrong.
"""

import os
import sys
import pickle
import numpy as np
from pathlib import Path
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------- CONFIG ----------
# Add any full paths you want the script to try in order (raw strings recommended).
DEFAULT_PATHS = [
    # the path you originally gave (kept here)
    r"C:\Users\Keerthi\OneDrive\Documents\online",
    # other likely places (adjust/remove as you prefer)
    r"C:\Users\Keerthi\OneDrive\Documents\online\predict_sentiment.py",
    r"C:/Users/Keerthi/OneDrive/Documents",
    r"C:/Users/Keerthi/Documents",
    # current working directory will also be checked automatically
]

MODEL_NAME = "sentiment_model.h5"
TOKENIZER_NAME = "tokenizer.pickle"
LABEL_ENCODER_NAME = "label_encoder.pickle"
MAX_LEN = 50   # must match the maxlen used during training
# ----------------------------

def find_files(base_paths):
    """
    Given a list of base folder paths, return the first folder that has all required files.
    If none found, return None.
    """
    # Always try current directory first
    candidate_dirs = [Path.cwd()] + [Path(p) for p in base_paths]

    for folder in candidate_dirs:
        try:
            folder = folder.expanduser().resolve()
        except Exception:
            # skip invalid path strings
            continue

        model_path = folder / MODEL_NAME
        tok_path = folder / TOKENIZER_NAME
        le_path = folder / LABEL_ENCODER_NAME

        if model_path.is_file() and tok_path.is_file() and le_path.is_file():
            return folder, model_path, tok_path, le_path

    return None, None, None, None

def ask_user_for_folder():
    """Prompt user to type the folder where the files are located."""
    print("\nI couldn't find the files automatically.")
    print("Please paste the folder path that contains these files:")
    print(f" - {MODEL_NAME}")
    print(f" - {TOKENIZER_NAME}")
    print(f" - {LABEL_ENCODER_NAME}")
    folder_input = input("Folder path (or type 'exit' to quit): ").strip()
    if folder_input.lower() == "exit" or folder_input == "":
        print("Exiting. Place the three files in the same folder as this script or provide a path next time.")
        sys.exit(1)
    folder = Path(folder_input).expanduser().resolve()
    model_path = folder / MODEL_NAME
    tok_path = folder / TOKENIZER_NAME
    le_path = folder / LABEL_ENCODER_NAME
    if not (model_path.is_file() and tok_path.is_file() and le_path.is_file()):
        print("\nOne or more files not found in that folder. Found files:")
        print(f" - {MODEL_NAME}: {'FOUND' if model_path.is_file() else 'MISSING'}")
        print(f" - {TOKENIZER_NAME}: {'FOUND' if tok_path.is_file() else 'MISSING'}")
        print(f" - {LABEL_ENCODER_NAME}: {'FOUND' if le_path.is_file() else 'MISSING'}")
        # Let user try again recursively
        return ask_user_for_folder()
    return folder, model_path, tok_path, le_path

def load_artifacts(folder, model_path, tok_path, le_path):
    """Load the model and pickles with helpful error messages."""
    print(f"\nLoading files from: {folder}")
    # load model
    try:
        model = load_model(str(model_path))
    except OSError as e:
        print("\nERROR loading model. Details:")
        print(e)
        print("\nPossible reasons:")
        print(" - The file path is incorrect.")
        print(" - The model file is corrupt.")
        print(" - h5py / tensorflow version mismatch.")
        print("Fix by ensuring the file exists and that you trained/saved the model with a compatible tensorflow/h5py.")
        sys.exit(1)
    except Exception as e:
        print("\nUnexpected error while loading model:")
        print(e)
        sys.exit(1)

    # load tokenizer pickle
    try:
        with open(tok_path, "rb") as f:
            tokenizer = pickle.load(f)
    except FileNotFoundError:
        print(f"Tokenizer file not found at {tok_path}")
        sys.exit(1)
    except Exception as e:
        print("Error while loading tokenizer pickle:", e)
        sys.exit(1)

    # load label encoder pickle
    try:
        with open(le_path, "rb") as f:
            label_encoder = pickle.load(f)
    except FileNotFoundError:
        print(f"Label encoder file not found at {le_path}")
        sys.exit(1)
    except Exception as e:
        print("Error while loading label encoder pickle:", e)
        sys.exit(1)

    print("✅ Model and preprocessing files loaded successfully!\n")
    return model, tokenizer, label_encoder

def predict_texts(model, tokenizer, label_encoder, texts):
    """Predict label and probabilities for a single text or list of texts."""
    if isinstance(texts, str):
        texts = [texts]

    seqs = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(seqs, maxlen=MAX_LEN, padding="post")
    probs = model.predict(padded)
    preds = np.argmax(probs, axis=1)
    decoded = label_encoder.inverse_transform(preds)
    return list(zip(decoded, probs))

def main():
    folder, model_path, tok_path, le_path = find_files(DEFAULT_PATHS)

    if folder is None:
        # couldn't auto-find; ask the user
        folder, model_path, tok_path, le_path = ask_user_for_folder()

    model, tokenizer, label_encoder = load_artifacts(folder, model_path, tok_path, le_path)

    # Example predictions
    samples = [
        "The food was absolutely wonderful!",
        "Worst experience ever. I will never come back.",
        "The service was okay, nothing special."
    ]
    results = predict_texts(model, tokenizer, label_encoder, samples)

    for text, (label, prob) in zip(samples, results):
        print("INPUT :", text)
        print("PRED  :", label, "-> probs:", prob)
        print("-" * 50)

    # interactive loop
    print("\nInteractive mode: type a sentence to predict (type 'exit' to quit).")
    while True:
        user_text = input("Enter text: ").strip()
        if user_text.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        try:
            label, prob = predict_texts(model, tokenizer, label_encoder, user_text)[0]
            print(f"Predicted: {label}    Probabilities: {prob}")
        except Exception as e:
            print("Error during prediction:", e)

if __name__ == "__main__":
    main()
