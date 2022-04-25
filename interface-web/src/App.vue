<template>
  <v-app id="app">
    <Navbar/>
    <router-view/>
    <Footer/>
  </v-app>
</template>

<script>
import Footer from "@/components/app/Footer";
import Navbar from "@/components/app/Navbar";

import firebase from 'firebase/app';
import 'firebase/firestore';

const config = {
  apiKey: "AIzaSyCA6wqd1CbI4ALT0IqMZJf5Rykh3HG4xXw",
  authDomain: "biennale-742d2.firebaseapp.com",
  databaseURL: "https://biennale-742d2-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "biennale-742d2",
  storageBucket: "biennale-742d2.appspot.com",
  messagingSenderId: "488997263871",
  appId: "1:488997263871:web:186e112436cde18f756fca"
};
firebase.initializeApp(config);

export default {
  name: 'App',
  components: {Navbar, Footer},
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  background-color: aliceblue;
}

</style>