<template>
    <section class="user-section">
        <!-- User Information Row -->
        <div class="user">
            <img 
                v-if="user.profileImage" 
                :src="user.profileImage" 
                alt="User Profile" 
                class="user-image" 
            />
            <div v-else class="user-placeholder">
            {{ user.name ? user.name.charAt(0).toUpperCase() : "?" }}
            </div>
            <div class="user-info">
                <h2>{{ user.name }}</h2>
                <p>{{ time }}</p>
            </div>
        </div>

        <!-- Post Content Row -->
        <div class="content">
            <p v-html="content"></p>
        </div>

        <!-- Actions Row -->
        <div class="actions">
            <i class="fa-solid fa-comment" @click="triggerAction('comment')"></i>
            <i class="fa-solid fa-retweet" @click="triggerAction('retweet')"></i>
            <i class="fa-solid fa-heart" @click="triggerAction('like')"></i>
        </div>

        <!-- Comments Link Row -->
        <div class="comments" @click="viewComments">
            View comments …
        </div>
    </section>
</template>

<script>
export default {
    props: {
        user: {
            type: Object,
            required: true,
        },
        content: {
            type: String,
            required: true,
        },
        time: {
            type: String,
            required: true,
        },
        actions: {
            type: Array,
            default: () => ["comment", "retweet", "like"]
        }
    },
    methods: {
        triggerAction(action) {
            alert(`Action triggered: ${action}`);
        },
        viewComments() {
            alert("Viewing comments...");
        }
    }
};
</script>


<style scoped>
.user-section {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 20px;
    gap: 10px;
}

.user {
    display: flex;
    align-items: center;
    gap: 10px;
}

.user-image {
    width: 60px;
    height: 60px;
    border-radius: 35%;
}

.user-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 35%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ccc; /* Adjust as needed */
  color: white; /* Adjust as needed */
  font-size: 24px;
  font-weight: bold;
  text-transform: uppercase;
}

.user-info h2 {
    font-weight: bold;
    margin-bottom: 0px;
    color: black;
}

.user-info p {
    color: gray;
}

.content p {
    line-height: 1.6;
}

.actions {
    display: flex;
    gap: 15px;
    color: #888;
    font-size: 22px;
}

.actions i {
    cursor: pointer;
}

.comments {
    color: gray;
    cursor: pointer;
}
</style>