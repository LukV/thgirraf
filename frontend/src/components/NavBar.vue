<template>
    <div class="nav-container">
      <div class="caret-left" v-show="showCaretLeft" @click="scrollNav('left')"><i class="fas fa-caret-left"></i></div>
      <div class="nav-scroller" ref="navScroller">
        <nav>
          <a href="#" class="active">All</a>
          <a href="#">Activism</a>
          <a href="#">Arts</a>
          <a href="#">Music</a>
          <a href="#">News</a>
          <a href="#">Science</a>
          <a href="#">Sport</a>
          <a href="#">Technology</a>
        </nav>       
      </div>
      <div class="caret-right" v-show="showCaretRight" @click="scrollNav('right')"><i class="fas fa-caret-right"></i></div>
    </div>
  </template>
  
<script>
export default {
    data() {
        return {
            showCaretLeft: false,
            showCaretRight: false
        };
    },
    mounted() {
        this.checkOverflow();
        window.addEventListener("resize", this.checkOverflow);
        this.$refs.navScroller.addEventListener("scroll", this.checkOverflow);
    },
    beforeUnmount() {
        window.removeEventListener("resize", this.checkOverflow);
        this.$refs.navScroller.removeEventListener("scroll", this.checkOverflow);
    },
    methods: {
        scrollNav(direction) {
            const scrollAmount = direction === "right" ? 150 : -150;
            this.$refs.navScroller.scrollBy({ left: scrollAmount, behavior: "smooth" });
        },
        checkOverflow() {
            const scroller = this.$refs.navScroller;
            this.showCaretLeft = scroller.scrollLeft > 0;
            this.showCaretRight = scroller.scrollWidth > scroller.clientWidth + scroller.scrollLeft;
        }
    }
};
</script>
  
<style scoped>
.nav-container {
    position: relative;
    display: flex;
    justify-content: center;
    overflow: hidden;
    border-bottom: 1px solid #ddd;
    background-color: #fff;
}

.nav-scroller {
    display: flex;
    overflow-x: auto;
    scrollbar-width: none; /* Hide scrollbar for Firefox */
    -ms-overflow-style: none; /* Hide scrollbar for IE and Edge */
    scroll-behavior: smooth;
}

.nav-scroller::-webkit-scrollbar {
    display: none; /* Hide scrollbar for Chrome, Safari, Opera */
}

nav {
    display: flex;
    justify-content: center;
    position: relative;
}

nav a {
    margin: 0 1em;
    padding: 1.1em .5em;
    text-decoration: none;
    color: #2c3e50;
    font-weight: 600;
    position: relative;
}

nav a.active {
    border-bottom: 1px solid #5052C0;
    color: #5052C0;
}

nav a::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 3px;
    background-color: #5052C0;
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

nav a.active::after,
nav a:hover::after {
    transform: scaleX(1);
}

.caret-left, .caret-right {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    font-size: 18px;
    color: #5052C0;
    background-color: white;
    padding: 0.2em;
    cursor: pointer;
    display: none; /* Hidden by default */
    z-index: 5;
}

.caret-left {
    left: 0;
}

.caret-right {
    right: 0;
}
</style>
  