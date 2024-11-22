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
                <!-- Automatically switch between relative and absolute time -->
                <p>{{ formattedTime }}</p>
            </div>
        </div>

        <!-- Post Content Row -->
        <div class="content">
            <p v-html="content"></p>
            <WebsiteEmbed 
                v-if="embed && embed.title && (embed.description || embed.image_url)"
                :title="embed.title"
                :description="embed.description"
                :image="embed.image_url"
                :url="embed.url"
            />
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
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import WebsiteEmbed from './WebsiteEmbed.vue';

// Extend Day.js with plugins
dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(timezone);

export default {
    components: { WebsiteEmbed },
    props: {
        user: Object,
        content: String,
        time: String,
        embed: {
            type: Object,
            required: false,
            default: null,
        },
        actions: {
            type: Array,
            default: () => ["comment", "retweet", "like"]
        }
    },
    computed: {
        formattedTime() {
            const now = dayjs();
            const postTime = dayjs.utc(this.time).tz("Europe/Paris"); // Convert UTC to CET

            // Show relative time if the timestamp is within the last 7 days
            if (now.diff(postTime, "days") < 7) {
                return postTime.fromNow(); // e.g., "2 hours ago"
            }

            // Show absolute time for older posts
            return postTime.format("MMMM D, YYYY h:mm A"); // e.g., "November 21, 2024, 8:55 PM"
        },
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
  background-color: #ccc;
  color: white;
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
