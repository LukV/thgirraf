<template>
  <footer class="post-footer">
    <div class="post-footer-container">
      <div class="post-input-area">
        <!-- Text Input Area -->
        <textarea
          id="postInput"
          ref="postInput"
          placeholder="Create a post..."
          rows="2"
          v-model="postContent"
          @focus="expandTextarea"
        ></textarea>

        <!-- Icon Container with Plus, Divider, and Send Icon -->
        <div class="icon-container">
          <!-- Post Type Selection Icons -->
          <div
            :class="[
              'post-type-icons',
              { show: showPostTypeIcons, hidden: !showPostTypeIcons },
            ]"
          >
            <button
              class="icon"
              @click="selectPostType('text')"
              title="Text"
            >
              <i class="fas fa-font"></i>
            </button>
            <button
              class="icon"
              @click="selectPostType('image')"
              title="Image"
            >
              <i class="fas fa-image"></i>
            </button>
            <button
              class="icon"
              @click="selectPostType('video')"
              title="Video"
            >
              <i class="fas fa-video"></i>
            </button>
            <button
              class="icon"
              @click="selectPostType('carousel')"
              title="Carousel"
            >
              <i class="fas fa-layer-group"></i>
            </button>
          </div>

          <!-- Plus Icon to Expand Post Types -->
          <button
            class="icon plus-icon"
            v-show="!showPostTypeIcons"
            @click="togglePostTypeIcons"
          >
            <i class="fas fa-plus"></i>
          </button>

          <!-- Divider and Send Icon -->
          <div class="vertical-divider"></div>
          <button class="icon send-icon" @click="submitPost">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>

      <!-- Additional Fields for Post Types -->
      <div v-if="showExtraFields" class="extra-fields">
        <input
          v-if="selectedPostType === 'image'"
          type="file"
          accept="image/*"
          multiple
          class="extra-input"
        />
        <input
          v-if="selectedPostType === 'video'"
          type="file"
          accept="video/*"
          class="extra-input"
        />
        <input
          v-if="selectedPostType === 'carousel'"
          type="file"
          accept="image/*, video/*"
          multiple
          class="extra-input"
        />
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      postContent: "",
      showExtraFields: false,
      selectedPostType: null,
      showPostTypeIcons: false,
    };
  },
  methods: {
    togglePostTypeIcons() {
      this.showPostTypeIcons = !this.showPostTypeIcons;
    },
    selectPostType(type) {
      this.selectedPostType = type;
      this.showExtraFields = true;
      this.hidePostTypeIcons();
    },
    submitPost() {
      alert("Post submitted!");
      this.postContent = "";
      this.showExtraFields = false;
      this.selectedPostType = null;
      this.showPostTypeIcons = false;
      this.$refs.postInput.rows = 2; // Reset the textarea rows
    },
    expandTextarea() {
      this.$refs.postInput.rows = 10;
      this.hidePostTypeIcons();
    },
    collapseTextarea() {
      if (!this.postContent.trim()) {
        this.$refs.postInput.rows = 2;
      }
    },
    hidePostTypeIcons() {
      this.showPostTypeIcons = false;
    },
    handleClickOutside(event) {
      if (!this.$el.contains(event.target)) {
        // The click was outside the component
        this.collapseTextarea();
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style scoped>
.post-footer {
  border-top: 1px solid #ddd;
  padding: 10px 20px;
  position: sticky;
  bottom: 0;
  background-color: #fff;
  display: flex;
  justify-content: center;
  z-index: 0;
}

.post-footer-container {
  max-width: 600px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

#postInput {
  width: 100%;
  border: none;
  font-size: 14px;
  resize: none;
  outline: none;
  background: transparent;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.post-input-area {
  display: flex;
  align-items: flex-start; /* Align items to the top by default */
  position: relative;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 5px 10px;
  background-color: #f8f8f8;
}

.icon-container {
  display: flex;
  align-items: flex-end; /* Anchor icons to the bottom */
  gap: 10px;
  margin-left: auto; /* Push icons to the right */
  padding-bottom: 5px; /* Adds a bit of space between icons and textarea */
  position: absolute;
  bottom: 5px;
  right: 10px;
}

.icon {
  font-size: 18px;
  color: #5052c0;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s;
}

.icon:hover {
  color: #333;
}

/* Vertical divider between icons */
.vertical-divider {
  width: 1px;
  height: 24px;
  background-color: #ddd;
}

/* Post Type Icons */
.post-type-icons {
  display: flex;
  gap: 10px;
  transform: translateX(50px); /* Start hidden, sliding from right */
  opacity: 0;
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.post-type-icons.show {
  transform: translateX(0); /* Slide into view */
  opacity: 1;
}

.hidden {
  display: none;
}

/* Additional Fields Styling */
.extra-fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}
</style>
