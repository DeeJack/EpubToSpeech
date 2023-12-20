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

let form = ref(null);
let valid = ref(false);
let title = ref('');
let author = ref('');
let id = ref('');
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
    created() {
        const args = this.$route.query
        this.title = args.title
        this.author = args.author
        this.id = args.id
    },
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