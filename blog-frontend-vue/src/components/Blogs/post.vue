<script>
export default{
    name: 'post',
    props:['title', 'body','author','publish_date', 'id']
}
</script>

<template>
    <div class="container">
                <h1><router-link :to="{name: 'showBlog', params:{ id: id} }">{{title}}</router-link></h1>
                <p class="small">{{publish_date}}  <router-link :to="{name: 'authorBlog', query:{ 'author':author}}">{{author}}</router-link></p>
            </div>
</template>