<template>
    <v-main>
        <v-container>
            <h1 class="formTitle">Epub to Voice</h1>
            <v-form ref="form" v-model="valid" @submit.prevent="createRequest">
                <v-text-field v-model="title" label="Title" :rules="[v => !!v || 'Title is required']"
                    required></v-text-field>

                <v-text-field v-model="author" label="Author" :rules="[v => !!v || 'Author is required']"
                    required></v-text-field>

                <v-textarea v-model="description" label="Description" :rules="[v => !!v || 'Description is required']"
                    required></v-textarea>

                <div class="center">
                    <v-btn color="primary" @click="toReader()">AI Reader</v-btn>
                    <v-btn color="primary" @click="toTTS()">TTS</v-btn>
                </div>
            </v-form>
        </v-container>
    </v-main>
</template>

<script>
import { ref } from 'vue';

let form = ref(null);
let valid = ref(false);
let title = ref('');
let author = ref('');
let description = ref('');

const createRequest = () => {
    if (form.value.validate()) {
        // Implement your request creation logic here
    }
};

export default {
    created: () => {
    },
    data: () => ({
        form,
        valid,
        title,
        author,
        description,
    }),
    methods: {
        createRequest,
        toReader() {
            this.$router.push('/reader')
        },
        toTTS() {
            this.$router.push('/tts')
        }
    },

}
</script>

<style scoped>
.center {
    display: flex;
    justify-content: center;
    align-items: center;
}

.center button:first-child {
    margin-right: 10%;
}

.v-btn {
    margin-top: 15px;
}

.formTitle {
    text-align: center;
    margin-bottom: 15px;
}
</style>