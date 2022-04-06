<script>
import CustomInput from "./customInput.vue"
import getCookie from "../../getCookie";

export default {
    name: "login",
    components: { CustomInput },
    mounted: function() {
        this.$emit("mounted");
    },
    data(){
        return{
            HOST: process.env.VUE_APP_SERVER_URL,
            inputs:[
                    {
                        label: "Username",
                        value: "",
                        type: "text"
                    },
                    {
                        label: "Password",
                        value: "",
                        type: "password"
                    },
                ],
                url:process.env.VUE_APP_SERVER_URL+'/api/token/'
            }
            
        },
    methods:{
        loginWithGoogleClick(){
            window.location.replace(this.HOST+'/api/social/google/login');    
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
                    document.cookie="UserId=dumpcookie;max-age=0";
                    document.cookie ='UserId='+data.results[0].id
            })
            .catch(error => {
                this.errorMessage = error
                console.error('There was an errror!', error)
                })
        },
        handleSubmit(){
            let form = new FormData()
            form.append('username', this.inputs[0].value)
            form.append('password', this.inputs[1].value)

            const requestOptions = {
                        method: "POST",
                        body: form
                    }
            fetch(this.url, requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)
                    }
                    document.cookie="VueBlog=dumpcookie;max-age=0";
                    document.cookie="VueBlogRefresh=dumpcookie;max-age=0";  
                    document.cookie ='VueBlog='+data.access
                    document.cookie ='VueBlogRefresh='+data.refresh
                    this.getUser()
                    this.$router.push({name: 'Home'})
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
    <div>
        <h1>Log In</h1>
        <form @submit.prevent="handleSubmit"> 
            <CustomInput 
                v-for="(input ,i) in inputs"
                :key="i"
                v-model="input.value"
                :label="input.label"
                :type="input.type"
            />
            <input class="btn btn-primary mt-2" type=submit value="Log In">
        </form>
        <a href="#" @click="loginWithGoogleClick">Log in with google</a>
    </div>
</template>