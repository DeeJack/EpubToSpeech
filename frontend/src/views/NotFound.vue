<template>
    <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="6">
                <div class="text-center">
                    <div class="center">
                        <v-img align="center" justify="center" max-width="200" src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"></v-img>
                    </div>
                    <v-alert type="error" dark icon="mdi-alert">
                        <h1 class="display-2 font-weight-bold mb-4">404</h1>
                        <h2 class="headline font-weight-normal">This page could not be found</h2>
                        <p class="title">You may have mistyped the address or the page may have moved.</p>
                        <v-btn color="primary" dark large router-link to="/">Go to Home</v-btn>
                    </v-alert>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    name: 'NotFound',
};
</script>

<style scoped>
.center {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>