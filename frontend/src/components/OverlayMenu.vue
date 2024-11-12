<template>
    <div class="overlay" @click.self="closeOverlay">
      <span class="close-btn" @click="closeOverlay">&times;</span>
      <a href="#" class="overlay-link">Sign up</a>
      <a href="#" class="overlay-link">Login</a>
      <a href="#" class="overlay-link">Search</a>
    </div>
</template>

<script>
export default {
methods: {
    closeOverlay() {
        this.$emit("toggle-overlay");
    }
}
};
</script>
  