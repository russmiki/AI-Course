import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from joblib import dump

from nlp.preprocess import preprocess

df = pd.read_csv("data/intents.csv")
df["text"] = df["text"].apply(preprocess)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["intent"], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))

dump(model, "models/intent_model.pkl")
dump(vectorizer, "models/vectorizer.pkl")
