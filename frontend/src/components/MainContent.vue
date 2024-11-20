<template>
  <div class="main-container" id="main-container">
    <main>
      <UserSection v-for="post in posts" :key="post.id" :user="post.user" :content="post.content"
        :actions="post.actions" />
    </main>
  </div>
</template>

<script>
import UserSection from './UserSection.vue';

export default {
  components: { UserSection },
  data() {
    return {
      posts: [],
    };
  },
  created() {
    this.initializePosts();
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
        }
      ];
    }
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