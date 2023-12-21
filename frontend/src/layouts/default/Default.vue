<template>
  <v-app>
    <!-- <default-bar /> -->
    <v-app-bar app>
      <v-toolbar-title>EpubToSpeech</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn to="/">Upload</v-btn>
      <v-btn :to="'/tts?id=' + this.$route.query.id" v-if="this.$route.query.id">TTS</v-btn>
      <v-btn :to="'/reader?id=' + this.$route.query.id" v-if="this.$route.query.id">Reader</v-btn>
    </v-app-bar>

    <default-view />
  </v-app>
</template>

<script setup>
import DefaultView from './View.vue'
</script>
