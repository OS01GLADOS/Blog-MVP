<script>
import getCookie from "../../getCookie";
import HOST from "../../host";

export default{
    name: "deleteBlogVue",
    methods:{
        goBack(){
            this.$router.push({name: 'Home'})
        },
        async handleSubmit(){
            const token = getCookie('VueBlog')
            const requestOptions = {
                    method: "DELETE",
                    headers: {
                        'Authorization':' Bearer '+ token
                        },
            }
            fetch(HOST+"/api/posts/"+this.$route.params.id+"/", requestOptions)
            .then(async response =>{
                if (response.status != 204){
                    const error = ('there was an error while deleting') || response.status
                    return Promise.reject(error)}
                    this.$router.push({name: 'Home'})
                })
                .catch(error => {
                    this.errorMessage = error
                    console.error('There was an errror!', error)
                })
        },
    }
}
</script>

<template>
    <h1>Are you sure?</h1>
    <p>delete blog {{$route.params.id}} </p>
    <form @submit.prevent="handleSubmit" class="mt2-"> 
        <input class="btn btn-danger" type=submit value="Yes, delete blog ">
        <input class="btn btn-primary ms-2" type=reset @click="goBack" value="back">
    </form>
</template>