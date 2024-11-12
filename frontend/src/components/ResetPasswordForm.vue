<template>
    <div class="reset-password-form">
      <h2>Reset Password</h2>
      <form @submit.prevent="resetPassword">
        <input type="email" v-model="email" placeholder="Email" required />
        <button type="submit" class="submit-button">Send Reset Email</button>
      </form>
      <p><a href="#" @click.prevent="switchToLogin">Back to Login</a></p>
    </div>
  </template>
  
  <script>
  import { auth } from '@/firebase';
  
  export default {
    data() {
      return {
        email: '',
      };
    },
    methods: {
      resetPassword() {
        auth.sendPasswordResetEmail(this.email)
          .then(() => {
            alert('Password reset email sent. Please check your inbox.');
            this.$emit('switch-mode', 'login');
          })
          .catch((error) => {
            console.error(error);
          });
      },
      switchToLogin() {
        this.$emit('switch-mode', 'login');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add styles as needed */
  </style>
  