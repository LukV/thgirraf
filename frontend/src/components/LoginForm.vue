<template>
  <div class="login-form">
    <h2>Welcome back!</h2>
    <button class="google-button" @click="signInWithGoogle">
      <i class="fab fa-google"></i> Log in with Google
    </button>
    <p>- or -</p>
    <h2>Log in with e-mail</h2>
    <form @submit.prevent="loginUser">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit" class="submit-button">Log in</button>
    </form>
    <p>
      <router-link to="/request-password-reset">Forgot Password?</router-link>
    </p>
    <p>
      Don’t have an account? 
      <router-link to="/signup">Sign up</router-link>
    </p>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { auth } from '@/firebase';

export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    ...mapActions(['login', 'addNotification']), 
    async loginUser() {
      try {
        await this.login({
          username: this.email,
          password: this.password,
        });
        this.$emit('auth-success'); // Emit success event to close overlay
      } catch (error) {
        console.error(error);
        this.addNotification({ message: error.message || 'Login failed. Please try again.', type: 'error' });
      }
    },
    async signInWithGoogle() {
      const provider = new GoogleAuthProvider();

      try {
        const result = await signInWithPopup(auth, provider); // Use initialized auth
        const user = result.user;
        const idToken = await user.getIdToken();

        await this.login({
          token: idToken,
        });

        this.$emit('auth-success'); // Emit success event to close overlay
      } catch (error) {
        console.error(error);
        this.addNotification({ message: error.message || 'Google login failed.', type: 'error' });
      }
    },
  },
};
</script>



