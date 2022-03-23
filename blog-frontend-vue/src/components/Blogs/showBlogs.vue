<script>

import postVue from "./post.vue"
import HOST from "../../host"

export default{
    name:'ShowBlogs',
    data(){
        return{
            items:[],
            url : HOST+"/api/posts/"
            }
    },
    components:{postVue},
    async mounted() {
        this.$emit("mounted");
        await this.handleClick()
    },
    watch:{
       async $route(){
            await this.handleClick()
        }
    },
    methods: {
        async handleClick(){

            const requestOptions = {method: "GET"}
            if(this.$route.query.author){
                this.url=this.url+'?author='+this.$route.query.author
            }
            fetch(this.url, requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                this.items = data.results
                this.$forceUpdate();
                })
            .catch(error => {
                this.errorMessage = error
                console.error('There was an errror!', error)
                })
            }
        },
    }

</script>
    
<template>
    <div class="container">
        <h3>All blogs</h3 >
        <postVue 
            v-for="(item, i) in items"
            :key="i"
            :id="item.id"
            :title="item.title"
            :body="item.content"
            :author="item.author_username"
            :publish_date="item.date_posted"
        />
    </div>
</template>