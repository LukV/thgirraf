<template>
        <div class="login-form">
            <h2>Welcome back!</h2>
            <button class="google-button" @click="signInWithGoogle">
                <i class="fab fa-google"></i> Log in with Google
            </button>
            <p>- or -</p>
            <h2>Log in with Email</h2>
            <form @submit.prevent="login">
                <input type="email" v-model="email" placeholder="Email" required />
                <input type="password" v-model="password" placeholder="Password" required />
                <button type="submit" class="submit-button">Log in</button>
            </form>
            <p><a href="#" @click.prevent="switchToReset">Forgot Password?</a></p>
            <p>Don’t have an account? <a href="#" @click.prevent="switchToSignUp">Sign up</a></p>
        </div>
</template>


<script>
import { getAuth, signInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';

export default {
    data() {
        return {
            email: '',
            password: '',
        };
    },
    methods: {
        login() {
            const auth = getAuth();
            signInWithEmailAndPassword(auth, this.email, this.password)
                .then((userCredential) => {
                    const user = userCredential.user;
                    this.$emit('auth-success', user);
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        signInWithGoogle() {
            const auth = getAuth();
            const provider = new GoogleAuthProvider();
            signInWithPopup(auth, provider)
                .then((result) => {
                    const user = result.user;
                    this.$emit('auth-success', user);
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        switchToReset() {
            this.$emit('switch-mode', 'reset');
        },
        switchToSignUp() {
            this.$emit('switch-mode', 'signup');
        },
    },
};
</script>