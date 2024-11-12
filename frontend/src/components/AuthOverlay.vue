<template>
  <div class="auth-overlay">
    <div class="close-btn" @click="$emit('close')">&times;</div>
    <component :is="currentComponent" @auth-success="onAuthSuccess" @switch-mode="switchMode" />
  </div>
</template>

<script>
import SignUpForm from './SignUpForm.vue';
import LoginForm from './LoginForm.vue';
import ResetPasswordForm from './ResetPasswordForm.vue';

export default {
  props: ['mode'],
  components: {
    SignUpForm,
    LoginForm,
    ResetPasswordForm,
  },
  data() {
    return {
      currentMode: this.mode,
    };
  },
  computed: {
    currentComponent() {
      switch (this.currentMode) {
        case 'signup':
          return 'SignUpForm';
        case 'reset':
          return 'ResetPasswordForm';
        default:
          return 'LoginForm';
      }
    },
  },
  methods: {
    onAuthSuccess() {
      this.$emit('close');
      // Optionally, update parent component or Vuex store
    },
    switchMode(mode) {
      this.currentMode = mode;
    },
  },
};
</script>

<style scoped>
/* Style me */
</style>