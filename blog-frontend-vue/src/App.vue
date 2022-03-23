<template>

<div class="container">
  <router-link :to="{name: 'Home'}">Home</router-link> | 

  <span v-if="!has_token">
  <router-link :to="{name: 'login'}">Login</router-link> | 
  <router-link :to="{name: 'register'}">Register</router-link> |
  </span>
  <span v-else>
  <router-link :to="{name: 'userProfile'}">Profile</router-link> | 
  <router-link :to="{name: 'createBlog', query:{ 'new':'True'}}">CreateBlog</router-link> |
  <a href="#" @click="logOut">Log Out</a>
  </span>
  <router-view @mounted="childMounted"></router-view>
</div>
</template>

<script>
import getCookie from "./getCookie"

export default {
  name: 'App',
  token:{},
  data(){
    return{
      has_token: false
    }
  },
  methods: {
        childMounted: function() {
            let token = getCookie('VueBlog')
            if (typeof token !== 'undefined'){
              this.has_token = true;
            }
            console.log(this.has_token)
        },
        logOut(){
          document.cookie="VueBlog=dumpcookie;max-age=0";
          document.cookie="VueBlogRefresh=dumpcookie;max-age=0";
          this.$router.push({name: 'Home'})
          this.childMounted()
        }
    }
}
</script>


