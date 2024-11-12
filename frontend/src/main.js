// main.js
import { createApp } from 'vue';
import App from './App.vue';
import { auth } from './firebase';

let app;

auth.onAuthStateChanged(() => {
  if (!app) {
    app = createApp(App);
    app.mount('#app');
  }
});
