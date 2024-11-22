<template>
  <div class="profile-form">
    <h2>Profile Settings</h2>

    <!-- Update Username Section -->
    <div class="section">
      <h3>Update Username</h3>
      <form @submit.prevent="handleUpdateUsername">
        <input type="text" v-model="username" placeholder="Enter new username" required />
        <button type="submit" class="submit-button" :disabled="!username">
          Save Username
        </button>
      </form>
    </div>

    <hr class="styled-divider" />

    <!-- Update Profile Picture Section -->
    <div class="section">
      <h3>Update Profile Picture</h3>
      <div class="profile-picture-container">
        <!-- Profile Picture Upload -->
        <input type="file" accept="image/*" @change="handleImageUpload" class="file-input" />

        <!-- Cropper -->
        <advanced-cropper v-if="imageSource" :src="imageSource" :aspect-ratio="1" :guidelines="true"
          :stencil-props="{ aspectRatio: 1, borderRadius: 50 }" ref="cropper" />

        <!-- Placeholder for No Picture -->
        <p v-else>No profile picture uploaded. Please upload one.</p>

        <button class="submit-button" @click="handleSaveProfilePicture" :disabled="!imageSource || loading">
          {{ loading ? "Saving..." : "Save Profile Picture" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { Cropper } from "vue-advanced-cropper";
import { mapState, mapActions } from 'vuex';
import apiClient from '@/apiClient';
import 'vue-advanced-cropper/dist/style.css';

export default {
  components: {
    AdvancedCropper: Cropper,
  },
  data() {
    return {
      username: "",
      imageSource: null,
      loading: false, // Indicates upload progress
    };
  },
  computed: {
    ...mapState(['user']),
  },
  methods: {
    ...mapActions(['addNotification']),
    async handleUpdateUsername() {
      try {
        const usernameData = {
          username: this.username,
        };
        const userId = this.user.id;
        await apiClient.put(`/users/${userId}`, usernameData);
        this.addNotification({ 
          message: `Username successfully updated to ${this.username}.`, 
          type: 'info' 
        });
        this.$router.push("/");
      } catch (error) {
        console.log(error);
        this.addNotification({ 
          message: error.response?.data?.detail[0].msg || 'Failed trying to update your username. Please try again.', 
          type: 'error' 
        });
      }
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Validate file type and size
        if (!file.type.startsWith("image/")) {
          this.addNotification({
            message: "Only image files are allowed (webp, png, jpg, gif). Please try again.",
            type: "error",
          });
          return;
        }
        if (file.size > 5 * 1024 * 1024) {
          this.addNotification({
            message: "File size should not exceed 5MB. I mean really...",
            type: "error",
          });
          return;
        }

        // Read file as data URL for the cropper
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageSource = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async handleSaveProfilePicture() {
      if (this.$refs.cropper) {
        this.loading = true;
        try {
          const croppedCanvas = this.$refs.cropper.getCanvas();
          const croppedImage = await new Promise((resolve) =>
            croppedCanvas.toBlob(resolve, "image/png")
          );

          const formData = new FormData();
          formData.append("file", croppedImage, "profile-picture.png");

          const userId = this.user.id; // Assuming current user info is available in your state

          await apiClient.put(`/users/${userId}/icon`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
          this.addNotification({
            message: "Profile picture updated successfully!",
            type: "info",
          });
          this.$router.push("/");
        } catch (error) {
          // Error notification
          const errorMessage = error;
          this.addNotification({
            message: errorMessage,
            type: "error",
          });
        } finally {
          this.loading = false;
        }
      } else {
        this.addNotification({
          message: "No profile picture available for saving.",
          type: "error",
        });
      }
    }
  },
};
</script>

<style scoped>
.profile-form {
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
}

form {
  display: flex;
  flex-direction: column;
}

input[type="text"] {
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.file-input {
  margin-bottom: 1rem;
}

button {
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button {
  background-color: #4caf50;
  color: white;
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.profile-picture-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  max-width: 300px; /* Adjust as necessary */
  margin: 0 auto;
}

.advanced-cropper {
  width: 100%; /* Ensure it scales to the container */
  max-height: 300px; /* Constrain height */
  overflow: hidden;
}
</style>
