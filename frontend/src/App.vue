<template>
  <NotificationBar v-if="notifications.length" :notifications="notifications" @dismiss="clearNotification" />
  <div v-if="authStatus !== 'pending'" class="morrissey">
    <HeaderBar @toggle-overlay="toggleOverlay" />
    <NavBar />
    <MainContent v-if="!showAuthOverlay" />
    <PostFooter v-if="!showAuthOverlay" />
  </div>
  <AuthOverlay
    v-if="showAuthOverlay"
    :mode="authMode"
    @close="closeAuthOverlay"
  />
  <OverlayMenu v-if="overlayVisible" @toggle-overlay="toggleOverlay" />
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import HeaderBar from "./components/HeaderBar.vue";
import NavBar from "./components/NavBar.vue";
import MainContent from "./components/MainContent.vue";
import PostFooter from "./components/PostFooter.vue";
import OverlayMenu from "./components/OverlayMenu.vue";
import AuthOverlay from "./components/AuthOverlay.vue";
import NotificationBar from "@/components/NotificationBar";

// Map route names to modes
const AUTH_ROUTES = {
  Login: "login",
  SignUp: "signup",
  RequestPasswordReset: "request-reset",
  ResetPassword: "reset",
  Account: "account",
  Profile: "profile",
  DeleteAccount: "delete-account",
};

export default {
  components: {
    HeaderBar,
    NavBar,
    MainContent,
    PostFooter,
    OverlayMenu,
    AuthOverlay,
    NotificationBar,
  },
  data() {
    return {
      overlayVisible: false,
    };
  },
  computed: {
    ...mapState(['authStatus', 'notifications']),
    showAuthOverlay() {
      return Object.keys(AUTH_ROUTES).includes(this.$route.name);
    },
    authMode() {
      return AUTH_ROUTES[this.$route.name] || null;
    },
  },
  methods: {
    ...mapMutations(["ADD_NOTIFICATION", "REMOVE_NOTIFICATION"]),
    clearNotification(notificationId) {
      this.REMOVE_NOTIFICATION(notificationId);
    },
    toggleOverlay() {
      this.overlayVisible = !this.overlayVisible;
    },
    closeAuthOverlay() {
      this.$router.push("/"); // Redirect to home when overlay is closed
    },
  },
};
</script>

<style>
.morrissey {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
@font-face {
  font-family: FlandersArtSerif;
  font-weight: bold;
  src: url("@/assets/fonts/FlandersArtSerif-Bold.otf") format("opentype");
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-size:15px;
}

body, html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-family: "Helvetica Neue", Helvetica, "Segoe UI", Arial, "Liberation Sans", sans-serif;
  color: #2c3e50;
  height: 100%;
}

.menu-icon {
    display: none;
    font-size: 22px;
    cursor: pointer;
}

.overlay, .auth-overlay {
    display: flex;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.85);
    z-index: 10;
    color: black;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
}

.overlay, .auth-overlay p {
    margin: 10px 0 30px auto;
}

.overlay a {
    color: black;
    margin: 10px 0;
    text-decoration: none;
}

.overlay a:hover {
    color: #5052C0;
}

.close-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 28px;
    cursor: pointer;
}

h2 {
    font-size: 22px;
    color: #5052C0;
    margin-bottom: 16px;
}

a {
    color: #5052C0;
    text-decoration: underline;
    cursor: pointer;
}

input {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border-radius: 4px;
    border: 1px solid #ccc;
}

.login-form, .sign-up-form, .reset-password-form, .account-form, .profile-form {
  width: 90%;
  max-width: 320px;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative;
}

.google-button {
    width: 100%;
    padding: 10px;
    background-color: #ffffff;
    color: #757575;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-bottom: 15px;
}

.google-button i {
    margin-right: 8px;
    color: #DB4437; /* Google's logo color */
}

.google-button:hover {
    background-color: #f5f5f5;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #5052C0;
  /* Your preferred purple color */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 12px;
}

.submit-button:hover {
  background-color: #3e3fa1;
}
</style>
