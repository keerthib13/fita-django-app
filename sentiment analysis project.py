import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
from tensorflow.keras.utils import to_categorical
import pickle

# 1️⃣ Load dataset
df = pd.read_csv(
    r"C:/Users/Keerthi/Documents/Payment Status nptel 2_files/OneDrive/Documents/yelp_labelled.txt",
    sep="\t",
    header=None,
    names=["text", "label"]
)

# 2️⃣ Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["label"])
y_cat = to_categorical(y)

# 3️⃣ Tokenize and pad text
tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(df["text"])
X = tokenizer.texts_to_sequences(df["text"])
X = pad_sequences(X, maxlen=50, padding="post")

# 4️⃣ Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

# 5️⃣ Build model
model = Sequential([
    Embedding(input_dim=5000, output_dim=64, input_length=50),
    LSTM(64),
    Dropout(0.3),
    Dense(2, activation="softmax")
])

# 6️⃣ Compile model
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# 7️⃣ Train model
model.fit(X_train, y_train, epochs=10, batch_size=4, validation_data=(X_test, y_test))

# 8️⃣ Evaluate
loss, acc = model.evaluate(X_test, y_test)
print(f"✅ Test Accuracy: {acc:.2f}")

# 9️⃣ Save model + tokenizer + label encoder
model.save("sentiment_model.h5")

with open("tokenizer.pickle", "wb") as f:
    pickle.dump(tokenizer, f)

with open("label_encoder.pickle", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Files created: sentiment_model.h5, tokenizer.pickle, label_encoder.pickle")
