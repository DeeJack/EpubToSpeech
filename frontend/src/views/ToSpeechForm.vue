<template>
    <v-main>
        <v-container>
            <h1 class="formTitle">Epub to Voice</h1>
            <v-form ref="form" v-model="valid" @submit.prevent="createRequest">
                <v-text-field v-model="title" label="Title" :rules="[v => !!v || 'Title is required']"
                    required></v-text-field>

                <v-text-field v-model="author" label="Author" :rules="[v => !!v || 'Author is required']"
                    required></v-text-field>

                <v-textarea v-model="description" label="Description"></v-textarea>
                
                <div class="center">
                    <v-btn color="primary" type="submit">Save</v-btn>
                </div>

                <div class="center more-btn">
                    <v-btn color="primary" @click="toReader()">AI Reader</v-btn>
                    <v-btn color="primary" @click="toTTS()">TTS</v-btn>
                </div>
            </v-form>
        </v-container>
    </v-main>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

let form = ref(null);
let valid = ref(false);
let title = ref('');
let author = ref('');
let id = ref('');
let description = ref('');

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
    created() {
        const args = this.$route.query
        this.title = args.title
        this.author = args.author
        this.id = args.id
    },
    methods: {
        createRequest() {
            if (valid.value) {
                const formData = new FormData();
                formData.append('title', this.title);
                formData.append('author', this.author);
                formData.append('description', this.description);
                formData.append('book_id', this.id);
                axios.put('http://localhost:5000/api/update_info/', formData, {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                }).then((response) => {
                    console.log(response.data)
                })
            }
        },
        toReader() {
            this.$router.push({path: '/reader', query: {id: this.id}})
        },
        toTTS() {
            this.$router.push({path: '/tts', query: {id: this.id}})
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

.more-btn {
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding: 0 20%; /* Adjust the percentage as needed */
}

.v-btn {
    margin-top: 15px;
}

.formTitle {
    text-align: center;
    margin-bottom: 15px;
}
</style>