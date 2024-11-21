<template>
  <div class="confirm-delete">
    <h2>Confirm account deletion</h2>
    <p>
      To confirm account deletion, please type
      <strong>"delete"</strong> below and click the
      <strong>Delete Account</strong> button. This action cannot be undone.
    </p>
    <form @submit.prevent="confirmDeleteAccount">
      <input type="text" v-model="confirmationInput" placeholder="Type 'delete' to confirm" required />
      <button type="submit" class="delete-button" :disabled="isDeleteDisabled">
        Delete account
      </button>
    </form>
    <router-link to="/account" class="back-link">
      Back to Account Settings
    </router-link>
  </div>
</template>

<script>
import apiClient from "@/apiClient";
import { mapActions, mapState } from "vuex";

export default {
  data() {
    return {
      confirmationInput: "",
    };
  },
  computed: {
    ...mapState(["user"]),
    isDeleteDisabled() {
      return this.confirmationInput.toLowerCase() !== "delete";
    },
  },
  methods: {
    ...mapActions(['addNotification', 'logout']), 
    async confirmDeleteAccount() {
      try {
        const userId = this.user.id; // Get user ID from Vuex state
        await apiClient.delete(`/users/${userId}`);
        this.addNotification({
          message: "Account deleted successfully. Wishing you all the best!",
          type: "info",
        });
        this.logout();
        this.$router.push("/");
      } catch (error) {
        console.error("Error deleting account:", error);
        this.addNotification({
          message: error.response?.data?.detail || "Failed to delete account.",
          type: "error",
        });
      }
    },
  },
};
</script>

<style scoped>
.confirm-delete {
  padding: 2rem;
  max-width: 400px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 1rem;
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

.delete-button {
  background-color: #d9534f;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.back-link {
  margin-top: 1rem;
  display: inline-block;
  color: #007bff;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}
</style>