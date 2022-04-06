<script>

import postVue from "./post.vue"
import loadingVue from "../loadingScreen/loading.vue"

export default{
    name:'ShowBlogs',
    data(){
        return{
            HOST: process.env.VUE_APP_SERVER_URL,
            items:[],
            url : process.env.VUE_APP_SERVER_URL+"/api/posts/",
            isLoading: true
            }
    },
    components:{postVue, loadingVue
    },
    async mounted() {
        let code = this.$route.query.code
        console.log('code =',code)
        if (code){
            this.logingWithGoogle(code)
        }
        this.$emit("mounted");
        await this.handleClick()
    },
    watch:{
        async $route(){
            await this.handleClick()
        }
    },
    methods: {

        logingWithGoogle(code){
            console.log('log in with google')
            //send request to google to get auth data
            let form = new FormData()
            form.append('grant_type', 'authorization_code')
            form.append('code', code)
            form.append('client_id', "394636177476-a58g5v78eok9lbuifo6pk0t8bicgs84d.apps.googleusercontent.com")
            form.append('client_secret', "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")
            form.append('redirect_uri', "http://127.0.0.1:8080")
            let requestOptions = {
                method: "POST",
                body: form
            }
            let token = ''
            fetch('https://oauth2.googleapis.com/token', requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                    console.log(data.access_token)
                    token = data.access_token
                    //send auth data from request to login/register and get token
            requestOptions = {
                method: 'POST',
                Headers:{
                    'Authorization': 'Bearer '+token
                }
            }
            fetch('https://www.googleapis.com/auth/userinfo.profile', requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                    console.log(data)
            })

            })
            
        },

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
                this.isLoading = false
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
        <loadingVue v-if="isLoading"></loadingVue>
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