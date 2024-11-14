import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import store from './store'; // Import your Vuex store

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;

store.dispatch('restoreAuth').then(() => {
  const app = createApp(App);
  app.use(store);
  app.mount('#app');

});
