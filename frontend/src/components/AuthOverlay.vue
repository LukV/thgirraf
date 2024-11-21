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
import AccountForm from "./AccountForm.vue";
import ProfileForm from "./ProfileForm.vue";
import DeleteAccountForm from "./DeleteAccountForm.vue";

export default {
  props: ["mode"],
  components: {
    SignUpForm,
    LoginForm,
    RequestPasswordReset,
    ResetPassword,
    AccountForm,
    ProfileForm,
    DeleteAccountForm
  },
  computed: {
    currentComponent() {
      return {
        signup: "SignUpForm",
        login: "LoginForm",
        "request-reset": "RequestPasswordReset",
        reset: "ResetPassword",
        account: "AccountForm",
        profile: "ProfileForm",
        "delete-account": "DeleteAccountForm"
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