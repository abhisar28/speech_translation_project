import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from langdetect import detect
import tkinter as tk
from tkinter import filedialog, messagebox, ttk  # Import ttk for themed widgets
import pyttsx3

# Load environment variables from .env file
load_dotenv()

# Get Azure credentials from environment variables
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
AZURE_KEY = os.getenv('AZURE_KEY')
AZURE_LOCATION = os.getenv('AZURE_LOCATION')

# Function to recognize speech using Azure Speech Service
def recognize_speech(is_file_input=False, file_path=None):
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_LOCATION)
    if is_file_input and file_path:
        print(f"Recognizing speech from file: {file_path}")
        try:
            audio_config = speechsdk.audio.AudioConfig(filename=file_path)
            recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
            print("Recognizing speech from file...")
            result = recognizer.recognize_once()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized from the file")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"Speech Recognition canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print(f"Error details: {cancellation_details.error_details}")
        except Exception as e:
            print(f"Error processing audio file: {e}")
    else:
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        print("Recognizing speech from microphone...")
        result = recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
    return None

# Function to detect language of the recognized text
def detect_language(text):
    try:
        detected_lang = detect(text)
        return detected_lang
    except Exception as e:
        print(f"Error detecting language: {e}")
        return "unknown"

# Function to translate text into multiple languages
def translate_text_multi(text, target_languages):
    client = TextTranslationClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))
    translation_request = [{"text": text}]
    translations = {}
    for lang in target_languages:
        try:
            response = client.translate(body=translation_request, to_language=[lang])
            translated_text = response[0].translations[0].text
            translations[lang] = translated_text
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
    return translations

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Function to read text using pyttsx3
def read_text(text):
    engine.say(text)
    engine.runAndWait()

# Frontend using Tkinter
def start_app():
    root = tk.Tk()
    root.title("Speech Recognition with Language Detection")
    root.geometry("600x600")
    root.config(bg="#EAEFF1")  # Light background color

    # Add a scrollbar for the entire application
    main_frame = tk.Frame(root, bg="#EAEFF1")
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg="#EAEFF1")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    content_frame = tk.Frame(canvas, bg="#EAEFF1")
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    target_languages_var = []

    # Define a style for buttons and labels
    button_style = {
        'font': ('Arial', 12, 'bold'),
        'bg': '#3498DB',
        'fg': 'white',
        'relief': 'flat',
        'padx': 20,
        'pady': 10,
    }

    label_style = {
        'font': ('Arial', 14),
        'fg': "#2C3E50",
        'bg': "#EAEFF1",
    }

    # Create title label with a larger font size and different color
    title_label = tk.Label(content_frame, text="Speech Recognition & Translation", font=('Arial', 18, 'bold'), fg="#2C3E50", bg="#EAEFF1")
    title_label.pack(pady=(20, 10))

    instructions_label = tk.Label(content_frame, text="Click the button and start speaking:", **label_style)
    instructions_label.pack(pady=(10, 5))

    def recognize_and_translate(is_file_input=False):
        recognized_text = None
        if is_file_input:
            file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
            if file_path:
                recognized_text = recognize_speech(is_file_input=True, file_path=file_path)
        else:
            recognized_text = recognize_speech()

        if recognized_text:
            detected_lang = detect_language(recognized_text)
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, f"Recognized Text: {recognized_text}\n")
            text_output.insert(tk.END, f"Detected Language: {detected_lang}\n")

            # Ensure target_languages_var is populated
            if not target_languages_var:
                messagebox.showwarning("No Languages Selected", "Please select at least one language for translation.")
                return

            translations = translate_text_multi(recognized_text, target_languages_var)
            for lang, translation in translations.items():
                text_output.insert(tk.END, f"Translated ({lang}): {translation}\n")
        else:
            messagebox.showwarning("Warning", "No speech recognized!")

    def read_translated_text():
        translated_text = text_output.get(1.0, tk.END).strip()
        if translated_text:  # Only read if there is text to read
            read_text(translated_text)

    # Create UI components with hover effect on buttons
    def on_enter(e):
        e.widget['bg'] = '#2980B9'  # Darker blue on hover

    def on_leave(e):
        e.widget['bg'] = '#3498DB'  # Original blue color

    btn_recognize = tk.Button(content_frame, text="Recognize Speech from Microphone", command=lambda: recognize_and_translate(is_file_input=False), **button_style)
    btn_recognize.pack(pady=10)
    btn_recognize.bind("<Enter>", on_enter)
    btn_recognize.bind("<Leave>", on_leave)

    btn_file = tk.Button(content_frame, text="Select File for Speech Recognition", command=lambda: recognize_and_translate(is_file_input=True), **button_style)
    btn_file.pack(pady=10)
    btn_file.bind("<Enter>", on_enter)
    btn_file.bind("<Leave>", on_leave)

    btn_read = tk.Button(content_frame, text="Read Translated Text", command=read_translated_text, **button_style)
    btn_read.pack(pady=10)
    btn_read.bind("<Enter>", on_enter)
    btn_read.bind("<Leave>", on_leave)

    # Volume control slider with label
    volume_label = tk.Label(content_frame, text="Adjust Volume:", **label_style)
    volume_label.pack(pady=(20, 0))

    volume_slider = ttk.Scale(content_frame, from_=0.0, to=1.0, orient='horizontal', command=lambda val: engine.setProperty('volume', float(val)))
    volume_slider.set(engine.getProperty('volume'))  # Set the current volume on the slider
    volume_slider.pack(pady=(0, 20), padx=20)

    # Add text area to display recognized and translated text with rounded corners (using a frame)
    frame_output = tk.Frame(content_frame, bg="#FFFFFF", bd=2, relief='groove')
    frame_output.pack(pady=(10, 20), padx=20)

    text_output = tk.Text(frame_output, height=10, width=60, font=('Arial', 12), wrap="word", bg="#F9F9F9", bd=0)
    text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add scrollbar to text area
    text_scrollbar = tk.Scrollbar(frame_output, command=text_output.yview)
    text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_output.config(yscrollcommand=text_scrollbar.set)

    label_lang = tk.Label(content_frame, text="Select target languages for translation:", **label_style)
    label_lang.pack(pady=5)

    # Language selection listbox with improved styling
    lang_listbox = tk.Listbox(content_frame, selectmode="multiple", font=('Arial', 12), bg="#F9F9F9", fg="#34495E", height=6, exportselection=0)
    for lang in ["es", "fr", "de", "zh", "hi"]:
        lang_listbox.insert(tk.END, lang)
    # Pre-select the first language as a default
    lang_listbox.selection_set(0)
    lang_listbox.pack(pady=5)

    def select_languages():
        selected_langs = lang_listbox.curselection()
        nonlocal target_languages_var
        target_languages_var = [lang_listbox.get(i) for i in selected_langs]
        messagebox.showinfo("Languages Selected", f"Selected Languages: {', '.join(target_languages_var)}")

    btn_select_langs = tk.Button(content_frame, text="Confirm Language Selection", command=select_languages, **button_style)
    btn_select_langs.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_app()
