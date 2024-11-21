<template>
    <div class="profile-form">
      <h2>Profile Settings</h2>
  
      <!-- Update Username Section -->
      <div class="section">
        <h3>Update Username</h3>
        <form @submit.prevent="handleUpdateUsername">
          <input
            type="text"
            v-model="username"
            placeholder="Enter new username"
            required
          />
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
          <input
            type="file"
            accept="image/*"
            @change="handleImageUpload"
            class="file-input"
          />
  
          <!-- Cropper -->
          <advanced-cropper
            v-if="imageSource"
            :src="imageSource"
            :aspect-ratio="1"
            :guidelines="true"
            :stencil-props="{ aspectRatio: 1, borderRadius: 50 }"
            ref="cropper"
          />
  
          <!-- Placeholder for No Picture -->
          <p v-else>No profile picture uploaded. Please upload one.</p>
  
          <button
            class="submit-button"
            @click="handleSaveProfilePicture"
            :disabled="!imageSource"
          >
            Save Profile Picture
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Cropper } from "vue-advanced-cropper";
  
  export default {
    components: {
      AdvancedCropper: Cropper,
    },
    data() {
      return {
        username: "",
        imageSource: null, // The image file source for the cropper
      };
    },
    methods: {
      handleUpdateUsername() {
        alert(`Username updated to "${this.username}"! (Backend integration required)`);
      },
      handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.imageSource = e.target.result; // Set the image source for the cropper
          };
          reader.readAsDataURL(file); // Read the file as a data URL
        }
      },
      handleSaveProfilePicture() {
        if (this.$refs.cropper) {
          const croppedCanvas = this.$refs.cropper.getCanvas();
          const croppedImage = croppedCanvas.toDataURL(); // Generate base64 image
          alert("Profile picture updated successfully! (Backend integration required)");
          console.log("Cropped Image Data:", croppedImage);
        } else {
          alert("No profile picture available for saving.");
        }
      },
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
  }
  </style>
  