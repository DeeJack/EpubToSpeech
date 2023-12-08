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

                <v-select v-model="service" :items="services" label="Service" :rules="[v => !!v || 'Service is required']"
                    required></v-select>

                <!-- Add voices select? -->

                <v-data-table :headers="headers" :items="chapters" item-key="id" class="elevation-1" >
                    <template v-slot:item.selected="{ item }">
                        <v-checkbox v-model="item.selected"></v-checkbox>
                    </template>
                </v-data-table>

                <div class="center">
                    <v-btn color="primary" type="submit">Create Request</v-btn>
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
let service = ref(null);
let services = ['Azure', 'OpenAI', 'ElevenLabs', 'Local'];

let headers = [
    { title: 'Select', value: 'selected', sortable: false, width: '10%' },
    { title: 'Chapter name', value: 'name' },
];
let chapters = ref([]); // This should be updated with the chapters from the server

const createRequest = () => {
    if (form.value.validate()) {
        // Implement your request creation logic here
    }
};

export default {
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
    data: () => ({
        form,
        valid,
        title,
        author,
        description,
        service,
        services,
        headers,
        chapters,
    }),
    methods: {
        createRequest,
    },

}
</script>

<style scoped>
.center {

    display: flex;
    justify-content: center;
    align-items: center;
}

.v-btn {
    margin-top: 15px;
}

.formTitle {
    text-align: center;
    margin-bottom: 15px;
}
</style>