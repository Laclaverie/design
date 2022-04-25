<template>
  <v-card ref="form" class="py-3 px-3">
    <v-form @submit.prevent="onSignIn">
      <v-card-text>
        <v-text-field
            id="email"
            v-model="email"
            label="Mail"
            name="email"
            required
            type="email"
        ></v-text-field>
        <v-text-field
            id="password"
            v-model="password"
            autocomplete="password"
            label="Password"
            name="Password"
            type="password"
        ></v-text-field>
      </v-card-text>
      <v-divider class="mt-12"></v-divider>
      <v-card-actions>
        <v-btn text>
          Annuler
        </v-btn>
        <v-spacer></v-spacer>
        <v-slide-x-reverse-transition>
          <v-tooltip
              v-if="formHasErrors"
              left
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                  v-bind="attrs"
                  v-on="on"
                  class="my-0"
                  icon
                  @click="resetForm"
              >
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </template>
            <span>Tout effacer</span>
          </v-tooltip>
        </v-slide-x-reverse-transition>
        <v-progress-circular
            v-if="loading"
            class="ma-3"
            color="primary"
            indeterminate
        ></v-progress-circular>
        <v-btn
            v-show="!loading"
            color="primary"
            text
            type="submit"
            @click="loading=true"
        >
          Valider
        </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
import firebase from "firebase/app";

export default {
  name: "Login",

  data: () => ({
    errorMessages: '',
    email: null,
    password: null,
    formHasErrors: false,
    loading: false,
  }),

  computed: {
    form() {
      return {
        name: this.name,
      }
    },
  },

  watch: {
    name() {
      this.errorMessages = ''
    },
  },

  methods: {

    resetForm() {
      this.errorMessages = []
      this.formHasErrors = false

      Object.keys(this.form).forEach(f => {
        this.$refs[f].reset()
      })
    },

    submit() {
      this.formHasErrors = false

      Object.keys(this.form).forEach(f => {
        if (!this.form[f]) this.formHasErrors = true

        this.$refs[f].validate(true)
      })

      if (this.formHasErrors === false)
        alert("ok")
    },

    async onSignIn() {
      try {
        const user = await firebase.auth().signInWithEmailAndPassword(this.email, this.password);
        console.log('user : ' + user);
        await this.$router.push('/pictures');

      } catch (e) {
        alert(e.message)
      } finally {
        this.loading = false;
      }

    }
  },
}
</script>

<style scoped>

</style>