<template>
    <v-main style="padding: 0">
        <v-container>
            <v-row>
                <v-col cols="12">
                    <v-select v-model="chapter" :items="chapters" item-value="id" item-title="name" label="Chapter" outlined
                        @update:model-value="changeChapter()"></v-select>
                </v-col>

            </v-row>
            <v-row>
                <v-col cols="12" md="6" class="reading">
                    <v-textarea ref="chapterText" height="100" auto-grow hide-details v-model="text" label="" readonly
                        @blur="stopSelection" @focus="startSelection"></v-textarea>
                </v-col>

                <v-col cols="12" md="6">
                    <div class="buttons">
                        <v-btn :disabled="loading" color="primary" @click="translate" :title="translateTooltip">Translate</v-btn>
                        <v-btn :disabled="loading" color="primary" @click="summarize" :title="summarizeTooltip">Summarize</v-btn>
                        <!-- <v-btn color="primary" @click="trivia" :title="triviaTooltip">Trivia</v-btn>-->
                        <v-btn :disabled="loading" color="primary" @click="generateImage" :title="generateImageTooltip">Generate Image</v-btn>
                        <v-btn :disabled="loading" color="primary" @click="customPrompt" :title="customPromptTooltip">Custom Prompt</v-btn>
                    </div>
                    <v-progress-linear v-if="loading" indeterminate color="blue"></v-progress-linear>

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
import axios from 'axios';

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
let loading = ref(false);

let id = ref(0);
let chapter = { id: 0, name: '' };
let chapters = []

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

export default {
    name: 'ReadingPane',
    data() {
        return {
            text,
            prompt,
            result,
            translateTooltip,
            generateImageTooltip,
            customPromptTooltip,
            summarizeTooltip,
            triviaTooltip,
            selectedText,
            chapters,
            chapter,
            loading
        };
    },
    created() {
        this.id = this.$route.query.id;
        this.chapter = this.$route.query.chapter || 0;
        // Fetch text from server
        axios.get(`http://localhost:5000/api/reader/chapter/${this.id}/${this.chapter}`).then((response) => {
            text.value = response.data.text;
        }).catch((error) => {
            console.log(error);
        });

        axios.get(`http://localhost:5000/api/reader/chapters/${this.id}`)
            .then((response) => {
                let index = 0;
                this.chapters = response.data.map((chapter) => {
                    return {
                        id: index++,
                        name: this.getChapterName(chapter),
                    }
                });
                this.chapter = this.chapters[0].id;
                console.log(chapters.value)
            }).catch((error) => {
                console.log(error);
            });
        // text.value = 'This is a test text';
    },
    methods: {
        startSelection() {
            document.addEventListener('selectionchange', selectionListener)
        },
        stopSelection() {
            document.removeEventListener('selectionchange', selectionListener)
        },
        customPrompt() {
            loading.value = true;
            axios.post(`http://localhost:5000/api/reader/generate/${this.id}/${this.chapter}`, {
                prompt: this.prompt,
            }).then((response) => {
                loading.value = false;
                console.log(response.data)
                result.value = response.data.text;
            }).catch((error) => {
                loading.value = false;
                console.log(error);
            });
        },
        summarize() {
            loading.value = true;
            axios.post(`http://localhost:5000/api/reader/summarize/${this.id}/${this.chapter}`)
                .then((response) => {
                    loading.value = false;
                    console.log(response.data)
                    result.value = response.data.text;
                }).catch((error) => {
                    loading.value = false;
                    console.log(error);
                });
        },
        translate() {
            loading.value = true;
            axios.post(`http://localhost:5000/api/reader/translate/${this.id}/${this.chapter}`)
                .then((response) => {
                    loading.value = false;
                    console.log(response.data)
                    result.value = response.data.text;
                }).catch((error) => {
                    loading.value = false;
                    console.log(error);
                });
        },
        generateImage() {
            loading.value = true;
            axios.post(`http://localhost:5000/api/reader/image/`, {
                prompt: getSelectedText(),
            }).then((response) => {
                loading.value = false;
                console.log(response.data)
                result.value = response.data.image;
            }).catch((error) => {
                loading.value = false;
                console.log(error);
            });
        },
        changeChapter() {
            console.log(this.chapter)
            axios.get(`http://localhost:5000/api/reader/chapter/${this.id}/${this.chapter}`).then((response) => {
                text.value = response.data.text;
            }).catch((error) => {
                console.log(error);
            });
        },
        getChapterName(chapter) {
            return chapter.split('/').pop().replace('.xhtml', '').replace('.html', '')
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