<template>
    <div class="embed-card" @click="openLink">
        <div class="embed-image" v-if="image">
            <img :src="image" alt="Website preview" />
        </div>
        <div class="embed-details">
            <h3 class="embed-title">{{ title }}</h3>
            <p class="embed-description" v-if="description">{{ description }}</p>
            <hr class="embed-divider" />
            <span class="embed-url">{{ formattedUrl }}</span>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true,
        },
        description: {
            type: String,
            required: false,
        },
        image: {
            type: String,
            required: false,
        },
        url: {
            type: String,
            required: true,
        },
    },
    computed: {
        formattedUrl() {
            try {
                const parsedUrl = new URL(this.url);
                return parsedUrl.hostname;
            } catch {
                return this.url;
            }
        }
    },
    methods: {
        openLink() {
            window.open(this.url, "_blank");
        }
    }
};
</script>

<style scoped>
.embed-card {
    display: flex;
    flex-direction: column;
    border: 1px solid #ddd;
    border-radius: 12px; /* Rounded corners for the entire card */
    overflow: hidden; /* Ensures the image follows the card's rounded corners */
    max-width: 500px;
    transition: box-shadow 0.2s ease-in-out;
    cursor: pointer;
    background-color: white;
    margin: 10px 0px;
}

.embed-card:hover {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.embed-image img {
    width: 100%; /* Full width for the image */
    height: auto;
    object-fit: cover;
    border-top-left-radius: 12px; /* Match the card's rounded corners */
    border-top-right-radius: 12px;
}

.embed-details {
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.embed-title {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin: 0;
    line-height: 1.2;
}

.embed-description {
    font-size: 14px;
    color: #555;
    margin: 0;
    line-height: 1.4;
}

.embed-divider {
    border: none;
    border-top: 1px solid #eee;
    margin: 10px 0;
}

.embed-url {
    font-size: 12px;
    color: #888;
    text-transform: lowercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>



