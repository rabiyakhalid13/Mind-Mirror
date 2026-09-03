import joblib
import mysql.connector
from datetime import date
import re
import os
import sys
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.sparse import hstack, csr_matrix

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import get_agent_response
from model.pattern_detector import analyze_patterns

model = joblib.load('model/mood_model.pkl')
vectorizer = joblib.load('model/tfidf_vectorizer.pkl')
analyzer = SentimentIntensityAnalyzer()
load_dotenv()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predict_mood(statement, debug=False):
    cleaned = clean_text(statement)
    vectorized = vectorizer.transform([cleaned])

    raw_vader = analyzer.polarity_scores(statement)['compound']
    vader_score = raw_vader * 7
    combined = hstack([vectorized, csr_matrix([[vader_score]])])

    model_prediction = model.predict(combined)[0]
    probabilities = model.predict_proba(combined)[0]
    class_probs = dict(zip(model.classes_, probabilities))

    if debug:
        print("Cleaned:", cleaned)
        print("Raw VADER:", raw_vader)
        print("Model's raw prediction:", model_prediction)
        print("Probabilities:", class_probs)

    # Explicit crisis language - always wins, no ambiguity allowed here
    crisis_keywords = [
        'suicide', 'kill myself', 'end my life', 'want to die', 'not want to live',
        'end it all', 'no reason to live', 'better off dead', 'hurt myself'
    ]
    if any(kw in cleaned for kw in crisis_keywords):
        if debug:
            print("Decision: explicit crisis keyword match")
        return "You're not Alone", raw_vader

    # Tiered decision based on VADER severity
    if raw_vader <= -0.6:
        # Very strong negative sentiment, no explicit crisis words -> serious distress
        prediction = "Going Through a Tough Time"
        if debug:
            print("Decision: VADER tier -> strong negative")

    elif raw_vader <= -0.25:
        # Clearly negative but moderate
        # Let the model pick between Overwhelmed and Tough Time (whichever it's more confident about)
        candidates = ['A Bit Overwhelmed', 'Going Through a Tough Time']
        prediction = max(candidates, key=lambda c: class_probs[c])
        if debug:
            print("Decision: VADER tier -> moderate negative")

    elif raw_vader < 0.1:
        # Mild or ambiguous sentiment - trust the model here, it has more context than VADER alone
        prediction = model_prediction
        if debug:
            print("Decision: ambiguous zone -> trusting model")

    else:
        # Clearly positive
        prediction = "Feeling Good"
        if debug:
            print("Decision: VADER tier -> positive")

    return prediction, raw_vader


def save_new_entry(user_id, statement):
    """predict statement and save in database"""
    mood_category, vader_score = predict_mood(statement, debug=True)
    entry_date = date.today()
    
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries (user_id, entry_date, statement, mood_category) VALUES (%s, %s, %s, %s)",
        (user_id, entry_date, statement, mood_category)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "statement": statement,
        "predicted_mood": mood_category,
        "vader_score": round(vader_score, 3),
        "date": str(entry_date)
    }
    
def process_journal_entry(user_id, statement):
    """
    FULL PIPELINE:
    1. Predict mood + save to database
    2. Get pattern insights
    3. Get AI agent response
    """
    entry_result = save_new_entry(user_id, statement)
    mood_category = entry_result['predicted_mood']

    pattern_insights = analyze_patterns(user_id)

    agent_reply = get_agent_response(statement, mood_category, pattern_insights)
    return {
        "statement": statement,
        "predicted_mood": mood_category,
        "pattern_insights": pattern_insights,
        "agent_response": agent_reply
    }

if __name__ == "__main__":
    test_statement = input("Enter journal entry for today: ")
    result = process_journal_entry(user_id=1, statement=test_statement)

    print("\n--- Full Pipeline Result ---")
    print("Mood:", result['predicted_mood'])
    print("\nPattern Insights:", result['pattern_insights'])
    print("\nAgent Response:")
    print(result['agent_response'])