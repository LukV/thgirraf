<template>
  <div class="auth-overlay">
    <div class="close-btn" @click="$emit('close')">&times;</div>
    <component :is="currentComponent" @auth-success="onAuthSuccess" @switch-mode="switchMode" />
  </div>
</template>

<script>
import SignUpForm from "./SignUpForm.vue";
import LoginForm from "./LoginForm.vue";
import RequestPasswordReset from "./RequestPasswordReset.vue";
import ResetPassword from "./ResetPassword.vue";

export default {
  props: ["mode"],
  components: {
    SignUpForm,
    LoginForm,
    RequestPasswordReset,
    ResetPassword,
  },
  computed: {
    currentComponent() {
      return {
        signup: "SignUpForm",
        login: "LoginForm",
        "request-reset": "RequestPasswordReset",
        reset: "ResetPassword",
      }[this.mode];
    },
  },
  methods: {
    onAuthSuccess() {
      this.$emit("close");
    },
    switchMode(mode) {
      this.$emit("switch-mode", mode);
    },
  },
};
</script>

