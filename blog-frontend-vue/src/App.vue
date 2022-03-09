<template>

<div class="container">
  <router-link :to="{name: 'Home'}">Home</router-link> | 
  <router-link :to="{name: 'login'}">Login</router-link> | 
  <router-link :to="{name: 'register'}">Register</router-link> | 
  <router-link :to="{name: 'userProfile'}">Profile</router-link> | 
  <router-link :to="{name: 'createBlog', query:{ 'new':'True'}}">CreateBlog</router-link>
  <router-view></router-view>
</div>
</template>

<script>
export default {
  name: 'App',
  token:{}
}
</script>


