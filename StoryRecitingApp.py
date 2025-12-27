import streamlit as st
import json
import requests
import re
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Story App", page_icon="📖")
st.title("📚 Story Reciter & Word Meaning App")

# -------- Load Stories from JSON --------
with open("stories.json", "r") as f:
    data = json.load(f)

stories = data["stories"]

# -------- Story Selection --------
titles = {story["title"]: story for story in stories}
selected_title = st.selectbox("Choose a story", titles.keys())
selected_story = titles[selected_title]

st.subheader("📖 Story")

for para in selected_story["text"]:
    st.write(para)

st.caption(f"🧠 Moral: {selected_story['moral']}")

# -------- Narration --------
def narrate(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

if st.button("▶️ Play Story"):
    full_story = " ".join(selected_story["text"])
    audio_file = narrate(full_story)
    st.audio(audio_file)

# -------- Word Meaning --------
st.subheader("🔍 Find Word Meaning")

word = st.text_input("Enter a word from the story")

def get_meaning(word):
    word = re.sub(r"[^\w\s]", "", word)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()[0]["meanings"][0]["definitions"][0]["definition"]
    return None

if st.button("Get Meaning"):
    if word:
        meaning = get_meaning(word.lower())
        if meaning:
            st.success(meaning)
        else:
            st.error("Word not found")
    else:
        st.warning("Please enter a word")
