<template>
  <v-app-bar
      app
      color="primary"
      dark
  >
    <div class="d-flex align-center">
      <a href="/">
        <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="@/assets/logoTse.png"
            transition="scale-transition"
            width="40"
        />
      </a>
      <H5 class="mx-5">Color your mood</H5>
    </div>

    <v-spacer></v-spacer>


    <v-btn
        href="https://github.com/"
        target="_blank"
        text
    >
      <span class="mr-2">Mode d'emploi</span>
      <v-icon>mdi-open-in-new</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "Navbar"
}
</script>

<style scoped>

</style>