<template>
  <div class="main-container" id="main-container">
    <main>
      <UserSection 
        v-for="post in filteredPosts" 
        :key="post.id" 
        :user="userDetails[post.user_id]" 
        :content="post.text"
        :time="post.date_created"
        :actions="['comment', 'retweet', 'like']" />
    </main>
  </div>
</template>

<script>
import UserSection from './UserSection.vue';
import apiClient from '@/apiClient';

export default {
  components: { UserSection },
  data() {
    return {
      posts: [],
      userDetails: {}, // Stores user details indexed by user_id
    };
  },
  computed: {
    filteredPosts() {
      // Filter posts to only include those with valid user details
      return this.posts.filter(post => this.userDetails[post.user_id]);
    },
  },
  async created() {
    await this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      try {
        // Fetch posts from the API
        const postResponse = await apiClient.get('/posts');
        this.posts = postResponse.data;

        // Extract unique user IDs from posts
        const userIds = [...new Set(this.posts.map(post => post.user_id))];

        // Fetch user details in a single batch call
        const userResponse = await apiClient.post('/users/batch', userIds);

        // Map user details by user_id
        this.userDetails = userResponse.data.reduce((map, user) => {
          map[user.id] = {
            name: user.username,
            profileImage: user.icon
              ? `${process.env.VUE_APP_API_BASE_URL}/icons/${user.icon}`
              : null,
            email: user.email,
            time: user.date_created,
          };
          return map;
        }, {});
      } catch (error) {
        console.error('Error fetching posts or users:', error);
      }
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
  font-weight: bold;
  color: black;
}

section .user-info p {
  color: gray;
  margin-top: 2px;
}

/* Content styling */
section .content p {
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
}

section .actions i {
  cursor: pointer;
}

/* View comments row styling */
section .comments {
  color: gray;
  cursor: pointer;
}

/* Responsive styles */
@media (max-width: 900px) {
  main {
    padding: 25px 10px;
  }
}
</style>