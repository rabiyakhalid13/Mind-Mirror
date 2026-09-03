import streamlit as st
import sys
import os
import mysql.connector
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model.journal_entry import process_journal_entry

load_dotenv()
st.set_page_config(page_title="MindMirror", page_icon=None, layout="centered")

# ---------------------------------------------------------------
# Styling
# ---------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #1E2328;
    --surface: #262B31;
    --surface-soft: #2C333A;
    --sage: #8FA98C;
    --sage-soft: #5F7060;
    --amber: #D3A06C;
    --clay: #C0846A;
    --rose: #C46A6A;
    --text: #EAE7E0;
    --text-muted: #A2A6A8;
    --border: #383F46;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
}

h1 {
    font-family: 'Source Serif 4', serif;
    font-weight: 600;
    font-size: 2.4rem;
    letter-spacing: -0.01em;
    color: var(--text);
    margin-bottom: 0.1rem;
}

.tagline {
    font-family: 'Inter', sans-serif;
    color: var(--text-muted);
    font-size: 1.02rem;
    margin-bottom: 2rem;
}

h2, h3 {
    font-family: 'Source Serif 4', serif;
    color: var(--text);
}

/* Text area */
.stTextArea textarea {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-size: 1rem;
    padding: 14px;
}
.stTextArea textarea:focus {
    border-color: var(--sage);
    box-shadow: 0 0 0 1px var(--sage);
}

/* Buttons */
.stButton button {
    background: var(--sage-soft);
    color: #F5F3EE;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.3rem;
    font-weight: 500;
    transition: background 0.15s ease;
}
.stButton button:hover {
    background: var(--sage);
    color: #1E2328;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background: var(--surface);
    border-radius: 8px;
}

/* Mood badge */
.mood-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    border-radius: 999px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    margin: 0.4rem 0 1rem 0;
}
.mood-good { background: rgba(143,169,140,0.18); color: var(--sage); border: 1px solid rgba(143,169,140,0.4); }
.mood-mild { background: rgba(211,160,108,0.18); color: var(--amber); border: 1px solid rgba(211,160,108,0.4); }
.mood-tough { background: rgba(192,132,106,0.18); color: var(--clay); border: 1px solid rgba(192,132,106,0.4); }
.mood-crisis { background: rgba(196,106,106,0.2); color: var(--rose); border: 1px solid rgba(196,106,106,0.5); }

.dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.dot-good { background: var(--sage); }
.dot-mild { background: var(--amber); }
.dot-tough { background: var(--clay); }
.dot-crisis { background: var(--rose); }

/* Agent response card */
.agent-card {
    background: var(--surface);
    border-left: 3px solid var(--sage-soft);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0 1.6rem 0;
    line-height: 1.65;
    font-size: 1.02rem;
}
.agent-label {
    font-family: 'Source Serif 4', serif;
    font-size: 0.9rem;
    color: var(--text-muted);
    text-transform: none;
    margin-bottom: 0.5rem;
    letter-spacing: 0.02em;
}

/* Crisis card - visually distinct but not alarming */
.crisis-card {
    background: rgba(196,106,106,0.08);
    border: 1px solid rgba(196,106,106,0.35);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0 1.6rem 0;
    line-height: 1.7;
}

hr {
    border-color: var(--border);
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface-soft);
    border-radius: 8px;
    font-family: 'Source Serif 4', serif;
}

.welcome-line {
    color: var(--text-muted);
    font-size: 1rem;
    margin-bottom: 1rem;
}

.feature-strip {
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 1.1rem 0;
    margin-bottom: 2rem;
}
.feature-item {
    font-size: 0.92rem;
    color: var(--text-muted);
    display: flex;
    align-items: baseline;
    gap: 10px;
}
.feature-num {
    font-family: 'Source Serif 4', serif;
    color: var(--sage);
    font-size: 0.85rem;
    min-width: 20px;
}
</style>
""", unsafe_allow_html=True)


def mood_badge_html(mood):
    mapping = {
        "Feeling Good": ("mood-good", "dot-good"),
        "A Bit Overwhelmed": ("mood-mild", "dot-mild"),
        "Going Through a Tough Time": ("mood-tough", "dot-tough"),
        "You're not Alone": ("mood-crisis", "dot-crisis"),
    }
    css_class, dot_class = mapping.get(mood, ("mood-mild", "dot-mild"))
    return f'<span class="mood-badge {css_class}"><span class="dot {dot_class}"></span>{mood}</span>'


# ---------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------
def get_all_users():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return {uid: name for uid, name in users}


def create_new_user(username):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


# ---------------------------------------------------------------
# App state
# ---------------------------------------------------------------
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

st.markdown("<h1>MindMirror</h1>", unsafe_allow_html=True)
st.markdown('<p class="tagline">A journaling companion that notices what you might not.</p>', unsafe_allow_html=True)
st.markdown("""
<div class="feature-strip">
    <div class="feature-item"><span class="feature-num">01</span>Write a journal entry, in your own words</div>
    <div class="feature-item"><span class="feature-num">02</span>A trained model reads your mood, not just your words</div>
    <div class="feature-item"><span class="feature-num">03</span>Get a response shaped by your own recent patterns</div>
</div>
""", unsafe_allow_html=True)

# ---- Profile selection ----
if st.session_state.user_id is None:
    st.subheader("Who's journaling today?")

    users = get_all_users()
    options = list(users.values()) + ["Create New Profile"]
    selected = st.selectbox("Choose a profile", options, label_visibility="collapsed")

    if selected == "Create New Profile":
        new_name = st.text_input("Your name")
        if st.button("Create and continue"):
            if new_name.strip() == "":
                st.warning("Please enter a name.")
            else:
                new_id = create_new_user(new_name.strip())
                st.session_state.user_id = new_id
                st.session_state.username = new_name.strip()
                st.rerun()
    else:
        if st.button("Continue"):
            user_id = [k for k, v in users.items() if v == selected][0]
            st.session_state.user_id = user_id
            st.session_state.username = selected
            st.rerun()

# ---- Journal screen ----
else:
    st.markdown(f'<p class="welcome-line">Welcome back, {st.session_state.username}.</p>', unsafe_allow_html=True)

    if st.button("Switch profile"):
        st.session_state.user_id = None
        st.rerun()

    statement = st.text_area(
        "How are you feeling today?",
        height=150,
        placeholder="Write whatever's on your mind..."
    )

    if st.button("Submit entry"):
        if statement.strip() == "":
            st.warning("Please write something before submitting.")
        else:
            with st.spinner("Reflecting on your entry..."):
                try:
                    result = process_journal_entry(user_id=st.session_state.user_id, statement=statement)
                    mood = result['predicted_mood']

                    st.markdown(mood_badge_html(mood), unsafe_allow_html=True)

                    if mood == "You're not Alone":
                        st.markdown(
                            f'<div class="crisis-card">{result["agent_response"]}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="agent-card"><div class="agent-label">MindMirror says</div>{result["agent_response"]}</div>',
                            unsafe_allow_html=True
                        )

                    insights = result.get('pattern_insights', {})
                    if insights:
                        with st.expander("Your patterns", expanded=True):
                            if "message" in insights:
                                st.write(insights['message'])
                            else:
                                if insights.get('worst_day'):
                                    st.write(f"Tough days tend to fall on **{insights['worst_day']}s**.")

                                trend = insights.get('trend')
                                if trend == "improving":
                                    st.success("Your mood has been trending upward over the past week.")
                                elif trend == "declining":
                                    st.warning("Your mood has dipped a bit over the past week. Be gentle with yourself.")
                                elif trend == "stable":
                                    st.info("Your mood has held fairly steady over the past week.")

                                mood_dist = insights.get('mood_distribution', {})
                                if mood_dist:
                                    st.write("Overall mood breakdown:")
                                    st.bar_chart(mood_dist)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")