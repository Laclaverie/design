<template>
  <v-container fill-height>
    <v-row align="center" justify="center">
      <v-col
          lg="6"
          md="8"
          sm="10">
        <v-img
            :src="require('../assets/logo.png')"
            class="mb-15"
            contain
            height="200"
        />
        <v-img
            :src="require('../assets/kinect.png')"
            class="my-10"
            contain
            height="100"
        />
      </v-col>
      <v-col
          lg="6"
          md="8"
          sm="12"
      >
        <h1 class="display-2 pb-12">Récupérez votre œuvre</h1>
        <v-card ref="form" max-width="600px" class="mx-auto">
          <v-tabs
              v-model="tab"
              background-color="blue"
              centered
              dark
              icons-and-text
          >
            <v-tab href="#tab-1">
              Entrer son code
              <v-icon>mdi-login</v-icon>
            </v-tab>

            <v-tab href="#tab-2">
              Se connecter
              <v-icon>mdi-login</v-icon>
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab">
            <v-tab-item value="tab-1">
              <v-card class="py-3 px-3" flat>
                <h3>Saisissez votre code</h3>
                <v-form
                    ref="form"
                    lazy-validation
                >
                  <v-text-field
                      v-model="id"
                      :counter="6"
                      label="Code en 6 caractères"
                      required
                  ></v-text-field>
                  <v-btn
                      class="mr-4"
                      color="success"
                      type="submit"
                      @click="submit"
                  >
                    Voir mon image
                  </v-btn>
                </v-form>
              </v-card>
            </v-tab-item>
            <v-tab-item value="tab-2">
              <v-card flat>
                <Login/>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Login from "@/components/Login";

export default {
  components: {
    Login,
  },
  data: () => ({
    tab: null,
    id: null,
  }),

  methods: {

    submit() {
      this.$router.push('/picture?q=' + this.id)
    },

  },
}
</script>

