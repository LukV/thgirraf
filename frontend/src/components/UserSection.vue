<template>
    <section class="user-section">
        <!-- User Information Row -->
        <div class="user">
            <img :src="require(`@/assets/images/${user.profileImage}`)" alt="User Profile" class="user-image" />
            <div class="user-info">
                <h2>{{ user.name }}</h2>
                <p>{{ user.time }}</p>
            </div>
        </div>

        <!-- Post Content Row -->
        <div class="content">
            <p v-html="content"></p> <!-- v-html allows rendering of HTML content such as <a> tags -->
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
.user-info h2 {
    font-size: 16px;
    font-weight: bold;
    color: black;
}
.user-info p {
    font-size: 12px;
    color: gray;
}
.content p {
    font-size: 14px;
    color: #333;
    line-height: 1.6;
}
.actions {
    display: flex;
    gap: 15px;
    color: #888;
    font-size: 16px;
}
.actions i {
    cursor: pointer;
}
.comments {
    color: gray;
    font-size: 14px;
    cursor: pointer;
}
</style>
  