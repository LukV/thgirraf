import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyAc1PjV2KEeCGhcPAtkf3ygnPxFBCMFpYg",
    authDomain: "thgirraf.firebaseapp.com",
    projectId: "thgirraf",
    storageBucket: "thgirraf.firebasestorage.app",
    messagingSenderId: "481117745167",
    appId: "1:481117745167:web:3c9c97cc3af0a560e4337a",
    measurementId: "G-K6KM3N3T2B"
  };

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);
const db = getFirestore(app);

export { auth, db };
