from transformers import pipeline
import speech_recognition as sr
from gtts import gTTS
import os
# from playsound import playsound
import pygame


def translate_text(text, target_lang):
    translator = pipeline("translation_en_to_xx",
                          model=f"Helsinki-NLP/opus-mt-en-{target_lang}", tokenizer=f"Helsinki-NLP/opus-mt-en-{target_lang}")
    translated_text = translator(text)[0]['translation_text']
    return translated_text


def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something:")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None


def play_translation(text):
    tts = gTTS(text, lang='en')
    tts.save("translation.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("translation.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove("translation.mp3")


def main():
    print("Welcome to the Language Translation App!")
    target_lang = input(
        "Enter the target language code (e.g., 'fr' for French): ")

    while True:
        input("Press Enter to start speaking...")
        user_input = speech_to_text()
        if user_input is None:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        translated_text = translate_text(user_input, target_lang)
        print(f"Translation: {translated_text}")
        play_translation(translated_text)


if __name__ == "__main__":
    main()
