import requests
import speech_recognition as sr
from gtts import gTTS
import os
import spacy
from googletrans import Translator

# Load the English language processing model
nlp = spacy.load("en_core_web_sm")

# Google API key for image search
API_KEY = "YOUR_GOOGLE_API_KEY"
CUSTOM_SEARCH_ENGINE_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"

def perform_web_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Your User Agent String",
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None

def perform_api_request(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.text
    else:
        return None

def text_to_speech(text):
    # Convert text to speech using gTTS and save it as an audio file
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")
    
    # Play the audio file (Linux) - Use appropriate command for other systems
    os.system("mpg321 output.mp3")

def extract_keywords(text):
    # Process the input text and extract relevant keywords
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop]
    return " ".join(keywords)

def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def image_search(query):
    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CUSTOM_SEARCH_ENGINE_ID,
        "q": query,
        "searchType": "image"
    }

    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            return data["items"][0]["link"]
    return None

def chat_input():
    while True:
        user_input = input("You (type 'voice' for voice input): ")
        
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'voice':
            voice_input()
        else:
            process_text_input(user_input)

def voice_input():
    recognizer = sr.Recognizer()

    print("Listening...")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        # Recognize voice input using Google's speech recognition
        user_input = recognizer.recognize_google(audio)
        print("You:", user_input)
        process_text_input(user_input)
        
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

def process_text_input(user_input):
    print(f"Performing web search for: {user_input}")
    
    # Extract keywords from user input and perform a web search
    keywords = extract_keywords(user_input)
    search_result = perform_web_search(keywords)

    if search_result:
        print("\nSearch Results:")
        print(search_result)
        text_to_speech(search_result)
        
        target_language = input("Enter target language for translation: ")
        if target_language.lower() != 'exit':
            translated_text = translate_text(search_result, target_language)
            print(f"\nTranslated Text ({target_language}): {translated_text}")
        
        image_link = image_search(keywords)
        if image_link:
            print(f"\nImage Link: {image_link}")
    else:
        print("Search results not available.")

    print("\nSearch completed.\n")

def main():
    print("Web Search Chatbot - Choose 'voice' for voice input or type 'exit' to quit.")
    chat_input()

if __name__ == "__main__":
    main()
