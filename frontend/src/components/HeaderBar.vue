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
            <a href="#" v-if="!user" @click.prevent="showSignUp">Sign up</a>
            <button v-if="!user" @click="showLogin">Login</button>
            <div v-else class="user-info">
                <span>Welcome, {{ user.displayName || user.email }}</span>
                <button @click="logout">Logout</button>
            </div>
            <div class="search-container">
                <input type="text" class="search-input" v-model="searchQuery" />
                <span class="search-icon"><i class="fas fa-search"></i></span>
            </div>
        </div>

        <!-- Authentication Overlay -->
        <AuthOverlay v-if="authOverlayVisible" :mode="authMode" @close="closeAuthOverlay" />
    </div>
</template>

<script>
import AuthOverlay from './AuthOverlay.vue';
import { auth } from '@/firebase';

export default {
    components: {
        AuthOverlay,
    },
    data() {
        return {
            searchQuery: '',
            authOverlayVisible: false,
            authMode: 'login', // 'login' or 'signup'
            user: null,
        };
    },
    created() {
        auth.onAuthStateChanged((user) => {
            this.user = user;
        });
    },
    methods: {
        showSignUp() {
            this.authMode = 'signup';
            this.authOverlayVisible = true;
        },
        showLogin() {
            this.authMode = 'login';
            this.authOverlayVisible = true;
        },
        closeAuthOverlay() {
            this.authOverlayVisible = false;
        },
        logout() {
            auth.signOut();
        },
    },
};
</script>

<style scoped>
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    /* Center the logo horizontally */
    height: 100px;
    /* Define a height for the header to add vertical space */
    position: relative;
    padding: 0 20px;
    border-bottom: 1px solid #ddd;
}

/* Logo */
.logo {
    display: flex;
    align-items: center;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}

.logo img {
    height: 70px;
    /* Adjust the size as needed */
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

/* Right section for Sign up, Login, and Search */
.header-right {
    display: flex;
    align-items: center;
    gap: 1em;
}

.header-right a {
    text-decoration: none;
    color: #505963;
}

.header-right a:hover {
    text-decoration: underline;
    color: #5052C0;
}

.header-right button {
    padding: 12px 30px;
    font-size: 12px;
    background-color: #5052C0;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.header-right button:hover {
    background-color: #51459c;
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


/* Responsive styles */
@media (max-width: 900px) {
    .header-right {
        display: none;
    }

    .menu-icon {
        display: block;
    }
}
</style>