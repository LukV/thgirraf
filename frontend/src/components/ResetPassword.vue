<template>
  <div class="set-password-form">
    <h2>Set New Password</h2>
    <form @submit.prevent="handleResetPassword">
      <input type="email" v-model="email" placeholder="Enter your email" required />
      <input type="password" v-model="newPassword" placeholder="Enter new password" required />
      <button type="submit" class="submit-button">Reset Password</button>
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
      newPassword: '',
    };
  },
  computed: {
    token() {
      // Automatically extract the token from the URL query string
      return this.$route.query.token || '';
    },
  },
  methods: {
    ...mapActions(['resetPassword']),
    async handleResetPassword() {
      try {
        // Pass the token extracted from the URL query string
        await this.resetPassword({
          email: this.email,
          newPassword: this.newPassword,
          token: this.token,
        });
        alert('Password has been reset successfully.');
        this.$router.push('/login'); // Redirect to login after success
      } catch (error) {
        alert(error.response?.data?.detail || 'Failed to reset password.');
      }
    },
  },
};
</script>


