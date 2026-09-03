import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

def get_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

def get_user_entries(user_id):
    """Extract all entries of a single user from database"""
    conn=get_connection()
    query = "SELECT entry_date, statement, mood_category FROM entries WHERE user_id = %s ORDER BY entry_date"
    df = pd.read_sql(query, conn, params=(user_id,))
    conn.close()
    return df

def analyze_patterns(user_id):
    """Analyze the pattern from user's data"""
    df=get_user_entries(user_id)
    if df.empty or len(df) < 3:
        return {"message": "Not enough data yet. Keep journaling to see your patterns!"}

    df['entry_date'] = pd.to_datetime(df['entry_date'])
    df['day_of_week'] = df['entry_date'].dt.day_name()

    insights = {}
    
    # 1_ overall mood distribution
    mood_counts=df['mood_category'].value_counts()
    insights['mood_distribution']=mood_counts.to_dict()

    # 2_ Day-of-week pattern - 
    tough_moods = ['Going Through a Tough Time', "You're not Alone"]
    tough_df = df[df['mood_category'].isin(tough_moods)]
    if not tough_df.empty:
        worst_day = tough_df['day_of_week'].value_counts().idxmax()
        insights['worst_day'] = worst_day
    else:
        insights['worst_day'] = None
    
    # 3_ Recent Trend Analysis
    df_sorted=df.sort_values('entry_date')
    recent_7=df_sorted.tail(7)
    previous_7=df_sorted.iloc[-14:-7] if len(df_sorted) >= 14 else pd.DataFrame()

    mood_score_map = {
        'Feeling Good': 3,
        'A Bit Overwhelmed': 2,
        'Going Through a Tough Time': 1,
        "You're not Alone": 0
    }
    recent_7['score'] = recent_7['mood_category'].map(mood_score_map)
    recent_avg = recent_7['score'].mean()

    if not previous_7.empty:
        previous_7['score'] = previous_7['mood_category'].map(mood_score_map)
        previous_avg = previous_7['score'].mean()

        if recent_avg > previous_avg:
            insights['trend'] = "improving"
        elif recent_avg < previous_avg:
            insights['trend'] = "declining"
        else:
            insights['trend'] = "stable"
    else:
        insights['trend'] = "not enough data for comparison"

    insights['recent_average_score'] = round(recent_avg, 2)

    recent_crisis = recent_7[recent_7['mood_category'] == "You're not Alone"]
    insights['recent_crisis_count'] = len(recent_crisis)

    return insights

if __name__ == "__main__":
    for uid in range(1, 6):
        print(f"\n--- User {uid} Insights ---")
        result = analyze_patterns(uid)
        print(result)