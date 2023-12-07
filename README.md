# Epub To Speech

This project is a web application where users can upload Epub files and use various services to translate certain chapters to voice (TTS). Additionally, users can use the GPT API to request information about the chapter, generate images, and more.

## Technologies Used

- Frontend: HTML & CSS
- Backend: Python with Flask
- Supported TTS Services: Azure, OpenAI, ElevenLabs, and a local one

## Getting Started

1. Clone the repository
   ```
   git clone https://github.com/DeeJack/EpubToSpeech.git
   ```

2. Install the dependencies
   ```
   cd backend/
   pip install -r requirements.txt
   ```

3. Run the backend
   ```
   python home.py
   ```

4. Run the frontend
   ```
   cd ..
   cd frontend/
   npm run dev
   ```

## Usage

1. Navigate to the home page and upload an Epub file.
2. Select the TTS service you want to use.
3. Select the chapters you want to translate to voice.
4. If you want, you can also use the GPT API to request information about the chapter or generate images.
