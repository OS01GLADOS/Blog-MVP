
<script>

import customInputVue from "../Authentification/customInput.vue";
import postVue from "../Blogs/post.vue";
import commentVue from "../Blogs/comment.vue";

export default{
    name: "search",
    components: {customInputVue, postVue, commentVue},
    data(){
        return{
            title:'Search on website',
            type: 'text',
            search_request:'',
            url: process.env.VUE_APP_SERVER_URL+'/api/search?request=',
            data: {
                'search users':[],
                'search post':[],
                'search comments':[]
            }
        }
    },
    computed:{

    },
    methods: {
        sendSearchRequest(){
            fetch(this.url+this.search_request, {method:"GET"})
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                    this.data = data
            })
        }
    },
}

</script>

<template>
    <div>
        <h1>search page</h1>
        <div class="container">
            <customInputVue 
                :label="title"
                :type="type"
                v-model="search_request"
            />
            <input class="btn btn-primary mt-2 mb-2" type="button" @click="sendSearchRequest" value="Search">
            
            <details>
                <summary>founded {{data["search users"].length}} in usernames</summary>
                <div v-for="(item, i) in data['search users']" :key="i">
                     <router-link :to="{name: 'authorBlog', query:{ 'author':item.username}}" >{{item.username}}</router-link>
                </div>
               
            </details>
            <details>
                <summary>founded {{data["search post"].length}} in posts (including in post text)</summary>
                <postVue 
                    v-for="(item, i) in data['search post']"
                    :key="i"
                    :id="item.id"
                    :title="item.title"
                    :body="item.content"
                    :author="item.author_username"
                    :publish_date="item.date_posted"
                />
            </details>
            <details>
                <summary>founded {{data["search comments"].length}} in comments</summary>
                <div class="card mb-4" v-for="(item, i) in data['search comments']" :key="i">
                    <div class="card-body">
                        <commentVue 
                        :user_image="item.sender_image"
                        :username="item.sender_username"
                        :date_posted="item.date_posted"
                        :text="item.content"/>
                    <router-link class="card-link" :to="{name: 'showBlog', params:{ id: item.post} }">to related post</router-link>
                    </div>
                    
                </div>
                
            </details>
        </div>
        
    </div>
    
</template>