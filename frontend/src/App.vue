<template>
    <HeaderBar @toggle-overlay="toggleOverlay" />
    <NavBar />
    <MainContent />
    <PostFooter />
    <OverlayMenu v-if="overlayVisible" @toggle-overlay="toggleOverlay" />
</template>

<script>
import HeaderBar from "./components/HeaderBar.vue";
import NavBar from "./components/NavBar.vue";
import MainContent from "./components/MainContent.vue";
import PostFooter from "./components/PostFooter.vue";
import OverlayMenu from "./components/OverlayMenu.vue";

export default {
  components: {
    HeaderBar,
    NavBar,
    MainContent,
    PostFooter,
    OverlayMenu
  },
  data() {
    return {
      overlayVisible: false
    };
  },
  methods: {
    toggleOverlay() {
      this.overlayVisible = !this.overlayVisible;
    }
  }
};
</script>

<style>
#app {
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
}

body, html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-family: "Helvetica Neue", Helvetica, "Segoe UI", Arial, "Liberation Sans", sans-serif;
  color: #2c3e50;
  font-size: 14px;
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
    margin: 10px 0;
}

.overlay a {
    color: black;
    font-size: 24px;
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

.overlay, .auth-overlay h2 {
    font-size: 22px;
    color: #5052C0;
    margin-bottom: 16px;
}

a {
    color: #5052C0;
    text-decoration: underline;
    cursor: pointer;
    font-size: 14px;
}

input {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-size: 16px;
}

.login-form, .sign-up-form, .reset-password-form {
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
    font-size: 16px;
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
  font-size: 16px;
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
