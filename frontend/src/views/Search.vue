<template>
    <v-container>
        <v-row>
            <v-col v-for="(book, index) in books" :key="index" cols="12">
                <v-card>
                    <v-card-title>{{ book.title }} - {{ book.author }}</v-card-title>
                    <v-card-text>
                        <v-list>
                            <v-list-item v-for="(chapter, index) in book.chapters" :key="index">
                                <v-list-item-content>{{ chapter.name }}</v-list-item-content>
                                <v-list-item-action>
                                    <v-btn @click="downloadChapter(book.id, chapter)">Download</v-btn>
                                    <v-progress-linear v-if="chapter.downloading" :value="chapter.progress" />
                                </v-list-item-action>
                            </v-list-item>
                        </v-list>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            books: [],
        }
    },
    created() {
        let args = this.$route.query
        let key = args.key || ''

        axios.get('http://localhost:5000/api/search/', {
            params: {
                keywords: key
            }
        }).then((response) => {
            console.log(response.data)
            this.books = response.data
        }).catch((error) => {
            console.error(error)
        });
    },
    methods: {
        downloadChapter(book_id, chapter) {
            chapter.downloading = true;
            axios.get(`http://localhost:5000/api/search/download/${book_id}/${chapter}/`,
                {
                    responseType: 'blob',
                    onDownloadProgress: (progressEvent) => {
                        chapter.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    }
                })
                .then((response) => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'file'); // or any other extension
                    document.body.appendChild(link);
                    link.click();
                    chapter.downloading = false;
                }).catch((error) => {
                    chapter.downloading = false;
                    chapter.progress = 0;
                    console.error(error)
                });
        }
    }
}
</script>