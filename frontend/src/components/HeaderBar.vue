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
      <div v-else class="user-info" ref="userInfo">
        <div class="user-details" @click.stop="toggleUserMenu">
          <img v-if="userIconUrl" :src="userIconUrl" alt="User Icon" class="user-icon" />
          <div v-else class="user-placeholder">
            {{ user.username ? user.username.charAt(0).toUpperCase() : "?" }}
          </div>
          <span class="user-name">{{ user.username }}</span>
        </div>
        <div v-if="showUserMenu" class="user-menu">
          <router-link to="/account" class="menu-item">
            <i class="fas fa-user"></i>
            <span>Account</span>
          </router-link>
          <div class="menu-divider"></div>
          <router-link to="/profile" class="menu-item">
            <i class="fas fa-edit"></i>
            <span>Profile</span>
          </router-link>
          <div class="menu-divider"></div>
          <div class="menu-item" @click="logout">
            <i class="fas fa-sign-out-alt"></i>
            <span>Logout</span>
          </div>
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
      showUserMenu: false,
    };
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated', 'userIconUrl']),
  },
  methods: {
    ...mapActions(['logout']),
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    closeUserMenu() {
      this.showUserMenu = false;
    },
    handleClickOutside(event) {
      if (
        this.showUserMenu &&
        this.$refs.userInfo &&
        !this.$refs.userInfo.contains(event.target)
      ) {
        this.closeUserMenu();
      }
    },
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
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
  font-weight: bold;
  margin: 15px;
  text-align: center;
}

.logo-title span {
  display: block;
  font-size: 38px;
  line-height: .9em ;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1em;
}

.button {
  display: inline-block;
  padding: 12px 30px;
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
  gap: 10px;
  cursor: pointer;
  position: relative;
}

.user-details {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
}

.user-icon {
  width: 40px;
  height: 40px;
  border-radius: 35%;
  object-fit: cover;
  cursor: pointer;
}

.user-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 35%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ccc;
  color: white;
  font-size: 24px;
  font-weight: bold;
  text-transform: uppercase;
}

.user-name {
  font-weight: bold;
  color: #333;
}

.user-menu {
  position: absolute;
  top: 50px;
  right: 0;
  width: 150px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 15px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-decoration: none;
}

.menu-item:hover {
  background-color: #f4f4f4;
}

.menu-item i {
  color: #5052C0;
}

.menu-divider {
  height: 1px;
  background-color: #ddd;
  margin: 0;
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
