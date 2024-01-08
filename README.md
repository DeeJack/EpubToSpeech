# Epub To Speech

This project is a web application where users can upload Epub files and use various services to translate certain chapters to voice (TTS). Additionally, users can use the GPT API to request information about the chapter, generate images, and more.

## Technologies Used

- Frontend: VueJS with Vuetify
- Backend: Python with Flask
- Supported TTS Services: Azure, OpenAI, ElevenLabs, and a local one (espeak for linux)

## Getting Started

1. Clone the repository

   ```cmd
   git clone https://github.com/DeeJack/EpubToSpeech.git
   ```

2. Run with docker!

   ```cmd
   ./start.sh
   ```

   OR:

   ```cmd
   docker-compose up --build
   ```

## Usage

1. Navigate to the home page and upload an Epub file.
2. Insert in the form the information you want
3. Select the process you need: TTS or the AI Reader.

### TTS

1. Select the service to use (Azure, OpenAI, ElevenLabs, Local)
2. Choose the chapters to generate from the table.

### Reader

1. Select the chapter to read from the select element.
2. Use the buttons to do the actions (Translate, Image generation)

# Example images

## Home - Upload

![Home/Upload](images/upload.jpeg)

## Form

![Form](images/form.jpeg)

## TTS

![TTS](images/tts.jpeg)

## AI Reader

![Reader](images/reader.jpeg)

## Search

![Search](images/search.jpeg)

## Examples

![Example](images/example.gif)

## Search vid

![Search vid](images/search.gif)