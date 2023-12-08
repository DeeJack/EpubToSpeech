<template>
    <v-main>
        <v-container>
            <v-row>
                <v-col cols="12" md="6" class="reading">
                    <v-textarea ref="chapterText" height="100" auto-grow hide-details v-model="text" label="" readonly
                        @blur="stopSelection" @focus="startSelection"></v-textarea>
                </v-col>

                <v-col cols="12" md="6">
                    <div class="buttons">
                        <v-btn color="primary" @click="translate" :title="translateTooltip">Translate</v-btn>
                        <v-btn color="primary" @click="summarize" :title="summarizeTooltip">Summarize</v-btn>
                        <v-btn color="primary" @click="trivia" :title="triviaTooltip">Trivia</v-btn>
                        <v-btn color="primary" @click="generateImage" :title="generateImageTooltip">Generate Image</v-btn>
                        <v-btn color="primary" @click="customPrompt" :title="customPromptTooltip">Custom Prompt</v-btn>
                    </div>

                    <v-text-field v-model="prompt" label="Custom Prompt"></v-text-field>
                    <v-textarea v-model="selectedText" label="Selected text" readonly></v-textarea>

                    <v-textarea v-model="result" label="Result" readonly></v-textarea>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>
  
<script >
import { nextTick } from 'vue';
import { ref } from 'vue';

let text = ref('');
let prompt = ref('');
let result = ref('');
let translateTooltip = ref('Translate the entire text in English');
let generateImageTooltip = ref('Generate an image from the selected text');
let customPromptTooltip = ref('Generate a custom prompt from the selected text');
let summarizeTooltip = ref('Summarize the entire text');
let triviaTooltip = ref('Generate trivia from the chapter');
// let chapterTextara = ref(null);
let selectedText = ref('');

const translate = () => {
    // Implement your translation logic here
};

const generateImage = () => {
    // Implement your image generation logic here
    getSelectedText();
};

const getSelectedText = () => {
    let text = '';
    if (window.getSelection) {
        text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != 'Control') {
        text = document.selection.createRange().text;
    }
    return text;
};

const selectionListener = () => {
    selectedText.value = getSelectedText();
};

// const customPrompt = () => {
//     // Implement your custom prompt logic here
// };

export default {
    name: 'ReadingPane',
    data() {
        return {
            text,
            prompt,
            result,
            translate,
            generateImage,
            // customPrompt,
            translateTooltip,
            generateImageTooltip,
            customPromptTooltip,
            selectedText,
            // chapterTextara
        };
    },
    created: async () => {
        await nextTick();
        // Fetch text from server
        text.value = 'This is a test text';
    },
    methods: {
        customPrompt() {
            console.log(getSelectedText())
        },
        startSelection() {
            document.addEventListener('selectionchange', selectionListener)
        },
        stopSelection() {
            document.removeEventListener('selectionchange', selectionListener)
        },
        summarize() {
            // Implement your summarization logic here
        },
        trivia() {
            // Implement your trivia logic here
        },
        requestGptResponse(prompt) {

        }
    }
};
</script>

<style >
/* .reading {
    width: 100%;
    height: 100%; 
    box-sizing: border-box;
} */

.reading .v-field {
    height: 90vh;
}

.buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 10px;
    justify-content: space-between;
    margin-bottom: 15px;
}
</style>