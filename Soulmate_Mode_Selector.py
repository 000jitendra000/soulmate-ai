import streamlit as st
import cohere
import pyttsx3
import speech_recognition as sr
import json
import os
from datetime import datetime
import pythoncom

# 🧠 Initialize Cohere API Client
cohere_api_key =""
cohere_client = cohere.Client(cohere_api_key)
pythoncom.CoInitialize()
# 🌀 Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def chat_with_soulmate(prompt):
    try:
        response = cohere_client.generate(
            model="command-r",  # ✅ Updated model
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"💥 Error: {str(e)}"
# 🗂️ File paths
GENDER_FILE = ".soulmate_gender.json"
NAME_FILE = ".soulmate_name.json"
MEMORY_FILE = ".user_memory.json"

# 📁 User's memory (or load existing memory)
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        user_memory = json.load(f)
else:
    user_memory = {}

# 🌟 Check and set user gender
if "user_gender" not in st.session_state:
    if os.path.exists(GENDER_FILE):
        with open(GENDER_FILE, "r") as f:
            st.session_state.user_gender = json.load(f).get("gender", "Other")
    else:
        gender = st.selectbox("Select your gender:", ["Girl", "Boy", "Other"])
        st.session_state.user_gender = gender
        with open(GENDER_FILE, "w") as f:
            json.dump({"gender": gender}, f)

           

# 🔁 Initialize session state
if "soulmate_name" not in st.session_state:
    st.session_state.soulmate_name = None
if "soulmate_gender" not in st.session_state:
    st.session_state.soulmate_gender = None

# 🔁 Reset Button Logic
if st.button("🔁 Reset Name and Gender"):
    st.session_state.soulmate_name = None
    st.session_state.soulmate_gender = None
    st.rerun()

# 💬 Set Name and Gender Only If Not Already Set
if st.session_state.soulmate_name is None or st.session_state.soulmate_gender is None:
    st.title("💙 SoulMate - Your AI Companion")
    st.subheader("Let's personalize your AI companion")

    name = st.text_input("Enter your AI companion's name:")
    gender = st.selectbox("Choose your AI companion's gender:", ["Female", "Male", "Non-binary"])

    if st.button("✅ Save"):
        st.session_state.soulmate_name = name
        st.session_state.soulmate_gender = gender
        st.success("Saved! Your companion is ready.")
        st.rerun()



# 📁 Name file
if os.path.exists(NAME_FILE):
    with open(NAME_FILE, "r") as f:
        st.session_state.soulmate_name = json.load(f).get("name", "SoulMate")
else:
    soulmate_name = st.text_input("Give your SoulMate a name:")
    if soulmate_name:
        st.session_state.soulmate_name = soulmate_name
        with open(NAME_FILE, "w") as f:
            json.dump({"name": soulmate_name}, f)
    else:
        st.stop()

# 🧠 Conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# 💬 Adjust tone based on user gender
def adjust_tone(message):
    if st.session_state.user_gender == "Girl":
        return message.replace("I'm here for you", "Hey beautiful, I'm here for you")
    else:
        return message.replace("I'm here for you", "Hey handsome, I'm here for you")

# 💾 Update memory
def update_memory(key, value):
    user_memory[key] = value
    with open(MEMORY_FILE, "w") as f:
        json.dump(user_memory, f)

# 📓 Save journal entry
def save_journal_entry(text):
    os.makedirs("journals", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"journals/{timestamp}.txt", "w") as f:
        f.write(text)

# 🌙 Nightly learning (summarization)
def nightly_learning():
    today = datetime.now().strftime("%Y-%m-%d")
    if user_memory.get("last_updated") != today:
        os.makedirs("summaries", exist_ok=True)
        summary_file = f"summaries/{today}.txt"

        conversation_text = "\n".join([
            f"You: {msg['content']}" if msg['role'] == 'user' else f"{st.session_state.soulmate_name}: {msg['content']}"
            for msg in st.session_state.conversation_history
        ])
        prompt = f"Summarize the following conversation:\n\n{conversation_text}"

        try:
            response = co.generate(
                model='command-r',
                prompt=prompt,
                max_tokens=200
            )
            summary = response.generations[0].text.strip()
        except Exception as e:
            summary = f"Summary failed: {str(e)}"

        with open(summary_file, "w") as f:
            f.write(summary)

        user_memory["last_updated"] = today
        with open(MEMORY_FILE, "w") as f:
            json.dump(user_memory, f)

# 🎤 Listen from microphone
def listen_to_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("🎤 Listening..."):
            audio = r.listen(source, timeout=5)
        try:
            return r.recognize_google(audio)
        except:
            return "Sorry, I didn't catch that."

# 🔊 Speak output
def speak(text):
    engine.say(text)
    engine.runAndWait()

# 💬 Display conversation
def display_chat():
    st.markdown("### 💬 Conversation")
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**{st.session_state.soulmate_name}:** {msg['content']}")

# 🎨 Streamlit UI

nightly_learning()

option = st.sidebar.radio("Choose Mode", ["Voice Chat", "Text Chat", "Recall Summary"])

def speak(text):
    engine.say(text)
    engine.runAndWait()
# 💬 Chat with SoulMate
def chat_with_soulmate(user_input):
    try:
        # Use the correct model ID
        response = cohere_client.generate(
            model="command-r7b-12-2024",  # Correct model ID
            prompt=user_input,
            max_tokens=100,
            temperature=0.7
        )
        ai_message = response.generations[0].text.strip()
        return ai_message
    except Exception as e:
        return f"Error: {str(e)}"
if __name__ == '__main__':
    # Display the app title at the top of the app
    st.title("💙 SoulMate - Your AI Companion")

    

    # Dropdown for selecting interaction mode
    option = st.selectbox("Choose your interaction mode:", ["Text Chat", "Voice Chat"])

    if option == "Voice Chat":
        
        if st.button("🎤 Start Listening"):
            user_input = listen_to_user()  # This function listens for user input via microphone
            st.write(f"🎤 You said: {user_input}")
            
            if user_input.lower() == "bye":
                st.write("💬 Ending conversation.")
            else:
                ai_response = chat_with_soulmate(user_input)  # Call the function here
                st.write(f"💙 {st.session_state.soulmate_name}: {ai_response}")
                speak(ai_response)  # Speak out the AI response using the TTS syste
    elif option == "Text Chat":
       
        user_input = st.text_input("You: ", "")
        if user_input:
            if user_input.lower() == "bye":
                st.write("💬 Ending conversation.")
            else:
                ai_response = chat_with_soulmate(user_input)  # Call the function here
                st.write(f"💙 {st.session_state.soulmate_name}: {ai_response}")
                speak(ai_response)  # Speak out the AI response using the TTS system

# 📅 Recall past summary
def recall_summary_by_date(date_str):
    try:
        summary_file = f"summaries/{date_str}.txt"
        with open(summary_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Summary not found for this date."
