<template>
  <v-card ref="form" class="py-3 px-3">
    <v-card-text>
      <v-text-field
          ref="name"
          v-model="name"
          :error-messages="errorMessages"
          :rules="[() => !!name || 'Ce champ est obligatoire']"
          label="Nom complet"
          placeholder="John Doe"
          required
      ></v-text-field>
      <v-text-field
          id="email"
          v-model="email"
          label="Mail"
          name="email"
          required
          type="email"
      ></v-text-field>
      <v-text-field
          ref="city"
          v-model="city"
          :rules="[() => !!city || 'Ce champ est obligatoire', addressCheck]"
          label="Ville"
          placeholder="Saint-etienne"
          required
      ></v-text-field>
      <v-text-field
          ref="zip"
          v-model="zip"
          :rules="[() => !!zip || 'Ce champ est obligatoire']"
          label="Code Postal"
          placeholder="42000"
          required
      ></v-text-field>
      <v-autocomplete
          ref="country"
          v-model="country"
          :items="countries"
          :rules="[() => !!country || 'Ce champ est obligatoire']"
          label="Pays"
          placeholder="Select..."
          required
      ></v-autocomplete>
      <v-text-field
          id="password"
          v-model="password"
          label="Password"
          name="Password"
          type="password"
      ></v-text-field>
      <v-text-field
          id="Confirm password"
          v-model="confirmPassword"
          :rules="[comparePasswords]"
          label="Confirm Password"
          name="confirmPassword"
          type="password">
      </v-text-field>
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
      <v-btn
          :loading="loading"
          color="primary"
          text
          @click="submit"
      >
        Valider
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'Register',

  data: () => ({
    countries: ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antigua &amp; Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia &amp; Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Cape Verde', 'Cayman Islands', 'Chad', 'Chile', 'China', 'Colombia', 'Congo', 'Cook Islands', 'Costa Rica', 'Cote D Ivoire', 'Croatia', 'Cruise Ship', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Polynesia', 'French West Indies', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyz Republic', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint Pierre &amp; Miquelon', 'Samoa', 'San Marino', 'Satellite', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'St Kitts &amp; Nevis', 'St Lucia', 'St Vincent', 'St. Lucia', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', `Timor L'Este`, 'Togo', 'Tonga', 'Trinidad &amp; Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks &amp; Caicos', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Virgin Islands (US)', 'Yemen', 'Zambia', 'Zimbabwe'],
    email: null,
    password: null,
    confirmPassword: '',
    name: null,
    city: null,
    zip: null,
    country: 'France',

    errorMessages: '',
    formHasErrors: false,

    loader: null,
    loading: false,
  }),

  computed: {
    form() {
      return {
        name: this.name,
        city: this.city,
        zip: this.zip,
        country: this.country,
      }
    },
  },

  watch: {
    name() {
      this.errorMessages = ''
    },

    user(value) {
      if (value !== null && value !== undefined)
        this.$router.push('/');
    },

    loader() {
      const l = this.loader
      this[l] = !this[l]

      setTimeout(() => (this[l] = false), 3000)

      this.loader = null
    },
  },

  methods: {
    comparePasswords() {
      return this.password !== this.confirmPassword ? 'Passwords do not match' : ''
    },

    testPasswordLength() {
      return this.password.length < 6 ? 'Password too short' : ''
    },

    user() {
      return this.$store.getters.user;
    },

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

      if (this.formHasErrors === false) {
        if (this.comparePasswords() !== '')
          alert("mot de passe non indentiques")
        else if (this.testPasswordLength() !== '')
          alert("Mot de passe trop court")
        else {
          this.$store.dispatch('signUserUp', {email: this.email, name: this.name, password: this.password,})
          this.loader = 'loading'
        }
      }
    },
  },
}
</script>

