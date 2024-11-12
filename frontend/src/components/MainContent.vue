<template>
  <div class="main-container" id="main-container">
    <main>
      <UserSection v-for="post in posts" :key="post.id" :user="post.user" :content="post.content"
        :actions="post.actions" />

      <!-- Display the ID Token -->
      <div v-if="idToken">
        <h3>Your Firebase ID Token:</h3>
        <p>{{ idToken }}</p>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import { getAuth } from 'firebase/auth'; // Correctly import getAuth
import UserSection from './UserSection.vue';

export default {
  components: { UserSection },
  data() {
    return {
      message: '',
      posts: [],
      idToken: '', // Add a data property for the ID token
    };
  },
  created() {
    // Fetch data from your backend
    axios.get('http://localhost:8000')
      .then(response => {
        this.message = response.data.message;
        this.initializePosts(); // Initialize posts after fetching the message
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });

    // Initialize Firebase Auth
    const auth = getAuth(); // Use getAuth() instead of firebase.auth()

    // Check the auth state and get the ID token if user is logged in
    auth.onAuthStateChanged((user) => {
      if (user) {
        // User is signed in, retrieve the ID token
        user.getIdToken(/* forceRefresh */ true)
          .then((idToken) => {
            this.idToken = idToken;
            console.log('ID Token:', idToken);

            // Optionally, send the ID token to your backend
            // this.sendTokenToBackend(idToken);
          })
          .catch((error) => {
            console.error('Error getting ID token:', error);
          });
      } else {
        // No user is signed in
        console.log('No user is signed in.');
        this.idToken = null;
      }
    });
  },
  methods: {
    initializePosts() {
      this.posts = [
        {
          id: 1,
          user: { name: '@Seeta', profileImage: 'user-2.mock.png', time: '23 min' },
          content: '<strong>Cat memes</strong> have always been a big part of internet culture, but now, <a href="#">catspiracies</a> are trending because of the US election. From JD Vance’s attacks on “childless cat ladies” to a baseless conspiracy theory boosted by Donald Trump and Elon Musk about people eating pets in Ohio, our feline friends are taking center stage ahead of November.',
          actions: ['comment', 'retweet', 'like'],
        },
        {
          id: 2,
          user: { name: '@friedrich', profileImage: 'user-3.mock.png', time: '1 week ago' },
          content: 'Hoe stap je over van Google Analytics naar privacy proof Matomo...',
          actions: ['comment', 'retweet', 'like'],
        },
        {
          id: 3,
          user: { name: '@Seeta', profileImage: 'user-2.mock.png', time: '23 min' },
          content: this.message,
          actions: ['comment', 'retweet', 'like'],
        },
      ];
    },
    // Optional method to send the ID token to your backend
    sendTokenToBackend(idToken) {
      axios.get('http://localhost:8000/protected-route', {
        headers: {
          Authorization: `Bearer ${idToken}`,
        },
      })
        .then((response) => {
          console.log('Backend response:', response.data);
        })
        .catch((error) => {
          console.error('Error sending token to backend:', error);
        });
    },
  },
};
</script>

<style scoped>
.main-container {
  flex: 1;
  background-color: #fafafa;
  display: flex;
  justify-content: center;
  overflow-y: auto;
  width: 100%;
}

main {
  max-width: 600px;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  width: 100%;
  padding: 20px;
}

main section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 20px;
  gap: 10px;
}

/* User row styling */
section .user {
  display: flex;
  align-items: center;
  gap: 10px;
}

section .user img {
  width: 60px;
  height: 60px;
  border-radius: 35%;
}

section .user-info h2 {
  font-size: 16px;
  font-weight: bold;
  color: black;
}

section .user-info p {
  font-size: 12px;
  color: gray;
  margin-top: 2px;
}

/* Content styling */
section .content p {
  font-size: 16px;
  color: #333;
  line-height: 1.6;
}

section .content p strong {
  font-weight: bold;
}

/* Action row styling */
section .actions {
  display: flex;
  gap: 15px;
  color: #888;
  font-size: 16px;
}

section .actions i {
  cursor: pointer;
}

/* View comments row styling */
section .comments {
  color: gray;
  font-size: 14px;
  cursor: pointer;
}

/* Responsive styles */
@media (max-width: 900px) {
  main {
    padding: 25px 10px;
  }
}
</style>