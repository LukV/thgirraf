<template>
  <div class="header">
    <div>
      <div class="menu-icon" @click="$emit('toggle-overlay')">
        <i class="fas fa-bars"></i>
      </div>
    </div>
    <div class="logo">
      <img src="@/assets/images/logo.png" alt="Logo" />
      <div class="logo-title">
        <span>The</span>
        <span>Standout</span>
      </div>
    </div>
    <div class="header-right">
      <router-link to="/signup" class="link-button" v-if="!isAuthenticated">Sign up</router-link>
      <router-link to="/login" class="button" v-if="!isAuthenticated">Login</router-link>
      <div v-else class="user-info">
        <img
          v-if="user && user.icon"
          :src="user.icon"
          alt="User Icon"
          class="user-icon"
          @click="toggleUserMenu"
        />
        <span v-if="user && !user.icon" class="user-placeholder" @click="toggleUserMenu">
          {{ user.username.charAt(0) }}
        </span>
        <div v-if="showUserMenu" class="user-menu">
          <p>Welcome, {{ user.username }}</p>
          <button @click="logout">Logout</button>
          <router-link to="/profile" class="menu-item">Edit Profile</router-link>
        </div>
      </div>
      <div class="search-container">
        <input type="text" class="search-input" v-model="searchQuery" />
        <span class="search-icon"><i class="fas fa-search"></i></span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';

export default {
  data() {
    return {
      searchQuery: '',
      showUserMenu: false,
    };
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated']),
  },
  methods: {
    ...mapActions(['logout']),
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100px;
  position: relative;
  padding: 0 20px;
  border-bottom: 1px solid #ddd;
}

.logo {
  display: flex;
  align-items: center;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.logo img {
  height: 70px;
}

.logo-title {
  font-family: FlandersArtSerif;
  font-size: 28px;
  font-weight: bold;
  line-height: 1em;
  margin: 15px;
  text-align: center;
}

.logo-title span {
  display: block;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1em;
}

.button {
  display: inline-block;
  padding: 12px 30px;
  font-size: 12px;
  background-color: #5052C0;
  color: white;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #51459c;
}

.link-button {
  text-decoration: none;
  color: #505963;
}

.link-button:hover {
  text-decoration: underline;
  color: #5052C0;
}

.search-container {
  position: relative;
  width: 50px;
  transition: width 0.3s ease;
}

.search-container:focus-within {
  width: 150px;
}

.search-input {
  width: 100%;
  padding: 18px 25px 18px 5px;
  height: 30px;
  border: 1px solid #6a5acd;
  border-radius: 2px;
  outline: none;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  transition: width 0.3s ease;
}

.search-icon {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  color: #555;
  pointer-events: none;
}

.user-info {
  display: flex;
  align-items: center;
  position: relative;
}

.user-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
}

.user-placeholder {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ddd;
  color: #333;
  border-radius: 50%;
  cursor: pointer;
  font-weight: bold;
}

.user-menu {
  position: absolute;
  top: 50px;
  right: 0;
  background-color: white;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  padding: 10px;
  z-index: 10;
}

.user-menu p {
  margin: 0;
  font-size: 14px;
}

.user-menu .menu-item {
  display: block;
  padding: 8px 0;
  color: #333;
  text-decoration: none;
}

.user-menu .menu-item:hover {
  color: #5052C0;
}

@media (max-width: 900px) {
  .header-right {
    display: none;
  }

  .menu-icon {
    display: block;
  }
}
</style>
