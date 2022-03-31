<script>
import postFullView from "./postFullView.vue"
import getCookie from "../../getCookie"
import loadingVue from "../loadingScreen/loading.vue"
import commentVue from "./comment.vue"
import addCommentVue from "./addComment.vue"

export default{
    name: 'ShowOneBlog',
    data(){
        return{
            HOST: process.env.VUE_APP_SERVER_URL,
            isLoading: true,
            item:{} ,
            url: process.env.VUE_APP_SERVER_URL+"/api/posts/",
            author: false,
            comments: [],
            post_id:0
        }
    },
    components:{
        postFullView,
        loadingVue,
        commentVue,
        addCommentVue,
    },
    computed:{
        isAuthor: {
            get() {
                return this.author
            },
            set(value){
                this.author = value
            }
        },
        id_post:{
            get() {
                return this.post_id
            },
            set(value){
                this.post_id = value
            }
        },
        commentArr:{
            get(){
                return this.comments
            },
            set(value){
                this.comments.unshift(value)
            }
        }

    },
    async mounted() {
        await this.onMount()
        this.id_post = this.$route.params.id
        window.setInterval(() => {
            this.updateComments()
        }, 30000)
    },
    
    methods:{
        updateComments(){
            
            console.log(this.last_update_date.toISOString())

            fetch(this.HOST+'/api/comments/'+'?datetime='+this.last_update_date.toISOString())
            .then(
                async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                    console.log(data.results)
                    for (var item in data.results){
                        console.log(item)
                        this.commentArr =  data.results[item]
                        this.last_update_date = new Date()
                    }
                }
            )

        },
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
                    this.comments = data.comments
                    this.last_update_date = new Date()
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
        <!-- comments -->

        <div id="comments">
            <h3>Comments</h3>
            <addCommentVue/>
            <commentVue
                v-for="(item, i) in commentArr"
                :key="i"
                :user_image="item.sender_image"
                :username="item.sender_username"
                :date_posted="item.date_posted"
                :text="item.content"
            />
        </div>
    </div>
</template>

