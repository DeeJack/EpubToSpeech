<template>
    <v-main>
        <v-container>
            <v-select v-model="service" :items="services" label="Service" :rules="[v => !!v || 'Service is required']"
                required></v-select>

            <!-- Add voices select? -->

            <v-data-table :headers="headers" :items="chapters" item-key="id" class="elevation-1">
                <template v-slot:item.selected="{ item }">
                    <v-checkbox v-model="item.selected"></v-checkbox>
                </template>
            </v-data-table>
        </v-container>
    </v-main>
</template>

<script>
import { ref } from 'vue';
let service = ref(null);
let services = ['Azure', 'OpenAI', 'ElevenLabs', 'Local'];

let headers = [
    { title: 'Select', value: 'selected', sortable: false, width: '10%' },
    { title: 'Chapter name', value: 'name' },
];
let chapters = ref([]); // This should be updated with the chapters from the server

export default {
    data: () => ({
        headers,
        chapters,
        services,
        service
    }),
    created: () => {
        // Fetch chapters from server
        console.log('TEST')
        chapters.value = [{
                id: 1,
                name: 'Chapter 1',
                selected: false,
            },
            {
                id: 2,
                name: 'Chapter 2',
                selected: false,
            },
            {
                id: 3,
                name: 'Chapter 3',
                selected: false,
            },
        ];
    },
}
</script>