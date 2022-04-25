<template>
  <v-container>
    <h1>Image n°{{ id }}</h1>
    <v-row v-if="loading">
      <v-col>
        <v-progress-linear indeterminate></v-progress-linear>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col>
        <v-img :src="link"></v-img>
        <v-btn :href="link" class="ma-5" color="primary" download target="_blank">Telecharger</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

import firebase from "firebase"


const storage = firebase.storage();

export default {
  name: "Picture",
  props: {},
  data: () => ({
    id: null,
    loading: true,
    link: null,
  }),
  async mounted() {
    this.id = this.$attrs.query;
    this.loading = true;
    try {
      this.link = await storage.ref('pictures/' + this.id + '.png').getDownloadURL();
    } catch (e) {
      switch (e.code) {
        case 'storage/object-not-found' : {
          alert("L'image n'existe pas. Veuillez rééssayer avec un code valide");
          break;
        }
        default : {
          alert("Impossible d'acceder à la base");
        }

      }
      await this.$router.push("/");
    } finally {
      this.loading = false

    }
  },

}
</script>

<style scoped>

</style>