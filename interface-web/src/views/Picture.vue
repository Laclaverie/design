<template>
  <v-container>
    <h1>Pictures</h1>
    <v-row v-if="loading" justify="center">
      <v-col align-self="center">
        <v-progress-linear indeterminate></v-progress-linear>
      </v-col>
    </v-row>
    <v-container v-else-if="files.length!==0" fluid>
      <v-toolbar
          class="my-3"
          dense
          floating
      >
        <v-text-field
            v-model="search"
            hide-details
            prepend-icon="mdi-magnify"
            single-line
        ></v-text-field>
      </v-toolbar>
      <v-row dense>
        <v-col
            v-for="(file, index) in files"
            v-show="search===''|| file.name.startsWith(search) "
            :key="index"
            lg="6"
            md="6"
            sm="12"
            xl="4"
        >
          <v-card>
            <v-img
                :src="file.link"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="300px"
            >
              <v-card-title :v-text="file.name">{{ file.name }}</v-card-title>
            </v-img>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn :href="file.link" download icon target="_blank">
                <v-icon>mdi-download</v-icon>
              </v-btn>

              <v-btn v-if="!deleteLoading" icon @click="deleteRef(file.name)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              <v-progress-circular
                  v-else
                  indeterminate/>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <H2 v-if="files.length===0 && !loading" class="mt-10">Pas d'image 😢</H2>

  </v-container>
</template>

<script>

import firebase from "firebase"

const storage = firebase.storage();
const storageRef = storage.ref('pictures');


export default {
  name: "Picture",
  data: () => ({
    loading: true,
    deleteLoading: false,
    files: [],
    search: '',
  }),

  async mounted() {
    this.loading = true;

    const res = await storageRef.listAll()
    res.prefixes.forEach((folderRef) => {
      console.log(folderRef)
    });

    for (const itemRef of res.items) {
      const link = await storage.ref('pictures/' + itemRef.name).getDownloadURL();

      this.files.push({name: itemRef.name, link: link})
    }

    this.loading = false

  },

  methods: {

    findWithAttr(array, attr, value) {
      for (let i = 0; i < array.length; i += 1) {
        if (array[i][attr] === value) {
          return i;
        }
      }
      return -1;
    },

    async deleteRef(name) {

      this.deleteLoading = true;
      const self = this;

      // Create a reference to the file to delete
      const toDelete = storage.ref('pictures/' + name);

      try {
        await toDelete.delete();
        let index = self.findWithAttr(self.files, "name", name);
        console.log(index)
        if (index > -1) {
          self.files.splice(index, 1);
          console.log("image supprimée")
          self.index++;
        }
      } catch (error) {
        alert(error.code + ' : ' + error.message);
      } finally {
        this.deleteLoading = false;
      }
    },
  }

}
</script>

<style scoped>

</style>