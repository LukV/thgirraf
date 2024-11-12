<template>
  <div class="sign-up-form">
    <h2>Sign Up</h2>
    <form @submit.prevent="signUp">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit" class="submit-button">Sign Up</button>
    </form>
    <p>Or</p>
    <button @click="signInWithGoogle" class="google-button">
      <i class="fab fa-google"></i> Sign Up with Google
    </button>
    <p>Already have an account? <a href="#" @click.prevent="switchToLogin">Login</a></p>
  </div>
</template>

<script>
import { getAuth, createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { getFirestore, doc, setDoc, serverTimestamp } from 'firebase/firestore';

export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
    };
  },
  methods: {
    signUp() {
      const auth = getAuth();
      const db = getFirestore();

      createUserWithEmailAndPassword(auth, this.email, this.password)
        .then((userCredential) => {
          const user = userCredential.user;
          // Update profile with username
          user.updateProfile({
            displayName: this.username,
          });

          // Save additional user data to Firestore
          setDoc(doc(db, 'users', user.uid), {
            email: this.email,
            username: this.username,
            dateCreated: serverTimestamp(),
          });
          this.$emit('auth-success', user);
        })
        .catch((error) => {
          console.error(error);
          // Handle errors (e.g., display error message)
        });
    },
    signInWithGoogle() {
      const auth = getAuth();
      const db = getFirestore();
      const provider = new GoogleAuthProvider();

      signInWithPopup(auth, provider)
        .then((result) => {
          const user = result.user;
          // Optionally save user data to Firestore
          setDoc(
            doc(db, 'users', user.uid),
            {
              email: user.email,
              username: user.displayName,
              dateCreated: serverTimestamp(),
            },
            { merge: true }
          );
          this.$emit('auth-success', user);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    switchToLogin() {
      this.$emit('switch-mode', 'login');
    },
  },
};
</script>