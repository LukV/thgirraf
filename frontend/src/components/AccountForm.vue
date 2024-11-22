<template>
  <div class="account-form">
    <h2>Account settings</h2>

    <!-- Change Password Section -->
    <div class="section">
      <h3>Change password</h3>
      <form @submit.prevent="handleChangePassword">
        <input type="password" v-model="newPassword" placeholder="New password" required />
        <input type="password" v-model="confirmPassword" placeholder="Confirm new password" required />
        <button type="submit" class="submit-button" :disabled="isChangePasswordDisabled">
          Update password
        </button>
      </form>
    </div>

    <hr class="styled-divider" />

    <!-- Delete Account Section -->
    <div class="section">
      <h3>Delete account</h3>
      <p>
        Warning -- Deleting your account will remove all your posts, followers,
        preferences, and other related data permanently.
      </p>
      <router-link to="/delete-account" class="delete-link">
        Proceed to Delete Account
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import apiClient from '@/apiClient';

export default {
  data() {
    return {
      newPassword: '',
      confirmPassword: '',
    };
  },
  computed: {
    isChangePasswordDisabled() {
      return (
        !this.newPassword || this.newPassword !== this.confirmPassword
      );
    },
  },
  methods: {
    ...mapActions(['addNotification']),
    async handleChangePassword() {
      try {
        const passwordData = {
          new_password: this.newPassword,
        };
        await apiClient.post("/users/change-password", passwordData);
        this.addNotification({ 
          message: 'Password successfully updated.', 
          type: 'info' 
        });
        this.$router.push("/");
      } catch (error) {
        this.addNotification({ 
          message: error.response?.data?.detail[0].msg || 'Password change failed. Please try again.', 
          type: 'error' 
        });
      }
    },
  },
};
</script>

<style scoped>
.account-form {
  padding: 2rem;
  max-width: 400px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section {
  margin-bottom: 2rem;
}

.styled-divider {
  border: none;
  height: 2px;
  background: #ddd;
  margin: 1.5rem 0;
}

h3 {
  margin-bottom: 1rem;
  text-align: left;
}

p {
  text-align: left;
  margin: 10px 0 25px auto;
}

form {
  display: flex;
  flex-direction: column;
}

input {
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-button {
  background-color: #4caf50;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.delete-link {
  color: #d9534f;
  font-weight: bold;
  text-decoration: none;
}

.delete-link:hover {
  text-decoration: underline;
}
</style>