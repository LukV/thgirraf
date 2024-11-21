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
      ...mapActions(['addNotification', 'requestPasswordReset']),
      async handlePasswordReset() {
        try {
          await this.requestPasswordReset({ email: this.email });
          this.addNotification({
            message: "Password reset email sent. Please check your inbox.",
            type: "info",
          });
          this.$router.push("/");
        } catch (error) {
          this.addNotification({
            message: error.response?.data?.detail[0].msg || 'Failed to send password reset email.',
            type: "error",
          });
        }
      },
      switchToLogin() {
        this.$emit('switch-mode', 'login');
      },
    },
  };
  </script>
  