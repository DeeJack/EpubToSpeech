<template>
    <v-container style="display: grid" dark>
        <v-row>
            <v-col cols="12">
                <v-text-field v-model="search" append-icon="mdi-magnify" label="Search files" single-line
                    hide-details></v-text-field>
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col cols="12" sm="8" md="6">
                <div class="container">
                    <v-file-input v-model="file" :loading="loading" :progress="progress" show-size accept=".epub"
                        label="Drag and drop .epub file here or click to select"
                        placeholder="Drag and drop .epub file here or click to select" outlined
                        @change="handleFileUpload"></v-file-input>

                    <v-progress-linear v-if="loading" :value="progress" color="blue" height="20">
                        <strong>Uploading, please wait...</strong>
                    </v-progress-linear>
                </div>

            </v-col>
        </v-row>
    </v-container>
</template>
  
<script setup>
import { ref } from 'vue';

let search = ref('');
let file = ref(null);
let loading = ref(false);
let progress = ref(0);

const handleFileUpload = () => {
    loading.value = true;
    // Implement your file upload logic here
    // Update the progress.value as the file uploads
};
</script>

<style scoped>
.v-container {
    height: 100%;

}

.container {
    max-width: 100%;
    margin: 0 auto;
}

.center {
    margin: auto;
    width: 50%;
    padding: 10px;
}
</style>