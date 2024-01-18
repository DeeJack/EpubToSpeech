<template>
    <v-main>
        <v-container>
            <v-form ref="form" v-model="valid" @submit.prevent="createRequest">
                <v-select v-model="service" :items="services" label="Service" :rules="[v => !!v || 'Service is required']"
                    required></v-select>

                <!-- Add voices select? -->

                <v-data-table :headers="headers" :items="chapters" item-key="id" class="elevation-1" items-per-page="3"
                    :items-per-page-options="[3, 6, 10]">
                    <template v-slot:item.selected="{ item }">
                        <v-checkbox v-model="item.selected"></v-checkbox>
                    </template>
                </v-data-table>

                <div class="center">
                    <v-btn color="primary" type="submit" :disabled="loading">Generate TTS</v-btn>
                </div>
                <v-progress-linear v-if="loading" indeterminate color="blue"></v-progress-linear>
            </v-form>

            <div v-for="(audio, index) in downloadedChapters" :key="index" class="audiobox">
                <h3>Chapter {{ audio.chapter }}</h3>
                <audio controls :src="audio.url"></audio>
            </div>
        </v-container>
    </v-main>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
let service = ref(null);
let services = ['Azure', 'OpenAI', 'ElevenLabs', 'Local'];
let form = ref(null);
let valid = ref(false);
let loading = ref(false);

let downloadedChapters = ref([]);

let headers = [
    { title: 'Select', value: 'selected', sortable: false, width: '10%' },
    { title: 'Chapter number', value: 'number', width: '10%' },
    // { title: 'Chapter name', value: 'name' },
];
let chapters = ref([]); // This should be updated with the chapters from the server

export default {
    data() {
        return {
            headers,
            chapters,
            services,
            service,
            valid,
            downloadedChapters,
            loading
        }
    },
    created() {
        this.downloadedChapters = [];
        let args = this.$route.query;
        let id = args.id;
        this.loading = false;
        this.service = null
        // Fetch chapters from server
        axios.get(`http://localhost:5000/api/reader/chapters/${id}`)
            .then((response) => {
                let index = 0
                let data = response.data.map((chapter) => {
                    let chapterName = chapter.split('/').pop();
                    chapterName = chapterName.replace('.xhtml', '');
                    chapterName = chapterName.replace('.html', '')
                    let chap = {
                        'number': index,
                        'name': chapterName,
                        'selected': false
                    }
                    index++;
                    return chap
                });
                chapters.value = data;
            })
            .catch((error) => {
                console.log(error);
            });
    },
    methods: {
        async createRequest() {
            // this.valid = this.$refs.form.validate();
            if (!valid.value || !service.value) {
                return;
            }
            loading.value = true;
            let selectedChapters = chapters.value.filter((chapter) => chapter.selected);
            let chapterNumbers = selectedChapters.map((chapter) => chapter.number);
            let args = this.$route.query;
            let id = args.id;
            console.log(chapterNumbers, id, service)
            for (let chapterNumber of chapterNumbers) {
                console.log(service)
                let response = null
                try {
                    response = await axios.post(`http://localhost:5000/api/tts/`, {
                        'chapter': chapterNumber,
                        'service': service.value.toLowerCase(),
                        'book_id': id
                    }, { responseType: 'arraybuffer', timeout: 5000 })
                } catch (error) {
                    console.log(error);
                    alert('Error generating TTS')
                    loading.value = false;
                    return
                }
                if (response.status == 200) {
                    // console.log(response.data);
                    const blob = new Blob([response.data], { type: 'audio/wav' });
                    const url = URL.createObjectURL(blob);
                    downloadedChapters.value.push({ url: url, chapter: chapterNumber });
                } else {
                    alert('Error generating TTS')
                    console.log(response);
                    loading.value = false;
                }
            }
            loading.value = false;
        }
    }
}
</script>

<style scoped>
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 10px;
}

.audiobox {
    margin: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.audiobox * {
    margin-right: 10px;
}
</style>