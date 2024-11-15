<template>
    <div class="reset-password-form">
      <h2>Request Password Reset</h2>
      <form @submit.prevent="handlePasswordReset">
        <input type="email" v-model="email" placeholder="Enter your email" required />
        <button type="submit" class="submit-button">Send Reset Email</button>
      </form>
      <p><router-link to="/login">Back to Login</router-link></p>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  
  export default {
    data() {
      return {
        email: '',
      };
    },
    methods: {
      ...mapActions(['requestPasswordReset']),
      async handlePasswordReset() {
        try {
          await this.requestPasswordReset({ email: this.email });
          alert('Password reset email sent. Please check your inbox.');
        } catch (error) {
          alert(error.response?.data?.detail || 'Failed to send password reset email.');
        }
      },
      switchToLogin() {
        this.$emit('switch-mode', 'login');
      },
    },
  };
  </script>
  