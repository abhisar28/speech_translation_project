# Speech Recognition & Translation App

This project is a desktop application that allows you to:
- Recognize speech from your microphone or audio files
- Detect the spoken language
- Translate the recognized text into multiple languages
- Listen to the translated text using text-to-speech

The app features a user-friendly interface built with Tkinter.

## Features

- **Speech Recognition:** Convert speech to text using your microphone or audio files.
- **Language Detection:** Automatically detect the language of the recognized text.
- **Translation:** Translate text into multiple target languages.
- **Text-to-Speech:** Listen to the translated text.
- **Modern UI:** Easy-to-use interface with language selection and volume control.

## Requirements

- Python 3.7+
- See `requirements.txt` for all dependencies.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/abhisar28/speech_translation.git
   cd speech_translation
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # Or
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```sh
   python main9.py
   ```

2. **Follow the on-screen instructions:**
   - Click to recognize speech from your microphone or select an audio file.
   - Choose target languages for translation.
   - Listen to the translated text.

## Notes

- If you use Azure or other cloud APIs, you may need to set up API keys and endpoints in a `.env` file.
- For a fully free solution, you can use open-source libraries like `speech_recognition` and `googletrans`.

## License

This project is for educational purposes.
