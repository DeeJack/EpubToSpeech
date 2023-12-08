<template>
    <v-main>
        <v-container>
            <v-row>
                <v-col cols="12" md="6" class="reading">
                    <v-textarea height="100" auto-grow hide-details v-model="text" label="" readonly></v-textarea>
                </v-col>

                <v-col cols="12" md="6">
                    <div class="buttons">
                        <v-btn color="primary" @click="translate" :title="translateTooltip">Translate</v-btn>
                        <v-btn color="primary" @click="generateImage" :title="generateImageTooltip">Generate Image</v-btn>
                        <v-btn color="primary" @click="customPrompt" :title="customPromptTooltip">Custom Prompt</v-btn>
                    </div>

                    <v-text-field v-model="prompt" label="Custom Prompt"></v-text-field>

                    <v-textarea v-model="result" label="Result" readonly></v-textarea>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>
  
<script >
import { ref } from 'vue';

let text = ref('');
let prompt = ref('');
let result = ref('');
let translateTooltip = ref('Translate the text in English');
let generateImageTooltip = ref('Generate an image from the selected text');
let customPromptTooltip = ref('Generate a custom prompt from the selected text');

const translate = () => {
    // Implement your translation logic here
};

const generateImage = () => {
    // Implement your image generation logic here
};

const customPrompt = () => {
    // Implement your custom prompt logic here
};

export default {
    name: 'ReadingPane',
    data() {
        return {
            text,
            prompt,
            result,
            translate,
            generateImage,
            customPrompt,
            translateTooltip,
            generateImageTooltip,
            customPromptTooltip,
        };
    },
    created: () => {
        // Fetch text from server
        text.value = 'This is a test text';
    }
};
</script>

<style >
/* .reading {
    width: 100%;
    height: 100%; 
    box-sizing: border-box;
} */

.reading  .v-field {
    height: 90vh;
}

.buttons {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 15px;
}


</style>