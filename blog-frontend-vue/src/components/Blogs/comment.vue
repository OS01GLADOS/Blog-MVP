<script>
export default{
    name: 'comment',
    props:['user_image', 'user_posts_link', 'date_posted', 'text', 'username'],
    computed:{
        
    }
}
</script>

<style>
.article-img {
  height: 65px;
  width: 65px;
}
</style>

<template>
    <div class="container">
        <img class="rounded-circle article-img" :src="user_image">
        <div class="media-body">
            <div class="article-metadata">
                <router-link :to="{name: 'authorBlog', query:{ 'author':username}}">{{username}}</router-link>
                <small class="text-muted ms-2">{{date_posted}}</small>
            </div>
            <p class="article-content">{{text}}</p>
        </div>
    </div>
</template>