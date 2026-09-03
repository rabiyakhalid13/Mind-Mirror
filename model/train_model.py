import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import accuracy_score, classification_report
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.sparse import hstack, csr_matrix

# Load cleaned data
df = pd.read_csv('data/cleaned_data.csv')
df = df.dropna(subset=['clean_statement', 'mood_category'])
df = df[df['clean_statement'].astype(str).str.strip() != '']

# Prepare features and target
X = df['clean_statement']
y = df['mood_category']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=15000, stop_words='english', ngram_range=(1,2),min_df=1,sublinear_tf=True)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# VADER Sentiment Scores
analyzer = SentimentIntensityAnalyzer()

def get_vader_score(text):
    return analyzer.polarity_scores(text)['compound']

X_train_vader = np.array([get_vader_score(t)*7 for t in X_train]).reshape(-1, 1)
X_test_vader = np.array([get_vader_score(t)*7 for t in X_test]).reshape(-1, 1)

# Combine TF-IDF + VADER
X_train_final = hstack([X_train_tfidf, csr_matrix(X_train_vader)])
X_test_final = hstack([X_test_tfidf, csr_matrix(X_test_vader)])

print("Combined feature shape:", X_train_final.shape)

# Compute balanced class weights, then boost "You're not Alone" category
classes = np.unique(y_train)
balanced_weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_train)
weight_dict = dict(zip(classes, balanced_weights))
weight_dict["You're not Alone"] *= 1.5

# Train final model
model = LogisticRegression(max_iter=1000, class_weight=weight_dict)
model.fit(X_train_final, y_train)

# Evaluate
y_pred = model.predict(X_test_final)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, 'model/mood_model.pkl')
joblib.dump(vectorizer, 'model/tfidf_vectorizer.pkl')
print("Model and vectorizer saved successfully!")