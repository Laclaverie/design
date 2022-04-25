<template>
  <v-footer
      class="footer"
      color="primary lighten-1"
      padless
  >
    <v-row
        justify="center"
        no-gutters
    >
      <v-btn
          v-for="(link, index) in links"
          :key="index"
          :href="link.link"
          class="my-2"
          color="white"
          rounded
          text
      >
        {{ link.name }}
      </v-btn>
      <v-col
          class="primary lighten-2 py-4 text-center white--text"
          cols="12"
      >
        Un projet des étudiants de Télécom Saint-Etienne — <strong>{{ new Date().getFullYear() }}</strong>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  name: 'Footer',

  data: () => ({
    links: [
      {
        name: 'Telecom Saint-Etienne',
        link: 'https://www.telecom-st-etienne.fr/'
      },
      {
        name: 'Faculté de Design',
      },
      {
        name: 'Contactez-nous'
      },
    ],
  }),
}
</script>

<style scoped>
.footer {
  margin-top: auto;
}

</style>