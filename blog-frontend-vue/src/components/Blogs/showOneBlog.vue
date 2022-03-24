<script>
import postFullView from "./postFullView.vue"
import getCookie from "../../getCookie"
import loadingVue from "../loadingScreen/loading.vue"

export default{
    name: 'ShowOneBlog',
    data(){
        return{
            HOST: process.env.VUE_APP_SERVER_URL,
            isLoading: true,
            item:{} ,
            url: process.env.VUE_APP_SERVER_URL+"/api/posts/",
            author: false
        }
    },
    components:{
        postFullView,
        loadingVue
    },
    computed:{
        isAuthor: {
            get() {
                return this.author
            },
            set(value){
                this.author = value
            }
    }
    },
    async mounted() {
        await this.onMount()
    },
    
    methods:{
        getUser(){
            const token = getCookie('VueBlog')
            const requestOptions = {
                method: "GET",
                headers: {
                    'Authorization':' Bearer '+ token
                }
            }
            fetch(this.HOST+'/api/profiles/?self=true', requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                return data.results[0].id

                
            })
            .catch(error => {
                this.errorMessage = error
                console.error('There was an errror!', error)
                })
        },
        async onMount(){
            const requestOptions = {
                method: "GET",
            }
            fetch(this.url+ this.$route.params.id, requestOptions)
                .then(async response => {
                    const data = await response.json()
                    if (!response.ok){
                            const error = (data && data.message) || response.status
                            return Promise.reject(error)
                        }
                    this.item = data
                    this.isLoading = false
                    if (getCookie('UserId')==data.author_id){
                        this.isAuthor = true
                    }

                })
                .catch(error => {
                    this.errorMessage = error
                    console.error('There was an errror!', error)
                })
        }
    }
}
</script>

<template>
    <div class="mt-2">
        <loadingVue v-if="isLoading"></loadingVue>
        <router-link v-if="isAuthor" class="btn btn-secondary" :to="{name: 'updateBlog', params:{ id: this.$route.params.id} }">update blog</router-link>
        <router-link v-if="isAuthor" class="ms-3 btn btn-danger" :to="{name: 'deleteBlog', params:{ id: this.$route.params.id} }">delete blog</router-link>
        <postFullView 
            :title="item.title"
            :body="item.content"
            :author="item.author_username"
            :publish_date="item.date_posted" 
        />
    </div>
</template>

