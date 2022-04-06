<script>
import customInputVue from "../Authentification/customInput.vue";
import getCookie from "../../getCookie";

export default{
    name: 'addComment',
    component: {customInputVue},
    data(){
        return{
            comment_text:"",
            ifAuthenticated: false,
            url: process.env.VUE_APP_SERVER_URL+'/api/comments/',
            post_id: 0
        }
    },
    mounted() {
        if (getCookie('UserId')){
            this.ifAuthenticated = true
        }
        this.post_id = this.$route.params.id
    },
    methods: {
        addComment(){
            const token = getCookie('VueBlog')

            let form = new FormData()
            form.append("content", this.comment_text,)
            form.append("post", this.post_id)

            const requestOptions = {
                        method: "POST",
                        headers: {
                            'Authorization':' Bearer '+ token,
                        },
                        body: form
                    }
            fetch(this.url, requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)
                }
                this.comment_text = ""
            })
        }
    },
}


</script>


<template>
    <div class="container">
        <h2 v-if="!ifAuthenticated">Log In or Register to add comment</h2>
        <div class="row"><textarea v-if="ifAuthenticated" class="form-control" v-model="comment_text" />
        <input v-if="ifAuthenticated" class="btn btn-primary mt-2 mb-2" type="button" @click="addComment" value="Send">
        </div>
    </div>
</template>