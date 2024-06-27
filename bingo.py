import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import time

# Define the state file path
STATE_FILE_PATH = 'bingo_state.json'

# Define the admin password (insecure, for demonstration purposes)
ADMIN_PASSWORD = "quitlookingatmysource"

st.set_page_config(page_title="🍸DESERTBLACKOUT🍶",page_icon="⏳",layout="wide")
# Function to load state from a file
def load_state():
    if os.path.exists(STATE_FILE_PATH):
        with open(STATE_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {
            'click_counts': {phrase: 0 for phrase in phrases},
            'player_boards': [],
            'usernames': [],
            'last_edit_time': 0 , # Initialize last edit time
            'log':[]
        }

# Function to save state to a file
def save_state(state):
    state['last_edit_time'] = time.time()  # Update last edit time
    with open(STATE_FILE_PATH, 'w') as file:
        json.dump(state, file)

# Function to create a new bingo board
def create_board():
    return np.random.choice(phrases, (4, 4), replace=False).tolist()

# Function to clear the state
def clear_state():
    state = {
        'click_counts': {phrase: 0 for phrase in phrases},
        'player_boards': [],
        'usernames': [],
        'last_edit_time': 0 , # Initialize last edit time
        'log':[]
    }
    save_state(state)
    return state

def clear_counts(state):
    state['click_counts'] = {phrase: 0 for phrase in phrases}
    state['log'] = []
    save_state(state)
    return state

# Bingo phrases
phrases = [
    "stormy - 💉", "hunter - 💉", "COVID - 🍺", "dark biden - 🍺", 
    "january 6th - 🍺", "stumbles words - 🍻", "You don’t like that - 🍻", 
    "this guy - 🍻", "air quotes - 🍻", "sleepy joe - 🍻", 
    "fake news - 🍻", "greatest/tremendous - 🍻", "Wall - 🍻", 
    "MAGA - 🍻", "woke - 🍻", "election interference - 🍻", 
    "battery/shark/boats - 🍻", "believe me - 🍻", "crooked joe - 🍻", "lock [pronoun] up - 🍻"
]

# Load state from file
state = load_state()

# Tabs for game and admin actions
tab1, tab2,tab3 = st.tabs(["Bingo Game", "Admin","Logs"])

with tab1:
    # Generate a new board for a new player
    column1,column2 = st.columns(2)
    # Get username from user
    with column1:
        st.image("https://raw.githubusercontent.com/hortinstein/DELIBATION/main/signal-2024-06-26-19-04-03-485.jpg", width=200)
    with column2:
        username = st.text_input("Enter your username:")
        if st.button('Join Game') and username:
            if username not in state['usernames']:
                new_board = create_board()
                state['player_boards'].append({'username': username, 'board': new_board})
                state['usernames'].append(username)
                save_state(state)
            else:
                st.warning("Username already taken. Please choose a different username.")

    # Display bingo phrases along the top with their counts in rows of 5
    st.write("### Bingo Phrases")
    for i in range(0, len(phrases), 5):
        cols = st.columns(5)
        for j, phrase in enumerate(phrases[i:i+5]):
            count = state['click_counts'][phrase]
            if cols[j].button(f"{phrase} ({count})", key=f"phrase-{i+j}"):
                current_time = time.time()
                if current_time - state['last_edit_time'] >= 10:
                    state['click_counts'][phrase] += 1
                    from datetime import datetime
                    import pytz

                    # Set the timezone to Eastern Time (ET)
                    eastern = pytz.timezone('America/New_York')

                    # Get current time in Eastern Time
                    current_time = datetime.now(eastern)

                    # Format timestamp as YYYY-MM-DD HH-MM-SS
                    formatted_time = current_time.strftime('%Y-%m-%d %H-%M-%S')
                    state["log"].append(formatted_time+" "+phrase)
                    save_state(state)
                    st.experimental_rerun()

                else:
                    st.error("Someone already marked this...Please wait at least 10 seconds before clicking again.")

    # Display all player boards
    for player in state['player_boards']:
        st.write(f"### {player['username']}'s Board")
        board = player['board']
        for r, row in enumerate(board):
            cols = st.columns(5)
            for c, phrase in enumerate(row):
                count = state['click_counts'][phrase]
                if count > 0:
                    button_color = 'background-color: lightblue;'
                else:
                    button_color = ''
                cols[c].markdown(f"<div style='padding: 5px; border: 1px solid black; {button_color}'>{phrase} ({count})</div>", unsafe_allow_html=True)

with tab2:
    st.write("### Admin Actions")

    # Password input for admin actions
    password = st.text_input("Enter admin password:", type="password")

    if password == ADMIN_PASSWORD:
        if st.button('Clear State'):
            state = clear_state()
            save_state(state)
            st.success("State has been cleared.")
        if st.button('Clear counts'):
            state = clear_counts(state)
            save_state(state)
            st.success("Counts have been cleared.")
            
with tab3:
    for entry in state['log']:
        st.write(entry)

# Auto-refresh every second
time.sleep(5)
st.experimental_rerun()
