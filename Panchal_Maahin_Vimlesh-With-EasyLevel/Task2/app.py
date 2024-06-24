import json
import random
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st 

# Load intents from JSON file
with open('intent.json') as file:
    intents = json.load(file)

# Initialize lists for patterns and tags
tags = []
patterns = []

# Populate the lists with data from the JSON file
for intent in intents['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])

# Vectorize the patterns using TF-IDF
vector = TfidfVectorizer()
patterns_scaled = vector.fit_transform(patterns)

# Train a logistic regression model
Bot = LogisticRegression(max_iter=100000)
Bot.fit(patterns_scaled, tags)

def ChatBot(input_message):
    input_message = vector.transform([input_message])
    pred_tag = Bot.predict(input_message)[0]
    for intent in intents['intents']:
        if intent['tag'] == pred_tag:
            response = random.choice(intent['responses'])
            return response

st.title("University Chat Bot")
st.markdown("Welcome to the University Chat Bot! 🤖 I'm here to help answer your questions. What's on your mind?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What's up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = ChatBot(prompt)
    if response:
        response = f"😊 {response}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        response = "Sorry, I didn't understand that. Can you please rephrase? 🤔"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Add a "clear chat" button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()