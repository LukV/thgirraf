<template>
  <div class="sign-up-form">
    <h2>Sign Up</h2>
    <form @submit.prevent="signUp">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit" class="submit-button">Sign Up</button>
    </form>
    <p>Or</p>
    <button @click="signInWithGoogle" class="google-button">
      <i class="fab fa-google"></i> Sign Up with Google
    </button>
    <p>Already have an account? <router-link to="/login">Back to Login</router-link></p>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import apiClient from '@/apiClient';
import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';

export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
    };
  },
  methods: {
    ...mapActions(['login']),
    async signUp() {
      try {
        // Create a new user in the backend
        await apiClient.post('/users/', {
          email: this.email,
          username: this.username,
          password: this.password,
        });

        // Log the user in via Vuex action
        await this.login({
          username: this.username,
          password: this.password,
        });

        // Emit success event to close overlay
        this.$emit('auth-success');
      } catch (error) {
        console.error(error);
        // Handle errors
      }
    },
    async signInWithGoogle() {
      const auth = getAuth();
      const provider = new GoogleAuthProvider();

      try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        const idToken = await user.getIdToken();

        // Log the user in via Vuex action
        await this.login({
          token: idToken,
        });

        // Emit success event to close overlay
        this.$emit('auth-success');
      } catch (error) {
        console.error(error);
        // Handle errors
      }
    },
  },
};
</script>
