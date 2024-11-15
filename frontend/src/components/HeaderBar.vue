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
        <span v-if="user">Welcome, {{ user.username }}</span>
        <button @click="logout">Logout</button>
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
    };
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated']),
  },
  methods: {
    ...mapActions(['logout']),
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
  /* space for the icon */
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
  /* icon won't interfere with clicking */
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1em;
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